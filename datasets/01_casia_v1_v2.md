# Dataset 01: CASIA v1 & v2 — Primary Benchmark

**Full Name:** CASIA Image Tampering Detection Evaluation Database  
**Versions:** v1.0 (2009), v2.0 (2013)  
**Source:** Chinese Academy of Sciences, Institute of Automation  
**Website:** http://forensics.idealtest.org/  

---

## My First-Person Walkthrough

I went through this dataset because it's **the most cited forgery detection benchmark** — literally thousands of papers use it. It comes in two versions: **v1** (uncompressed TIFF, 800 authentic + 921 forged) and **v2** (JPEG compressed, 7,491 authentic + 5,123 forged). The forged images cover **copy-move** and **splicing** with ground truth masks.

When I looked at the v1 details: **800 authentic** (various scenes, cameras), **921 forged** — copy-move (duplicated regions within same image) and splicing (regions from other images pasted in). All **TIFF, 384×256 or 256×384**, uncompressed. Ground truth is **binary mask PNG** (white=tampered, black=authentic). The forgeries are **manually created** — not algorithmic — so they look realistic but have clean boundaries.

Then v2: **Massive scale-up** — 7,491 authentic + 5,123 forged. All **JPEG** (various QFs). Includes **copy-move, splicing, and some removal**. Masks are **pixel-level binary**. The authentic set is much larger (good for training), forged set covers more variety. But v2 masks are sometimes **noisy at boundaries** — not as clean as v1.

On the 2nd iteration of my analysis, I realized: **Most papers only use a subset** — typically 100-200 forged + 100-200 authentic for testing, rest for training. The **standard split isn't fixed** — everyone makes their own. This makes cross-paper comparison tricky. Also, **v1 is too small for deep learning training** (only 921 forged), so people use v2 for training, v1 for testing, or mix both.

When I checked what the encrypted-domain papers used: **Paper 11 (IFED/LEFN)** used a subset of CASIA v1 for encrypted filtering tests. **Paper 12 (PP-JPEG)** used CASIA v2 because it's already JPEG — perfect for their double-JPEG energy analysis. **Paper 14 (SecDFDNet)** didn't use CASIA (it's face DeepFake only). So for my encrypted-domain project, **CASIA v2 is the natural fit** for PP-JPEG style evaluation, **v1 for uncompressed baseline**.

**My takeaway:** CASIA is **non-negotiable as primary benchmark**. Use v2 for training (large, JPEG), v1 for clean uncompressed testing. Download both. Create your own fixed train/val/test split and **publish it** so your results are reproducible. The masks are good but check boundary quality — some v2 masks need morphological cleaning.

---

## Technical Spec Sheet

| Property | CASIA v1.0 | CASIA v2.0 |
|----------|------------|------------|
| **Release Year** | 2009 | 2013 |
| **Format** | TIFF (uncompressed) | JPEG (compressed) |
| **Resolution** | 384×256 / 256×384 | Various (max ~1024×768) |
| **Authentic Images** | 800 | 7,491 |
| **Forged Images** | 921 | 5,123 |
| **Total Images** | 1,721 | 12,614 |
| **Forgery Types** | Copy-move, Splicing | Copy-move, Splicing, Removal |
| **Ground Truth** | Binary mask PNG | Binary mask PNG |
| **Mask Quality** | Clean boundaries | Some noisy boundaries |
| **Compression** | None | JPEG (various QFs) |
| **Download Size** | ~200 MB | ~1.2 GB |
| **License** | Research only | Research only |

## Forgery Type Breakdown (v2)

| Type | Count | Description |
|------|-------|-------------|
| Copy-Move | ~2,000 | Region duplicated within image |
| Splicing | ~2,500 | Region from another image pasted |
| Removal | ~600 | Object removed + inpainted |

## Standard Evaluation Metrics Used in Papers

| Metric | Formula | Typical Threshold |
|--------|---------|-------------------|
| **Pixel F1** | 2·P·R/(P+R) | > 0.7 |
| **IoU (mIoU)** | TP/(TP+FP+FN) | > 0.5 |
| **AUC-ROC** | Area under ROC | > 0.85 |
| **Precision@Recall** | P@R=0.5, 0.7, 0.9 | Higher better |
| **F1@Image** | Image-level binary | > 0.8 |

## Recommended Train/Val/Test Split (Create Your Own)

```
# Suggested fixed split for reproducibility
CASIA_v2_train:  4,000 authentic + 3,000 forged  (70%)
CASIA_v2_val:    1,500 authentic + 1,000 forged  (20%)
CASIA_v2_test:   1,991 authentic + 1,123 forged  (10%)

CASIA_v1_test:   800 authentic + 921 forged       (uncompressed holdout)
```

**Stratify by forgery type** (copy-move / splicing / removal) in each split.

## Download Links

| Version | Direct Link | Mirror |
|---------|-------------|--------|
| v1.0 | http://forensics.idealtest.org/download/CASIA1.0.zip | IEEE DataPort |
| v2.0 | http://forensics.idealtest.org/download/CASIA2.0.zip | IEEE DataPort |

> **Note:** Official site sometimes down. Search "CASIA image tampering dataset download" for academic mirrors (IEEE DataPort, Kaggle, Google Drive shares from researchers).

## Encrypted-Domain Evaluation Protocol

For your project, evaluate on **both versions**:

| Setup | Purpose |
|-------|---------|
| **v2 (JPEG)** → Encrypt → PP-JPEG/LEFN/SecDFDNet | Main encrypted-domain benchmark |
| **v1 (TIFF)** → Compress at QF={75,90,95} → Encrypt | Double-JPEG analysis (PP-JPEG style) |
| **v1 (TIFF)** → Encrypt directly (no compress) | Uncompressed encrypted forensics (IFED style) |
| **Cross-QF**: Train QF=90, Test QF=75 | Generalization test |

## Constraints & Gotchas

- ❌ **No fixed official split** — create and publish yours
- ❌ **v1 too small for DL training** — use v2 for train, v1 for test
- ❌ **v2 mask boundaries noisy** — apply morphological opening
- ❌ **Class imbalance** (more authentic than forged) — use weighted loss
- ❌ **Old dataset** — forgeries may not reflect modern GAN/DeepFake
- ✅ **Most cited** — direct comparison with 1000+ papers
- ✅ **Both compressed/uncompressed** — perfect for encrypted domain
- ✅ **Pixel-level masks** — localization evaluation
- ✅ **Multiple forgery types** — comprehensive

## Relevance to My Project

**Primary dataset — use for all evaluations:**
- PP-JPEG replication: CASIA v2 (already JPEG)
- LEFN/IFED replication: CASIA v1 (uncompressed) + self-compress
- MPC/Secret Sharing: Any version (encrypted at pixel level)
- Hybrid selective encryption: v2 (test MSB/LSB split)

---

## Tags
#casia #casia-v1 #casia-v2 #primary-dataset #copy-move #splicing #removal #jpeg #uncompressed #benchmark #encrypted-domain-eval #pixel-masks

---

## Cross-References

- **Papers using CASIA:** [[../papers/01_ecdc_copy_move_detection]], [[../papers/06_mfafnet_splicing_detection]], [[../papers/07_cmfdformer_transformer_continual]], [[../papers/08_trufor_universal_detection]], [[../papers/09_dl_survey_mehrjardi_2023]], [[../papers/11_ifed_lefnd_foundational]], [[../papers/12_ppjpeg_paillier_tampering]]
- **Master Index:** [[00_DATASET_MASTER_INDEX]]