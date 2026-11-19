"""
Client-Side Domain Adaptation for Encrypted Domain Adaptation
Run locally to compute adaptation matrices A, b from decrypted features.
"""

import json
import numpy as np
import pandas as pd
from paillier_client import PaillierClient, load_encrypted_dataset


def procrustes_adaptation(X_target: np.ndarray, X_source: np.ndarray, reg: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
    """
    Solve for A, b such that X_target * A + b ≈ X_source
    Using regularized least squares (ridge regression).
    
    A = (X_target^T X_target + λI)^-1 @ X_target^T @ X_source
    b = mean(X_source) - mean(X_target) @ A
    """
    # Center the data
    mean_target = X_target.mean(axis=0)
    mean_source = X_source.mean(axis=0)
    
    Xt_centered = X_target - mean_target
    Xs_centered = X_source - mean_source
    
    # Ridge regression
    XtXt = Xt_centered.T @ Xt_centered + reg * np.eye(Xt_centered.shape[1])
    XtXs = Xt_centered.T @ Xs_centered
    
    A = np.linalg.solve(XtXt, XtXs).astype(np.float32)
    b = (mean_source - mean_target @ A).astype(np.float32)
    
    return A, b


def encrypt_matrix(client: PaillierClient, matrix: np.ndarray) -> List[List[str]]:
    """Encrypt a 2D matrix element-wise."""
    d1, d2 = matrix.shape
    enc_matrix = []
    for i in range(d1):
        row = []
        for j in range(d2):
            enc_val = client.encrypt_scalar(float(matrix[i, j]))
            row.append(enc_val)
        enc_matrix.append(row)
    return enc_matrix


def encrypt_vector(client: PaillierClient, vector: np.ndarray) -> List[str]:
    """Encrypt a 1D vector element-wise."""
    return [client.encrypt_scalar(float(v)) for v in vector]


def save_enc_matrix_parquet(enc_matrix: List[List[str]], output_path: str):
    """Save encrypted matrix to parquet."""
    df = pd.DataFrame({'values': enc_matrix})
    df.to_parquet(output_path, index=False)


def save_enc_vector_parquet(enc_vector: List[str], output_path: str):
    """Save encrypted vector to parquet."""
    df = pd.DataFrame({'values': enc_vector})
    df.to_parquet(output_path, index=False)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compute encrypted domain adaptation matrices")
    parser.add_argument("--keys-dir", type=str, default="keys", help="Directory with Paillier keys")
    parser.add_argument("--data-root", type=str, required=True, help="Root directory with encrypted datasets")
    parser.add_argument("--source-dataset", type=str, default="enc_casia.parquet", help="Source domain (CASIA)")
    parser.add_argument("--target-datasets", nargs='+', default=["enc_korus.parquet", "enc_micc.parquet"], 
                        help="Target domains to adapt to")
    parser.add_argument("--output-dir", type=str, default=".", help="Output directory for Enc(A), Enc(b)")
    parser.add_argument("--adapt-samples", type=int, default=500, help="Number of samples for adaptation")
    parser.add_argument("--regularization", type=float, default=0.01, help="Ridge regularization")
    args = parser.parse_args()
    
    # Load client keys
    client = PaillierClient()
    client.load_keys(f"{args.keys_dir}/public_key.json", f"{args.keys_dir}/private_key.json")
    
    # Load source domain features (CASIA)
    print(f"Loading source domain: {args.source_dataset}")
    enc_source_features, _ = load_encrypted_dataset(f"{args.data_root}/{args.source_dataset}")
    enc_source_features = enc_source_features[:args.adapt_samples]
    
    # Decrypt source features
    print("Decrypting source features...")
    source_features = np.array([client.decrypt_vector(f) for f in enc_source_features])
    print(f"Source shape: {source_features.shape}")
    
    # Process each target domain
    for target_name in args.target_datasets:
        print(f"\n=== Processing {target_name} ===")
        
        # Load target domain features
        enc_target_features, _ = load_encrypted_dataset(f"{args.data_root}/{target_name}")
        enc_target_features = enc_target_features[:args.adapt_samples]
        
        # Decrypt target features
        print("Decrypting target features...")
        target_features = np.array([client.decrypt_vector(f) for f in enc_target_features])
        print(f"Target shape: {target_features.shape}")
        
        # Compute adaptation
        print("Computing Procrustes adaptation...")
        A, b = procrustes_adaptation(target_features, source_features, args.regularization)
        print(f"A shape: {A.shape}, b shape: {b.shape}")
        
        # Encrypt A and b
        print("Encrypting adaptation matrices...")
        enc_A = encrypt_matrix(client, A)
        enc_b = encrypt_vector(client, b)
        
        # Save
        domain_name = target_name.replace('enc_', '').replace('.parquet', '')
        save_enc_matrix_parquet(enc_A, f"{args.output_dir}/enc_A_{domain_name}.parquet")
        save_enc_vector_parquet(enc_b, f"{args.output_dir}/enc_b_{domain_name}.parquet")
        
        print(f"Saved: enc_A_{domain_name}.parquet, enc_b_{domain_name}.parquet")
    
    print("\nAll domain adaptations complete!")
    print("Upload Enc(A), Enc(b) files to Google Drive for Colab inference.")


if __name__ == "__main__":
    from typing import List, Tuple
    main()