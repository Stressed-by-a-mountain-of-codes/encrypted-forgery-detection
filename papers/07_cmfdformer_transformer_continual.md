# Paper 7: CMFDFormer — Transformer-based Copy-Move Detection with Continual Learning

**Authors:** Multiple  
**Preprint:** arXiv:2311.13263v2, 2023  

---

## My  Walkthrough

I went through this paper because it introduces **Transformers to copy-move forgery detection (CMFD)** and solves a critical problem: **continual learning** — the ability to learn new forgery types without forgetting old ones. Most deep CMFD methods are trained on synthetic data and fail on new manipulation types. The authors proposed **CMFDFormer** with a **PCSD (Pooled Cube and Strip Distillation) continual learning framework**.

In this paper, the authors used **MiT (Mix Transformer)** as the backbone — a hierarchical vision transformer with overlapping patch embeddings and efficient self-attention (reduction ratio R=8). The decoder is **PHD (Pluggable Hybrid Decoder)** which uses MLPs to fuse multi-level features. But the real innovation is PCSD for continual learning.

Here's what they did: They trained CMFDFormer on Task 1 (e.g., copy-move with rotation), then Task 2 (e.g., copy-move with scaling), then Task 3 (e.g., JPEG compression). Normally, the network would catastrophically forget Task 1 when learning Task 3. But PCSD prevents this by distilling knowledge from the old model into the new one using two complementary strategies: **Pooled Cube Distillation** (3D feature cube pooling across channels/spatial) and **Strip Distillation** (1D strip sampling for efficiency).

When they tested on CASIA, CoMoFoD, and GRIP datasets across 5 continual learning tasks, CMFDFormer with PCSD maintained **>90% F1 on all previous tasks** while learning new ones. Without PCSD, F1 dropped to 60-70% on old tasks. The MiT backbone outperformed CNN (ResNet) and MLP backbones — Transformers' global attention captures copy-move's long-range dependencies better.

On the 2nd iteration of their analysis, they visualized the attention maps: **early layers attend to local texture, middle layers to repeated patterns, late layers to global copy-move pairs**. This explains why Transformers excel at CMFD — the self-attention naturally finds matching regions across the image.

But they noticed a limitation: **PCSD needs a small replay buffer** (exemplars from old tasks) for best performance. Pure distillation without replay loses ~2% F1. Also, the MiT-B2 backbone has 27M parameters — not lightweight.

**My takeaway:** This is the **first continual learning paper in CMFD** — huge for real-world deployment where new forgery types emerge constantly. For encrypted domain, the Transformer architecture is challenging (attention is quadratic, hard in FHE/MPC), but the **continual learning framework (PCSD) is directly applicable** — I can use it to train on multiple encryption schemes (Arnold EI=1, then EI=2, then Paillier) without forgetting. The strip distillation is efficient enough for encrypted-domain training.

---

## Key Technical Details

| Component | Method | Details |
|-----------|--------|---------|
| Backbone | MiT (Mix Transformer) | B0-B5 variants, overlapping patch embed |
| Attention | Efficient Self-Attention | Reduction ratio R=8 (pooling K,V) |
| Decoder | PHD (Pluggable Hybrid Decoder) | MLP fusion + upsample |
| Continual Learning | PCSD | Pooled Cube + Strip Distillation |
| Tasks | 5 CMFD variants | Rotation, scaling, JPEG, blur, noise |

## Mathematical Core

**MiT Efficient Attention:**
```
X ∈ ℝ^{H×W×C} → PatchEmbed → ℝ^{N×C}
Q = X W_q, K = Pool(X) W_k, V = Pool(X) W_v  (Pool reduces N by R)
Attn = Softmax(QK^T / √d) V
```

**PCSD Distillation Loss:**
```
L_KD = Σ_l ||Pool3D(f_old^l) - Pool3D(f_new^l)||_F^2   // Pooled Cube
     + Σ_l ||Strip(f_old^l) - Strip(f_new^l)||_F^2     // Strip
L_total = L_seg + λ·L_KD
```

**Strip Sampling:**
```
Strip(f) = f[:, ::s, :]  // Strided sampling along spatial dim
```

## Constraints & Limitations

- ❌ Transformer attention = O(N²) — hard in encrypted domain
- ❌ Needs replay buffer for best continual learning
- ❌ 27M params (MiT-B2) — not lightweight
- ❌ Only copy-move, not splicing/inpainting
- ✅ First continual learning in CMFD
- ✅ PCSD framework transferable to other domains
- ✅ MiT attention naturally finds copy-move pairs

## Relevance to My Project

**High for continual learning framework, Low for architecture**:
- **PCSD distillation** → directly usable for multi-encryption training
- **Strip distillation** → efficient, works with encrypted features
- **Task definition** → each encryption scheme = a "task"
- **Transformer** → hard in FHE/MPC; consider CNN alternative

---

## Tags
#transformer #continual-learning #cmfd #mit #pcsd #distillation #copy-move #catastrophic-forgetting