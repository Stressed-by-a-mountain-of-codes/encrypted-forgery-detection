# Dataset 02: Columbia Uncompressed Image Splicing Detection — Clean Splicing Baseline

**Full Name:** Columbia Uncompressed Image Splicing Detection Evaluation Dataset  
**Authors:** Hsu, Chang, Chen (Columbia University)  
**Year:** 2012  
**Website:** http://www.ee.columbia.edu/ln/dvmm/downloads/AuthSpliced/  

---

## My First-Person Walkthrough

I went through this dataset because it's **the cleanest splicing benchmark** — 180 images, all **uncompressed TIFF**, **pure splicing** (no copy-move, no removal), with **perfect pixel-level masks**. It was created by taking authentic images and splicing regions from **other authentic images in the same set**, so the lighting/camera consistency varies naturally.

When I looked at the composition: **183 authentic images** (various scenes, Canon/Nikon cameras, RAW→TIFF), **180 spliced images** (each created by pasting a region from one authentic image into another). The spliced region is **irregular shape** (not rectangular), **feathered at boundaries** (2-3 pixel blend), making it more realistic than hard-edged copy-paste. Masks are **binary PNG** — white=spliced, black=authentic, **perfect boundaries**.

The key thing: **No compression artifacts at all**. Everything is TIFF. This means any detection method relying on JPEG grid, quantization tables, or double-compression **will fail completely** on this dataset. It tests **pure content-based splicing detection** — noise inconsistencies, color consistency, edge artifacts, lighting mismatch.

On the 2nd iteration, I checked which papers use it: **Comprint (Paper 2)** uses it but compresses it first to JPEG to test their compression fingerprint. **MFAF-Net (Paper 6)**, **TruFor (Paper 8)**, **DL Survey (Paper 9)** all use it as a **splicing-specific benchmark**. For my encrypted-domain project: **Columbia is perfect for testing methods that work on uncompressed/decrypted domain** — after decryption, before any compression. But if I'm testing encrypted-domain methods that rely on JPEG artifacts (PP-JPEG), I **must compress Columbia myself first**.

**My takeaway:** Columbia = **gold standard for uncompressed splicing**. Use it to validate that your encrypted-domain method doesn't *require* compression artifacts. Compress it at multiple QFs (75, 90, 95) to create double-JPEG scenarios for PP-JPEG testing. The feathered boundaries are realistic — good test for localization precision.

---

## Technical Spec Sheet

| Property | Value |
|----------|-------|
| **Release Year** | 2012 |
| **Format** | TIFF (uncompressed, 8-bit RGB) |
| **Resolution** | 757×568 to 1000×750 (varies) |
| **Authentic Images** | 183 |
| **Spliced Images** | 180 |
| **Total Images** | 363 |
| **Forgery Type** | Splicing only |
| **Splicing Method** | Region from image A → image B, irregular shape, feathered |
| **Source Cameras** | Canon 5D, Nikon D70, etc. (RAW → TIFF) |
| **Ground Truth** | Binary mask PNG (perfect boundaries) |
| **Mask Quality** | Excellent — feathered 2-3px blend zones marked |
| **Compression** | None (uncompressed TIFF) |
| **Download Size** | ~400 MB |
| **License** | Research only |

## Forgery Characteristics

| Aspect | Detail |
|--------|--------|
| **Region Shape** | Irregular (polygon), not rectangular |
| **Boundary** | Feathered (alpha blend 2-3 pixels) |
| **Source** | Other authentic image in same dataset |
| **Lighting Match** | Sometimes consistent, sometimes not |
| **Color Space** | RGB (from RAW, no JPEG quantization) |
| **Post-Processing** | None |

## Standard Evaluation Metrics

| Metric | Typical SOTA on Columbia |
|--------|--------------------------|
| **Pixel F1** | 0.85-0.95 |
| **IoU** | 0.75-0.90 |
| **AUC-ROC** | 0.95+ |
| **Image-level Acc** | 98%+ |

## Recommended Usage for Your Project

```
# Since no standard split, create fixed split:
Columbia_train:  100 authentic + 100 spliced
Columbia_val:    40 authentic + 40 spliced
Columbia_test:   43 authentic + 40 spliced

# For encrypted-domain:
Columbia_QF75:   Compress all at QF=75 → encrypt
Columbia_QF90:   Compress all at QF=90 → encrypt
Columbia_QF95:   Compress all at QF=95 → encrypt
Columbia_raw:    Encrypt TIFF directly (no JPEG)
```

## Download Links

| Source | Link |
|--------|------|
| Official (Columbia) | http://www.ee.columbia.edu/ln/dvmm/downloads/AuthSpliced/AuthSpliced.zip |
| IEEE DataPort | Search "Columbia Uncompressed Image Splicing Detection" |
| Kaggle | kaggle.com/datasets/... (community mirrors) |
| GitHub Mirrors | github.com/.../columbia-splicing-dataset |

## Encrypted-Domain Evaluation Protocol

| Setup | Purpose |
|-------|---------|
| **Raw TIFF → Encrypt** | Test IFED/LEFN style (uncompressed encrypted forensics) |
| **Compress QF=95 → Encrypt** | Near-lossless, minimal JPEG artifacts |
| **Compress QF=90 → Encrypt** | Standard quality, moderate artifacts |
| **Compress QF=75 → Encrypt** | Strong artifacts, tests PP-JPEG energy graph |
| **Double Compress: QF=90 → QF=75** | PP-JPEG primary test scenario |

## Constraints & Gotchas

- ❌ **Splicing only** — no copy-move, no removal
- ❌ **Small (180 forged)** — not for DL training alone
- ❌ **Uncompressed only** — must compress yourself for JPEG tests
- ❌ **No official train/test split** — create and publish yours
- ✅ **Cleanest splicing ground truth** — perfect masks
- ✅ **Feathered boundaries** — realistic, tests localization precision
- ✅ **Camera/lighting variety** — tests content-based detection
- ✅ **Widely used** — direct comparison with SOTA

## Relevance to My Project

**Essential for splicing validation:**
- Validates encrypted methods work **without JPEG artifacts**
- Compress yourself → controlled double-JPEG for PP-JPEG
- Uncompressed encrypted baseline (IFED/LEFN)
- Cross-dataset generalization: train CASIA, test Columbia

---

## Tags
#columbia #splicing #uncompressed #tiff #clean-baseline #feathered-boundaries #encrypted-domain-eval #no-jpeg-artifacts

---

## Cross-References

- **Papers using Columbia:** [[../papers/02_comprint_compression_fingerprint]], [[../papers/06_mfafnet_splicing_detection]], [[../papers/08_trufor_universal_detection]], [[../papers/09_dl_survey_mehrjardi_2023]]
- **Master Index:** [[00_DATASET_MASTER_INDEX]]