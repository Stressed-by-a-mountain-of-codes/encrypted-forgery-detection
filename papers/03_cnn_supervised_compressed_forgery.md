# Paper 3: Robust Forgery Detection for Compressed Images using CNN Supervision

**Authors:** Bondi et al. (referenced), Extended by authors  
**Journal:** Forensic Science International: Digital Investigation, 2020  
**DOI:** 10.1016/j.fsir.2020.100112  

---

## My Walkthrough

I went through this paper because it tackles the **real-world problem**: images on social media are almost always compressed, and most forensic methods fail on compressed images. The authors' strategy was clever — instead of building a forgery detector from scratch, they first trained a **Camera Model Identification (CMI) network** (called CNNm), then transferred it to forgery detection.

In this paper, the authors used a **CNN trained to identify which camera model took a photo**. The idea: authentic images come from one camera; forged images (splicing) combine patches from different cameras. So if a region has a different camera fingerprint, it's forged. They trained CNNm on the Dresden dataset (73 camera models) and then fine-tuned it for forgery detection.

Here's what they did step by step: First, they constructed forged images by pasting patches from different camera models onto pristine images. Then they trained CNNm to classify camera models. The key innovation: **multi-QF training**. They didn't just train on original quality images — they trained on QF 70, 80, 90, and 100 simultaneously. This forced the network to learn compression-invariant camera fingerprints.

When they tested on "Known" cameras (seen during training) vs "Unknown" cameras (unseen), the results were striking. At QF=90, Bondi et al.'s method got 0.56 accuracy while their CNNm got **0.72**. At QF=80: 0.52 vs **0.65**. At QF=70: 0.52 vs **0.61**. The gap widened as compression increased — their method was **robust to compression** while the baseline collapsed.

What this proves: **Camera model identification features are more compression-robust than handcrafted forensic features**. The CNN learns to ignore compression artifacts and focus on sensor-pattern noise (PRNU) which survives compression better.

But on the 5th iteration of their experiments, they noticed something: **fine-tuning all layers** worked better than freezing early layers. They tried freezing the first 4 conv layers (transfer learning style) but the fully fine-tuned model outperformed it. This suggests the camera fingerprint features need adaptation for the forgery task.

They also tested on "Unknown" cameras (not in training set) and still beat the baseline: QF=90: 0.56 vs 0.63; QF=80: 0.52 vs 0.57. This shows **generalization to unseen cameras**.

**My takeaway:** This is a **transfer learning approach** that could work in encrypted domain IF we can compute camera fingerprints in encrypted domain. But CNNm needs raw pixel access for PRNU extraction. With Paillier, we could potentially compute the noise residual homomorphically. With Arnold permutation, the spatial PRNU pattern is scrambled — might still work if the permutation is known (since PRNU is multiplicative noise). The multi-QF training strategy is directly applicable: train encrypted-domain detector on multiple encryption intensities (EI).

---

## Key Technical Details

| Component | Method | Details |
|-----------|--------|---------|
| Backbone | Custom CNN (CNNm) | 5 conv layers + FC |
| Pre-training | Camera Model ID | 73 models, Dresden dataset |
| Fine-tuning | Forgery detection | Binary: pristine vs forged |
| Training QFs | 70, 80, 90, 100 | Multi-QF data augmentation |
| Forgery Type | Splicing (cross-camera) | Patch pasting |

## Mathematical Core

**Camera Model Identification:**
```
P(camera | I) = Softmax(CNNm(I))
Loss_CMI = -Σ y_c log(P(c|I))
```

**Forgery Detection Score:**
```
For each region R: score(R) = 1 - max_c P(camera_c | R)
Forged if score(R) > τ
```

**Multi-QF Training:**
```
I_QF = JPEG_Compress(I, QF)  for QF ∈ {70, 80, 90, 100}
Loss_total = Σ_{QF} Loss_CMI(I_QF) + λ·Loss_forgery(I_QF)
```

**PRNU Model (what CNNm implicitly learns):**
```
I = I_ideal + I_ideal ⊙ K + noise
K = sensor pattern noise (PRNU) — unique per camera
```

## Constraints & Limitations

- ❌ Requires camera model labels for pre-training
- ❌ Assumes forgery = different camera source (fails for copy-move, same-camera splicing)
- ❌ Performance drops at QF < 70
- ❌ Needs raw pixel access for PRNU — hard in encrypted domain
- ✅ Multi-QF training is a great strategy for domain robustness
- ✅ Transfer learning from related task (CMI) works well

## Relevance to My Project

**Low-Moderate** for encrypted domain:
- **Arnold**: PRNU pattern scrambled but deterministic — might recover if EI known
- **Paillier**: Can compute noise residual homomorphically (expensive)
- **Selective encryption**: LSBs may preserve PRNU
- **Key insight**: Multi-condition training (multi-EI, multi-QF) directly applicable

---

## Tags
#deep-learning #transfer-learning #camera-model-id #prnu #compression-robust #multi-qf-training #cnn