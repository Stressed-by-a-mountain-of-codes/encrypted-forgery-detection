# Paper 6: MFAF-Net — Multi-Scale Feature Attention Fusion for Image Splicing Detection

**Authors:** Multiple  
**Journal:** ACM Transactions on Multimedia Computing, Communications, and Applications (TOMM), 2024  
**DOI:** 10.1145/3698770  

---

## My Walkthrough

I went through this paper because it's a **state-of-the-art CNN + Attention** method for splicing detection, and I wanted to understand how modern attention mechanisms improve forgery localization. The authors proposed **MFAF-Net** (Multi-scale Feature Attention Fusion Network) which uses a Feature Pyramid Network (FPN) backbone with three attention modules.

In this paper, the authors used a **ResNet-50 / EfficientNet backbone** with FPN to extract multi-scale features (P3, P4, P5 corresponding to 1/8, 1/16, 1/32 scale). Then they applied three attention mechanisms in sequence: **Channel Attention (SE-block)**, **Spatial Attention (CBAM-style)**, and **Cross-Scale Attention** (transformer-style attention across pyramid levels).

Here's what they did: The channel attention learns which feature channels are most forensic-relevant (e.g., high-frequency noise channels). The spatial attention highlights suspicious regions (boundaries, inconsistencies). The cross-scale attention lets coarse semantic features guide fine-grained localization — this is the key innovation. They fuse all three attended features and decode to a pixel-level mask.

When they tested on four benchmarks (CASIA, Columbia, NIST16, In-the-wild), MFAF-Net achieved **SOTA performance**. But what impressed me more was the **robustness testing**: they attacked images with JPEG QF 70-95, Gaussian noise σ=5-20, resize 0.5×-2×, and MFAF-Net maintained performance while baselines (PSCC-Net, MantraNet, TruFor) degraded significantly.

On the 4th iteration of their ablation, they removed each attention module: **Cross-scale attention contributed the most** (+3.2% F1), followed by spatial (+2.1%), then channel (+1.4%). This proves that **multi-scale interaction is critical** for splicing detection — spliced boundaries appear at different scales.

They also analyzed failure cases: **heavy JPEG (QF<70)** and **large homogeneous regions** (sky, walls) still cause false positives. The attention maps show the network focuses on edges and texture boundaries — makes sense since splicing leaves traces at boundaries.

**My takeaway:** This is a **strong supervised deep learning baseline** for splicing. The attention fusion architecture is directly applicable to encrypted domain IF we can compute attention in encrypted domain. With FHE (CKKS), we could do approximate attention. With MPC (secret sharing), we could do secure attention. The multi-scale pyramid + cross-scale attention is a great architecture template. But the supervised requirement (pixel-level masks) is a bottleneck — encrypted domain data labeling is hard.

---

## Key Technical Details

| Component | Method | Details |
|-----------|--------|---------|
| Backbone | ResNet-50 / EfficientNet-B3 | Pre-trained on ImageNet |
| Neck | FPN | P3(1/8), P4(1/16), P5(1/32) |
| Attention 1 | Channel (SE) | GlobalAvgPool → FC → ReLU → FC → Sigmoid |
| Attention 2 | Spatial (CBAM) | Conv7×7([AvgPool; MaxPool]) → Sigmoid |
| Attention 3 | Cross-Scale | Transformer attention across P3,P4,P5 |
| Decoder | Upsample + Conv | 4× upsampling to original resolution |
| Loss | BCE + Dice + IoU | λ₁=1, λ₂=1, λ₃=0.5 |

## Mathematical Core

**Channel Attention:**
```
z_c = σ(FC₂(ReLU(FC₁(GAP(F)))))  ∈ ℝ^C
F' = F ⊗ z_c  (channel-wise multiply)
```

**Spatial Attention:**
```
M_s = σ(Conv7×7([AvgPool(F); MaxPool(F)]))  ∈ ℝ^{H×W}
F'' = F' ⊗ M_s  (spatial multiply)
```

**Cross-Scale Attention:**
```
Q_i = W_q P_i, K_j = W_k P_j, V_j = W_v P_j
A_{i→j} = Softmax(Q_i K_j^T / √d) V_j
F_fused = Σ_j A_{i→j} + P_i
```

**Total Loss:**
```
L = L_BCE + λ₁ L_Dice + λ₂ L_IoU
L_Dice = 1 - 2|Y∩Ŷ| / (|Y| + |Ŷ|)
L_IoU = 1 - |Y∩Ŷ| / |Y∪Ŷ|
```

## Constraints & Limitations

- ❌ Requires pixel-level ground truth masks (expensive to annotate)
- ❌ Supervised only — no self-supervised variant
- ❌ Heavy model (ResNet-50 + FPN + 3 attention modules)
- ❌ Fails on heavy compression (QF<70) and homogeneous regions
- ✅ SOTA on standard benchmarks
- ✅ Robust to moderate attacks
- ✅ Attention maps are interpretable

## Relevance to My Project

**Moderate-High as architecture reference**:
- **Multi-scale pyramid** → good for encrypted domain (different encryption effects at different scales)
- **Cross-scale attention** → adaptable to MPC/FHE
- **Interpretability** → attention maps show where network looks (useful for debugging encrypted nets)
- **Robustness testing protocol** → directly usable for my evaluation

---

## Tags
#deep-learning #splicing #attention #multi-scale #fpn #cross-scale-attention #channel-attention #spatial-attention #robustness