# Major Project - Update Log

## Project: Encrypted-Domain Image Forgery Detection
**Started:** 2026-11-17  
**Environment:** Google Colab Free (T4, 12hr, ~70GB)  
**Encryption:** Paillier (Additive HE) — `phe` library  
**Datasets (5 Selected):** CASIA v1/v2, Korus 2018, COVERAGE, IMD2020, MICC-F600  
**Threat Model:** Client encrypts forensic features → Server computes encrypted classification → Client decrypts result

---

## Novel Contribution: "Encrypted Domain Adaptation for Cross-Dataset Forgery Detection Generalization"

**Combines three novel elements (no paper does all three in encrypted domain):**

1. **Encrypted Training** — Paillier encrypted SGD for linear classifier (not just inference)
2. **Encrypted Domain Adaptation** — Learn encrypted feature-space mapping (CASIA → COVERAGE/IMD2020)
3. **Encrypted Generalization Test** — Evaluate on target datasets entirely in encrypted domain (never decrypt test features)

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────────┐
│ PHASE 1: ENCRYPTED TRAINING (CASIA v2)                            │
├────────────────────────────────────────────────────────────────────┤
│  Client: Extract forensic features → Encrypt(x_i, y_i) → Send     │
│  Colab:  Encrypted SGD on linear classifier                       │
│          Enc(W) ← Enc(W) - η * Enc(∇L)  [Paillier supports this]  │
│  Output: Enc(W_casia), Enc(b_casia)  [never decrypted!]           │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ PHASE 2: ENCRYPTED DOMAIN ADAPTATION (CASIA → COVERAGE/IMD2020)   │
├────────────────────────────────────────────────────────────────────┤
│  Client: Extract features from COVERAGE/IMD2020 → Encrypt(x_tgt)  │
│  Colab:  Learn encrypted linear map Enc(A), Enc(b) s.t.           │
│          Enc(x_tgt) * A + b ≈ Enc(x_casia)                        │
│          (Encrypted least squares / Procrustes)                   │
│  Output: Enc(A), Enc(b)  [feature space alignment, encrypted]     │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ PHASE 3: ENCRYPTED GENERALIZATION TEST                            │
├────────────────────────────────────────────────────────────────────┤
│  Client: Encrypt(test features from COVERAGE/IMD2020)             │
│  Colab:  Enc(x_test) → Enc(x_test) * A + b → Enc(W_casia) →      │
│          Enc(logits) → Enc(poly sigmoid) → Return Enc(pred)       │
│  Client: Decrypt → AUC per dataset, per forgery type              │
│  Result: Cross-dataset generalization **fully encrypted**         │
└────────────────────────────────────────────────────────────────────┘
```

---

## Forensic Feature Vector (~300 dimensions, extracted client-side, plaintext)

| Feature Group | Dimensions | Description |
|---------------|------------|-------------|
| **DCT Histogram Moments** | 64 | Mean, var, skew, kurtosis per 8×8 DCT frequency band (16 bands × 4 moments) |
| **Double-JPEG Detection** | 20 | Alignment stats, QF estimates, ghost peaks (Korus-style) |
| **Noise Residual (SRM)** | 100 | 30 SRM filters × stats (mean, var, energy) on residual |
| **Block Correlation** | 50 | DCT block self-similarity for copy-move (rotation/scale robust) |
| **JPEG Ghost** | 30 | Re-compression artifacts at different QFs |
| **Metadata/EXIF** | 10 | Consistency checks, software tags, timestamps |
| **Compression Artifacts** | 30 | Blocking artifacts, quantization table estimation |
| **TOTAL** | **~304** | Manageable for Paillier on Colab Free |

---

## Dataset Roles

| Dataset | Role | Feature Focus |
|---------|------|---------------|
| **CASIA v2** | Primary train (encrypted) | All features — JPEG native |
| **Korus 2018** | Train/Val for domain adaptation | Double-JPEG, controlled QF, camera labels |
| **MICC-F600** | Train/Val for domain adaptation | Block correlation (known rotation/scale) |
| **COVERAGE** | Encrypted test (generalization) | Modern generators (GAN, diffusion), multi-forgery |
| **IMD2020** | Encrypted test (generalization) | Semantic realism, inpainting/removal |

---

## Implementation Priority

| Step | Task | Dependencies |
|------|------|--------------|
| 1 | Feature extraction pipeline (plaintext, client) | OpenCV, jpeg4py, SRM filters |
| 2 | Download Korus, IMD2020, MICC (direct links) | — |
| 3 | Request CASIA v1/v2 access (academic form) | — |
| 4 | Colab notebook: Drive mount, dataset loaders | Google Drive |
| 5 | Paillier encrypted linear classifier + SGD | `phe` library |
| 6 | Encrypted domain adaptation (linear Procrustes) | Client assists with non-linear steps |
| 7 | Encrypted polynomial sigmoid approximation | σ(x) ≈ 0.5 + 0.21x - 0.008x³ |
| 8 | Evaluation: AUC per dataset, per forgery type | — |

---

## Colab Free Optimizations

- **Patch-based training** — 256×256 patches, not full images
- **Gradient checkpointing** + mixed precision (fp16)
- **Pre-extract features locally** → upload only encrypted feature vectors
- **Paillier batching** — pack multiple features per ciphertext where possible
- **Model weights stay plaintext** on server (only data encrypted)

---

## Language Decision: Python (Not Rust)

**Rationale:**
- `phe` (Paillier) library: mature pure Python, no Rust equivalent
- OpenCV/jpeg4py/SRM: native Python bindings, Colab-native
- Colab = Python runtime; Rust would need WASM/binary workaround
- Prototyping speed: 10x faster iteration in Python
- Dataset tooling (pandas/parquet): first-class in Python

**Rust later:** Only for production deployment (edge, speed, memory safety). Not for research phase.

---

## Dataset Access Status

| Dataset | Access Method | Status |
|---------|---------------|--------|
| CASIA v1/v2 | Academic request (forensics.idealtest.org) | **Pending** — request today |
| Korus 2018 | GitHub: pkorus/korus2018-dataset | **Ready** — direct download |
| COVERAGE | GitHub: SCLBD/COVERAGE | **Ready** — large, download subset first |
| IMD2020 | GitHub: imd2020/IMD2020 | **Ready** — direct download |
| MICC-F600 | micc.unifi.it/MICC-F600/ | **Ready** — request or direct |

---

## Key Files

| File | Purpose |
|------|---------|
| `D:\major project\datasets\00_FINAL_SELECTION_5_DATASETS.md` | Final dataset selection rationale |
| `D:\major project\datasets\00_DATASET_MASTER_INDEX.md` | Master index with paper cross-references |
| `D:\major project\UPDATE_LOG.md` | This file — session continuity |

---

## Next Session Continuation Prompt

> "Read UPDATE_LOG.md. Continue from Step 1: feature extraction code for forensic features (DCT, SRM, double-JPEG, block correlation). Target: ~300-dim vector. Plaintext, client-side. Output: Python module + Colab-ready feature extraction notebook."

---

## Client-Side Implementation (Created 2026-11-17)

### Files Created

| File | Purpose |
|------|---------|
| `D:\major project\client\forensic_features.py` | Complete ~304-dim feature extractor (DCT, SRM, double-JPEG, block correlation, JPEG ghost, compression artifacts, metadata) |
| `D:\major project\client\paillier_client.py` | Paillier key management, vector encryption/decryption, dataset encryption to parquet |
| `D:\major project\client\extract_and_encrypt.py` | End-to-end CLI: load dataset → extract features → encrypt → save parquet for Colab |
| `D:\major project\client\requirements.txt` | Dependencies: phe, opencv, numpy, pandas, pyarrow, tqdm |

### Client Pipeline

```bash
# 1. Install deps
cd D:\major project\client
pip install -r requirements.txt

# 2. Run for each dataset (generates keys on first run)
python extract_and_encrypt.py --dataset-root D:\major_project_datasets --dataset CASIA_v2 --output ..\colab_data\enc_casia.parquet --generate-keys
python extract_and_encrypt.py --dataset-root D:\major_project_datasets --dataset Korus_2018 --output ..\colab_data\enc_korus.parquet
python extract_and_encrypt.py --dataset-root D:\major_project_datasets --dataset MICC_F600 --output ..\colab_data\enc_micc.parquet
# COVERAGE/IMD2020 for test sets (no training)
python extract_and_encrypt.py --dataset-root D:\major_project_datasets --dataset COVERAGE --output ..\colab_data\enc_coverage_test.parquet
python extract_and_encrypt.py --dataset-root D:\major_project_datasets --dataset IMD2020 --output ..\colab_data\enc_imd2020_test.parquet

# 3. Upload colab_data/ to Google Drive
# 4. Colab reads encrypted parquet files
```

### Key Design Points

- **Private key NEVER leaves client** — only public key uploaded to Colab
- **Features encrypted per-dimension** — each float scaled to int (×1e6) then encrypted
- **Output: Parquet** — efficient columnar storage for encrypted vectors
- **Dataset indexer** — handles CASIA, Korus, COVERAGE, IMD2020, MICC structures

---

## Tags
#encrypted-domain #forgery-detection #paillier #domain-adaptation #cross-dataset-generalization #colab-free #novel-contribution