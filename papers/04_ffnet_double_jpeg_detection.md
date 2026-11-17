# Paper 4: FF-Net — End-to-End Feature-Fusion Network for Double JPEG Detection

**Authors:** Liu, Wu, Bi, Xiao  
**Conference:** ML4CS 2022 (Proceedings of Machine Learning Research, Vol 189)  
**DOI:** proceedings.mlr.press/v189/liu23a/liu23a.pdf  

---

## My Walkthrough

I went through this paper because it's a deep learning approach specifically for **double JPEG compression detection and localization** — the same task as Comprint (Paper 2) but with a learned end-to-end network instead of handcrafted SRM+DWT features. The authors built **FF-Net** (Feature-Fusion Network) with two learned encoders instead of fixed filters.

In this paper, the authors used an **SRM encoder** (but learnable, not fixed 30 filters) and a **DWT encoder** (Haar wavelet, learned weights). The key difference from Comprint: the SRM filters are **learned from data** via backpropagation, not handcrafted. They also added **dense connections** between encoder layers and a **DWT-based feature pyramid** for multi-scale fusion.

Here's what they did: they created training pairs by taking pristine images, compressing at QF1, then recompressing at QF2 (simulating forgery). The network takes a 256×256 patch and outputs a pixel-level localization map. They tested on various QF pairs: (40,60), (50,70), (60,80), (70,90) — covering both "aligned" and "misaligned" grid scenarios.

When they compared against RRU-Net, FusionNet, and Park et al., FF-Net **consistently won** on all QF pairs for both small (512×384) and large (3008×2000) images. The dense connections and learned DWT encoder gave it better ability to distinguish subtle compression fingerprint differences.

But on the 3rd iteration of their ablation study, they noticed something critical: **removing the SRM encoder dropped performance significantly on misaligned grids**, while **removing the DWT encoder hurt aligned-grid detection**. This proved the two encoders capture complementary signals — SRM for high-frequency quantization noise, DWT for grid-structure artifacts.

They also tested generalization to **five forgery types**: copy-move, object removal, blurring, color change, object resizing. FF-Net detected and localized all of them accurately because all these operations create double-compression traces when saved as JPEG.

**My takeaway:** This is a **stronger version of Comprint** with learned features. But it has the same fundamental limitation: **JPEG only, fails when QF1=QF2**. For encrypted domain, the learned SRM filters would need to operate on encrypted data. With Paillier, we could learn encrypted-domain "SRM-like" filters homomorphically. With Arnold, the 8×8 grid is destroyed — but maybe the network could learn the permuted grid pattern if EI is fixed? The dense connection architecture is a good reference for any encrypted-domain network design.

---

## Key Technical Details

| Component | Method | Details |
|-----------|--------|---------|
| SRM Encoder | Learnable 5×5 filters | 30 filters, initialized from SRM |
| DWT Encoder | Learnable Haar wavelet | 3 levels, learned scaling |
| Fusion | Dense connections | Cross-encoder dense blocks |
| Decoder | U-Net style | Deconv + skip connections |
| Training | Simulated double JPEG | QF1 ∈ {40,50,60,70}, QF2 ∈ {60,70,80,90} |
| Loss | BCE + Dice | Pixel-level |

## Mathematical Core

**Learnable SRM:**
```
F_srm = ReLU(Conv_learned(I))  // Instead of fixed kernels
Initialized with SRM kernels, then fine-tuned
```

**Learnable DWT:**
```
LL, LH, HL, HH = DWT_learned(I)
Wavelet filters parameterized, learned end-to-end
```

**Dense Fusion:**
```
F_fused = Concat[F_srm^l, F_dwt^l] for l=1..L
         → DenseBlock → Upsample → Localization map
```

**Double JPEG Grid Detection (implicit):**
```
Grid offset = (8 - (block_start mod 8)) mod 8
Network learns to detect offset via DWT encoder
```

## Constraints & Limitations

- ❌ JPEG only (same as Comprint)
- ❌ Fails when QF1 = QF2
- ❌ Requires paired (QF1, QF2) training data
- ❌ Block-level artifacts limit pixel precision
- ✅ Learned features > handcrafted (adapts to data)
- ✅ Dense connections help gradient flow
- ✅ Generalizes to multiple forgery types

## Relevance to My Project

**Moderate** — same domain limitations as Comprint, but architecture insights valuable:
- **Dense connections** → good for encrypted-domain networks (gradient flow)
- **Dual encoder (high-freq + multi-scale)** → adapt to encrypted domain statistics
- **End-to-end training** → can train directly on encrypted data if differentiable
- **QF pair training** → analogous to multi-EI training for encrypted domain

---

## Tags
#deep-learning #double-jpeg #feature-fusion #srm #dwt #dense-connections #end-to-end #localization