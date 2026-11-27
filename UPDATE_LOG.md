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
| `D:\major project\client\client_compute_gradients.py` | Client-assisted gradient computation for encrypted SGD |
| `D:\major project\client\client_domain_adaptation.py` | Client-side Procrustes adaptation (computes Enc(A), Enc(b)) |
| `D:\major project\client\client_decrypt_evaluate.py` | Decrypt predictions, compute AUC/metrics |

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

## Colab-Side Implementation (Created 2026-11-19)

### Files Created

| File | Purpose |
|------|---------|
| `D:\major project\colab\paillier_server.py` | Server-side Paillier ops: encrypted dot product, linear forward, sigmoid, linear map apply |
| `D:\major project\colab\encrypted_training.ipynb` | Phase 1: Encrypted SGD on CASIA (client-assisted sigmoid) |
| `D:\major project\colab\encrypted_adaptation.ipynb` | Phase 2: Encrypted domain adaptation (CASIA → Korus/MICC) |
| `D:\major project\colab\encrypted_inference.ipynb` | Phase 3: Encrypted test on COVERAGE/IMD2020 |

### Colab Workflow

```bash
# 1. Upload to Google Drive:
# MyDrive/major_project/
#   colab/paillier_server.py
#   colab/encrypted_training.ipynb
#   colab/encrypted_adaptation.ipynb
#   colab/encrypted_inference.ipynb
#   data/enc_casia.parquet
#   data/enc_korus.parquet
#   data/enc_micc.parquet
#   data/enc_coverage_test.parquet
#   data/enc_imd2020_test.parquet
#   data/public_key_for_colab.json
```

```python
# 2. In each Colab notebook - first cell:
from google.colab import drive
drive.mount('/content/drive')
import sys
sys.path.append('/content/drive/MyDrive/major_project/colab')
from paillier_server import PaillierServer
server = PaillierServer(public_key_path='/content/drive/MyDrive/major_project/data/public_key_for_colab.json')
```

### Training Protocol (Client-Assisted)

1. **Server (Colab):** Computes `Enc(logits) = Enc(x) · w + b` for batch
2. **Server:** Saves batch (Enc(logits), Enc(labels), weights, bias) to Drive
3. **Client (local):** Runs `client_compute_gradients.py` → decrypts, computes gradients, encrypts gradients
4. **Client:** Uploads encrypted gradients to Drive
5. **Server:** Reads gradients, updates `w ← w - η * ∇L`
6. **Repeat** for all batches/epochs

### Domain Adaptation Protocol

1. **Client (local):** Runs `client_domain_adaptation.py` → decrypts adaptation samples, computes Procrustes A, b, encrypts them
2. **Client:** Uploads `Enc(A_korus)`, `Enc(b_korus)`, `Enc(A_micc)`, `Enc(b_micc)` to Drive
3. **Server (Colab):** During inference, applies `Enc(x_target) → Enc(x_target * A + b)` via `encrypted_linear_map_apply()`

### Inference Protocol

1. **Server (Colab):** Runs `encrypted_inference.ipynb` on COVERAGE/IMD2020
2. **Server:** Applies adaptation (if available) → encrypted forward pass → encrypted sigmoid
3. **Server:** Saves `Enc(predictions)` to Drive
4. **Client (local):** Runs `client_decrypt_evaluate.py` → decrypts, computes AUC/per-forgery metrics

---

## Tags
#encrypted-domain #forgery-detection #paillier #domain-adaptation #cross-dataset-generalization #colab-free #novel-contribution

---

## Next Phase: Dataset Preparation & Execution (Pending)

### Dataset Download Status

| Dataset | Access Method | Direct Link | Status |
|---------|---------------|-------------|--------|
| **CASIA v1/v2** | Academic request | http://forensics.idealtest.org/ | ⏳ Request needed |
| **Korus 2018** | Direct download | https://github.com/pkorus/korus2018-dataset | ✅ Ready |
| **COVERAGE** | Direct download | https://github.com/SCLBD/COVERAGE | ✅ Ready (large) |
| **IMD2020** | Direct download | https://github.com/imd2020/IMD2020 | ✅ Ready |
| **MICC-F600** | Direct download | http://micc.unifi.it/MICC-F600/ | ✅ Ready |

### Download Script

Run locally to fetch Korus, IMD2020, COVERAGE, MICC-F600:

```bash
cd client
python download_datasets.py --root D:\major_project_datasets --datasets all
# Or selectively:
python download_datasets.py --datasets korus imd2020 micc coverage
```

Creates directory structure and attempts git clone / HTTP download for each.

### CASIA Request Template

```
To: forensics@idealtest.org
Subject: CASIA v1/v2 Dataset Access Request

Dear CASIA Team,

I am a graduate student researching encrypted-domain image forgery detection.
I would like to request access to the CASIA v1 and v2 datasets for academic research.

Project: "Encrypted Domain Adaptation for Cross-Dataset Forgery Detection Generalization"
Institution: [Your Institution]
Advisor: [Advisor Name]
Expected publication: [Conference/Journal]

Thank you for your consideration.
```

### Execution Checklist

#### Step 1: Local Environment Setup
- [ ] `cd client && pip install -r requirements.txt`
- [ ] Verify `python forensic_features.py test_image.jpg` works
- [ ] Generate Paillier keys: `python -c "from paillier_client import PaillierClient; c=PaillierClient(); c.generate_keys(); c.save_keys('keys/public_key.json','keys/private_key.json')"`

#### Step 2: Dataset Download & Organization
- [ ] Create `D:\major_project_datasets\` with subdirs:
  ```
  major_project_datasets/
  ├── CASIA_v2/
  │   ├── Au/ (authentic)
  │   └── Tp/ (tampered)
  ├── Korus_2018/
  ├── COVERAGE/
  ├── IMD2020/
  └── MICC_F600/
  ```
- [ ] Download Korus, IMD2020, MICC-F600 (direct links above)
- [ ] Submit CASIA request (can take 1-3 days)

#### Step 3: Feature Extraction & Encryption
- [ ] Run for each dataset:
  ```bash
  python extract_and_encrypt.py --dataset-root D:\major_project_datasets --dataset CASIA_v2 --output ..\colab_data\enc_casia.parquet --generate-keys
  python extract_and_encrypt.py --dataset-root D:\major_project_datasets --dataset Korus_2018 --output ..\colab_data\enc_korus.parquet
  python extract_and_encrypt.py --dataset-root D:\major_project_datasets --dataset MICC_F600 --output ..\colab_data\enc_micc.parquet
  python extract_and_encrypt.py --dataset-root D:\major_project_datasets --dataset COVERAGE --output ..\colab_data\enc_coverage_test.parquet --max-samples 2000
  python extract_and_encrypt.py --dataset-root D:\major_project_datasets --dataset IMD2020 --output ..\colab_data\enc_imd2020_test.parquet --max-samples 2000
  ```
- [ ] Verify outputs: `enc_casia.parquet`, `enc_korus.parquet`, etc.

#### Step 4: Google Drive Upload
- [ ] Create `MyDrive/major_project/` structure:
  ```
  MyDrive/major_project/
  ├── colab/
  │   ├── paillier_server.py
  │   ├── encrypted_training.ipynb
  │   ├── encrypted_adaptation.ipynb
  │   ├── encrypted_inference.ipynb
  │   └── requirements.txt
  └── data/
      ├── enc_casia.parquet
      ├── enc_korus.parquet
      ├── enc_micc.parquet
      ├── enc_coverage_test.parquet
      ├── enc_imd2020_test.parquet
      └── public_key_for_colab.json
  ```

#### Step 5: Colab Execution (Sequential)
- [ ] **Notebook 1:** `encrypted_training.ipynb` — Encrypted SGD on CASIA
  - Mount Drive, run cells
  - When client batch saved: run `client_compute_gradients.py` locally, upload gradients
  - Repeat until convergence
  - Saves `enc_model_casia.json`
- [ ] **Notebook 2:** `encrypted_adaptation.ipynb` — Domain adaptation
  - Run client request cell
  - Run `client_domain_adaptation.py` locally → uploads `enc_A_korus.parquet`, `enc_b_korus.parquet`, etc.
  - Server loads and verifies
- [ ] **Notebook 3:** `encrypted_inference.ipynb` — Generalization test
  - Runs on COVERAGE + IMD2020
  - Saves `enc_preds_coverage.parquet`, `enc_preds_imd2020.parquet`

#### Step 6: Client Evaluation
- [ ] Download prediction files from Drive
- [ ] Run: `python client_decrypt_evaluate.py --keys-dir keys --preds-coverage enc_preds_coverage.parquet --preds-imd2020 enc_preds_imd2020.parquet --labels-coverage ... --labels-imd2020 ... --output-dir results/`
- [ ] Review `metrics_coverage.json`, `metrics_imd2020.json`

### Expected Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Encrypted model | `data/enc_model_casia.json` | Trained weights (plaintext on server) |
| Adaptation matrices | `data/enc_A_*.parquet`, `enc_b_*.parquet` | Encrypted domain maps |
| Encrypted predictions | `data/enc_preds_*.parquet` | Encrypted probabilities |
| Metrics | `results/metrics_*.json` | AUC, Acc, Prec, Rec, F1 per dataset |

### Known Limitations & Mitigations

| Limitation | Mitigation |
|------------|------------|
| Client-assisted sigmoid (round-trips) | Batch size 32, ~1000 samples = ~30 round-trips/epoch |
| Linear sigmoid approx (degree=1) | Acceptable for logits in [-4,4]; monitor calibration |
| Encrypted domain adaptation needs client compute | One-time cost; adaptation matrices reused |
| Colab Free 12hr limit | Checkpoint every epoch; resume from Drive |
| Paillier slow for high-dim (304) | Feature selection (PCA) or batching; 304 is manageable |

### Future Enhancements (Post-MVP)

- [ ] Feature selection to reduce 304 → 100 dims (faster encryption)
- [ ] Polynomial sigmoid degree=3 with client-assisted x², x³
- [ ] Encrypted ensemble (multiple specialized detectors)
- [ ] CKKS/FHE migration if Colab Pro+ available
- [ ] Synthetic data augmentation for domain adaptation
- [ ] Per-forgery-type evaluation (splicing vs copy-move vs removal)

---

## Session Continuity

**To resume in new session:**
1. Clone repo: `git clone https://github.com/Stressed-by-a-mountain-of-codes/encrypted-forgery-detection.git`
2. Read `UPDATE_LOG.md` — this file
3. Check GitHub Issues for any tracked blockers
4. Continue from next unchecked item above

---

## GitHub Repository
**https://github.com/Stressed-by-a-mountain-of-codes/encrypted-forgery-detection** (Public)

All code, logs, and dataset analyses committed.