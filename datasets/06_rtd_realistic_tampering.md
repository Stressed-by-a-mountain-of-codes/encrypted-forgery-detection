# Dataset 06: RTD — Realistic Tampering Dataset

**Full Name:** Realistic Tampering Dataset (RTD)  
**Authors:** Bappy, Simons, Nataraj, Manjunath (UCSB)  
**Year:** 2017 (CVPR Workshop)  
**Website:** https://github.com/bappy/Realistic-Tampering-Dataset  

---

## My Walkthrough

I went through this dataset because it was **one of the first "realistic" tampering datasets** — created before IMD2020, COVERAGE. 680 images: 340 authentic + 340 tampered. Tampering done with **Photoshop by experts** — object removal, addition, splicing — with **semantic coherence** (lighting, perspective matched). Not algorithmic copy-paste.

Composition: **340 authentic** (Flickr, diverse), **340 tampered** — 4 types: **Removal** (object removed + inpainted), **Addition** (object added from another image), **Splicing** (region replaced), **Combination** (multiple ops). All **JPEG** (native web compression). Masks: **binary PNG** per image + type label.

Key difference from CASIA: **Semantic realism**. The tampered regions make sense in context — "remove this trash can", "add this person", not random patches. Boundaries are **feathered, color-matched**. This tests **high-level semantic inconsistency detection**, not low-level artifacts.

On the 2nd iteration: **Small (340 tampered)** — not for training. But **high quality**. Used in early DL papers (RGB-N, ManTra-Net). For encrypted-domain: **Native JPEG** — good for testing on real compression. But **superseded by IMD2020/COVERAGE** (larger, more types, modern generators).

**My takeaway:** RTD = **early realistic dataset**, historically important. Use only if you need a **small clean realistic test set** and IMD2020/COVERAGE are too large. Otherwise, skip — IMD2020 covers same ground better.

---

## Technical Spec Sheet

| Property | Value |
|----------|-------|
| **Release Year** | 2017 |
| **Format** | JPEG (native web compression) |
| **Resolution** | Up to 1024×1024 |
| **Authentic Images** | 340 |
| **Tampered Images** | 340 |
| **Total Images** | 680 |
| **Tampering Types** | Removal, Addition, Splicing, Combination |
| **Creation Method** | Photoshop by experts (semantic) |
| **Ground Truth** | Binary mask + type label |
| **Mask Quality** | Good (feathered boundaries) |
| **Compression** | Native JPEG (various QFs) |
| **Download Size** | ~500 MB |
| **License** | Research only |

## Tampering Breakdown

| Type | Count | Description |
|------|-------|-------------|
| Removal | ~85 | Object removed + inpainted |
| Addition | ~85 | Object added from another image |
| Splicing | ~85 | Region replaced |
| Combination | ~85 | Multiple operations |

## Standard Evaluation

| Metric | Typical SOTA |
|--------|--------------|
| **Pixel F1** | ~0.75 |
| **IoU** | ~0.65 |
| **AUC-ROC** | ~0.88 |

## Download Links

| Source | Link |
|--------|------|
| GitHub | https://github.com/bappy/Realistic-Tampering-Dataset |
| Google Drive | Link in GitHub README |

## Encrypted-Domain Protocol

| Setup | Purpose |
|-------|---------|
| Native JPEG → Encrypt | Realistic semantic tampering on real compression |
| Per-type metrics | Which semantic edits detectable when encrypted? |

## Constraints & Gotchas

- ❌ **Small (340 tampered)** — not for training
- ❌ **Superseded by IMD2020/COVERAGE** — larger, more modern
- ❌ **Only 4 types** — no copy-move, no DeepFake
- ✅ **Semantic realism** — expert Photoshop
- ✅ **Native JPEG** — real compression
- ✅ **Historical benchmark** — cited by early DL papers

## Relevance to My Project

**Low priority — superseded by IMD2020/COVERAGE.** Only use if you need a small additional realistic test set.

---

## Tags
#rtd #realistic-tampering #semantic #photoshop #native-jpeg #small #superseded #encrypted-domain-eval

---

## Cross-References

- **Master Index:** [[00_DATASET_MASTER_INDEX]]