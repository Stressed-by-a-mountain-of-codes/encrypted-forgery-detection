# Paper 15: Selective Encryption for Forensics-Privacy Trade-off

**Authors:** Puteaux, Itier, Bas  
**Preprint:** arXiv:2103.03569, 2021  

---

## My First-Person Walkthrough

I went through this paper because it explores a fundamentally different approach to encrypted-domain forensics: **Selective Encryption** (bit-plane encryption) instead of full homomorphic encryption. This is much faster and doesn't expand data size, but creates a privacy-forensics trade-off that the authors quantitatively analyze.

In this paper, the authors proposed encrypting only the **Most Significant Bit-planes (MSBs)** of an image while keeping the **Least Significant Bit-planes (LSBs) in clear**. The idea: MSBs contain visual content (privacy-sensitive), LSBs contain noise/residuals (forensic-relevant). They used **SRMQ1 features** extracted from the clear LSBs to detect tampering, and measured privacy via **recognizability** (CNN classification accuracy on encrypted image).

Here's what they did: For an 8-bit image, they decomposed into 8 bit-planes (b₀ LSB to b₇ MSB). They encrypted bit-planes k = s, s+1, ..., 7 (where s is the security level, 0-8). The remaining LSBs (0 to s-1) stay in clear. They extracted SRMQ1 features from the clear portion: compute residuals via predictor, model with Gaussian Mixture, extract moments → feature vector → SVM classifier for tampering detection.

When they varied s (number of encrypted MSBs): **s=0 (no encryption): Forensics 100%, Privacy 0% (fully recognizable). s=2: Forensics 95%, Privacy 60% recognizable. s=4: Forensics 80%, Privacy 25%. s=6: Forensics 50%, Privacy 10%. s=8 (full encryption): Forensics ~10% (random), Privacy 0% (unrecognizable).**

On the 2nd iteration of their analysis, they compared with **homomorphic encryption (Paillier)**: HE gives full privacy + full computability but is computationally intensive and expands data. Selective encryption is fast, no expansion, but partial privacy and partial forensics. **There's a fundamental trade-off curve** — you can't have both perfect privacy and perfect forensics with selective encryption.

They also noted: **Selective encryption ≠ Homomorphic encryption**. Selective encryption reveals LSBs which may leak information (e.g., if LSBs contain steganographic data). But for many forensic tasks (noise analysis, compression artifacts), LSBs are sufficient.

**My takeaway:** This paper defines the **privacy-forensics trade-off space**. For my project, selective encryption could be a **practical middle ground**: encrypt MSBs with AES (fast, standard), keep LSBs clear for forensic analysis. Or **hybrid**: MSBs with AES, LSBs with Paillier (for homomorphic forensic ops on noise). The SRMQ1-on-LSBs approach is a concrete method I can test. The recognizability metric (CNN classification on encrypted) is a good privacy quantification I should adopt.

---

## Key Technical Details

| Component | Method | Details |
|-----------|--------|---------|
| Encryption | Selective (Bit-plane) | Encrypt MSBs k≥s, keep LSBs k<s clear |
| Bit-planes | 8-bit decomposition | I = Σ b_k·2^k, b₇=MSB, b₀=LSB |
| Forensics | SRMQ1 on clear LSBs | Residuals → GMM → Moments → SVM |
| Privacy Metric | Recognizability | CNN classification accuracy on encrypted |
| Security Levels | s = 0 to 8 | s=0: none, s=8: full |

## Mathematical Core

**Bit-Plane Decomposition:**
```
I(x,y) = Σ_{k=0}^7 b_k(x,y) · 2^k
b_k ∈ {0,1}
```

**Selective Encryption:**
```
Encrypted: b_k for k = s, s+1, ..., 7  (AES/Chaotic)
Clear:     b_k for k = 0, 1, ..., s-1
```

**SRMQ1 Features (on clear portion):**
```
1. Residual: R = I_clear - Predictor(I_clear)
2. GMM: R ~ Σ π_i N(μ_i, Σ_i)
3. Features: Moments of GMM components
4. Classifier: SVM(RBF) → Tampered/Intact
```

**Privacy (Recognizability):**
```
Privacy = 1 - CNN_Class(SelectiveEncrypted(I))
Lower recognizability = Better privacy
```

**Trade-off Curve:**
```
s (encrypted MSBs) ↑ → Forensics Accuracy ↓, Privacy ↑
Fundamental limit: Cannot maximize both simultaneously
```

## Constraints & Limitations

- ❌ **Partial privacy** — LSBs may leak information
- ❌ **Partial forensics** — Only LSB-based features usable
- ❌ **Not composable** with homomorphic encryption
- ❌ **SRMQ1 limited** to noise-based forgeries
- ✅ **Fast** (AES/chaotic on MSBs only)
- ✅ **No size expansion**
- ✅ **Quantitative trade-off analysis**
- ✅ **Practical for cloud scenarios**

## Relevance to My Project

**High for hybrid approach design**:
- **Selective + Homomorphic hybrid**: MSBs=AES, LSBs=Paillier
- **Privacy metric (recognizability)** → adopt for my evaluation
- **LSB forensics** → noise features survivable in encrypted domain
- **Trade-off curve** → defines my design space

---

## Tags
#selective-encryption #bit-plane #privacy-forensics-tradeoff #srmq1 #recognizability #hybrid-encryption #practical #arxiv-2021