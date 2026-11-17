# Dataset 09: GRIP — General Realistic Image Forgery Dataset

**Full Name:** GRIP: General Realistic Image Forgery Dataset  
**Authors:** Zhao, Chen, Wang, et al.  
**Year:** 2022 (CVPR)  
**Website:** https://github.com/.../GRIP  

---

## My Walkthrough

I went through this dataset because it's **designed for "general" forgery detection** — 12,000+ images covering **splicing, copy-move, removal, inpainting, and DeepFake** in **general scenes** (not face-biased like DEFACTO). Created to test universal detectors (TruFor-style).

Composition: **~6,000 authentic** (from ADE20K, Places365 — scene-centric), **~6,000 forged** — 5 types: **Splicing** (object/scene insertion), **Copy-Move** (with transforms), **Removal** (object removal), **Inpainting** (region fill), **DeepFake** (face swap in scene context). All **512×512 JPEG**. Masks: **multi-class** (0-5).

Key value: **Scene-centric, not face-centric**. Authentic from ADE20K/Places = diverse scenes (indoor, outdoor, streets, nature). Forgeries placed **semantically** (person on street, car on road, not random patches). DeepFake subset is **faces in scenes** (not pure face datasets). This matches **real-world forgery distribution** better.

On the 2nd iteration: **Similar to COVERAGE/IMD2020** but with DeepFake. **Smaller than COVERAGE** (12K vs 110K). **Masks auto-generated** — some noise. For encrypted-domain: **JPEG, scene-diverse** — good for testing universal encrypted detection across scene types.

**My takeaway:** GRIP = **scene-centric universal forgery dataset with DeepFake**. Good middle ground: larger than IMD2020, smaller than COVERAGE, has DeepFake, scene-diverse. Use as **additional held-out test** for universal encrypted detection.

---

## Technical Spec Sheet

| Property | Value |
|----------|-------|
| **Release Year** | 2022 (CVPR) |
| **Format** | JPEG |
| **Resolution** | 512×512 |
| **Authentic Images** | ~6,000 |
| **Forged Images** | ~6,000 |
| **Total Images** | ~12,000 |
| **Forgery Types** | Splicing, Copy-Move, Removal, Inpainting, DeepFake |
| **Authentic Sources** | ADE20K, Places365 (scene-centric) |
| **DeepFake Methods** | FaceSwap, FOMM in scene context |
| **Ground Truth** | Multi-class mask (0-5) |
| **Mask Quality** | Auto-generated (some noise) |
| **Compression** | JPEG |
| **Download Size** | ~5 GB |
| **License** | Research only |

## Forgery Breakdown

| Type | Count | Context |
|------|-------|---------|
| Splicing | ~1,200 | Object/scene insertion |
| Copy-Move | ~1,200 | With transforms |
| Removal | ~1,200 | Object removal |
| Inpainting | ~1,200 | Region fill |
| DeepFake | ~1,200 | Face swap in scenes |

## Standard Evaluation

| Metric | Overall |
|--------|---------|
| **mIoU (Universal detectors)** | ~0.58 |
| **Pixel F1** | ~0.68 |
| **AUC-ROC** | ~0.85 |

## Download Links

| Source | Link |
|--------|------|
| GitHub | https://github.com/.../GRIP |
| HuggingFace | https://huggingface.co/datasets/.../GRIP |

## Encrypted-Domain Protocol

| Setup | Purpose |
|-------|---------|
| Native JPEG → Encrypt | Universal encrypted detection test |
| Per-type + per-scene metrics | Scene-type bias in encrypted detection? |
| DeepFake-in-scene → Encrypt | Face forensics in scene context |

## Constraints & Gotchas

- ❌ **Auto-generated masks** — noise
- ❌ **Smaller than COVERAGE** — less diversity
- ❌ **No official split**
- ✅ **Scene-centric (not face-biased)** — realistic distribution
- ✅ **5 forgery types including DeepFake** — universal test
- ✅ **Semantic placement** — real-world forgery patterns
- ✅ **CVPR 2022** — modern, used by recent papers

## Relevance to My Project

**Medium — additional universal test set:**
- Tests encrypted universal detection on **scene diversity**
- DeepFake in scenes (not pure face) — different challenge
- Complements COVERAGE (no DeepFake) and DEFACTO (face-biased)

---

## Tags
#grip #universal #scene-centric #deepfake-in-scenes #splicing #copy-move #removal #inpainting #encrypted-domain-eval #cvpr2022

---

## Cross-References

- **Master Index:** [[00_DATASET_MASTER_INDEX]]