# Paper 13: Robust Image Hashing in Encrypted Domain with Paillier + HVS

**Authors:** Qin, Guo, Li, Qian, Zhang  
**Journal:** Journal of Software (Chinese), 2023, 34(2), 868-883  
**DOI:** 10.13328/j.cnki.jos.006419  

---

## My Walkthrough

I went through this paper because it addresses a different encrypted-domain problem: **perceptual hashing for integrity verification** rather than forgery localization. The authors propose a **three-party protocol** (Owner → Cloud → Receiver) where the cloud computes a hash on encrypted images using Paillier homomorphic encryption, incorporating **Human Visual System (HVS) weighting** via Watson's model.

In this paper, the authors used a **three-stage pipeline**: (1) Owner encrypts image with Paillier, uploads to cloud. (2) Cloud computes **encrypted DCT**, applies **Watson HVS weights** (plaintext, public), multiplies by **key-controlled pseudo-random matrix** for security, outputs ciphertext hash. (3) Receiver decrypts hash, compares with locally computed hash from plaintext.

Here's what they did step by step: The image is converted to grayscale (0.2989R + 0.5870G + 0.1140B), resized to M×M. Each pixel encrypted with Paillier: `c = g^m · r^n mod n²`. The cloud computes 8×8 block DCT homomorphically using Paillier's additive property. Then applies Watson weights: `F_{u,v} = DCT_{u,v}^{W_{u,v}}` (scalar multiplication in encrypted domain). Then applies pseudo-random ±1 matrix: `H_{u,v} = F_{u,v}^{R_{u,v}}` (sign flip). The final hash is the set of selected frequency coefficients.

When they tested robustness: **JPEG QF≥50, Gaussian noise σ≤10, rotation ≤2°** — all passed (hash distance below threshold). **Uniqueness**: Different images → hash distance >> threshold. **Security**: Ciphertext indistinguishable from random (Paillier semantic security + PR matrix).

On the 2nd iteration of their security analysis, they realized the **pseudo-random matrix is critical** — without it, an attacker could reverse-engineer the DCT coefficients from the hash. The key-controlled matrix adds a secret permutation that only the owner knows.

But the limitations are clear: **Authentication only (not localization)** — you know *if* the image was tampered, not *where*. **Paillier overhead** — large ciphertexts, slow computation. **Fixed 8×8 DCT** — not adaptive. **Trusted key management** required.

**My takeaway:** This is a **complementary approach** to PP-JPEG (Paper 12). PP-JPEG does localization (where), this does authentication (whether). Both use Paillier + DCT. For my project, I could combine them: use robust hash for quick integrity check, then PP-JPEG-style analysis for localization if tampered. The HVS weighting (Watson model) is a great idea — it makes the hash robust to perceptual-equivalent changes. In encrypted domain, Watson weights are plaintext (public), so homomorphic scalar multiplication works perfectly.

---

## Key Technical Details

| Component | Method | Details |
|-----------|--------|---------|
| Encryption | Paillier (Additive HE) | Per-pixel encryption |
| Preprocessing | Grayscale + Resize | 0.2989R+0.5870G+0.1140B → M×M |
| Feature | Encrypted DCT (8×8) | Homomorphic via Paillier add/scalar-mul |
| HVS Weighting | Watson Model | Perceptual importance per frequency |
| Security | PR Matrix (±1) | Key-controlled, sign flip in encrypted domain |
| Output | Ciphertext Hash | Decrypted by receiver for comparison |
| Task | Authentication | Tampered vs Intact (binary) |

## Mathematical Core

**Paillier Encryption (per pixel):**
```
c_{i,j} = E(I[i,j]) = g^{I[i,j]} · r^n mod n²
```

**Encrypted DCT:**
```
DCT_{u,v} = Σ_{x,y} c_{x,y} · w_{u,v}(x,y)
w = cos((2x+1)uπ/16) · cos((2y+1)vπ/16)
Using: E(a)·E(b) = E(a+b), E(a)^k = E(ka)
```

**Watson HVS Weighting (Encrypted):**
```
W_{u,v} = WatsonWeight(u,v)  (plaintext)
F_{u,v} = DCT_{u,v}^{W_{u,v}} = E(W_{u,v} · DCT_{u,v})
```

**Pseudo-Random Sign Flip:**
```
R_{u,v} = PRNG(key)_{u,v} ∈ {±1}
H_{u,v} = F_{u,v}^{R_{u,v}}  // Sign flip in encrypted domain
```

**Hash Comparison:**
```
Hash_plain = Decrypt(Hash_cipher) from cloud
Hash_local = Compute from plaintext (same pipeline)
Distance = ||Hash_plain - Hash_local||
Tampered if Distance > τ
```

## Constraints & Limitations

- ❌ **Authentication only** — no localization
- ❌ **Paillier overhead** (large ciphertexts, slow)
- ❌ **Fixed 8×8 DCT blocks**
- ❌ **Requires trusted key management**
- ✅ **Robust to JPEG≥50, noise σ≤10, rotation ≤2°**
- ✅ **Unique: inter-image distance >> intra-image**
- ✅ **Secure: ciphertext indistinguishable from random**
- ✅ **HVS weighting = perceptual robustness**

## Relevance to My Project

**High for authentication component**:
- Combine with localization method (PP-JPEG, LEFN)
- HVS weighting → adapt to encrypted domain forensic features
- Three-party protocol → matches cloud forensics scenario
- Watson weights are plaintext → perfect for homomorphic ops

---

## Tags
#encrypted-domain #paillier #perceptual-hashing #hvs #watson-model #authentication #integrity-verification #three-party-protocol #robust-hash