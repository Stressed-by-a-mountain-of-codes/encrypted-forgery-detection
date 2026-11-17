# Dataset 10: ForgeryNet — Massive Multi-Task Forgery Dataset

**Full Name:** ForgeryNet: A Versatile Benchmark for Image Forgery Detection and Localization  
**Authors:** He, Zhang, Sun, et al. (Alibaba, etc.)  
**Year:** 2021 (ICCV)  
**Website:** https://github.com/He-Y/ForgeryNet  

---

## My Walkthrough

I went through this dataset because it's **one of the largest and most comprehensive** — 2.9M images, **15 forgery types**, **multi-task**: detection, localization, classification, segmentation. Created by Alibaba for production-scale forgery analysis.

Composition: **~1.5M authentic** (from web, diverse), **~1.4M forged** — **15 forgery categories** grouped into: **Splicing** (3 types), **Copy-Move** (3 types), **Removal** (3 types), **Inpainting** (3 types), **DeepFake** (3 types: identity swap, expression edit, attribute edit). Each with **multiple generation methods** (traditional, GAN, diffusion). Masks: **pixel-level segmentation** + **image-level label** + **forgery type label** + **method label**.

Key value: **Massive scale + fine-grained taxonomy**. 15 types let you test: "Does my encrypted method detect identity swap but fail on attribute edit?" **Method labels** let you test: "Traditional vs GAN vs diffusion forgeries." **Production-scale** — reflects real distribution.

On the 2nd iteration: **Huge (2.9M images, ~100 GB)** — impractical for most academic compute. **Auto-generated masks** — noise at boundaries. **Web-sourced authentic** — quality varies. For encrypted-domain: **JPEG, massive** — if you have compute, great for large-scale encrypted training. But **overkill for evaluation** — use smaller held-out sets.

**My takeaway:** ForgeryNet = **production-scale comprehensive benchmark**. Use a **curated subset** for evaluation (e.g., 1K per type). Full dataset only if you have massive compute for encrypted training. The taxonomy (15 types) is the reference for fine-grained evaluation.

---

## Technical Spec Sheet

| Property | Value |
|----------|-------|
| **Release Year** | 2021 (ICCV) |
| **Format** | JPEG |
| **Resolution** | 512×512 (standardized) |
| **Authentic Images** | ~1,500,000 |
| **Forged Images** | ~1,400,000 |
| **Total Images** | ~2,900,000 |
| **Forgery Categories** | 15 (3 each: Splicing, Copy-Move, Removal, Inpainting, DeepFake) |
| **Generation Methods** | Traditional, GAN (StyleGAN, etc.), Diffusion |
| **Ground Truth** | Segmentation mask + image label + type label + method label |
| **Mask Quality** | Auto-generated (boundary noise) |
| **Compression** | JPEG (web-native) |
| **Download Size** | ~100 GB |
| **License** | Research only |

## 15 Forgery Categories

| Group | Categories (3 each) |
|-------|---------------------|
| **Splicing** | Object insertion, Scene replacement, Texture splicing |
| **Copy-Move** | Translation, Rotation, Scale |
| **Removal** | Small object, Large object, Text removal |
| **Inpainting** | Face editing, Scene completion, Texture fill |
| **DeepFake** | Identity swap, Expression edit, Attribute edit |

## Standard Evaluation (Per ForgeryNet Paper)

| Task | Metric | SOTA |
|------|--------|------|
| Detection | AUC-ROC | ~0.98 |
| Localization | mIoU | ~0.65 |
| Classification (15-way) | Acc | ~0.85 |
| Segmentation | mIoU | ~0.58 |

## Download Links

| Source | Link |
|--------|------|
| GitHub | https://github.com/He-Y/ForgeryNet |
| Official Site | https://forgerynet.alibaba.com/ |

## Encrypted-Domain Protocol

| Setup | Purpose |
|-------|---------|
| Curated subset (1K/type) → Encrypt | Fine-grained encrypted evaluation (15 types) |
| Method-stratified (Traditional/GAN/Diffusion) | Encrypted detection vs generator type |
| Full dataset (if compute) | Large-scale encrypted training |

## Constraints & Gotchas

- ❌ **Massive (100 GB)** — impractical for most
- ❌ **Auto masks** — boundary noise
- ❌ **Web quality varies** — not curated
- ❌ **No official small split**
- ✅ **Most comprehensive taxonomy** (15 types)
- ✅ **Method labels** (Traditional/GAN/Diffusion)
- ✅ **Production scale** — real distribution
- ✅ **Multi-task labels** — detection/localization/classification/segmentation

## Relevance to My Project

**Low for full dataset (too large), High for curated subset:**
- Use **curated 1K per type (15K total)** for fine-grained encrypted eval
- Test: "Does encrypted PP-JPEG fail on diffusion inpainting?"
- Taxonomy reference for your evaluation design

---

## Tags
#forgerynet #massive #15-types #multi-task #fine-grained #production-scale #encrypted-domain-eval #iccv2021

---

## Cross-References

- **Master Index:** [[00_DATASET_MASTER_INDEX]]