# Paper 1: Copy-Move Forgery Detection via Evolving Circular Domains Coverage (ECDC)

**Authors:** Wang et al.  
**Journal:** Multimedia Tools and Applications, 2022  
**DOI:** 10.1007/s11042-022-12755-w  

---

## My Walkthrough

I went through this paper because it's one of the most cited recent hybrid approaches for copy-move forgery detection (CMFD), combining both block-based and keypoint-based methods. The authors wanted to improve detection accuracy and achieve precise localization of forged regions.

In this paper, the authors used **SURF features in log-polar space** combined with **SIFT descriptors** extracted from the entire image. They did this because SIFT gives good scale/rotation invariance but is slow, while SURF in log-polar adds rotation invariance more efficiently. They got a massive set of matched pairs using **generalized 2-Nearest Neighbor (g2NN)** matching, which finds the two closest features for each keypoint.

Then they applied **RANSAC** to filter out mismatched pairs — this gave them rough localization of counterfeit areas. But here's where it gets interesting: they noticed the RANSAC output was still too coarse, so they developed the **ECDC (Evolving Circular Domains Coverage) algorithm**. 

The ECDC algorithm works like this: for each matched pair, they initialize a circular domain centered on that pair with a small radius. Then they iteratively expand/contract the domain based on block feature similarity within the domain. They kept doing this until convergence — the domain stops growing when the boundary pixels no longer match the interior statistics. On the final iteration, the domain precisely covers the forged region.

They tested this on CASIA v1 (null subset, 48 images) and got **Precision 92.61%, Recall 91.48%, F1 91.56%** — beating all compared methods including DCT, PCET, SIFT, SURF, and their combinations. Under geometric attacks (rotation, scaling), their method maintained the highest F1.

What this proves: the hybrid approach (keypoint for candidate generation + block-based for precise localization) works better than either alone. The ECDC's adaptive domain evolution is the key innovation — it doesn't need a fixed threshold like traditional block methods.

When they increased the initial radius, coverage became more comprehensive but introduced more false positives. When they decreased it, they missed parts of the forged region. The sweet spot was around radius 8-12 pixels for 256×256 images.

**My takeaway:** This is a solid classical method, but it's computationally heavy (SIFT + SURF + RANSAC + iterative ECDC). For encrypted domain work, the keypoint extraction would fail completely after encryption since spatial relationships are destroyed. But the block-based evolution idea might be adaptable if we can compute block statistics in encrypted domain (e.g., via Paillier homomorphic operations).

---

## Key Technical Details

| Component | Method | Parameters |
|-----------|--------|------------|
| Keypoint | SURF (log-polar) + SIFT | Hessian threshold 400 |
| Matching | g2NN | k=2, ratio test 0.7 |
| Filtering | RANSAC | Inlier threshold 3px, 2000 iterations |
| Localization | ECDC | Initial radius 10, max 50 iterations |
| Refinement | Morphological | Close (3×3), Open (3×3) |

## Mathematical Core

**ECDC Iteration:**
```
Domain D_i^(t) = {p : ||p - center_i|| < r_i^(t)}
Feature stats: μ_i^(t) = mean(block_features in D_i^(t))
Boundary test: for p ∈ ∂D_i^(t), if |feat(p) - μ_i^(t)| < τ → include
Radius update: r_i^(t+1) = r_i^(t) + α·(|included| - |excluded|)
Convergence: |r_i^(t+1) - r_i^(t)| < ε
```

## Constraints & Limitations

- ❌ Fails under heavy JPEG compression (QF < 70)
- ❌ High computational cost (~5-10s per image on CPU)
- ❌ Requires parameter tuning (initial radius, τ, α, ε)
- ❌ Keypoints destroyed by encryption → not usable in encrypted domain directly
- ✅ Good baseline for hybrid approach philosophy

## Relevance to My Project

**Low direct applicability** to encrypted domain (keypoints need spatial coherence). But the **block-based evolution concept** could inspire encrypted-domain block statistics comparison if we use homomorphic encryption for block DCT/mean/variance.

---

## Tags
#classical #copy-move #hybrid #ecdc #sift #surf #ransac #block-based #keypoint-based