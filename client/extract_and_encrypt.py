"""
End-to-end pipeline: Load images → Extract forensic features → Encrypt → Save for Colab.
Run locally on your machine (has private key).
"""

import argparse
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from tqdm import tqdm
import cv2

# Local imports
from forensic_features import extract_features_from_path, extract_all_features
from paillier_client import PaillierClient, encrypt_dataset_features


def load_dataset_index(dataset_root: str, dataset_name: str) -> pd.DataFrame:
    """
    Load or create dataset index with image paths and labels.
    Expected structure:
    dataset_root/
        CASIA_v2/
            Au/ (authentic)
            Tp/ (tampered)
        Korus_2018/
            ...
    """
    dataset_path = Path(dataset_root) / dataset_name
    
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    
    records = []
    
    # Try common forgery dataset structures
    if dataset_name == "CASIA_v2":
        au_dir = dataset_path / "Au"
        tp_dir = dataset_path / "Tp"
        if au_dir.exists():
            for img_path in au_dir.glob("*.*"):
                records.append({'path': str(img_path), 'label': 0, 'dataset': 'CASIA_v2'})
        if tp_dir.exists():
            for img_path in tp_dir.glob("*.*"):
                records.append({'path': str(img_path), 'label': 1, 'dataset': 'CASIA_v2'})
    
    elif dataset_name == "Korus_2018":
        # Korus structure varies - adapt as needed
        for split in ["train", "val", "test"]:
            for label_dir, label in [("authentic", 0), ("tampered", 1)]:
                dir_path = dataset_path / split / label_dir
                if dir_path.exists():
                    for img_path in dir_path.glob("*.*"):
                        records.append({'path': str(img_path), 'label': label, 'dataset': 'Korus_2018'})
    
    elif dataset_name == "COVERAGE":
        # COVERAGE has specific structure
        for label_dir, label in [("authentic", 0), ("forged", 1)]:
            dir_path = dataset_path / label_dir
            if dir_path.exists():
                for img_path in dir_path.rglob("*.*"):
                    records.append({'path': str(img_path), 'label': label, 'dataset': 'COVERAGE'})
    
    elif dataset_name == "IMD2020":
        for label_dir, label in [("authentic", 0), ("tampered", 1)]:
            dir_path = dataset_path / label_dir
            if dir_path.exists():
                for img_path in dir_path.rglob("*.*"):
                    records.append({'path': str(img_path), 'label': label, 'dataset': 'IMD2020'})
    
    elif dataset_name == "MICC_F600":
        for label_dir, label in [("original", 0), ("forged", 1)]:
            dir_path = dataset_path / label_dir
            if dir_path.exists():
                for img_path in dir_path.glob("*.*"):
                    records.append({'path': str(img_path), 'label': label, 'dataset': 'MICC_F600'})
    
    else:
        # Generic: assume subdirectories are class labels
        for label_dir in dataset_path.iterdir():
            if label_dir.is_dir():
                label = 0 if 'authentic' in label_dir.name.lower() or 'original' in label_dir.name.lower() else 1
                for img_path in label_dir.glob("*.*"):
                    records.append({'path': str(img_path), 'label': label, 'dataset': dataset_name})
    
    df = pd.DataFrame(records)
    print(f"Found {len(df)} images in {dataset_name} ({df['label'].sum()} forged, {(df['label']==0).sum()} authentic)")
    return df


def extract_features_batch(df: pd.DataFrame, max_samples: int = None) -> Tuple[np.ndarray, np.ndarray]:
    """Extract features for all images in dataframe."""
    if max_samples:
        df = df.head(max_samples)
    
    features_list = []
    labels_list = []
    failed = []
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Extracting features"):
        try:
            feats = extract_features_from_path(row['path'])
            features_list.append(feats)
            labels_list.append(row['label'])
        except Exception as e:
            print(f"Failed on {row['path']}: {e}")
            failed.append(row['path'])
    
    if failed:
        print(f"Failed on {len(failed)} images")
    
    return np.array(features_list, dtype=np.float32), np.array(labels_list, dtype=np.int32)


def main():
    parser = argparse.ArgumentParser(description="Extract forensic features and encrypt for Colab")
    parser.add_argument("--dataset-root", type=str, required=True, help="Root directory containing datasets")
    parser.add_argument("--dataset", type=str, required=True, 
                        choices=["CASIA_v2", "Korus_2018", "COVERAGE", "IMD2020", "MICC_F600"],
                        help="Dataset name")
    parser.add_argument("--output", type=str, required=True, help="Output parquet path")
    parser.add_argument("--keys-dir", type=str, default="keys", help="Directory for Paillier keys")
    parser.add_argument("--max-samples", type=int, default=None, help="Limit samples (for testing)")
    parser.add_argument("--generate-keys", action="store_true", help="Generate new keypair")
    parser.add_argument("--key-size", type=int, default=2048, help="Paillier key size")
    
    args = parser.parse_args()
    
    # Setup paths
    keys_dir = Path(args.keys_dir)
    keys_dir.mkdir(exist_ok=True)
    pub_key_path = keys_dir / "public_key.json"
    priv_key_path = keys_dir / "private_key.json"
    
    # Initialize Paillier client
    client = PaillierClient(key_size=args.key_size)
    
    if args.generate_keys or not pub_key_path.exists():
        print("Generating new Paillier keypair...")
        client.generate_keys()
        client.save_keys(str(pub_key_path), str(priv_key_path))
    else:
        print("Loading existing keys...")
        client.load_keys(str(pub_key_path), str(priv_key_path))
    
    # Load dataset index
    print(f"Loading {args.dataset} index...")
    df = load_dataset_index(args.dataset_root, args.dataset)
    
    if len(df) == 0:
        print("No images found! Check dataset structure.")
        return
    
    # Extract features
    print("Extracting forensic features...")
    features, labels = extract_features_batch(df, args.max_samples)
    print(f"Feature matrix shape: {features.shape}")
    
    # Encrypt and save
    print("Encrypting features...")
    encrypt_dataset_features(features, labels, client, args.output)
    
    # Also save public key for Colab
    import json
    pub_dict = client.get_public_key_dict()
    with open(keys_dir / "public_key_for_colab.json", 'w') as f:
        json.dump(pub_dict, f)
    print(f"Public key saved for Colab: {keys_dir}/public_key_for_colab.json")
    
    print("Done!")


if __name__ == "__main__":
    main()