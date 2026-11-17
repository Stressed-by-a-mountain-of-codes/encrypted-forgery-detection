# Dataset 08: DEFACTO — Large-Scale Multi-Type Forgery Dataset

**Full Name:** DEFACTO: A Large-Scale Dataset for DeepFake Detection and Localization  
**Authors:** Tariq, Lee, Woo (Sungkyunkwan Univ.)  
**Year:** 2021 (ICCV Workshop)  
**Website:** https://github.com/tariq93/DEFACTO  

---

## My Walkthrough

I went through this dataset because it's **large-scale (240K+ images) with multiple forgery types including DeepFake** — splicing, copy-move, removal, and **DeepFake (face swap, expression edit)**. Created to address "small dataset" problem for DL training.

Composition: **~120K authentic** (from COCO, FFHQ, CelebA-HQ), **~120K forged** — 4 types: **Splicing** (traditional + GAN-blended), **Copy-Move** (with transforms), **Removal** (LaMa, MAT inpainting), **DeepFake** (FaceSwap, FOMM, StyleGAN). Masks: **multi-class** (0=authentic, 1=splicing, 2=copy-move, 3=removal, 4=DeepFake). Resolution: **512×512**.

Key value: **DeepFake included** — most forgery datasets (CASIA, COVERAGE, IMD2020) don't have DeepFake. **Large enough for DL training**. Modern generators (StyleGAN, diffusion). But: **Face-focused** (many from FFHQ/CelebA), not general scene forgery.

On the 2nd iteration: **DeepFake subset is ~30K images** — good for SecDFDNet (Paper 14) replication. But **general forgery (splicing/copy-move/removal) is also face-heavy** due to source datasets. For encrypted-domain: **JPEG compressed**, good for testing. But **face bias** may not match your threat model.

**My takeaway:** DEFACTO = **only large-scale dataset with DeepFake + traditional forgery**. Essential if you need DeepFake in your eval (SecDFDNet replication). For general forgery, COVERAGE/IMD2020 are more diverse. Use DeepFake subset for face-specific encrypted tests.

---

## Technical Spec Sheet

| Property | Value |
|----------|-------|
| **Release Year** | 2021 |
| **Format** | JPEG (compressed) |
| **Resolution** | 512×512 |
| **Authentic Images** | ~120,000 |
| **Forged Images** | ~120,000 |
| **Total Images** | ~240,000 |
| **Forgery Types** | Splicing, Copy-Move, Removal, DeepFake |
| **DeepFake Methods** | FaceSwap, FOMM, StyleGAN, DiffAE |
| **Traditional Methods** | Copy-paste, Poisson, LaMa, MAT |
| **Ground Truth** | Multi-class mask (0-4) |
| **Mask Quality** | Good (auto-generated) |
| **Compression** | JPEG |
| **Download Size** | ~20 GB |
| **License** | Research only |

## Forgery Breakdown

| Type | Count | Methods |
|------|-------|---------|
| Splicing | ~30K | Traditional + GAN-blended |
| Copy-Move | ~30K | With rotation/scale |
| Removal | ~30K | LaMa, MAT inpainting |
| DeepFake | ~30K | FaceSwap, FOMM, StyleGAN, DiffAE |

## Standard Evaluation

| Metric | Splicing | Copy-Move | Removal | DeepFake |
|--------|----------|-----------|---------|----------|
| **Pixel F1 (SOTA)** | ~0.78 | ~0.75 | ~0.68 | ~0.85 |
| **AUC-ROC** | ~0.92 | ~0.90 | ~0.87 | ~0.95 |

## Download Links

| Source | Link |
|--------|------|
| GitHub | https://github.com/tariq93/DEFACTO |
| HuggingFace | https://huggingface.co/datasets/tariq93/DEFACTO |

## Encrypted-Domain Protocol

| Setup | Purpose |
|-------|---------|
| Native JPEG → Encrypt | Large-scale encrypted training (if compute allows) |
| DeepFake subset → Encrypt | **SecDFDNet replication** (Paper 14) |
| Per-type metrics | Encrypted detection per forgery type |

## Constraints & Gotchas

- ❌ **Huge (20 GB)** — download/storage heavy
- ❌ **Face-biased** (FFHQ/CelebA sources) — not general scenes
- ❌ **Auto-generated masks** — may have noise
- ❌ **No official train/test split**
- ✅ **Only large dataset with DeepFake + traditional**
- ✅ **Modern generators** (StyleGAN, diffusion)
- ✅ **Large enough for DL training**
- ✅ **Multi-class masks** — per-type evaluation

## Relevance to My Project

**Medium — only for DeepFace/encrypted face forensics:**
- SecDFDNet (Paper 14) replication needs DeepFake data
- Face-specific encrypted detection (MPC on face regions)
- Not for general scene forgery (use COVERAGE/IMD2020)

---

## Tags
#defacto #large-scale #deepfake #face-swap #splicing #copy-move #removal #training-scale #encrypted-domain-eval #face-biased

---

## Cross-References

- **Papers using DEFACTO:** [[../papers/14_secdfdnet_deepfake_secret_sharing]]
- **Master Index:** [[00_DATASET_MASTER_INDEX]]