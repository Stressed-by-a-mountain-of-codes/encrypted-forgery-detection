# Paper 12: PP-JPEG — Privacy-Preserving JPEG Tampering Localization with Paillier

**Authors:** Jena, Singh, Mohanty  
**Journal:** Journal of Imaging, 2023, 9(9), 172  
**DOI:** 10.3390/jimaging9090172  
**PMCID:** PMC10532548  

---

## My Walkthrough

I went through this paper because it's one of the **only papers that actually implements forgery detection in the encrypted domain using homomorphic encryption (Paillier)**. This is directly relevant to my project — it uses Paillier's additive homomorphism to compute DCT and analyze compression artifacts on ciphertexts.

In this paper, the authors proposed **PP-JPEG**, a framework where the image owner encrypts a JPEG image with Paillier, sends it to the cloud, and the cloud detects tampering **without ever decrypting**. The key insight: **double JPEG compression leaves different quantization artifacts in authentic vs forged regions**, and these artifacts can be detected via **energy analysis of DCT coefficients** — all computable homomorphically.

Here's what they did: The image owner generates Paillier keys, encrypts each pixel (or DCT coefficient), uploads ciphertexts. The cloud computes **encrypted DCT** on 8×8 blocks using Paillier's homomorphic properties: `E(Σ a_i·x_i) = Π E(x_i)^{a_i}`. Then for each possible JPEG quality factor QF, they compute the **energy graph**: `E(QF) = Σ|DCT_coeff(QF)|²`. The **first minimum** in this energy graph corresponds to the original (featured) image's QF. If a region has a different QF (dummy image), its energy minimum appears elsewhere — that's the tampered region.

They tested on copy-move forgeries with different QF combinations. **When featured QF ≠ dummy QF, detection rate was high (~90%+). When QF1 = QF2, detection failed completely** — the energy graphs are identical. This is a fundamental limitation of double-JPEG-based detection.

On the 2nd iteration of their experiments, they tested **same camera vs different camera** for the featured/dummy images — **no significant difference**. The detection depends purely on QF mismatch, not camera fingerprint. They also tested block sizes down to 8×8 (single DCT block) and it still worked.

But the **computational cost is massive**: Paillier encrypts each pixel to a ~2048-bit ciphertext. An 8×8 block DCT requires 64 homomorphic multiplications and additions per coefficient. For a 512×512 image, that's 4096 blocks × 64 coeffs × ~100 ops = ~26 million homomorphic ops per image. **Hours per image on CPU.** They acknowledge this and suggest multi-CPU parallelization.

**My takeaway:** This proves **Paillier-based encrypted-domain forensics is possible** but **computationally impractical** for real use. The double-JPEG energy analysis is clever but limited to JPEG and QF mismatch. For my project, I need to consider: (1) Can I use **CKKS (approximate FHE)** for faster batched DCT? (2) Can I use **selective encryption + Paillier only on forensic regions**? (3) The **energy graph / first minima concept** is a great forensic feature I can adapt.

---

## Key Technical Details

| Component | Method | Details |
|-----------|--------|---------|
| Encryption | Paillier (Additive HE) | 2048-bit key, per-pixel encryption |
| Homomorphic Op | DCT on ciphertexts | E(Σ a_i·x_i) = Π E(x_i)^{a_i} |
| Forensic Feature | Energy Graph | E(QF) = Σ|DCT(QF)|² |
| QF Estimation | First Minima | QF* = argmin_{local} E(QF) |
| Tampering Detection | Block-wise QF comparison | |E_block(QF*) - E_global(QF*)| > τ |
| Forgery Type | Copy-move (JPEG) | Double compression scenario |

## Mathematical Core

**Paillier Cryptosystem:**
```
KeyGen: n=pq, λ=lcm(p-1,q-1), g∈Z*_{n²}, μ=(L(g^λ mod n²))⁻¹
Encrypt:  c = g^m · r^n mod n²
Decrypt:  m = L(c^λ mod n²) · μ mod n
Add:      E(m1) · E(m2) = E(m1+m2 mod n)
ScalarMul: E(m)^k = E(k·m mod n)
```

**Homomorphic DCT (8×8 block):**
```
DCT_{u,v} = Σ_{x=0}^7 Σ_{y=0}^7 c_{x,y} · w_{u,v}(x,y)
w = cos((2x+1)uπ/16) · cos((2y+1)vπ/16)  (plaintext weights)
c_{x,y} = E(I[x,y])  (ciphertext pixels)
Compute via: Π c_{x,y}^{w_{u,v}(x,y)}  (scalar mult + multiplication)
```

**Energy Graph:**
```
E(QF) = Σ_{u,v} |DCT_{u,v}(QF)|²
QF* = first local minimum of E(QF)
```

**Tampering Localization:**
```
For each block b:
  if |E_b(QF*) - E_global(QF*)| > τ → Tampered
```

## Constraints & Limitations

- ❌ **JPEG only** — relies on double quantization
- ❌ **Fails when QF1 = QF2** (fundamental)
- ❌ **Extreme computational cost** (hours/image)
- ❌ **Ciphertext expansion** ~2048× per pixel
- ❌ **Block-level (8×8) only**, not pixel-level
- ✅ **First working Paillier forensics implementation**
- ✅ **Proves homomorphic DCT + energy analysis works**
- ✅ **Privacy-preserving: cloud never sees plaintext**

## Relevance to My Project

**High — Direct encrypted-domain forensics with HE**:
- Paillier DCT → my baseline for homomorphic forensics
- Energy graph → forensic feature to adapt
- QF mismatch limitation → defines my scope
- Computational cost → motivates CKKS/MPC/hybrid approaches

---

## Tags
#encrypted-domain #paillier #homomorphic-encryption #jpeg #double-compression #energy-graph #dct #privacy-preserving #computational-cost