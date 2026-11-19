"""
Paillier Server-Side Operations for Encrypted-Domain Forgery Detection
Runs on Colab (no private key) — only public key operations.
"""

import json
import pickle
import base64
import numpy as np
from typing import List, Tuple, Optional, Union
from phe import paillier
import warnings
warnings.filterwarnings('ignore')


class PaillierServer:
    """
    Server-side Paillier operations (public key only).
    Supports encrypted linear algebra for logistic regression.
    """
    
    def __init__(self, public_key_path: str = None, public_key_dict: dict = None, n_value: int = None):
        """
        Initialize with public key from file, dict, or raw n value.
        """
        if public_key_path:
            with open(public_key_path, 'r') as f:
                pk_data = json.load(f)
            n = int(pk_data['n'])
        elif public_key_dict:
            n = int(public_key_dict['n'])
        elif n_value:
            n = n_value
        else:
            raise ValueError("Must provide public_key_path, public_key_dict, or n_value")
        
        self.public_key = paillier.PaillierPublicKey(n=n)
        self.scale = 1_000_000  # Must match client scale factor
        
        print(f"PaillierServer initialized with {self.public_key.n.bit_length()}-bit key")
    
    # ============================================================
    # Core Encrypted Linear Algebra
    # ============================================================
    
    def encrypted_dot_product(self, enc_vector: List[str], plain_vector: np.ndarray) -> str:
        """
        Compute Enc(x) · w = Σ Enc(x_i) * w_i (homomorphic)
        
        Args:
            enc_vector: List of base64-encoded ciphertexts
            plain_vector: Plaintext weights (numpy array)
        
        Returns:
            base64-encoded ciphertext of dot product
        """
        if len(enc_vector) != len(plain_vector):
            raise ValueError(f"Dimension mismatch: {len(enc_vector)} vs {len(plain_vector)}")
        
        # Deserialize first ciphertext
        result = pickle.loads(base64.b64decode(enc_vector[0]))
        result = result * plain_vector[0]  # Scalar multiplication
        
        # Add remaining terms
        for i in range(1, len(enc_vector)):
            enc_val = pickle.loads(base64.b64decode(enc_vector[i]))
            term = enc_val * plain_vector[i]
            result = result + term  # Homomorphic addition
        
        return base64.b64encode(pickle.dumps(result)).decode('utf-8')
    
    def encrypted_vector_add(self, enc_vec1: List[str], enc_vec2: List[str]) -> List[str]:
        """Enc(x) + Enc(y) = Enc(x + y) element-wise."""
        return [
            base64.b64encode(pickle.dumps(
                pickle.loads(base64.b64decode(a)) + pickle.loads(base64.b64decode(b))
            )).decode('utf-8')
            for a, b in zip(enc_vec1, enc_vec2)
        ]
    
    def encrypted_scalar_mul(self, enc_vector: List[str], scalar: float) -> List[str]:
        """Enc(x) * c = Enc(c * x) element-wise."""
        return [
            base64.b64encode(pickle.dumps(
                pickle.loads(base64.b64decode(enc)) * scalar
            )).decode('utf-8')
            for enc in enc_vector
        ]
    
    def encrypted_add_plain(self, enc_vector: List[str], plain_vector: np.ndarray) -> List[str]:
        """Enc(x) + y = Enc(x + y) element-wise (plain vector added to encrypted)."""
        return [
            base64.b64encode(pickle.dumps(
                pickle.loads(base64.b64decode(enc)) + int(val * self.scale)
            )).decode('utf-8')
            for enc, val in zip(enc_vector, plain_vector)
        ]
    
    # ============================================================
    # Encrypted Logistic Regression
    # ============================================================
    
    def encrypted_linear_forward(self, enc_features: List[str], weights: np.ndarray, bias: float) -> str:
        """
        Encrypted linear layer: Enc(features) · weights + bias
        Returns Enc(logits)
        """
        enc_logits = self.encrypted_dot_product(enc_features, weights)
        
        # Add bias (plaintext)
        bias_cipher = self.public_key.encrypt(int(bias * self.scale))
        enc_logits_obj = pickle.loads(base64.b64decode(enc_logits))
        enc_logits_obj = enc_logits_obj + bias_cipher
        
        return base64.b64encode(pickle.dumps(enc_logits_obj)).decode('utf-8')
    
    def encrypted_sigmoid(self, enc_logits: str, degree: int = 3) -> str:
        """
        Polynomial approximation of sigmoid on ciphertext.
        σ(x) ≈ 0.5 + 0.2159x - 0.0082x³ (degree 3, optimized for [-4, 4])
        
        For degree=1: σ(x) ≈ 0.5 + 0.25x
        For degree=3: σ(x) ≈ 0.5 + 0.2159x - 0.0082x³
        
        Returns Enc(probability)
        """
        enc_obj = pickle.loads(base64.b64decode(enc_logits))
        
        if degree == 1:
            # σ(x) ≈ 0.5 + 0.25x
            result = enc_obj * 0.25
            half = self.public_key.encrypt(int(0.5 * self.scale))
            result = result + half
            
        elif degree == 3:
            # σ(x) ≈ 0.5 + 0.2159x - 0.0082x³
            # Need x² and x³ - but Paillier can't do Enc(x) * Enc(x)
            # Approximation: use precomputed powers or client-assisted
            # For now, use degree 1 as fallback
            # TODO: Client-assisted higher degree
            result = enc_obj * 0.25
            half = self.public_key.encrypt(int(0.5 * self.scale))
            result = result + half
            
        else:
            # Linear fallback
            result = enc_obj * 0.25
            half = self.public_key.encrypt(int(0.5 * self.scale))
            result = result + half
        
        return base64.b64encode(pickle.dumps(result)).decode('utf-8')
    
    def encrypted_sigmoid_client_assisted(self, enc_logits: str, client_public_key: paillier.PaillierPublicKey) -> str:
        """
        Client-assisted sigmoid for better approximation.
        Server sends Enc(logits) to client → client decrypts → computes sigmoid → encrypts → returns.
        This is a round-trip but gives exact sigmoid.
        """
        # Server just returns the logits; client does the rest
        return enc_logits
    
    # ============================================================
    # Encrypted SGD Training
    # ============================================================
    
    def encrypted_sgd_step(
        self,
        enc_features: List[str],      # Enc(x_i)
        enc_label: str,               # Enc(y_i)
        weights: np.ndarray,          # w (plaintext)
        bias: float,                  # b (plaintext)
        learning_rate: float
    ) -> Tuple[np.ndarray, float]:
        """
        One step of encrypted SGD for logistic regression.
        
        Server computes:
        1. Enc(logits) = Enc(x) · w + b
        2. Returns Enc(logits) to client
        3. Client decrypts, computes gradient ∇L = (σ(logits) - y) * x
        4. Client encrypts gradient, sends back
        5. Server updates: w ← w - η * ∇L
        
        Since server can't compute sigmoid well, we use client-assisted approach.
        
        Returns: (updated_weights, updated_bias) — both plaintext
        """
        # Server computes Enc(logits)
        enc_logits = self.encrypted_linear_forward(enc_features, weights, bias)
        
        # Client does: decrypt → sigmoid → gradient → encrypt gradient
        # This is a placeholder - actual implementation needs client round-trip
        # For now, return unchanged (client will compute gradient)
        
        return weights, bias
    
    def encrypted_sgd_step_server_only(
        self,
        enc_features: List[str],
        enc_label: str,
        weights: np.ndarray,
        bias: float,
        learning_rate: float,
        use_linear_sigmoid: bool = True
    ) -> Tuple[np.ndarray, float]:
        """
        Server-only SGD using linear sigmoid approximation.
        Less accurate but no client round-trip.
        
        Gradient: ∇L = (σ(logits) - y) * x
        With linear sigmoid: σ(z) ≈ 0.5 + 0.25z
        ∇L ≈ (0.5 + 0.25*logits - y) * x
        """
        # Compute Enc(logits)
        enc_logits = self.encrypted_linear_forward(enc_features, weights, bias)
        
        if use_linear_sigmoid:
            # Server computes Enc(0.5 + 0.25*logits - y) approximately
            # But we can't multiply Enc(logits) by 0.25 and subtract Enc(y) easily
            # because we need to then multiply by x (encrypted)...
            # This requires client assistance for the multiplication by x
            
            pass
        
        # For full server-side, we'd need client to help with Enc(x) * Enc(scalar)
        # which Paillier can't do directly.
        
        return weights, bias
    
    # ============================================================
    # Encrypted Domain Adaptation (Linear Procrustes)
    # ============================================================
    
    def encrypted_linear_map_apply(self, enc_features: List[str], A: np.ndarray, b: np.ndarray) -> List[str]:
        """
        Apply encrypted linear transformation: Enc(x) * A + b
        A: (d, d) matrix, b: (d,) vector
        Returns: Enc(x_transformed) as list of ciphertexts
        """
        d = A.shape[0]
        if len(enc_features) != d:
            raise ValueError(f"Feature dim {len(enc_features)} != A dim {d}")
        
        result = []
        for j in range(d):
            # Compute Enc(Σ_i x_i * A_ij)
            enc_sum = self.encrypted_dot_product(enc_features, A[:, j])
            # Add bias b_j
            bias_cipher = self.public_key.encrypt(int(b[j] * self.scale))
            enc_obj = pickle.loads(base64.b64decode(enc_sum))
            enc_obj = enc_obj + bias_cipher
            result.append(base64.b64encode(pickle.dumps(enc_obj)).decode('utf-8'))
        
        return result
    
    def encrypted_linear_map_learn(
        self,
        enc_source_features: List[List[str]],   # Enc(x_casia) - list of samples
        enc_target_features: List[List[str]],   # Enc(x_target) - list of samples
        regularization: float = 0.01
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Learn linear map A, b such that: x_target * A + b ≈ x_casia
        
        This is encrypted least squares. Server can't solve directly because
        it needs matrix operations on ciphertexts.
        
        Approach: Client assists by providing Enc(x_target^T * x_target) etc.
        Or: Server computes in plaintext if client sends encrypted statistics.
        
        For now, return identity (placeholder).
        """
        d = len(enc_source_features[0])
        A = np.eye(d, dtype=np.float32)
        b = np.zeros(d, dtype=np.float32)
        return A, b
    
    # ============================================================
    # Utility: Encrypted Statistics (Client-Assisted)
    # ============================================================
    
    def compute_encrypted_covariance_client_assisted(
        self,
        enc_features_list: List[List[str]],  # List of Enc(x_i)
    ) -> List[List[str]]:
        """
        Compute Enc(covariance matrix) with client assistance.
        Client sends Enc(x_i * x_j) for all pairs.
        Server sums them up.
        """
        # This requires client to precompute outer products
        pass


# ============================================================
# Helper Functions
# ============================================================

def load_encrypted_dataset(parquet_path: str) -> Tuple[List[List[str]], List[str]]:
    """Load encrypted features and labels from parquet."""
    import pandas as pd
    df = pd.read_parquet(parquet_path)
    features = df['features'].tolist()  # List of List[str]
    labels = df['label'].tolist()       # List[str]
    return features, labels


def save_encrypted_predictions(enc_predictions: List[str], output_path: str, sample_ids: List[int] = None):
    """Save encrypted predictions to parquet for client download."""
    import pandas as pd
    if sample_ids is None:
        sample_ids = list(range(len(enc_predictions)))
    df = pd.DataFrame({'sample_id': sample_ids, 'prediction': enc_predictions})
    df.to_parquet(output_path, index=False)


if __name__ == "__main__":
    # Test with dummy key
    n = paillier.generate_paillier_keypair(n_length=1024)[0].n
    server = PaillierServer(n_value=n)
    
    # Test encrypted dot product
    pub = server.public_key
    w = np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32)
    x = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)
    
    enc_x = [base64.b64encode(pickle.dumps(pub.encrypt(int(v * server.scale)))).decode('utf-8') for v in x]
    
    enc_dot = server.encrypted_dot_product(enc_x, w)
    print("Encrypted dot product computed successfully")