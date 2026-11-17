# Paper 10: Review of Image Forensic Techniques Based on Deep Learning (2023)

**Authors:** Multiple  
**Journal:** Mathematics, 11(14), 3134, 2023  
**DOI:** 10.3390/math11143134  

---

## My Walkthrough

I went through this paper because it provides a **unified framework** for deep learning-based image forgery detection, which is exactly what I need to adapt for encrypted domain. The authors proposed a three-stage pipeline: Preprocessing → Feature Extraction (multi-stream) → Feature Fusion → Detection Head. This modular view lets me swap components for encrypted-domain compatibility.

In this paper, the authors emphasized that **noise features are the backbone** of modern forgery detection. They broke down noise into four types: (1) **Camera Model Noise (PRNU)** — sensor imperfections, unique per device, (2) **Compression Noise** — JPEG quantization artifacts, DCT coefficient distributions, (3) **Processing Noise** — resampling, filtering, editing traces, (4) **DeepFake Noise** — GAN up-sampling artifacts, frequency anomalies.

Here's what they did: They surveyed 80+ deep learning papers and mapped each to their framework. The **two-stream (RGB + Noise) architecture** dominated the top performers. Noise extraction methods included: SRM filters (handcrafted), Bayesian denoising residuals, constrained convolution (Bayar layer), and self-supervised denoising (like TruFor). The fusion methods: concatenation, attention, cross-attention, bilinear pooling.

On the 2nd iteration of their analysis, they made a key observation: **methods using camera noise (PRNU) fail on images from unknown cameras or heavy compression**, while **methods using compression noise (double JPEG) fail when QF1=QF2**, but **methods using processing noise (general artifacts) generalize best** — though with lower peak accuracy. The winners (TruFor, PSCC-Net) combine multiple noise types.

They also reviewed **evaluation metrics** and standardized on: Image-level AUC/Accuracy, Pixel-level F1/IoU/MCC, and robustness to post-processing (JPEG, resize, noise, blur). They called for a **universal benchmark** — which doesn't exist yet.

**My takeaway:** This paper's **unified framework is my implementation blueprint**. For encrypted domain:
- Preprocessing → Encrypted domain normalization (if possible)
- Feature Extraction → Two streams: Encrypted Content + Encrypted Noise
- Noise Extraction → Must work in encrypted domain (homomorphic SRM? Encrypted denoising?)
- Fusion → Must be FHE/MPC compatible (avoid softmax, use polynomial approx)
- Detection Head → Simple classifier (linear + polynomial activation)

The noise taxonomy tells me: **focus on processing noise** (most generalizable) and **compression noise** (if JPEG structure preserved). PRNU is hardest in encrypted domain.

---

## Key Technical Details

| Pipeline Stage | Options | Encrypted-Domain Feasibility |
|----------------|---------|------------------------------|
| Preprocessing | Denoise, Resize, Normalize, Augment | ★★★☆☆ (Resize hard in HE) |
| Stream 1: RGB | Raw pixels, DCT, Wavelet | ★★☆☆☆ (Need raw access) |
| Stream 2: Noise | SRM, Bayes, Constrained Conv, Self-Sup Denoise | ★★★★☆ (Self-sup denoise adaptable) |
| Stream 3: Freq | DCT coeffs, FFT, Wavelet | ★★★☆☆ (DCT homomorphic in Paillier) |
| Fusion | Concat, Attention, Cross-Attn, Bilinear | ★★★☆☆ (Attention hard) |
| Head | Classification, Segmentation, Both | ★★★★★ (Simple) |

## Mathematical Core

**Unified Framework:**
```
Preprocess → [Stream_RGB, Stream_Noise, Stream_Freq] → Fusion → [Cls_Head, Seg_Head]
```

**Noise Extraction Types:**
```
PRNU:          K = (I - I_denoised) / I_denoised  (per camera)
Compression:   DCT histogram peaks at quantization steps
Processing:    Resampling → periodic correlation in freq domain
DeepFake:      Up-sampling → checkerboard artifacts in freq
```

**Fusion Methods:**
```
Concat:     F = [F_rgb; F_noise]
Attention:  F = Attn(F_rgb, F_noise)
Cross-Attn: F = CrossAttn(Q=F_rgb, K=F_noise, V=F_noise)
Bilinear:   F = F_rgb^T W F_noise
```

## Constraints & Limitations

- ❌ Framework assumes raw pixel access
- ❌ No encrypted domain discussion
- ❌ Fusion methods (attention) not FHE-friendly
- ✅ Modular design = easy to adapt components
- ✅ Noise taxonomy guides encrypted-domain feature choice
- ✅ Self-supervised denoising = path for encrypted pre-training

## Relevance to My Project

**Very High** — this is my **system architecture template**:
- Adopt the 3-stage pipeline
- Replace Stream_RGB with Encrypted_Content_Stream
- Replace Stream_Noise with Encrypted_Noise_Stream (self-sup denoiser on encrypted data)
- Use polynomial-approximated fusion (no softmax)
- Target the same metrics (AUC, F1, IoU, Robustness)

---

## Tags
#framework #unified-pipeline #noise-features #prnu #compression-noise #processing-noise #deepfake-noise #two-stream #self-supervised #architecture-template