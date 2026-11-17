"""
Paillier Encryption Client for Encrypted-Domain Forgery Detection
Handles key generation, feature encryption, and result decryption.
"""

import json
import pickle
import base64
from typing import List, Tuple, Union, Optional
import numpy as np
from phe import paillier


class PaillierClient:
    """
    Client-side Paillier encryption for forensic features.
    Private key stays local; only public key sent to server.
    """
    
    def __init__(self, key_size: int = 2048):
        """
        Initialize with key size (2048 recommended for security).
        Larger keys = slower but more secure.
        """
        self.key_size = key_size
        self.public_key: Optional[paillier.PaillierPublicKey] = None
        self.private_key: Optional[paillier.PaillierPrivateKey] = None
    
    def generate_keys(self) -> Tuple[paillier.PaillierPublicKey, paillier.PaillierPrivateKey]:
        """Generate new Paillier keypair."""
        print(f"Generating Paillier keypair ({self.key_size}-bit)...")
        self.public_key, self.private_key = paillier.generate_paillier_keypair(n_length=self.key_size)
        print("Keys generated.")
        return self.public_key, self.private_key
    
    def load_keys(self, public_key_path: str, private_key_path: str):
        """Load keys from files."""
        with open(public_key_path, 'r') as f:
            pub_data = json.load(f)
        self.public_key = paillier.PaillierPublicKey(n=pub_data['n'])
        
        with open(private_key_path, 'r') as f:
            priv_data = json.load(f)
        self.private_key = paillier.PaillierPrivateKey(
            public_key=self.public_key,
            p=priv_data['p'],
            q=priv_data['q']
        )
    
    def save_keys(self, public_key_path: str, private_key_path: str):
        """Save keys to files (JSON format)."""
        if not self.public_key or not self.private_key:
            raise ValueError("Keys not generated/loaded")
        
        pub_data = {'n': self.public_key.n}
        with open(public_key_path, 'w') as f:
            json.dump(pub_data, f)
        
        priv_data = {'p': self.private_key.p, 'q': self.private_key.q}
        with open(private_key_path, 'w') as f:
            json.dump(priv_data, f)
        
        print(f"Keys saved to {public_key_path}, {private_key_path}")
    
    def get_public_key_dict(self) -> dict:
        """Return public key as dict for sending to server."""
        if not self.public_key:
            raise ValueError("Public key not available")
        return {'n': str(self.public_key.n)}  # n as string for JSON
    
    def encrypt_vector(self, vector: np.ndarray) -> List[str]:
        """
        Encrypt a feature vector (1D numpy array).
        Returns list of base64-encoded ciphertext strings.
        """
        if not self.public_key:
            raise ValueError("Public key not available")
        
        encrypted = []
        for val in vector.flatten():
            # Scale float to int (Paillier encrypts integers)
            # Scale factor: 10^6 for 6 decimal precision
            scaled = int(val * 1_000_000)
            ciphertext = self.public_key.encrypt(scaled)
            # Serialize ciphertext
            enc_str = base64.b64encode(pickle.dumps(ciphertext)).decode('utf-8')
            encrypted.append(enc_str)
        
        return encrypted
    
    def encrypt_scalar(self, value: float) -> str:
        """Encrypt a single scalar value (e.g., label)."""
        if not self.public_key:
            raise ValueError("Public key not available")
        scaled = int(value * 1_000_000)
        ciphertext = self.public_key.encrypt(scaled)
        return base64.b64encode(pickle.dumps(ciphertext)).decode('utf-8')
    
    def decrypt_vector(self, encrypted_vector: List[str], scale: float = 1_000_000) -> np.ndarray:
        """
        Decrypt a vector of ciphertexts back to float array.
        """
        if not self.private_key:
            raise ValueError("Private key not available")
        
        decrypted = []
        for enc_str in encrypted_vector:
            ciphertext = pickle.loads(base64.b64decode(enc_str))
            plaintext = self.private_key.decrypt(ciphertext)
            decrypted.append(plaintext / scale)
        
        return np.array(decrypted, dtype=np.float32)
    
    def decrypt_scalar(self, enc_str: str, scale: float = 1_000_000) -> float:
        """Decrypt a single ciphertext."""
        if not self.private_key:
            raise ValueError("Private key not available")
        ciphertext = pickle.loads(base64.b64decode(enc_str))
        plaintext = self.private_key.decrypt(ciphertext)
        return plaintext / scale


def encrypt_dataset_features(
    features_array: np.ndarray,  # (n_samples, n_features)
    labels_array: np.ndarray,    # (n_samples,) - 0 or 1
    client: PaillierClient,
    output_path: str
):
    """
    Encrypt entire dataset and save to parquet.
    """
    import pandas as pd
    
    n_samples, n_features = features_array.shape
    print(f"Encrypting {n_samples} samples × {n_features} features...")
    
    enc_data = []
    for i in range(n_samples):
        enc_features = client.encrypt_vector(features_array[i])
        enc_label = client.encrypt_scalar(labels_array[i])
        enc_data.append({
            'sample_id': i,
            'features': enc_features,
            'label': enc_label
        })
        
        if (i + 1) % 100 == 0:
            print(f"  Encrypted {i + 1}/{n_samples}")
    
    df = pd.DataFrame(enc_data)
    df.to_parquet(output_path, index=False)
    print(f"Saved encrypted dataset to {output_path}")
    
    return df


def load_encrypted_dataset(parquet_path: str) -> Tuple[List[List[str]], List[str]]:
    """Load encrypted dataset from parquet."""
    import pandas as pd
    df = pd.read_parquet(parquet_path)
    features = df['features'].tolist()
    labels = df['label'].tolist()
    return features, labels


if __name__ == "__main__":
    # Quick test
    client = PaillierClient(key_size=2048)
    client.generate_keys()
    client.save_keys("public_key.json", "private_key.json")
    
    # Test encryption/decryption
    test_vec = np.array([0.123456, -0.654321, 1.0, 0.0, 0.5], dtype=np.float32)
    enc = client.encrypt_vector(test_vec)
    dec = client.decrypt_vector(enc)
    print(f"Original: {test_vec}")
    print(f"Decrypted: {dec}")
    print(f"Max error: {np.max(np.abs(test_vec - dec))}")