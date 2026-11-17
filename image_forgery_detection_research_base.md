# Image Forgery Detection Research Base
## Comprehensive Literature Survey for Major Project

**Created:** November 17, 2026  
**Focus:** Image Forgery Detection in Encrypted Domain  
**Total Papers:** 15 (5 Classical + 5 Deep Learning + 5 Encrypted Domain)  
**Format:** Markdown (easy to read, version control, low token generation)

---

## Table of Contents

1. [Classical/Traditional Methods (5 papers)](#1-classicaltraditional-methods)
2. [Deep Learning Methods (5 papers)](#2-deep-learning-methods)
3. [Encrypted Domain / Privacy-Preserving Methods (5 papers)](#3-encrypted-domain--privacy-preserving-methods)
4. [Comparative Analysis](#4-comparative-analysis)
5. [Key Terminologies & Mathematical Formulas](#5-key-terminologies--mathematical-formulas)
6. [Datasets & Evaluation Metrics](#6-datasets--evaluation-metrics)
7. [Research Gaps & Future Directions](#7-research-gaps--future-directions)

---

## 1. Classical/Traditional Methods

### Paper 1: Copy-Move Forgery Detection via Evolving Circular Domains Coverage (ECDC)
**Authors:** Wang et al.  
**Journal:** Multimedia Tools and Applications, 2022  
**DOI:** 10.1007/s11042-022-12755-w  
**Type:** Hybrid (Block-based + Keypoint-based)

#### Objectives
- Improve accuracy of Copy-Move Forgery Detection (CMFD)
- Integrate block-based and keypoint-based methods
- Achieve precise localization of forged regions

#### Methodology
1. **Feature Extraction:** SURF in log-polar space + SIFT from entire image
2. **Feature Matching:** Generalized 2-Nearest Neighbor (g2NN) for massive matched pairs
3. **Outlier Rejection:** RANSAC to filter mismatched pairs → rough localization
4. **Precise Localization:** **ECDC Algorithm** — evolving circular domains centered on matched pairs
5. **Refinement:** Morphological operations

#### ECDC Algorithm (Key Innovation)
```
For each matched pair (x_i, y_i):
  Initialize circular domain C_i with radius r_0
  While not converged:
    Extract block features from C_i
    Update domain boundary based on feature similarity
    Expand/contract radius adaptively
  Final domain = precise forged region
```

#### Mathematical Formulations
- **SIFT Descriptor:** 128-dim vector from gradient histograms in 4×4 subregions
- **SURF in Log-Polar:** Invariant to rotation/scale via log-polar transform
- **g2NN Matching:** For each feature f_i, find 2 nearest neighbors in feature space
- **RANSAC:** Iterative model fitting with inlier threshold ε

#### Results
| Dataset | Precision | Recall | F1-Score |
|---------|-----------|--------|----------|
| CASIA v1 (null) | 92.61% | 91.48% | 91.56% |
| Under geometric attacks | Best among compared methods |

#### Constraints/Limitations
- Computationally heavy (SIFT + SURF + RANSAC + ECDC)
- Requires parameter tuning (initial radius, convergence threshold)
- Struggles with heavy JPEG compression (QF < 70)

---

### Paper 2: Double JPEG Detection via Compression Fingerprints (Comprint)
**Authors:** Liu et al.  
**Conference:** ECCV 2022 / Springer 2023  
**DOI:** 10.1007/978-3-031-37742-6_23  
**Type:** Traditional (Compression Artifact Analysis)

#### Objectives
- Detect forgery via compression history inconsistencies
- Train on pristine images only (no forged samples needed)
- Generalize to unknown manipulation types

#### Key Concept: Compression Fingerprint (Comprint)
When a forged JPEG is saved:
- **Authentic regions:** Doubly compressed (QF1 → QF2)
- **Tampered regions:** Singly compressed (QF2 only)
- **Grid misalignment:** 8×8 block boundaries differ

#### Methodology
1. **SRM Encoder:** Learn high-frequency residuals (Rich Models)
2. **DWT Encoder:** Multi-scale wavelet decomposition
3. **Fusion Network:** Combine SRM + DWT features
4. **Detection:** Localize regions with different compression fingerprints

#### Mathematical Formulations
```
JPEG Compression:
  I → DCT → Quantize(Q) → Zigzag → Huffman

Double Quantization Artifact:
  Y = round(round(X/Q1) * Q1 / Q2) * Q2

Comprint Feature:
  f = SRM_Encoder(I) ⊕ DWT_Encoder(I)
  where ⊕ = feature fusion (concatenation + 1×1 conv)
```

#### Results
| Metric | Comprint | Comprint+Noiseprint | Noiseprint |
|--------|----------|---------------------|------------|
| Image-level AUC | 0.686 | 0.685 | 0.630 |
| Pixel-level F1 | 0.527 | 0.592 | 0.549 |

#### Constraints/Limitations
- Only works on JPEG images
- Fails when QF1 = QF2 (same quality)
- Limited to compression-based forgeries

---

### Paper 3: Robust Forgery Detection for Compressed Images using CNN Supervision
**Authors:** Bondi et al. (referenced), Extended by authors  
**Journal:** Forensic Science International: Digital Investigation, 2020  
**DOI:** 10.1016/j.fsir.2020.100112  
**Type:** Hybrid (Traditional + CNN)

#### Objectives
- Improve robustness against compression (common in social media)
- Camera Model Identification (CMI) as proxy for forgery detection
- Handle "known" and "unknown" camera datasets

#### Methodology
1. **CNNm Model:** Train CNN for Camera Model Identification
2. **Transfer Learning:** Fine-tune for forgery detection
3. **Multi-QF Training:** Train across quality factors (70, 80, 90, 100)

#### Mathematical Formulations
```
Camera Model Identification:
  P(camera | image) = Softmax(CNNm(image))

Forgery Detection:
  Forged if ∃ region with different camera fingerprint
  Score = 1 - max_c P(camera_c | region)

Fine-tuning Loss:
  L = α·L_CMI + (1-α)·L_forgery
```

#### Results
| Dataset | Compression | Bondi et al. | CNNm (proposed) |
|---------|-------------|--------------|-----------------|
| Known | Original (QF=100) | 0.84 | 0.77 |
| Known | QF=90 | 0.56 | **0.72** |
| Known | QF=80 | 0.52 | **0.65** |
| Known | QF=70 | 0.52 | **0.61** |
| Unknown | QF=90 | 0.56 | **0.63** |

#### Constraints/Limitations
- Requires camera model labels for training
- Performance drops significantly at QF < 70
- Assumes forgery = different camera source

---

### Paper 4: FF-Net: End-to-End Feature-Fusion Network for Double JPEG Detection
**Authors:** Liu, Wu, Bi, Xiao  
**Conference:** ML4CS 2022  
**DOI:** proceedings.mlr.press/v189/liu23a/liu23a.pdf  
**Type:** Deep Learning (but traditional task: Double JPEG)

#### Objectives
- Detect/localize double JPEG compression regions
- Handle various QF combinations (QF1 ≠ QF2)
- Generalize to multiple forgery types

#### Architecture
```
FF-Net:
  Input: Image patch (256×256)
  ├── SRM Encoder (30 fixed high-pass filters)
  ├── DWT Encoder (Haar wavelet, 3 levels)
  └── Feature Fusion Module
       ├── Dense connections
       ├── Multi-scale feature aggregation
       └── Upsampling (deconvolution)
  Output: Localization map (same resolution)
```

#### Mathematical Formulations
```
SRM Filters: 30 fixed 5×5 kernels for noise residual extraction
  R = Σ_k w_k * I  (convolution with fixed kernels)

DWT Decomposition:
  LL, LH, HL, HH = DWT(I)
  Multi-scale: Repeat on LL subband

Double JPEG Grid Detection:
  Grid offset = (8 - (block_start mod 8)) mod 8
  Misaligned blocks → tampered region indicator

Loss Function:
  L = BCE(Ŷ, Y) + λ·Dice(Ŷ, Y)
  where Ŷ = predicted mask, Y = ground truth
```

#### Results
- Outperforms RRU-Net, FusionNet, Park et al. on all QF pairs
- Best on small images (512×384) and large images (3008×2000)
- Handles: copy-move, object removal, blurring, color change, resizing

#### Constraints/Limitations
- JPEG-only
- Requires paired (QF1, QF2) training data
- SRM filters fixed (not learned)

---

### Paper 5: Survey on Copy-Move Forgery Detection (2024)
**Authors:** Multiple  
**Journal:** Multimedia Tools and Applications, 2024  
**DOI:** 10.1007/s11042-024-18399-2  
**Type:** Survey Paper

#### Comprehensive Categorization
| Category | Methods | Key Techniques |
|----------|---------|----------------|
| **Block-based** | DCT, DWT, PCET, SVD | Fixed/overlapping blocks, lexicographic sorting |
| **Keypoint-based** | SIFT, SURF, ORB, AKAZE, BRISK | Scale/rotation invariant features |
| **Deep Learning** | CNN, RNN, Transformer, GAN | End-to-end, patch-based, pixel-level |

#### Evaluation Metrics (Standard)
```
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F1 = 2 × Precision × Recall / (Precision + Recall)
AUC = Area Under ROC Curve
Pixel-level: per-pixel classification
Image-level: binary (forged/pristine)
```

#### Key Datasets
| Dataset | Type | Size | Forgeries |
|---------|------|------|-----------|
| CASIA v1/v2 | Copy-move, splicing | 1,700+ | Various |
| CoMoFoD | Copy-move | 200 | Geometric transforms |
| MICC-F220 / F600 | Copy-move | 220/600 | Rotation, scaling |
| GRIP | Copy-move, splicing | 1,000+ | Realistic |
| Columbia | Splicing | 180 | Uncompressed |
| Coverage | Splicing | 100 | Known source |
| IMDb2020 | Generic | 2,000 | In-the-wild |

---

## 2. Deep Learning Methods

### Paper 6: Multi-Scale Feature Attention Fusion for Image Splicing Detection (MFAF-Net)
**Authors:** Multiple  
**Journal:** ACM TOMM, 2024  
**DOI:** 10.1145/3698770  
**Type:** CNN + Attention

#### Objectives
- State-of-the-art splicing detection
- Robust to post-processing (JPEG, noise, resize)
- Multi-scale feature fusion with attention

#### Architecture
```
MFAF-Net:
  Backbone: ResNet-50 / EfficientNet
  ├── Multi-Scale Feature Extractor (P3, P4, P5 from FPN)
  ├── Attention Fusion Module
  │   ├── Channel Attention (SE-block)
  │   ├── Spatial Attention (CBAM)
  │   └── Cross-Scale Attention
  └── Decoder: Upsample + Fuse → Localization Map
```

#### Mathematical Formulations
```
Feature Pyramid:
  P_l = Conv1x1(C_l) + Upsample(P_{l+1})  (FPN style)

Channel Attention:
  z_c = GlobalAvgPool(F) → FC → ReLU → FC → Sigmoid
  F' = F × z_c

Spatial Attention:
  M_s = Sigmoid(Conv7x7([AvgPool(F); MaxPool(F)]))
  F'' = F' × M_s

Cross-Scale Attention:
  A_{i→j} = Softmax(Q_i K_j^T / √d) V_j
  where Q_i = W_q P_i, K_j = W_k P_j, V_j = W_v P_j

Loss:
  L = L_BCE + λ_1 L_Dice + λ_2 L_IoU
```

#### Results
- SOTA on 4 benchmark datasets (CASIA, Columbia, NIST16, In-the-wild)
- Robust to JPEG QF≥70, Gaussian noise σ≤15, resize 0.5×-2×

---

### Paper 7: CMFDFormer: Transformer-based Copy-Move Detection with Continual Learning
**Authors:** Multiple  
**Preprint:** arXiv:2311.13263v2, 2023  
**Type:** Transformer + Continual Learning

#### Objectives
- Transformer-based CMFD (MiT backbone)
- Continual learning for new forgery types (PCSD framework)
- Address synthetic data domain gap

#### Architecture
```
CMFDFormer:
  Backbone: MiT (Mix Transformer) - B0 to B5 variants
  ├── Overlapping Patch Embedding
  ├── Transformer Blocks (Efficient Self-Attention)
  │   └── Reduction Ratio R for attention (default R=8)
  └── Multi-Level Features (C1, C2, C3, C4)

Decoder: PHD (Pluggable Hybrid Decoder)
  ├── MLPs for each level
  ├── Feature Fusion
  └── Upsample → Mask Prediction

PCSD Continual Learning:
  1. Pooled Cube Distillation: 3D feature cube pooling
  2. Strip Distillation: 1D strip sampling for efficiency
  3. Knowledge distillation loss: L_KD = ||f_old - f_new||^2
```

#### Mathematical Formulations
```
MiT Attention:
  X ∈ ℝ^{H×W×C} → Patch Embedding → ℝ^{N×C}
  Q = X W_q, K = X W_k, V = X W_v
  Attention = Softmax(QK^T / √d) V
  Efficient: K, V reduced by ratio R via pooling

PCSD Loss:
  L_total = L_seg + λ·L_KD
  L_KD = Σ_l ||Pool3D(f_old^l) - Pool3D(f_new^l)||_F^2
        + Σ_l ||Strip(f_old^l) - Strip(f_new^l)||_F^2
```

#### Results
- Outperforms CNN-based methods on CASIA, CoMoFoD, GRIP
- Continual learning maintains performance on old tasks while learning new ones

---

### Paper 8: TruFor: All-Round Clues for Trustworthy Forgery Detection
**Authors:** Guillaro, Cozzolino, Sud, Dufour, Verdoliva  
**Conference:** CVPR 2023  
**DOI:** openaccess.thecvf.com/content/CVPR2023/papers/Guillaro_TruFor...  
**Type:** Transformer + Noise Fingerprint + Reliability

#### Objectives
- Universal detector (cheapfakes + deepfakes)
- Pixel-level localization + image-level score + **reliability map**
- Self-supervised noise fingerprint learning

#### Architecture
```
TruFor:
  Input: RGB Image (224×224 or 512×512)
  ├── Noise Fingerprint Extractor (Self-supervised)
  │   ├── Random noise injection
  │   ├── Denoising autoencoder
  │   └── Fingerprint = Residual (Input - Denoised)
  ├── Transformer Fusion (Swin Transformer backbone)
  │   ├── RGB Stream
  │   ├── Noise Stream
  │   └── Cross-Attention Fusion
  ├── Output Heads
  │   ├── Integrity Score (Binary: pristine/forged)
  │   ├── Localization Map (Pixel-level)
  │   └── Reliability Map (Uncertainty estimation)
```

#### Mathematical Formulations
```
Noise Fingerprint (Self-Supervised):
  x̃ = x + n,  n ~ N(0, σ^2)
  x̂ = Denoiser(x̃)
  f = x̃ - x̂  (learned noise residual)

Transformer Fusion:
  F_rgb = SwinBlock(x)
  F_noise = SwinBlock(f)
  F_fused = CrossAttn(F_rgb, F_noise) + F_rgb

Reliability Map:
  r = σ(Conv1x1(F_fused))  ∈ [0,1]
  High r = reliable prediction; Low r = uncertain

Loss:
  L = L_cls + λ_loc·L_loc + λ_rel·L_rel
  L_rel = BCE(r, 1_{|ŷ - y| < τ})  (reliable if error < threshold)
```

#### Results
- SOTA on multiple datasets (CASIA, Columbia, NIST16, IMDb2020, FF++)
- Detects: splicing, copy-move, removal, DeepFake, FaceSwap, NeuralTextures
- Reliability map reduces false alarms in forensic applications

---

### Paper 9: Survey on Deep Learning-based Image Forgery Detection (2023)
**Authors:** Mehrjardi, Latif, Zarchi, Sheikhpour  
**Journal:** Pattern Recognition, Vol 144, 109778, 2023  
**DOI:** 10.1016/j.patcog.2023.109778  
**Type:** Comprehensive Survey (156 references)

#### Deep Learning Architecture Taxonomy
| Architecture | Variants | Forgery Types | Key Papers |
|--------------|----------|---------------|------------|
| **CNN** | VGG, ResNet, DenseNet, U-Net, FPN | All | Bayar 2016, Wu 2019, Liu 2022 |
| **RNN/LSTM** | Bi-LSTM, ConvLSTM | Splicing, Video | Rao 2017, Li 2018 |
| **Transformer** | ViT, Swin, MiT, PSCC-Net | Splicing, CMFD | Liu 2022, CMFDFormer 2023 |
| **GAN-based** | GANomaly, AnoGAN | Inpainting, DeepFake | Schlegl 2017, Cozzolino 2018 |
| **Two-Stream** | RGB + Noise, RGB + SRM, RGB + DCT | All | Kwon 2021, Bayar 2019 |
| **Self-Supervised** | Contrastive, Masked Autoencoder | Generic | TruFor 2023, GAN-Fingerprint 2022 |

#### Training Strategies
```
1. Supervised: Forged/pristine pairs (needs labeled data)
2. Self-Supervised: 
   - Pretext: Noise extraction, JPEG artifact prediction
   - Fine-tune on small labeled set
3. Contrastive Learning:
   L_contrast = -log(exp(sim(z_i, z_j)/τ) / Σ_k exp(sim(z_i, z_k)/τ))
4. Domain Adaptation:
   L_total = L_source + λ·L_MMD + μ·L_adv
```

#### Benchmark Comparison (from survey Table 2)
| Method | Backbone | CMFD F1 | Splicing F1 | Inpainting F1 | Generic |
|--------|----------|---------|-------------|---------------|---------|
| PSCC-Net | ResNet50 | 0.89 | 0.85 | 0.78 | 0.82 |
| TruFor | Swin-T | **0.92** | **0.89** | **0.85** | **0.87** |
| CMFDFormer | MiT-B2 | 0.91 | - | - | - |
| Comprint+NP | Custom | 0.71 | 0.68 | 0.62 | 0.67 |
| Noiseprint | Custom | 0.68 | 0.65 | 0.59 | 0.63 |

---

### Paper 10: Review of Image Forensic Techniques Based on Deep Learning (2023)
**Authors:** Multiple  
**Journal:** Mathematics, 11(14), 3134, 2023  
**DOI:** 10.3390/math11143134  
**Type:** Survey with Framework

#### Proposed Unified Framework
```
Image Forgery Detection Framework:
┌─────────────────────────────────────────┐
│         Preprocessing                   │
│  (Denoise, Resize, Normalize, Augment)  │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│      Feature Extraction                 │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │  RGB    │ │ Noise   │ │ Freq.   │   │
│  │ Stream  │ │ Stream  │ │ Stream  │   │
│  └────┬────┘ └────┬────┘ └────┬────┘   │
└───────┼────────────┼────────────┼───────┘
        ▼            ▼            ▼
┌─────────────────────────────────────────┐
│      Feature Fusion                     │
│  (Concat, Attention, Cross-Attn, Bilinear)│
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│      Detection Head                     │
│  • Binary Classification (Image-level)  │
│  • Segmentation (Pixel-level)           │
│  • Localization + Classification        │
└─────────────────────────────────────────┘
```

#### Key Insight: Noise Features are Critical
- **Camera Model Noise:** PRNU (Photo-Response Non-Uniformity)
- **Compression Noise:** DCT coefficient distributions
- **Processing Noise:** Resampling, filtering artifacts
- **DeepFake Noise:** GAN fingerprint (up-sampling artifacts)

---

## 3. Encrypted Domain / Privacy-Preserving Methods

### Paper 11: Image Forensics in the Encrypted Domain (IFED) — **FOUNDATIONAL PAPER**
**Authors:** Yu, Lu, Li, Chen, Yan  
**Journal:** Entropy, 2024, 26(11), 900  
**DOI:** 10.3390/e26110900  
**PMCID:** PMC11593136  
**Type:** First formal definition of IFED + Deep Learning baseline

#### Objectives
- **First formal definition** of Image Forensics in Encrypted Domain (IFED)
- Define problem, metrics, and evaluation protocol
- Propose LEFN (Lightweight Enhanced Forensic Network) for copy-move in encrypted domain

#### IFED Formal Definition
```
IFED = Technique to authenticate encrypted images and establish source/legitimacy

Categories:
1. Source Detection/Identification
2. Forgery Detection ← This paper's focus
3. Processing Operations Identification
4. Forgery Cracking (recover original)
5. Forgery Attack (render unusable)

Encryption Model: Arnold Permutation (Classic)
  EI (Encryption Intensity): Number of Arnold iterations
  CR (Copy Rate): % of pixels copied/moved (0.25% - 25%)

Metrics:
  Accuracy = (TP + TN) / (TP + TN + FP + FN)
  Precision, Recall, F1 (standard)
```

#### Arnold Permutation Encryption
```
For image I of size N×N:
  x' = (x + y) mod N
  y' = (x + 2y) mod N
  Apply EI times (EI = 1, 2, 3...)

Properties:
  - Periodic: After N iterations, returns to original (for N=256, period=192)
  - Scrambles spatial correlations
  - Preserves histogram (global statistics unchanged)
```

#### LEFN Architecture
```
LEFN (Lightweight Enhanced Forensic Network):
  Input: Encrypted Image (256×256×1)
  ├── RFE: Residual Feature Enhancement Module
  │   ├── High-pass filtering (SRM-like)
  │   └── Residual learning
  ├── KV: Key-Value Attention Module
  │   ├── Non-local attention on encrypted features
  │   └── Global context modeling
  ├── FE: Feature Enhancement Module
  │   ├── Channel attention
  │   └── Spatial attention
  └── B: Binary Classification Head
       └── Output: Forged / Pristine

Parameters: 0.065M (very lightweight)
```

#### Mathematical Formulations
```
RFE Module:
  R = I - Conv3x3(I)  (residual = high-freq)
  F_rfe = Conv1x1(ReLU(Conv3x3(R)))

KV Attention:
  Q = F W_q, K = F W_k, V = F W_v
  Attn = Softmax(QK^T/√d) V
  F_kv = Attn + F

FE Module:
  F_fe = ChannelAttn(F_kv) ⊗ SpatialAttn(F_kv)

Total Loss:
  L = L_CE + λ_1 L_RFE + λ_2 L_KV + λ_3 L_FE
```

#### Experimental Setup
| Parameter | Value |
|-----------|-------|
| Dataset | 11,000 grayscale 256×256 images |
| Encryption | Arnold Permutation |
| EI (Train/Test) | 2 |
| CR Range | 0.25% - 25% |
| Train Pairs | 10,000 |
| Test Pairs | 1,000 |

#### Key Results
| CR Range | Accuracy (EI=2) |
|----------|-----------------|
| 0.25% - 9% | Low (< 70%) |
| 9% - 25% | High (> 85%) |

| EI | Accuracy (CR=10%) |
|----|-------------------|
| 1 | ~95% |
| 2 | ~88% |
| 3 | ~75% |

**Key Finding:** Higher EI → dramatically harder detection. Model needs more capacity for higher EI.

#### Constraints/Limitations
- Only Arnold permutation (simple spatial scrambling)
- Only copy-move forgery
- Grayscale images only
- EI=2 fixed for training (doesn't generalize to EI=3)
- Dataset not publicly released yet

---

### Paper 12: PP-JPEG: Privacy-Preserving JPEG Tampering Localization with Paillier
**Authors:** Jena, Singh, Mohanty  
**Journal:** Journal of Imaging, 2023, 9(9), 172  
**DOI:** 10.3390/jimaging9090172  
**PMCID:** PMC10532548  
**Type:** Paillier Homomorphic Encryption + Compression Analysis

#### Objectives
- Detect JPEG tampering in encrypted domain
- Use Paillier homomorphic encryption (additive)
- Preserve privacy during forensic analysis

#### Paillier Cryptosystem (Key Math)
```
KeyGen:
  Choose large primes p, q
  n = p·q, λ = lcm(p-1, q-1)
  g ∈ Z*_{n^2} (generator)
  Public: (n, g), Private: λ

Encryption:
  E(m) = g^m · r^n mod n^2  (r random ∈ Z*_n)

Decryption:
  D(c) = L(c^λ mod n^2) · μ mod n
  where L(x) = (x-1)/n, μ = (L(g^λ mod n^2))^{-1}

Homomorphic Properties:
  E(m1) · E(m2) mod n^2 = E(m1 + m2 mod n)  [Addition]
  E(m)^k mod n^2 = E(k·m mod n)              [Scalar Mult]
```

#### Methodology
```
PP-JPEG Framework:
1. Image Owner: Encrypt image with Paillier → Send to Cloud
2. Cloud (Encrypted Domain):
   a. Compute DCT on encrypted blocks (using homomorphic props)
   b. Analyze quantization artifacts
   c. Energy Graph: E(QF) = Σ |DCT_coeff|^2 at quality QF
   d. Featured Image QF = First Minima in Energy Graph
   e. Dummy (Forged) Region QF ≠ Featured QF → Detect
3. Return encrypted results → Owner decrypts

Detection Principle:
  Double JPEG → Different QF in regions
  Energy Graph minima reveals original QF
  Mismatch → Tampering
```

#### Mathematical Formulations
```
DCT in Encrypted Domain (8×8 block):
  For each pixel: c_{u,v} = E(Σ_{x,y} I[x,y] · cos(...) · cos(...))
  Using: E(Σ a_i·x_i) = Π E(x_i)^{a_i}  (scalar mult + addition)

Energy at QF:
  E(QF) = Σ_{u,v} |DCT_{u,v}(QF)|^2
  
First Minima Detection:
  QF* = argmin_{QF} E(QF)  (first local minimum)

Tampering Localization:
  For each block: 
    if |E_block(QF*) - E_global(QF*)| > τ → Tampered
```

#### Results
| Scenario | Detection Rate |
|----------|----------------|
| Different QF (Featured vs Dummy) | High (~90%+) |
| Same QF | Low (fundamental limitation) |
| Same camera / Different camera | No significant difference |

#### Constraints/Limitations
- **Only JPEG** (relies on double quantization)
- **Fails when QF1 = QF2** (same compression quality)
- Paillier: Large ciphertext expansion (×2048 bits per pixel!)
- Computationally heavy (homomorphic DCT on encrypted data)
- Block-level only (8×8), not pixel-level

---

### Paper 13: Robust Image Hashing in Encrypted Domain with Paillier
**Authors:** Qin, Guo, Li, Qian, Zhang  
**Journal:** Journal of Software (Chinese), 2023, 34(2), 868-883  
**DOI:** 10.13328/j.cnki.jos.006419  
**Type:** Perceptual Hashing + Paillier + HVS

#### Objectives
- Verify integrity/authenticity of encrypted images
- Cloud computes hash without seeing plaintext
- Robust to content-preserving operations

#### System Architecture
```
Three-Party Protocol:
1. Image Owner: Paillier Encrypt → Upload to Cloud
2. Cloud Server: 
   a. Encrypted DCT (homomorphic)
   b. Watson HVS Weighting (encrypted)
   c. Pseudo-random Matrix (key-controlled)
   d. Output: Ciphertext Hash
3. Receiver: Decrypt Hash → Compare with Local Hash
```

#### Mathematical Formulations
```
Preprocessing:
  I_gray = 0.2989·R + 0.5870·G + 0.1140·B
  Resize to M×M

Paillier Encryption (per pixel):
  c_{i,j} = E(I[i,j]) = g^{I[i,j]} · r^n mod n^2

Encrypted DCT (8×8 block):
  DCT_{u,v} = Σ_{x=0}^7 Σ_{y=0}^7 c_{x,y} · w_{u,v}(x,y)
  where w = cos((2x+1)uπ/16) · cos((2y+1)vπ/16)
  Using homomorphic: E(a)·E(b) = E(a+b), E(a)^k = E(ka)

Watson HVS Weighting (Encrypted):
  W_{u,v} = WatsonWeight(u,v)  (plaintext, public)
  F_{u,v} = DCT_{u,v}^{W_{u,v}} = E(W_{u,v} · DCT_{u,v})

Pseudo-Random Matrix (Key-controlled):
  R_{u,v} = PRNG(key)_{u,v} ∈ {±1}
  H_{u,v} = F_{u,v}^{R_{u,v}}  (sign flip in encrypted domain)

Final Hash:
  Hash = {H_{u,v}} for selected frequencies
```

#### Security Properties
| Property | Mechanism |
|----------|-----------|
| **Robustness** | HVS weighting → invariant to JPEG, noise, slight rotation |
| **Uniqueness** | Key-controlled PR matrix → different keys → different hashes |
| **Security** | Paillier semantic security + PR matrix randomness |

#### Results
- Robust: JPEG QF≥50, Gaussian noise σ≤10, rotation ≤2°
- Unique: Hash distance (authentic vs tampered) >> threshold
- Secure: Ciphertext indistinguishable from random

#### Constraints/Limitations
- Authentication only (not localization)
- Requires trusted key management
- Paillier overhead (large ciphertexts, slow)
- Fixed block size (8×8 DCT)

---

### Paper 14: Privacy-Preserving DeepFake Detection (SecDFDNet)
**Authors:** Chen, Liu, Xia, Zhao  
**Journal:** Digital Signal Processing, 2023, 104233  
**DOI:** 10.1016/j.dsp.2023.104233  
**Conference Version:** Oulu Repo, 2023  
**Type:** Additive Secret Sharing + Secure MPC

#### Objectives
- Detect DeepFake faces without exposing private face images
- First privacy-preserving DeepFake detection model
- Maintain plaintext-level accuracy

#### Threat Model
```
Semi-Honest (Honest-but-Curious) Servers:
  - Two non-colluding cloud servers (S1, S2)
  - Trusted Third Party (TTP) for key generation
  - User splits input → sends shares to S1, S2
  - Servers compute → return result shares
  - User reconstructs result
```

#### Additive Secret Sharing (ASS)
```
Split: x = ⟦x⟧_1 + ⟦x⟧_2  (mod 256 for pixels)
  ⟦x⟧_1 ← random [0,255], ⟦x⟧_2 = x - ⟦x⟧_1 mod 256

Secure Protocols Designed:
1. SecReLU:   Secure ReLU activation
2. SecSigm:   Secure Sigmoid
3. SecSpatial: Secure Spatial Operations (Conv, Pool)
4. SecChannel: Secure Channel Operations (Concat, Split)

Key Innovation: Resharing for Numerical Range
  After SecReLU: values can exceed 255
  Protocol: Servers exchange masks to reshare within range
```

#### Mathematical Formulations
```
SecReLU (Input: ⟦x⟧_1, ⟦x⟧_2):
  1. S1, S2 locally compute sign shares
  2. Compare ⟦x⟧_1 + ⟦x⟧_2 with 0 (secure comparison)
  3. Output: ⟦max(0, x)⟧_1, ⟦max(0, x)⟧_2

Resharing Protocol:
  S1: y1 = f(x1), mask1 = x1 - y1 → send mask1 to S2
  S2: y2 = f(x2), mask2 = x2 - y2 → send mask2 to S1
  S1: x1' = y1 - mask2
  S2: x2' = y2 - mask1
  Result: x1' + x2' = f(x1) + f(x2) = f(x)  (correct!)

Model: SecDFDNet (based on DFDNet)
  Backbone: Xception / EfficientNet-B0
  Modified: All non-linear → secure protocols
```

#### Results (Accuracy %)
| Model | FF++ (DF) | FF++ (FS) | FF++ (F2F) | FF++ (NT) | CelebDF | DFDC |
|-------|-----------|-----------|------------|-----------|---------|------|
| Plaintext DFDNet | 98.24 | 96.52 | 95.13 | 93.68 | 98.12 | 89.13 |
| **Ciphertext SecDFDNet** | **98.24** | **96.52** | **95.13** | **93.68** | **98.12** | **89.13** |
| Plaintext Xception | 93.78 | 93.46 | 90.47 | 70.75 | 92.45 | 81.74 |
| Secure Xception | 93.78 | 93.46 | 90.47 | 70.75 | 92.45 | 81.74 |
| Plaintext EffNet-B0 | 96.91 | 97.18 | 92.13 | 71.24 | 97.54 | 85.57 |
| Secure EffNet-B0 | 96.91 | 97.18 | 92.13 | 71.24 | 97.54 | 85.57 |

**Key Achievement: Zero accuracy loss** with privacy preservation.

#### Constraints/Limitations
- Face-only (DeepFake detection)
- Two-server model (trust assumption)
- Communication overhead (4 rounds per non-linear layer)
- Requires TTP for key generation
- Video: Process frame-by-frame (slow)

---

### Paper 15: Selective Encryption for Forensics-Privacy Trade-off
**Authors:** Puteaux, Itier, Bas  
**Preprint:** arXiv:2103.03569, 2021  
**Type:** Selective Encryption (Bit-plane) + SRMQ1 Forensics

#### Objectives
- Trade-off: Privacy (encryption) vs Forensics (detectability)
- Selective encryption: Encrypt MSBs, keep LSBs clear
- Forensics on residual (LSB) information

#### Selective Encryption Model
```
Bit-Plane Decomposition (8-bit pixel):
  I = Σ_{k=0}^7 b_k · 2^k
  b_7: MSB (most visual info), b_0: LSB (noise-like)

Selective Encryption:
  Encrypt bit-planes k = s, s+1, ..., 7  (s = security level)
  Keep bit-planes k = 0, 1, ..., s-1  in clear
  
  Example: s=4 → Encrypt 4 MSBs, keep 4 LSBs clear
```

#### Forensics on Selectively Encrypted Images
```
SRMQ1 Features (on clear LSBs):
  1. Compute residuals: R = I - Predictor(I)
  2. Model residuals with Gaussian Mixture
  3. Extract moments → Feature vector
  4. Classifier: SVM / Random Forest → Tampered/Not

Privacy Evaluation:
  Recognizability = CNN_Class(Predict(SelectiveEncrypted(I)))
  Lower = Better Privacy
```

#### Trade-off Analysis
| Encrypted Bit-planes (s) | Forensics Accuracy | Privacy (Recognizability) |
|--------------------------|-------------------|---------------------------|
| 0 (None) | 100% | 100% (No privacy) |
| 2 | 95% | 60% |
| 4 | 80% | 25% |
| 6 | 50% | 10% |
| 8 (Full) | 10% (Random) | 0% (Max privacy) |

#### Key Insight
```
Selective Encryption ≠ Homomorphic Encryption
- Selective: Fast, no size expansion, partial privacy
- Homomorphic: Slow, large expansion, full privacy + computability
- Trade-off is fundamental: More encryption → Less forensic signal
```

---

## 4. Comparative Analysis

### 4.1 Method Comparison Matrix

| Aspect | Classical | Deep Learning | Encrypted Domain |
|--------|-----------|---------------|------------------|
| **Accuracy** | Moderate | High (SOTA) | Low-Moderate |
| **Speed** | Fast (CPU) | Slow (GPU) | Very Slow |
| **Generalization** | Low | High (with data) | Very Low |
| **Privacy** | None | None | **Full/Partial** |
| **Localization** | Pixel/Block | Pixel-level | Block-level |
| **Compression Robust** | Poor | Good (TruFor) | N/A (encrypted) |
| **Implementation** | Easy | Complex | Very Complex |

### 4.2 Encrypted Domain: Encryption Scheme Comparison

| Scheme | Type | Operations | Ciphertext Expansion | Speed | Forensics Support |
|--------|------|------------|---------------------|-------|-------------------|
| **Arnold Permutation** | Symmetric (Scrambling) | Permutation only | 1× (no expansion) | Very Fast | **Only spatial stats** |
| **Paillier** | PHE (Additive) | +, ×_scalar | ~2048× (per pixel) | Slow | Linear ops, DCT, mean |
| **CKKS/BFV** | FHE | +, ×, approximate | ~1000-4000× | Very Slow | Arbitrary circuits |
| **Selective Encryption** | Hybrid | Partial | 1× (partial) | Fast | On clear portion only |
| **Secret Sharing (ASS)** | MPC | +, × (via protocols) | 2× (2 shares) | Medium | Any (with protocols) |

### 4.3 Forgery Types vs Detection Capability

| Forgery Type | Classical | Deep Learning | Encrypted (Arnold) | Encrypted (Paillier) |
|--------------|-----------|---------------|---------------------|----------------------|
| Copy-Move | ✓ Good | ✓ Excellent | ✓ (LEFN) | △ (Hash only) |
| Splicing | ✓ Good | ✓ Excellent | ✗ | △ (DCT-based) |
| Inpainting/Removal | △ Limited | ✓ Good | ✗ | ✗ |
| DeepFake | ✗ | ✓ Excellent | ✗ | ✓ (SecDFDNet) |
| Double JPEG | ✓ Excellent | ✓ Good | ✗ | ✓ (PP-JPEG) |
| Recompression | ✗ Poor | △ Moderate | ✗ | △ |

---

## 5. Key Terminologies & Mathematical Formulas

### 5.1 Forgery Detection Terminology

| Term | Definition |
|------|------------|
| **Passive/Blind Forensics** | No prior info (watermark/signature); analyze image traces only |
| **Active Forensics** | Requires embedded watermark/signature at creation |
| **Copy-Move (CMFD)** | Copy region from same image, paste elsewhere |
| **Splicing** | Combine regions from different images |
| **Inpainting/Removal** | Remove object, fill with background synthesis |
| **DeepFake** | GAN-based face swap/expression transfer |
| **Double JPEG** | Image compressed twice with different QFs |
| **PRNU** | Photo-Response Non-Uniformity (camera fingerprint) |
| **SRM** | Spatial Rich Models (handcrafted high-pass filters) |
| **ELA** | Error Level Analysis (re-save difference) |

### 5.2 Encryption Terminology

| Term | Definition |
|------|------------|
| **PHE** | Partially Homomorphic Encryption (one operation: + or ×) |
| **SWHE** | Somewhat Homomorphic Encryption (limited + and ×) |
| **FHE** | Fully Homomorphic Encryption (unlimited + and ×) |
| **Paillier** | Additive PHE (E(m1)·E(m2) = E(m1+m2)) |
| **ElGamal** | Multiplicative PHE (E(m1)·E(m2) = E(m1×m2)) |
| **CKKS** | Approximate FHE (real numbers, SIMD/batching) |
| **BFV/BGV** | Exact FHE (integers, polynomial rings) |
| **Arnold Permutation** | Chaotic map for image scrambling (periodic) |
| **EI (Encryption Intensity)** | Arnold iterations; higher = more scrambled |
| **CR (Copy Rate)** | % of image area copied/moved in forgery |
| **Selective Encryption** | Encrypt only selected bit-planes (MSBs) |

### 5.3 Core Mathematical Formulas

#### JPEG Compression & Double Quantization
```
Forward DCT:     F[u,v] = ¼ C(u)C(v) Σ Σ f[x,y] cos(...) cos(...)
Quantization:    Q[u,v] = round(F[u,v] / QTable[u,v])
Dequantization:  F'[u,v] = Q[u,v] · QTable[u,v]
Inverse DCT:     f'[x,y] = ¼ Σ Σ C(u)C(v) F'[u,v] cos(...) cos(...)

Double Quantization Artifact:
  Q2 = round( round(F/Q1) · Q1 / Q2 )
  Periodic peaks in histogram of Q2 → Detect QF1, QF2
```

#### Paillier Homomorphic Encryption
```
KeyGen:     n=pq, λ=lcm(p-1,q-1), g∈Z*_{n²}, μ=(L(g^λ mod n²))⁻¹
Encrypt:    c = g^m · r^n mod n²
Decrypt:    m = L(c^λ mod n²) · μ mod n
Add:        E(m1) ⊙ E(m2) = E(m1+m2)  (⊙ = multiply mod n²)
ScalarMul:  E(m)^k = E(k·m)
```

#### Arnold Cat Map (Permutation)
```
[x']   [1 1] [x]   (mod N)
[y'] = [1 2] [y]   (mod N)

Period for N=256: 192 iterations
Eigenvalues: λ₁,₂ = (3 ± √5)/2  (chaotic)
```

#### Evaluation Metrics
```
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2·P·R / (P + R)
Accuracy  = (TP + TN) / (TP + TN + FP + FN)
IoU       = |Pred ∩ GT| / |Pred ∪ GT|
AUC       = ∫ TPR(FPR) dFPR  (Area under ROC)
```

#### Deep Learning Losses
```
Binary Cross Entropy:  BCE = -[y log(ŷ) + (1-y) log(1-ŷ)]
Dice Loss:             1 - 2|X∩Y| / (|X|+|Y|)
Focal Loss:            -α(1-ŷ)^γ log(ŷ)  (for class imbalance)
Contrastive:           max(0, m - sim(pos) + sim(neg))
Triplet:               max(0, d(a,p) - d(a,n) + m)
```

---

## 6. Datasets & Evaluation Metrics

### 6.1 Standard Datasets

| Dataset | Year | Type | Size | Splits | Link |
|---------|------|------|------|--------|------|
| **CASIA v1** | 2013 | CM, Splicing | 1,721 | - | IEEE |
| **CASIA v2** | 2014 | CM, Splicing | 12,614 | - | IEEE |
| **CoMoFoD** | 2013 | CM | 200 | - | Unizg |
| **MICC-F220** | 2015 | CM | 220 | - | MICC |
| **MICC-F600** | 2015 | CM | 600 | - | MICC |
| **GRIP** | 2019 | CM, Splicing | 1,000+ | - | Unina |
| **Columbia** | 2004 | Splicing | 183 | - | Columbia |
| **Coverage** | 2016 | Splicing | 100 | - | Polimi |
| **NIST16** | 2016 | Splicing | 564 | - | NIST |
| **IMDb2020** | 2020 | Generic | 2,000 | Train/Val/Test | Unina |
| **FaceForensics++** | 2019 | DeepFake | 1000 vids | Train/Val/Test | FF++ |
| **CelebDF** | 2020 | DeepFake | 590 vids | - | CelebDF |
| **DFDC** | 2020 | DeepFake | 100k+ vids | - | Kaggle |

### 6.2 IFED-Specific Dataset (Paper 11)
```
Custom Dataset (Yu et al. 2024):
  Source: 11,000 grayscale natural images, 256×256
  Encryption: Arnold Permutation
  Forgery: Copy-move only
  CR Range: 0.25% - 25%
  EI: 1, 2, 3
  Train: 10,000 pairs (normal/forged)
  Test: 1,000 pairs
  Status: To be released after peer review
```

### 6.3 Evaluation Protocols
```
Image-Level: Binary classification (Forged/Intact)
  Metrics: Accuracy, AUC, Precision, Recall, F1

Pixel-Level: Segmentation (Tampered mask)
  Metrics: Pixel F1, IoU, AUC, MCC

Localization: Bounding box / Region
  Metrics: Precision@IoU, Recall@IoU

Robustness: Test on attacked images
  Attacks: JPEG (QF 50-95), Resize, Noise, Blur, Rotation
  Metric: Performance drop % vs clean
```

---

## 7. Research Gaps & Future Directions

### 7.1 Identified Gaps

| Gap | Current State | Needed |
|-----|---------------|--------|
| **Encryption Diversity** | Only Arnold (scrambling) tested | Paillier, CKKS, AES, selective |
| **Forgery Types in ED** | Only copy-move | Splicing, inpainting, DeepFake |
| **Localization in ED** | Image-level only (LEFN) | Pixel-level in encrypted domain |
| **Generalization across EI** | EI=2 train → EI=3 fails | EI-invariant or multi-EI training |
| **Real-world ED Data** | Synthetic only | Real encrypted-forensic dataset |
| **Efficiency** | Paillier: hours/image | Optimized HE / MPC / hybrid |
| **Multi-party ED Forensics** | Single party (PP-JPEG) | Collaborative (SecDFDNet style) |

### 7.2 Promising Research Directions

#### Direction 1: Hybrid Encryption for Forensics
```
Combine: Selective Encryption (fast, privacy) + Homomorphic (key regions)
  - Encrypt MSBs with AES (privacy)
  - Encrypt LSBs with Paillier (forensic computability)
  - Forensics on LSB residuals in encrypted domain
```

#### Direction 2: Transformer-based IFED
```
Adapt TruFor / CMFDFormer for encrypted domain:
  - Encrypted noise fingerprint extraction (homomorphic)
  - Encrypted attention (requires FHE or MPC)
  - Knowledge distillation: Plaintext teacher → Encrypted student
```

#### Direction 3: Compressive Sensing + Encryption
```
Compressive Sensing (CS) naturally encrypts:
  y = Φx  (Φ = measurement matrix, secret key)
  - Forensics on measurements y (lower dim)
  - Joint reconstruction + detection
  - Paper: "Optimized Orthogonal CS for Encryption" (2024)
```

#### Direction 4: Federated Forensics in Encrypted Domain
```
Multiple parties hold encrypted images:
  - Local forensic feature extraction (encrypted)
  - Secure aggregation (MPC)
  - Global model update without sharing data
  - Extends SecDFDNet to multi-institution
```

#### Direction 5: Benchmark for IFED
```
Create standardized IFED benchmark:
  - Multiple encryption schemes (Arnold, Paillier, AES, CS)
  - Multiple forgery types (CM, Splicing, Inpainting, DeepFake)
  - Multiple EI / security levels
  - Standard train/val/test splits
  - Baseline implementations
```

### 7.3 Recommended Project Roadmap

```
Phase 1 (Literature & Setup):     COMPLETE ✓
  ├── This research base
  ├── Environment setup (PyTorch, SEAL/Pyfhel, TenSEAL)
  └── Dataset acquisition

Phase 2 (Baseline Implementation): 
  ├── Implement LEFN (Paper 11) for Arnold + CM
  ├── Implement PP-JPEG (Paper 12) for Paillier + Double JPEG
  ├── Implement SecDFDNet (Paper 14) for ASS + DeepFake
  └── Compare on common test set

Phase 3 (Novel Contribution):
  ├── Design: Hybrid Encryption Forensic Framework
  │   ├── Selective encryption for privacy
  │   ├── Homomorphic for key forensic ops
  │   └── Transformer-based detector
  ├── Train: Multi-EI, Multi-forgery, Multi-encryption
  ├── Evaluate: Standard IFED benchmark (new)
  └── Optimize: Efficiency (batching, quantization, distillation)

Phase 4 (Validation & Publication):
  ├── Ablation studies
  ├── Real-world testing (cloud deployment)
  ├── Paper writing (target: TIFS, CVPR, ICCV)
  └── Code release
```

---

## Appendix: Quick Reference Cards

### Paper 11 (IFED/LEFN) - Key Equations
```
Arnold: (x',y') = ((x+y) mod N, (x+2y) mod N)^EI
LEFN: RFE → KV-Attn → FE → Binary Classifier
Loss: CE + λ₁L_RFE + λ₂L_KV + λ₃L_FE
Key Insight: CR > 9% → Detectable; EI > 2 → Hard
```

### Paper 12 (PP-JPEG) - Key Equations
```
Paillier: E(m1)·E(m2) = E(m1+m2), E(m)^k = E(km)
Encrypted DCT: Via homomorphic scalar mult + add
Energy Graph: E(QF) = Σ|DCT(QF)|² → Minima = Original QF
Limitation: Fails if QF1 = QF2
```

### Paper 13 (Robust Hash) - Key Equations
```
Encrypted DCT → Watson HVS Weight → PR Matrix Sign Flip
Hash = Decrypt(Cloud_Output) → Compare with Local
Properties: Robust (JPEG≥50), Unique, Secure
```

### Paper 14 (SecDFDNet) - Key Equations
```
ASS: x = ⟦x⟧₁ + ⟦x⟧₂
SecReLU/SecSigm/SecSpatial/SecChannel protocols
Resharing: Fix numerical overflow after non-linear
Result: 0% accuracy loss vs plaintext
```

### Paper 15 (Selective Encryption) - Key Equations
```
Bit-planes: I = Σ b_k·2^k
Encrypt MSBs (k≥s), Keep LSBs (k<s) clear
SRMQ1 on LSBs → Forensics
Trade-off: s↑ → Privacy↑, Forensics↓
```

---

## References (BibTeX Ready)

```bibtex
@article{yu2024ifed,
  title={Image Forensics in the Encrypted Domain},
  author={Yu, Yongqiang and Lu, Yuliang and Li, Longlong and Chen, Feng and Yan, Xuehu},
  journal={Entropy},
  volume={26}, number={11}, pages={900},
  year={2024}, doi={10.3390/e26110900}
}

@article{jena2023ppjpeg,
  title={PP-JPEG: A Privacy-Preserving JPEG Image-Tampering Localization},
  author={Jena, Riyanka and Singh, Priyanka and Mohanty, Manoranjan},
  journal={Journal of Imaging},
  volume={9}, number={9}, pages={172},
  year={2023}, doi={10.3390/jimaging9090172}
}

@article{qin2023robusthash,
  title={Robust Image Hashing in Encrypted Domain},
  author={Qin, Chuan and Guo, Meng-Qi and Li, Xin-Ran and Qian, Zhen-Xing and Zhang, Xin-Peng},
  journal={Journal of Software},
  volume={34}, number={2}, pages={868--883},
  year={2023}, doi={10.13328/j.cnki.jos.006419}
}

@article{chen2023secdfdnet,
  title={Privacy-preserving DeepFake face image detection},
  author={Chen, Beijing and Liu, Xin and Xia, Zhihua and Zhao, Guoying},
  journal={Digital Signal Processing},
  volume={141}, pages={104233},
  year={2023}, doi={10.1016/j.dsp.2023.104233}
}

@article{guillaro2023trufor,
  title={TruFor: Leveraging all-round clues for trustworthy image forgery detection and localization},
  author={Guillaro, Fabrizio and Cozzolino, Davide and Sud, Avneesh and Dufour, Nicholas and Verdoliva, Luisa},
  booktitle={CVPR}, pages={20606--20615}, year={2023}
}

@article{liu2022ffnet,
  title={FF-Net: An End-to-end Feature-Fusion Network for Double JPEG Detection and Localization},
  author={Liu, Bo and Wu, Rui and Bi, Xuan and Xiao, Baowei},
  booktitle={Proceedings of ML4CS}, volume={189}, year={2022}
}

@article{liu2022comprint,
  title={Comprint: Image Forgery Detection and Localization using Compression Fingerprints},
  author={Liu, Bo and Wu, Rui and Bi, Xuan and Xiao, Baowei},
  booktitle={ECCV}, pages={23--39}, year={2022}
}

@article{wang2022ecdc,
  title={Copy-move image forgery detection based on evolving circular domains coverage},
  author={Wang, et al.},
  journal={Multimedia Tools and Applications},
  year={2022}, doi={10.1007/s11042-022-12755-w}
}

@article{putteaux2021selective,
  title={Combining Forensics and Privacy Requirements for Digital Images},
  author={Puteaux, Pauline and Itier, Vincent and Bas, Patrick},
  journal={arXiv preprint arXiv:2103.03569},
  year={2021}
}

@article{mehrjardi2023survey,
  title={A survey on deep learning-based image forgery detection},
  author={Mehrjardi, Fatemeh Zare and Latif, Ali Mohammad and Zarchi, Mohsen Sardari and Sheikhpour, Razieh},
  journal={Pattern Recognition},
  volume={144}, pages={109778},
  year={2023}, doi={10.1016/j.patcog.2023.109778}
}
```

---

**Document Version:** 1.0  
**Last Updated:** November 17, 2026  
**Next Review:** After Phase 2 implementation  
**Maintainer:** Major Project Team

---

*This document serves as the comprehensive reference base for the Image Forgery Detection in Encrypted Domain project. All papers have been analyzed for objectives, methodology, mathematical formulations, results, and constraints. Use this as the single source of truth for literature-derived decisions.*