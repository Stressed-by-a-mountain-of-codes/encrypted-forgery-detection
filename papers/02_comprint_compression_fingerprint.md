# Paper 2: Comprint — Image Forgery Detection via Compression Fingerprints

**Authors:** Liu, Wu, Bi, Xiao  
**Conference:** ECCV 2022 / Springer LNCS 2023  
**DOI:** 10.1007/978-3-031-37742-6_23  

---

## My Walkthrough

I went through this paper because it's a fundamentally different approach — it doesn't look at image content at all. Instead, it analyzes the **compression history** of JPEG images. The authors' key insight: when you forge a JPEG image and save it, the authentic regions get compressed twice (original QF1 → forged QF2) while tampered regions only get compressed once (at QF2). This creates a detectable "compression fingerprint" or **Comprint**.

In this paper, the authors used a **two-stream encoder**: an **SRM encoder** (Spatial Rich Models — 30 fixed high-pass filters that capture noise residuals) and a **DWT encoder** (Discrete Wavelet Transform with Haar wavelets, 3 levels). They trained this on **pristine images only** — no forged samples needed. That's huge because it means the method generalizes to unseen forgery types.

Here's what they did: they took pristine JPEGs, recompressed them at different quality factors to simulate double compression, and trained the network to predict the compression fingerprint. The SRM encoder captures the high-frequency quantization artifacts, while the DWT encoder captures multi-scale structure. They fused these with dense connections and a feature fusion module.

When they tested on five datasets (CASIA, Columbia, Coverage, NIST16, IMDb2020), Comprint alone got **image-level AUC 0.686** and **pixel-level F1 0.527**. But when they fused it with **Noiseprint** (camera model fingerprint), the combination **Comprint+Noiseprint** jumped to **AUC 0.685** and **F1 0.592** — beating 13 reference methods including MantraNet, PSCC-Net, and TruFor on in-the-wild data.

What this proves: **compression history is a powerful forensic signal** that's orthogonal to camera noise. The two complement each other — Comprint catches splicing/copy-move from different sources, Noiseprint catches same-camera manipulations.

But here's the catch they noticed: when the **featured image and dummy image have the same JPEG quality (QF1 = QF2)**, detection fails completely. The double quantization artifact disappears. They tested this extensively — same camera, different camera, doesn't matter. If QF matches, you're blind.

On the 10th iteration of their analysis (figuratively), they realized the **grid alignment** matters too. If the 8×8 block grids align perfectly between the two compressions, even different QFs can be hard to detect. They handle this by learning the grid offset implicitly through the DWT encoder.

**My takeaway:** This is one of the few methods that could **partially work in encrypted domain** if the encryption preserves DCT coefficient statistics (like selective encryption of MSBs). But with full encryption (Arnold, Paillier), the JPEG structure is destroyed. However, the "train on pristine only" philosophy is directly applicable to encrypted domain — we could train on encrypted pristine images to learn the "encrypted compression fingerprint."

---

## Key Technical Details

| Component | Method | Details |
|-----------|--------|---------|
| SRM Encoder | 30 fixed 5×5 filters | High-pass residual extraction |
| DWT Encoder | Haar, 3 levels | LL, LH, HL, HH at each scale |
| Fusion | DenseNet-style | Concatenation + 1×1 conv + upsample |
| Training Data | Pristine JPEGs only | Simulated double compression (QF1→QF2) |
| Loss | BCE + λ·Dice | Pixel-level supervision |

## Mathematical Core

**Double Quantization Artifact:**
```
Original: F → Q1 = round(F/QF1) → F1 = Q1·QF1
Forge:    Paste region → Recompress at QF2
Authentic region: Q2 = round(F1/QF2) = round(round(F/QF1)·QF1/QF2)
Tampered region:  Q2' = round(F/QF2)  (single quantization)
```

**Energy Graph (for QF estimation):**
```
E(QF) = Σ|DCT_coeff(QF)|²
QF* = first local minimum of E(QF)
```

**Comprint Feature:**
```
f_comprint = Fusion(SRM(I), DWT(I))
SRM(I) = {I * k_i} for i=1..30  (fixed kernels)
DWT(I) = {LL₃, LH₃, HL₃, HH₃, LH₂, HL₂, HH₂, LH₁, HL₁, HH₁}
```

## Constraints & Limitations

- ❌ **JPEG only** — fails on PNG, BMP, uncompressed
- ❌ **Fails when QF1 = QF2** — fundamental limitation
- ❌ Grid alignment can mask artifacts
- ❌ Block-level (8×8) not pixel-level precision
- ✅ Train on pristine only — excellent generalization
- ✅ Complementary to noise-based methods
- ✅ No forged samples needed for training

## Relevance to My Project

**Moderate** for encrypted domain:
- If using **selective encryption** (LSBs clear), DCT on clear portions might work
- **Paillier**: Can compute DCT homomorphically (Paper 12 does this)
- **Arnold permutation**: Destroys 8×8 grid → Comprint fails
- **Core idea** (learn pristine statistics, detect deviations) is directly transferable

---

## Tags
#traditional #compression-fingerprint #double-jpeg #srm #dwt #pristine-training #noiseprint-fusion #jpeg-only