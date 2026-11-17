# Final Selection: 5 Datasets for Encrypted-Domain Forgery Detection Project

> **Decision:** From 10 analyzed datasets, these 5 are selected for the project  
> **Criteria:** Complementarity, encrypted-domain relevance, feasibility, benchmark comparability

---

## Selected 5 Datasets

### 1. CASIA v1 & v2 — **Primary Benchmark** (NON-NEGOTIABLE)
**File:** `01_casia_v1_v2.md`

**Why Selected:**
- **Most cited forgery dataset** — direct comparison with 1000+ papers
- **Both uncompressed (v1) and JPEG (v2)** — perfect for encrypted-domain: test uncompressed encrypted (IFED/LEFN) AND JPEG encrypted (PP-JPEG)
- **Multiple forgery types** — copy-move, splicing, removal
- **Pixel-level masks** — localization evaluation
- **Your stated primary dataset** — project requirement

**Role in Project:** Main train/val/test. v2 for training (large, JPEG), v1 for uncompressed holdout test.

---

### 2. Korus 2018 — **JPEG Forensics Gold Standard**
**File:** `07_korus_2018.md`

**Why Selected:**
- **Controlled QF + known double-JPEG** — essential for PP-JPEG (Paper 12) replication
- **Camera labels** — enables encrypted camera fingerprint (Comprint, Paper 2)
- **Single + double compression at exact QFs** — no other dataset has this control
- **Matches PP-JPEG paper setup exactly** — QF1=90 → QF2=75 double JPEG
- **No other dataset provides this** — unique value for encrypted compression forensics

**Role in Project:** Primary test for PP-JPEG/LEFN/Comprint encrypted methods. Controlled compression experiments.

---

### 3. COVERAGE — **Modern Generalization Stress Test**
**File:** `03_coverage.md`

**Why Selected:**
- **Largest diverse dataset** (10K+ forged) with **modern generators** (GAN, diffusion)
- **Multi-forgery per image** — tests universal detection (TruFor, Paper 8)
- **Per-forgery-type masks** — fine-grained analysis: does encrypted method fail on GAN splicing?
- **Used by SOTA (TruFor, CMFDFormer)** — direct comparison
- **If your encrypted method works here, it's genuinely robust** — not overfitting to CASIA artifacts

**Role in Project:** Held-out test set ONLY (no training). Cross-dataset generalization: Train CASIA v2 encrypted → Test COVERAGE encrypted.

---

### 4. IMD2020 — **Realistic Semantic Manipulation**
**File:** `04_imd2020.md`

**Why Selected:**
- **Semantically meaningful manipulations** (Photoshop + manual) — not algorithmic copy-paste
- **4 distinct types** including **Removal/Inpainting** (generative artifacts) — tests if encrypted detection catches generative traces
- **Native JPEG from web** — real-world compression distribution
- **Used by TruFor (SOTA)** — direct comparison
- **Complements COVERAGE**: COVERAGE = algorithmic diversity, IMD2020 = semantic realism

**Role in Project:** Held-out test set. Per-manipulation-type analysis in encrypted domain. Removal/Inpainting = generative forensics test.

---

### 5. MICC-F600 — **Copy-Move Geometric Robustness**
**File:** `05_micc_f220_f600.md`

**Why Selected:**
- **Only dataset with known transform parameters** (rotation angle, scale factor, affine matrix)
- **Controlled geometric robustness test** — "Detection rate vs 45° rotation" — no other dataset
- **CASIA copy-move is translation-only** — MICC fills the geometric gap
- **Essential for "universal encrypted copy-move detection" claim**
- **Small, focused, high-signal** — low cost, high insight

**Role in Project:** Specialized copy-move test. Per-transform metrics in encrypted domain. Compress at multiple QFs.

---

## Rejected 5 Datasets (with Reasons)

| Dataset | File | Reason for Rejection |
|---------|------|---------------------|
| **Columbia Splicing** | `02_columbia_splicing.md` | **Redundant with CASIA v1 + Korus**. Uncompressed splicing covered by CASIA v1; controlled JPEG splicing covered by Korus. No unique value for encrypted domain. |
| **RTD (Realistic Tampering)** | `06_rtd_realistic_tampering.md` | **Superseded by IMD2020**. Same semantic realism, but smaller (340 vs 1000 forged), older, fewer types. IMD2020 is strictly better. |
| **DEFACTO** | `08_defacto.md` | **Face-biased** (FFHQ/CelebA sources). Your project is general image forgery, not face-specific. DeepFake covered by SecDFDNet paper but not your main threat model. 20 GB download not justified. |
| **GRIP** | `09_grip.md` | **Redundant with COVERAGE + IMD2020**. Scene-centric universal with DeepFake — but COVERAGE has more diversity, IMD2020 has better semantic realism. Smaller than COVERAGE. No unique encrypted-domain value. |
| **ForgeryNet** | `10_forgerynet.md` | **Impractically large** (2.9M images, 100 GB). Taxonomy (15 types) is useful as reference, but full dataset unusable for academic encrypted-domain compute. Curated subset possible but COVERAGE+IMD2020 cover the same types. |

---

## Final 5-Dataset Portfolio Coverage

| Forgery Type | CASIA | Korus | COVERAGE | IMD2020 | MICC | **Covered?** |
|--------------|-------|-------|----------|---------|------|--------------|
| **Splicing** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| **Copy-Move** | ✅ | ✅ | ✅ | ✅ | ✅ (transforms) | ✅ |
| **Removal** | ✅ (v2) | ❌ | ✅ | ✅ | ❌ | ✅ |
| **Inpainting** | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| **DeepFake** | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ (see note) |
| **Double JPEG** | ✅ (v2) | ✅ (controlled) | ✅ | ✅ (native) | ✅ (compress) | ✅ |
| **Known QF** | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Known Transforms** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Modern Generators** | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| **Semantic Realism** | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |

> **DeepFake Note:** Not covered in final 5. If DeepFace encrypted detection becomes a requirement, add **DEFACTO DeepFake subset** or **FaceForensics++** as 6th dataset. For general image forgery project, DeepFake is out of scope.

---

## Encrypted-Domain Evaluation Matrix

| Dataset | Primary Encrypted Test | Secondary Tests |
|---------|------------------------|-----------------|
| **CASIA v2** | Main train/val/test (PP-JPEG, LEFN, MPC) | v1 uncompressed holdout |
| **Korus 2018** | **PP-JPEG replication** (double-JPEG energy graph) | Comprint encrypted fingerprint, QF estimation |
| **COVERAGE** | Cross-dataset generalization (Train CASIA → Test COVERAGE) | Per-forgery-type, per-generator encrypted metrics |
| **IMD2020** | Semantic manipulation in encrypted domain | Removal/Inpainting = generative artifact detection |
| **MICC-F600** | Geometric robustness in encrypted domain | Per-angle/scale detection rate curves |

---

## Implementation Priority

| Phase | Dataset | Purpose |
|-------|---------|---------|
| **1. Baseline** | CASIA v2 | Train/eval all encrypted methods |
| **2. Compression Forensics** | Korus 2018 | PP-JPEG, LEFN, Comprint replication |
| **3. Generalization** | COVERAGE | Cross-dataset test (no training) |
| **4. Semantic Realism** | IMD2020 | Real-world manipulation test |
| **5. Geometric Robustness** | MICC-F600 | Copy-move transform test |

---

## Tags
#final-selection #5-datasets #casia #korus #coverage #imd2020 #micc #encrypted-domain #project-decision

---

## Cross-References

- **All 10 Dataset Files:** [[00_DATASET_MASTER_INDEX]]
- **Papers Vault:** [[../papers/00_MASTER_INDEX]]