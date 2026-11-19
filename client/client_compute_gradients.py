"""
Client-Side Gradient Computation for Encrypted SGD
Run locally after server saves a batch for processing.
"""

import json
import pickle
import base64
import numpy as np
from paillier_client import PaillierClient


def sigmoid(x):
    """Sigmoid function."""
    return 1 / (1 + np.exp(-np.clip(x, -20, 20)))


def compute_gradients(client: PaillierClient, batch_path: str, output_path: str):
    """
    Load server batch, decrypt, compute gradients, encrypt and save.
    
    Server batch format:
    {
        'enc_logits': [enc_str, ...],
        'enc_labels': [enc_str, ...],
        'weights': [...],
        'bias': float,
        'learning_rate': float,
        'feature_dim': int
    }
    """
    with open(batch_path, 'r') as f:
        batch = json.load(f)
    
    enc_logits_list = batch['enc_logits']
    enc_labels_list = batch['enc_labels']
    weights = np.array(batch['weights'], dtype=np.float32)
    bias = batch['bias']
    lr = batch['learning_rate']
    feature_dim = batch['feature_dim']
    
    print(f"Processing batch of {len(enc_logits_list)} samples...")
    
    # Decrypt logits and labels
    logits = client.decrypt_vector(enc_logits_list)
    labels = client.decrypt_vector(enc_labels_list)
    
    # Compute sigmoid and gradients
    probs = sigmoid(logits)
    errors = probs - labels  # (probs - y)
    
    # Gradient w.r.t weights: (probs - y) * x
    # But we don't have x! Server only sent logits.
    # We need the original features to compute weight gradients.
    
    # OPTION 1: Server also sends encrypted features (more bandwidth)
    # OPTION 2: Client already has features locally (recommended)
    
    print("NOTE: Need original features to compute weight gradients.")
    print("Options:")
    print("  1. Server sends Enc(features) too (more bandwidth)")
    print("  2. Client recomputes gradients from local features (recommended)")
    
    # For now, compute bias gradient only (doesn't need features)
    grad_bias = float(np.mean(errors))
    
    # For weight gradients, client must have local features
    # This requires client to know which samples were in the batch
    # Server should send sample_ids in batch
    
    # Placeholder: if sample_ids provided, client loads local features
    if 'sample_ids' in batch:
        # Client loads features for these sample_ids
        # grad_weights = np.mean(errors[:, None] * features, axis=0)
        pass
    else:
        print("WARNING: No sample_ids in batch. Cannot compute weight gradients.")
        print("Server must include 'sample_ids' in batch for full gradient.")
    
    # Encrypt gradients and save
    # For now, just save bias gradient
    enc_grad_bias = client.encrypt_scalar(grad_bias)
    
    result = {
        'enc_grad_bias': enc_grad_bias,
        'grad_bias_plaintext': grad_bias,  # For debugging
        'note': 'Weight gradients need sample_ids from server'
    }
    
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Saved gradients to {output_path}")
    print(f"Bias gradient: {grad_bias:.6f}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python client_compute_gradients.py <batch_json> <output_json>")
        sys.exit(1)
    
    client = PaillierClient()
    client.load_keys("keys/public_key.json", "keys/private_key.json")
    
    compute_gradients(client, sys.argv[1], sys.argv[2])