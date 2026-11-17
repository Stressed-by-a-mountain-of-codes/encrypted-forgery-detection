# Paper 5: Copy-Move Forgery Detection Survey (2024)

**Authors:** Multiple  
**Journal:** Multimedia Tools and Applications, 2024  
**DOI:** 10.1007/s11042-024-18399-2  

---

## My Walkthrough

I went through this survey because it's the most recent comprehensive review of copy-move forgery detection (CMFD) methods, covering classical, keypoint-based, and deep learning approaches all in one place. The authors systematically analyzed 100+ papers across three categories, and I needed this bird's-eye view to understand the landscape before diving into encrypted domain work.

In this paper, the authors organized everything into **three distinct categories**: Block-based methods (DCT, DWT, PCET, SVD), Keypoint-based methods (SIFT, SURF, ORB, AKAZE, BRISK), and Deep Learning methods (CNN, RNN, Transformer, GAN). For each category, they broke down the pipeline into four stages: pre-processing, feature extraction, feature matching, and post-processing.

What struck me: they evaluated methods on **standard datasets** (CASIA v1/v2, CoMoFoD, MICC-F220/F600, GRIP) using consistent metrics (Precision, Recall, F1 at pixel and image level). The survey tables let me directly compare methods. For block-based, **PCET (Polar Complex Exponential Transform)** gave the highest recall (94.2%) but lower precision. For keypoint-based, **AKAZE+SIFT fusion** achieved best F1 (91.5%). For deep learning, **PSCC-Net** (ResNet50 backbone) led with F1 0.89 on CASIA.

But here's what I noticed on my 2nd read-through: **no surveyed method works in encrypted domain**. Every single one assumes raw pixel access. The survey mentions this as a gap in the "Future Directions" section — they call for "forensics in encrypted/compressed domains" and "privacy-preserving forensics." That's exactly my project.

The survey also standardized the **evaluation protocol**: they distinguish between image-level (binary: forged/pristine) and pixel-level (segmentation mask) metrics. Most classical methods only report image-level; deep learning methods report both. They also categorize attacks: JPEG compression, rotation, scaling, noise addition, blurring — and show which methods survive which attacks.

**My takeaway:** This survey is my **reference map** for classical CMFD. It tells me: (1) Block-based methods are fast but brittle to geometric transforms; (2) Keypoint-based handle rotation/scale but fail on smooth regions; (3) Deep learning dominates but needs lots of data; (4) **Hybrid methods (like ECDC in Paper 1) are the sweet spot** for classical; (5) **Zero encrypted-domain coverage** — confirmed gap.

For my project, the survey's dataset list and evaluation metrics are directly usable. I'll use CASIA, CoMoFoD, MICC for benchmarking. The attack taxonomy (JPEG, rotation, scale, noise, blur) becomes my robustness test suite.

---

## Key Technical Details

| Category | Top Methods | Best F1 (CASIA) | Strengths | Weaknesses |
|----------|-------------|-----------------|-----------|------------|
| Block-based | DCT, DWT, PCET, SVD | PCET: 0.87 (recall) | Fast, no training | Brittle to rotation/scale |
| Keypoint | SIFT, SURF, ORB, AKAZE | AKAZE+SIFT: 0.915 | Rotation/scale invariant | Fails on smooth areas |
| Deep Learning | PSCC-Net, TruFor, CMFDFormer | PSCC-Net: 0.89 | End-to-end, robust | Needs GPU, large data |

## Mathematical Core

**Standard Evaluation Metrics:**
```
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2·P·R / (P + R)
Pixel-level: per-pixel classification
Image-level: binary decision
```

**Block-based Feature (DCT example):**
```
Block B → DCT → Zigzag → Feature vector (first k coefficients)
Lexicographic sort → Match adjacent blocks → Shift vectors
```

**Keypoint Matching (SIFT):**
```
Descriptor: 128-dim (4×4 grid × 8 orientation bins)
Match: Ratio test (Lowe): ||d1 - d2|| / ||d1 - d3|| < 0.7
RANSAC: Geometric verification (affine/homography)
```

## Constraints & Limitations (of Surveyed Methods)

- ❌ All assume raw pixel access
- ❌ Block-based: fixed grid → fails on rotation
- ❌ Keypoint: needs texture → fails on smooth regions
- ❌ Deep learning: domain gap (synthetic train → real test)
- ❌ No encrypted domain, no privacy preservation
- ✅ Comprehensive taxonomy and benchmark

## Relevance to My Project

**High as reference**, **Low as direct method**:
- Dataset list → my benchmark datasets
- Attack taxonomy → my robustness tests
- Metrics → my evaluation protocol
- Gap confirmation → validates my project direction

---

## Tags
#survey #copy-move #cmfd #block-based #keypoint-based #deep-learning #benchmark #taxonomy #gap-analysis