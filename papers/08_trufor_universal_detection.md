# Paper 8: TruFor — All-Round Clues for Trustworthy Image Forgery Detection

**Authors:** Guillaro, Cozzolino, Sud, Dufour, Verdoliva  
**Conference:** CVPR 2023  
**DOI:** openaccess.thecvf.com/content/CVPR2023/papers/Guillaro_TruFor...  

---

## My First-Person Walkthrough

I went through this paper because it's widely considered the **current SOTA for universal image forgery detection** — it handles everything: splicing, copy-move, inpainting, DeepFake, FaceSwap, NeuralTextures, you name it. The authors proposed **TruFor**, a transformer-based framework that outputs three things: (1) image-level integrity score, (2) pixel-level localization map, and (3) a **reliability map** that tells you where the prediction might be wrong. That third output is genius for forensics — it reduces false alarms.

In this paper, the authors used a **two-stream Swin Transformer** architecture. One stream processes the **RGB image**, the other processes a **learned noise fingerprint**. The noise fingerprint is extracted via **self-supervised denoising**: they add random noise to pristine images, train a denoiser, and the residual (noisy - denoised) becomes the fingerprint. This captures camera PRNU, compression artifacts, processing traces — all without any forged training data.

Here's what they did: The two streams go through Swin Transformer blocks (shifted window attention), then fuse via **cross-attention** (RGB queries, noise keys/values). The fused features go to three heads: classification (binary), segmentation (localization), and reliability (uncertainty). The reliability head is trained to predict where the localization error exceeds a threshold.

When they tested on **7 datasets** (CASIA, Columbia, NIST16, IMDb2020, FaceForensics++, CelebDF, DFDC), TruFor **beat every baseline** on almost every metric. On IMDb2020 (in-the-wild), it got **F1 0.87** vs 0.82 for PSCC-Net and 0.78 for MantraNet. On DeepFake datasets, it matched specialized DeepFake detectors. The reliability map correctly flagged uncertain regions (homogeneous areas, heavy compression) — this is huge for courtroom evidence.

But on the 5th iteration of their experiments, they found something surprising: **training the noise fingerprint on pristine images ONLY (self-supervised) worked better than training on forged images**. The fingerprint learns "what pristine looks like" and flags deviations. This is the "anomaly detection" paradigm — no need for forged data at all for the fingerprint extractor.

They also analyzed failure cases: **heavy JPEG (QF<50)**, **extreme resizing**, and **adversarial attacks** still fool it. The reliability map drops in these regions — which is actually good behavior (it knows it's uncertain).

**My takeaway:** This is the **gold standard** for universal forgery detection. Three things I'm stealing for my project: (1) **Self-supervised noise fingerprint** — can be adapted to encrypted domain (train denoiser on encrypted pristine images), (2) **Reliability map** — essential for forensic credibility, (3) **Cross-attention fusion** — RGB + noise is a powerful pattern. The Swin Transformer is hard for encrypted domain (window attention + shifting), but the overall architecture is a perfect template.

---

## Key Technical Details

| Component | Method | Details |
|-----------|--------|---------|
| Backbone | Swin Transformer (Tiny/Small) | Shifted window attention |
| Stream 1 | RGB | Standard image input |
| Stream 2 | Noise Fingerprint | Self-supervised denoising residual |
| Fusion | Cross-Attention | RGB=Query, Noise=Key/Value |
| Head 1 | Integrity Score | Binary: pristine/forged |
| Head 2 | Localization Map | Pixel-level segmentation |
| Head 3 | Reliability Map | Uncertainty estimation |
| Training | 2-stage | 1. Fingerprint (self-sup), 2. Full (sup) |

## Mathematical Core

**Noise Fingerprint (Self-Supervised):**
```
x̃ = x + n,  n ~ N(0, σ²)
x̂ = Denoiser(x̃)
f = x̃ - x̂  // Learned noise residual = fingerprint
```

**Cross-Attention Fusion:**
```
F_rgb = SwinBlock(x)
F_noise = SwinBlock(f)
F_fused = CrossAttn(Q=F_rgb, K=F_noise, V=F_noise) + F_rgb
```

**Reliability Map:**
```
r = σ(Conv1x1(F_fused))  ∈ [0,1]
L_rel = BCE(r, 1_{|ŷ - y| < τ})  // Reliable if error < threshold
```

**Total Loss:**
```
L = L_cls + λ_loc·L_loc + λ_rel·L_rel
L_loc = BCE + Dice (pixel-level)
```

## Constraints & Limitations

- ❌ Swin Transformer complex for encrypted domain (window shift, cyclic)
- ❌ Needs some labeled data for full training (though fingerprint is self-sup)
- ❌ Heavy model (~28M params for Swin-T)
- ❌ Fails on QF<50, extreme resize, adversarial
- ✅ Universal: works on ALL forgery types
- ✅ Reliability map = forensic game-changer
- ✅ Self-supervised fingerprint = less labeled data needed
- ✅ SOTA on 7 diverse datasets

## Relevance to My Project

**Very High as architecture template**:
- **Self-supervised fingerprint** → Train on encrypted pristine images
- **Reliability map** → Must-have for encrypted forensics credibility
- **Two-stream (content + noise)** → Adapt to (encrypted_content + encrypted_noise)
- **Cross-attention** → Implementable in MPC/FHE with approximations
- **Failure analysis** → Defines my robustness test suite

---

## Tags
#transformer #universal-detection #swin #self-supervised #noise-fingerprint #reliability-map #cross-attention #cvpr2023 #sota