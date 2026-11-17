# Paper 9: Survey on Deep Learning-based Image Forgery Detection (2023)

**Authors:** Mehrjardi, Latif, Zarchi, Sheikhpour  
**Journal:** Pattern Recognition, Vol 144, 109778, 2023  
**DOI:** 10.1016/j.patcog.2023.109778  

---

## My Walkthrough

I went through this survey because it's the most **comprehensive deep learning forgery detection survey** I've found — 156 references, covering every architecture type (CNN, RNN, Transformer, GAN, Two-Stream, Self-Supervised) and every forgery type (copy-move, splicing, inpainting, DeepFake). The authors organized it by **architecture strategy** and **learning paradigm**, not just by forgery type.

In this paper, the authors created a **taxonomy table** that I found incredibly useful. They categorize methods by: (1) **Architecture**: CNN (VGG, ResNet, U-Net, FPN), RNN/LSTM, Transformer (ViT, Swin, MiT), GAN-based, Two-Stream (RGB+Noise, RGB+SRM, RGB+DCT), Self-Supervised. (2) **Training Strategy**: Supervised, Self-Supervised (pretext tasks), Contrastive, Domain Adaptation. (3) **Forgery Type**: Single-type (CMFD only, Splicing only) vs Generic (all types).

What I noticed on my 3rd read: they included a **performance comparison table** (their Table 2) with actual numbers across methods. TruFor (Swin-T) leads with CMFD F1 0.92, Splicing F1 0.89, Inpainting F1 0.85, Generic F1 0.87. PSCC-Net (ResNet50) is close: 0.89, 0.85, 0.78, 0.82. Comprint+Noiseprint (traditional) lags at 0.71, 0.68, 0.62, 0.67. This confirms **Transformers > CNNs > Traditional** for generic detection.

They also analyzed **training strategies in depth**:
- **Supervised**: Needs pixel-level masks (expensive)
- **Self-Supervised**: Pretext tasks like noise extraction, JPEG artifact prediction, masked autoencoding — then fine-tune on small labeled set
- **Contrastive**: Pull pristine patches together, push forged apart in feature space
- **Domain Adaptation**: Synthetic → Real (MMD loss, adversarial)

On the 2nd iteration of their benchmark analysis, they highlighted a critical issue: **most methods are evaluated on synthetic datasets** (CASIA, CoMoFoD) but **fail on in-the-wild data** (IMDb2020). The domain gap is real. They recommend: (1) More realistic datasets, (2) Self-supervised pre-training on real data, (3) Domain adaptation techniques.

**My takeaway:** This survey is my **deep learning architecture menu**. For encrypted domain, I need to pick an architecture that's **FHE/MPC-friendly**. From their taxonomy: CNNs are easiest (linear ops + ReLU), Transformers are hardest (attention = quadratic, softmax). Two-stream (RGB+Noise) is promising because noise stream might be computable in encrypted domain. Self-supervised pre-training on encrypted pristine data is a must — no labeled encrypted forgeries exist.

The survey's **Table 2 (performance comparison)** is my benchmark target. If I can get TruFor-level performance in encrypted domain, that's a breakthrough.

---

## Key Technical Details

| Architecture | Key Variants | Forgery Types | Encrypted-Domain Feasibility |
|--------------|--------------|---------------|------------------------------|
| CNN | ResNet, U-Net, FPN, DenseNet | All | ★★★★★ (Linear + ReLU) |
| RNN/LSTM | Bi-LSTM, ConvLSTM | Video, Splicing | ★★★☆☆ (Sequential) |
| Transformer | ViT, Swin, MiT, PSCC-Net | Splicing, CMFD | ★★☆☆☆ (Attention, Softmax) |
| GAN | GANomaly, AnoGAN | Inpainting, DeepFake | ★★☆☆☆ (Adversarial) |
| Two-Stream | RGB+Noise, RGB+SRM, RGB+DCT | All | ★★★★☆ (Parallel streams) |
| Self-Supervised | MAE, Contrastive, Denoising | Generic | ★★★★★ (No labels needed) |

## Mathematical Core

**Contrastive Learning:**
```
L_contrast = -log( exp(sim(z_i, z_j)/τ) / Σ_k exp(sim(z_i, z_k)/τ) )
z = Projector(Encoder(x))
```

**Domain Adaptation (MMD + Adversarial):**
```
L_total = L_source + λ·MMD(f_source, f_target) + μ·L_adv
MMD² = ||E[φ(f_s)] - E[φ(f_t)]||²_H
```

**Self-Supervised Pretext (Denoising):**
```
x̃ = x + n
x̂ = Decoder(Encoder(x̃))
L_pretext = ||x - x̂||²
```

## Constraints & Limitations (of Surveyed Field)

- ❌ Domain gap: synthetic train → real test
- ❌ Pixel-level annotations scarce
- ❌ No encrypted domain coverage
- ❌ Transformer dominance = hard for FHE/MPC
- ✅ Comprehensive taxonomy and benchmarks
- ✅ Self-supervised = path forward for encrypted domain
- ✅ Two-stream architecture = modular, adaptable

## Relevance to My Project

**Very High** — this is my **architecture selection guide**:
- Choose **CNN + Two-Stream** for encrypted domain feasibility
- Use **Self-Supervised pre-training** on encrypted pristine data
- Target **TruFor-level performance** (Generic F1 0.87)
- Apply **Domain Adaptation** for encryption intensity gaps

---

## Tags
#survey #deep-learning #taxonomy #architecture-comparison #training-strategies #self-supervised #contrastive #domain-adaptation #benchmark