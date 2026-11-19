"""
Client-Side Decryption & Evaluation for Encrypted Inference
Run locally to decrypt predictions and compute metrics.
"""

import json
import numpy as np
import pandas as pd
from paillier_client import PaillierClient, load_encrypted_dataset
from sklearn.metrics import roc_auc_score, accuracy_score, precision_recall_fscore_support


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Decrypt predictions and evaluate")
    parser.add_argument("--keys-dir", type=str, default="keys", help="Directory with Paillier keys")
    parser.add_argument("--preds-coverage", type=str, required=True, help="Path to enc_preds_coverage.parquet")
    parser.add_argument("--preds-imd2020", type=str, required=True, help="Path to enc_preds_imd2020.parquet")
    parser.add_argument("--labels-coverage", type=str, help="Path to original coverage labels (optional)")
    parser.add_argument("--labels-imd2020", type=str, help="Path to original imd2020 labels (optional)")
    parser.add_argument("--output-dir", type=str, default=".", help="Output directory for metrics")
    args = parser.parse_args()
    
    # Load client keys
    client = PaillierClient()
    client.load_keys(f"{args.keys_dir}/public_key.json", f"{args.keys_dir}/private_key.json")
    
    # Load and decrypt COVERAGE predictions
    print("=== COVERAGE Evaluation ===")
    df_cov_preds = pd.read_parquet(args.preds_coverage)
    enc_preds_cov = df_cov_preds['prediction'].tolist()
    preds_cov = client.decrypt_vector(enc_preds_cov)
    preds_cov = np.array(preds_cov)
    
    print(f"Decrypted {len(preds_cov)} predictions")
    print(f"Range: [{preds_cov.min():.4f}, {preds_cov.max():.4f}]")
    print(f"Mean: {preds_cov.mean():.4f}")
    
    # Load and decrypt IMD2020 predictions
    print("\n=== IMD2020 Evaluation ===")
    df_imd_preds = pd.read_parquet(args.preds_imd2020)
    enc_preds_imd = df_imd_preds['prediction'].tolist()
    preds_imd = client.decrypt_vector(enc_preds_imd)
    preds_imd = np.array(preds_imd)
    
    print(f"Decrypted {len(preds_imd)} predictions")
    print(f"Range: [{preds_imd.min():.4f}, {preds_imd.max():.4f}]")
    print(f"Mean: {preds_imd.mean():.4f}")
    
    # If labels provided, compute metrics
    if args.labels_coverage:
        print("\n--- COVERAGE Metrics ---")
        # Load labels (adapt to your format)
        labels_cov = pd.read_parquet(args.labels_coverage)['label'].values
        # Or if CSV: pd.read_csv(...)['label'].values
        
        auc_cov = roc_auc_score(labels_cov, preds_cov)
        acc_cov = accuracy_score(labels_cov, (preds_cov > 0.5).astype(int))
        prec_cov, rec_cov, f1_cov, _ = precision_recall_fscore_support(
            labels_cov, (preds_cov > 0.5).astype(int), average='binary'
        )
        
        print(f"AUC:  {auc_cov:.4f}")
        print(f"Acc:  {acc_cov:.4f}")
        print(f"Prec: {prec_cov:.4f}")
        print(f"Rec:  {rec_cov:.4f}")
        print(f"F1:   {f1_cov:.4f}")
        
        # Save metrics
        metrics_cov = {
            'dataset': 'COVERAGE',
            'auc': float(auc_cov),
            'accuracy': float(acc_cov),
            'precision': float(prec_cov),
            'recall': float(rec_cov),
            'f1': float(f1_cov),
            'n_samples': len(labels_cov)
        }
        
        with open(f"{args.output_dir}/metrics_coverage.json", 'w') as f:
            json.dump(metrics_cov, f, indent=2)
    
    if args.labels_imd2020:
        print("\n--- IMD2020 Metrics ---")
        labels_imd = pd.read_parquet(args.labels_imd2020)['label'].values
        
        auc_imd = roc_auc_score(labels_imd, preds_imd)
        acc_imd = accuracy_score(labels_imd, (preds_imd > 0.5).astype(int))
        prec_imd, rec_imd, f1_imd, _ = precision_recall_fscore_support(
            labels_imd, (preds_imd > 0.5).astype(int), average='binary'
        )
        
        print(f"AUC:  {auc_imd:.4f}")
        print(f"Acc:  {acc_imd:.4f}")
        print(f"Prec: {prec_imd:.4f}")
        print(f"Rec:  {rec_imd:.4f}")
        print(f"F1:   {f1_imd:.4f}")
        
        metrics_imd = {
            'dataset': 'IMD2020',
            'auc': float(auc_imd),
            'accuracy': float(acc_imd),
            'precision': float(prec_imd),
            'recall': float(rec_imd),
            'f1': float(f1_imd),
            'n_samples': len(labels_imd)
        }
        
        with open(f"{args.output_dir}/metrics_imd2020.json", 'w') as f:
            json.dump(metrics_imd, f, indent=2)
    
    # Save decrypted predictions for further analysis
    pd.DataFrame({'prediction': preds_cov}).to_parquet(
        f"{args.output_dir}/dec_preds_coverage.parquet", index=False)
    pd.DataFrame({'prediction': preds_imd}).to_parquet(
        f"{args.output_dir}/dec_preds_imd2020.parquet", index=False)
    
    print(f"\nDecrypted predictions saved to {args.output_dir}/")
    print("Done!")


if __name__ == "__main__":
    main()