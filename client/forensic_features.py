"""
Forensic Feature Extraction for Encrypted-Domain Forgery Detection
Extracts ~304-dim feature vector from images (plaintext, client-side).
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


# ============================================================
# SRM Filter Kernels (30 filters for noise residual extraction)
# ============================================================
SRM_KERNELS = [
    # 1st order derivatives
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, -2, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], dtype=np.float32) / 2,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, -2, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], dtype=np.float32) / 2,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, -2, 0, 0, 0], [0, 1, 0, 0, 0]], dtype=np.float32) / 2,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, -2, 1, 0]], dtype=np.float32) / 2,
    np.array([[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, -2, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]], dtype=np.float32) / 2,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, -2, 1, 0, 0]], dtype=np.float32) / 2,
    # 2nd order derivatives
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, -2, 1, 0], [0, 0, 0, 0, 0]], dtype=np.float32) / 4,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, -2, 1], [0, 0, 0, 0, 0]], dtype=np.float32) / 4,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, -2, 1, 0, 0]], dtype=np.float32) / 4,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, -2, 1, 0]], dtype=np.float32) / 4,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, -2, 1]], dtype=np.float32) / 4,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 0, 0, 0]], dtype=np.float32) / 4,
    # 3rd order (simplified subset for 30 total)
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, -3, 3, -1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, -3, 3, -1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], dtype=np.float32) / 6,
    np.array([[0, 0, 1, 0, 0], [0, 0, -3, 0, 0], [0, 0, 3, 0, 0], [0, 0, -1, 0, 0], [0, 0, 0, 0, 0]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, -3, 0, 0], [0, 0, 3, -1, 0]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, -3, 0, 0, 0], [0, 3, 0, 0, 0], [0, -1, 0, 0, 0]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, -3, 3]], dtype=np.float32) / 6,
    # Additional directional filters
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, -3, 3, -1], [0, 0, 0, 0, 0]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, -3, 3], [0, 0, 0, 0, -1]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, -3, 3, -1, 0], [0, 0, 0, 0, 0]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, -3, 3, -1], [0, 0, 0, 0, 0]], dtype=np.float32) / 6,
    np.array([[0, 0, 1, 0, 0], [0, 0, -3, 0, 0], [0, 0, 3, 0, 0], [0, 0, -1, 0, 0], [0, 0, 0, 0, 0]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, -3, 0, 0, 0], [0, 3, 0, 0, 0], [0, -1, 0, 0, 0]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, -3, 3, -1, 0]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, -3, 3, -1]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, -3, 3]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, -3]], dtype=np.float32) / 6,
    np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 1]], dtype=np.float32) / 6,
    # Square 5x5 averaging for baseline
    np.ones((5, 5), dtype=np.float32) / 25,
    # Edge-enhancement
    np.array([[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, 24, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]], dtype=np.float32) / 25,
]


def extract_dct_histogram_moments(image: np.ndarray, block_size: int = 8, num_bands: int = 16) -> np.ndarray:
    """
    Extract DCT histogram moments per frequency band.
    Returns: 64-dim vector (16 bands × 4 moments: mean, var, skew, kurtosis)
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    h, w = gray.shape
    gray = gray[:h//block_size*block_size, :w//block_size*block_size]
    
    # Compute DCT for each block
    dct_coeffs = []
    for y in range(0, gray.shape[0], block_size):
        for x in range(0, gray.shape[1], block_size):
            block = gray[y:y+block_size, x:x+block_size].astype(np.float32)
            dct_block = cv2.dct(block)
            dct_coeffs.append(dct_block.flatten())
    
    dct_coeffs = np.array(dct_coeffs)  # (num_blocks, 64)
    
    # Group 64 frequencies into bands (zigzag order approximation)
    # Simplified: group by frequency magnitude (low to high)
    zigzag_order = [
        0, 1, 8, 16, 9, 2, 3, 10, 17, 24, 32, 25, 18, 11, 4, 5,
        12, 19, 26, 33, 40, 48, 41, 34, 27, 20, 13, 6, 7, 14, 21, 28,
        35, 42, 49, 56, 57, 50, 43, 36, 29, 22, 15, 23, 30, 37, 44,
        51, 58, 59, 52, 45, 38, 31, 39, 46, 53, 60, 61, 54, 47, 55, 62, 63
    ]
    
    features = []
    bands_per_group = 64 // num_bands
    
    for b in range(num_bands):
        start_idx = b * bands_per_group
        end_idx = (b + 1) * bands_per_group if b < num_bands - 1 else 64
        band_indices = zigzag_order[start_idx:end_idx]
        
        band_coeffs = dct_coeffs[:, band_indices].flatten()
        
        if len(band_coeffs) > 0:
            mean_val = np.mean(band_coeffs)
            var_val = np.var(band_coeffs)
            skew_val = _skewness(band_coeffs)
            kurt_val = _kurtosis(band_coeffs)
        else:
            mean_val = var_val = skew_val = kurt_val = 0.0
        
        features.extend([mean_val, var_val, skew_val, kurt_val])
    
    return np.array(features, dtype=np.float32)


def _skewness(x: np.ndarray) -> float:
    if len(x) < 3 or np.std(x) == 0:
        return 0.0
    return float(np.mean(((x - np.mean(x)) / np.std(x)) ** 3))


def _kurtosis(x: np.ndarray) -> float:
    if len(x) < 4 or np.std(x) == 0:
        return 0.0
    return float(np.mean(((x - np.mean(x)) / np.std(x)) ** 4) - 3)


def extract_double_jpeg_features(image: np.ndarray) -> np.ndarray:
    """
    Extract double-JPEG detection features (Korus-style).
    Returns: 20-dim vector
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    features = []
    
    # 1. DCT coefficient histogram periodicity (Benford's law deviation)
    dct = cv2.dct(gray.astype(np.float32))
    dct_flat = dct.flatten()
    hist, _ = np.histogram(dct_flat, bins=100, range=(-50, 50))
    hist = hist.astype(np.float32) + 1e-10
    
    # Periodicity in histogram (double JPEG creates periodic peaks)
    fft_hist = np.fft.fft(hist)
    fft_mag = np.abs(fft_hist[1:50])  # Ignore DC
    features.append(float(np.max(fft_mag) / (np.mean(fft_mag) + 1e-10)))  # Peak strength
    features.append(float(np.argmax(fft_mag)))  # Peak position (related to QF)
    
    # 2. Block-wise QF estimation variation
    h, w = gray.shape
    block_qfs = []
    for y in range(0, h - 8, 8):
        for x in range(0, w - 8, 8):
            block = gray[y:y+8, x:x+8].astype(np.float32)
            dct_block = cv2.dct(block)
            # Estimate QF from quantization step (simplified)
            ac_coeffs = dct_block.flatten()[1:]  # Skip DC
            if np.std(ac_coeffs) > 0:
                qf_est = 100 - min(99, int(np.std(ac_coeffs) * 10))
                block_qfs.append(qf_est)
    
    if block_qfs:
        features.append(float(np.mean(block_qfs)))
        features.append(float(np.std(block_qfs)))
        features.append(float(np.max(block_qfs) - np.min(block_qfs)))
    else:
        features.extend([0.0, 0.0, 0.0])
    
    # 3. JPEG ghost detection (re-compress at different QFs, measure difference)
    for test_qf in [50, 60, 70, 75, 80, 85, 90, 95]:
        _, buf = cv2.imencode('.jpg', gray, [cv2.IMWRITE_JPEG_QUALITY, test_qf])
        recon = cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE)
        diff = np.mean(np.abs(gray.astype(np.float32) - recon.astype(np.float32)))
        features.append(float(diff))
    
    # 4. Alignment statistics (double JPEG grid alignment)
    # Check 8x8 block boundary artifacts
    h, w = gray.shape
    v_boundary_diff = 0
    h_boundary_diff = 0
    count = 0
    for y in range(8, h, 8):
        if y < h:
            v_boundary_diff += np.mean(np.abs(gray[y, :].astype(np.float32) - gray[y-1, :].astype(np.float32)))
            count += 1
    for x in range(8, w, 8):
        if x < w:
            h_boundary_diff += np.mean(np.abs(gray[:, x].astype(np.float32) - gray[:, x-1].astype(np.float32)))
            count += 1
    
    features.append(float(v_boundary_diff / max(1, count//2)))
    features.append(float(h_boundary_diff / max(1, count//2)))
    
    # Pad to 20 dims
    while len(features) < 20:
        features.append(0.0)
    
    return np.array(features[:20], dtype=np.float32)


def extract_srm_noise_residual(image: np.ndarray) -> np.ndarray:
    """
    Extract noise residual features using SRM filters.
    Returns: 100-dim vector (30 filters × ~3 stats each)
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    gray = gray.astype(np.float32)
    features = []
    
    for kernel in SRM_KERNELS:
        residual = cv2.filter2D(gray, -1, kernel)
        
        # Statistics on residual
        mean_val = np.mean(residual)
        var_val = np.var(residual)
        energy = np.mean(residual ** 2)
        
        features.extend([float(mean_val), float(var_val), float(energy)])
    
    # Ensure 100 dims (30 filters × 3 = 90, pad to 100)
    while len(features) < 100:
        features.append(0.0)
    
    return np.array(features[:100], dtype=np.float32)


def extract_block_correlation(image: np.ndarray, block_size: int = 8) -> np.ndarray:
    """
    Extract DCT block self-similarity for copy-move detection.
    Rotation/scale robust via DCT coefficient correlation.
    Returns: 50-dim vector
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    h, w = gray.shape
    gray = gray[:h//block_size*block_size, :w//block_size*block_size]
    
    # Extract DCT blocks
    blocks = []
    positions = []
    for y in range(0, gray.shape[0], block_size):
        for x in range(0, gray.shape[1], block_size):
            block = gray[y:y+block_size, x:x+block_size].astype(np.float32)
            dct_block = cv2.dct(block)
            blocks.append(dct_block.flatten())
            positions.append((y, x))
    
    blocks = np.array(blocks)  # (num_blocks, 64)
    num_blocks = len(blocks)
    
    if num_blocks < 2:
        return np.zeros(50, dtype=np.float32)
    
    # Compute correlation matrix (sample subset for efficiency)
    sample_size = min(200, num_blocks)
    idx = np.random.choice(num_blocks, sample_size, replace=False)
    sampled_blocks = blocks[idx]
    
    # Normalize blocks
    norms = np.linalg.norm(sampled_blocks, axis=1, keepdims=True)
    norms[norms == 0] = 1
    normalized = sampled_blocks / norms
    
    # Correlation matrix
    corr_matrix = normalized @ normalized.T
    np.fill_diagonal(corr_matrix, 0)
    
    # Statistics of correlations
    features = [
        float(np.max(corr_matrix)),           # Max correlation (copy-move indicator)
        float(np.mean(corr_matrix)),          # Mean correlation
        float(np.std(corr_matrix)),           # Std correlation
        float(np.percentile(corr_matrix, 95)), # 95th percentile
        float(np.percentile(corr_matrix, 99)), # 99th percentile
    ]
    
    # Per-frequency-band correlation (group 64 coeffs into 9 bands, 5 stats each = 45)
    zigzag_order = [
        0, 1, 8, 16, 9, 2, 3, 10, 17, 24, 32, 25, 18, 11, 4, 5,
        12, 19, 26, 33, 40, 48, 41, 34, 27, 20, 13, 6, 7, 14, 21, 28,
        35, 42, 49, 56, 57, 50, 43, 36, 29, 22, 15, 23, 30, 37, 44,
        51, 58, 59, 52, 45, 38, 31, 39, 46, 53, 60, 61, 54, 47, 55, 62, 63
    ]
    
    for b in range(9):
        start_idx = b * 7
        end_idx = (b + 1) * 7 if b < 8 else 64
        band_indices = zigzag_order[start_idx:end_idx]
        
        band_blocks = sampled_blocks[:, band_indices]
        band_norms = np.linalg.norm(band_blocks, axis=1, keepdims=True)
        band_norms[band_norms == 0] = 1
        band_normalized = band_blocks / band_norms
        band_corr = band_normalized @ band_normalized.T
        np.fill_diagonal(band_corr, 0)
        
        features.extend([
            float(np.max(band_corr)),
            float(np.mean(band_corr)),
            float(np.std(band_corr)),
            float(np.percentile(band_corr, 95)),
            float(np.percentile(band_corr, 99)),
        ])
    
    # Pad to 50
    while len(features) < 50:
        features.append(0.0)
    
    return np.array(features[:50], dtype=np.float32)


def extract_jpeg_ghost(image: np.ndarray) -> np.ndarray:
    """
    JPEG ghost detection across multiple QFs.
    Returns: 30-dim vector
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    features = []
    qfs = list(range(50, 100, 5))  # 50, 55, ..., 95
    
    for qf in qfs:
        # Re-compress at QF
        _, buf = cv2.imencode('.jpg', gray, [cv2.IMWRITE_JPEG_QUALITY, qf])
        recon = cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE)
        
        # Compute difference
        diff = np.abs(gray.astype(np.float32) - recon.astype(np.float32))
        features.append(float(np.mean(diff)))
        features.append(float(np.std(diff)))
        features.append(float(np.max(diff)))
    
    # Ensure 30 dims
    while len(features) < 30:
        features.append(0.0)
    
    return np.array(features[:30], dtype=np.float32)


def extract_metadata_features(image_path: str) -> np.ndarray:
    """
    Extract EXIF/metadata consistency features.
    Returns: 10-dim vector (placeholder - needs PIL/exifread for real impl)
    """
    # Placeholder - real implementation would use PIL.Exif or exifread
    # For now return zeros; implement with PIL when available
    return np.zeros(10, dtype=np.float32)


def extract_compression_artifacts(image: np.ndarray) -> np.ndarray:
    """
    Extract blocking artifacts and quantization table estimates.
    Returns: 30-dim vector
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    features = []
    
    # 1. Blocking artifact strength (8x8 grid)
    h, w = gray.shape
    block_diff_v = []
    block_diff_h = []
    
    for y in range(8, h, 8):
        if y < h:
            diff = np.mean(np.abs(gray[y, :].astype(np.float32) - gray[y-1, :].astype(np.float32)))
            block_diff_v.append(diff)
    
    for x in range(8, w, 8):
        if x < w:
            diff = np.mean(np.abs(gray[:, x].astype(np.float32) - gray[:, x-1].astype(np.float32)))
            block_diff_h.append(diff)
    
    features.append(float(np.mean(block_diff_v) if block_diff_v else 0))
    features.append(float(np.std(block_diff_v) if block_diff_v else 0))
    features.append(float(np.mean(block_diff_h) if block_diff_h else 0))
    features.append(float(np.std(block_diff_h) if block_diff_h else 0))
    
    # 2. Quantization table estimation (from DCT coefficient distribution)
    dct = cv2.dct(gray.astype(np.float32))
    ac_coeffs = dct.flatten()[1:]  # Skip DC
    
    # Estimate quantization steps from histogram gaps
    hist, bins = np.histogram(ac_coeffs, bins=200, range=(-100, 100))
    hist = hist.astype(np.float32)
    
    # Find periodic zeros in histogram (quantization artifacts)
    fft_hist = np.fft.fft(hist)
    fft_mag = np.abs(fft_hist[1:100])
    
    # Top 10 frequencies
    top_freqs = np.argsort(fft_mag)[-10:]
    for freq in top_freqs:
        features.append(float(freq))
        features.append(float(fft_mag[freq]))
    
    # 3. DCT coefficient distribution stats
    features.append(float(np.mean(ac_coeffs)))
    features.append(float(np.std(ac_coeffs)))
    features.append(float(_skewness(ac_coeffs)))
    features.append(float(_kurtosis(ac_coeffs)))
    
    # Pad to 30
    while len(features) < 30:
        features.append(0.0)
    
    return np.array(features[:30], dtype=np.float32)


# ============================================================
# Main Feature Extraction Pipeline
# ============================================================
def extract_all_features(image: np.ndarray, image_path: str = "") -> np.ndarray:
    """
    Extract complete ~304-dim forensic feature vector.
    
    Args:
        image: BGR or grayscale image (numpy array)
        image_path: Optional path for metadata extraction
    
    Returns:
        304-dim float32 feature vector
    """
    features = []
    
    # 1. DCT Histogram Moments (64)
    features.append(extract_dct_histogram_moments(image))
    
    # 2. Double-JPEG Features (20)
    features.append(extract_double_jpeg_features(image))
    
    # 3. SRM Noise Residual (100)
    features.append(extract_srm_noise_residual(image))
    
    # 4. Block Correlation (50)
    features.append(extract_block_correlation(image))
    
    # 5. JPEG Ghost (30)
    features.append(extract_jpeg_ghost(image))
    
    # 6. Metadata (10)
    features.append(extract_metadata_features(image_path))
    
    # 7. Compression Artifacts (30)
    features.append(extract_compression_artifacts(image))
    
    # Concatenate
    feature_vector = np.concatenate(features).astype(np.float32)
    
    # Verify dimension
    expected = 304
    if len(feature_vector) != expected:
        if len(feature_vector) > expected:
            feature_vector = feature_vector[:expected]
        else:
            feature_vector = np.pad(feature_vector, (0, expected - len(feature_vector)))
    
    return feature_vector


def extract_features_from_path(image_path: str) -> np.ndarray:
    """Convenience: load image from path and extract features."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    return extract_all_features(image, image_path)


if __name__ == "__main__":
    # Quick test
    import sys
    if len(sys.argv) > 1:
        test_path = sys.argv[1]
        feats = extract_features_from_path(test_path)
        print(f"Extracted {len(feats)} features from {test_path}")
        print(f"Range: [{feats.min():.4f}, {feats.max():.4f}]")
        print(f"Mean: {feats.mean():.4f}, Std: {feats.std():.4f}")
    else:
        print("Usage: python forensic_features.py <image_path>")