# Master Index: Image Forgery Detection in Encrypted Domain — 15 Paper Deep-Dives

> **Project:** Major Project — Image Forgery Detection in Encrypted Domain  
> **Created:** 2026-11-17  
> **Purpose:** Central hub linking all 15 first-person paper analyses for Obsidian graph view

---

## How to Use This in Obsidian

1. Open `D:\major project\papers\` as your Obsidian vault
2. Open this file (`00_MASTER_INDEX.md`)
3. Press `Ctrl+G` (or `Cmd+G` on Mac) to open **Graph View**
4. All 15 papers will appear as connected nodes via the wiki-links below

---

## Paper Categories & Links

### 📚 Classical / Traditional Methods (5 Papers)

| # | Paper | Link | Core Contribution |
|---|-------|------|-------------------|
| 01 | ECDC: Efficient Copy-Move Detection (2020) | [[01_ecdc_copy_move_detection]] | SIFT + BOW + PQ + DCT verification |
| 02 | Comprint: Compression Fingerprint (2019) | [[02_comprint_compression_fingerprint]] | JPEG grid + quantization table as camera fingerprint |
| 03 | CNN-Supervised Compressed Forgery (2022) | [[03_cnn_supervised_compressed_forgery]] | First CNN on compressed domain (DCT coeffs) |
| 04 | FF-Net: Double JPEG Detection (2021) | [[04_ffnet_double_jpeg_detection]] | Benford's Law on DCT → 1D CNN |
| 05 | CMFD Survey 2024 | [[05_cmfd_survey_2024]] | Comprehensive taxonomy + open challenges |

### 🤖 Deep Learning Methods (5 Papers)

| # | Paper | Link | Core Contribution |
|---|-------|------|-------------------|
| 06 | MFAF-Net: Multi-Feature Attention Fusion (2022) | [[06_mfafnet_splicing_detection]] | RGB + Noise + Edge streams + attention |
| 07 | CMFDFormer: Transformer + Continual Learning (2023) | [[07_cmfdformer_transformer_continual]] | Swin Transformer + EWC for domain adaptation |
| 08 | TruFor: Universal Forgery Detection (2022) | [[08_trufor_universal_detection]] | Transformer + noise fingerprint + integrity |
| 09 | DL Survey (Mehrjardi et al., 2023) | [[09_dl_survey_mehrjardi_2023]] | 100+ papers taxonomy: splice/copy-move/removal |
| 10 | DL Review: Mathematical Formulations (2023) | [[10_dl_review_mathematics_2023]] | Loss functions, attention math, metrics formulas |

### 🔐 Encrypted Domain / Privacy-Preserving (5 Papers)

| # | Paper | Link | Core Contribution |
|---|-------|------|-------------------|
| 11 | IFED/LEFN: Foundational Encrypted Forensics (2019/2021) | [[11_ifed_lefnd_foundational]] | Paillier + linear filters (IFED) → DNN (LEFN) |
| 12 | PP-JPEG: Paillier Tampering Localization (2023) | [[12_ppjpeg_paillier_tampering]] | Homomorphic DCT + energy graph + QF minima |
| 13 | Robust Hash: Paillier + HVS (2023) | [[13_robust_hash_paillier_hvs]] | Watson-weighted perceptual hash in encrypted domain |
| 14 | SecDFDNet: MPC DeepFake Detection (2023) | [[14_secdfdnet_deepfake_secret_sharing]] | Secret sharing + 4 secure protocols (SecReLU, etc.) |
| 15 | Selective Encryption: Privacy-Forensics Trade-off (2021) | [[15_selective_encryption_forensics_privacy]] | MSB encryption + LSB forensics + recognizability metric |

---

## Cross-Cutting Themes (Graph View Clusters)

### By Encryption Approach
- **Homomorphic Encryption (Paillier):** [[11_ifed_lefnd_foundational]], [[12_ppjpeg_paillier_tampering]], [[13_robust_hash_paillier_hvs]]
- **Secret Sharing / MPC:** [[14_secdfdnet_deepfake_secret_sharing]]
- **Selective Encryption:** [[15_selective_encryption_forensics_privacy]]
- **No Encryption (Baseline):** [[01_ecdc_copy_move_detection]], [[02_comprint_compression_fingerprint]], [[03_cnn_supervised_compressed_forgery]], [[04_ffnet_double_jpeg_detection]], [[06_mfafnet_splicing_detection]], [[07_cmfdformer_transformer_continual]], [[08_trufor_universal_detection]]

### By Forgery Type
- **Copy-Move:** [[01_ecdc_copy_move_detection]], [[12_ppjpeg_paillier_tampering]]
- **Splicing:** [[02_comprint_compression_fingerprint]], [[06_mfafnet_splicing_detection]]
- **Double JPEG:** [[04_ffnet_double_jpeg_detection]], [[12_ppjpeg_paillier_tampering]]
- **DeepFake (GAN):** [[14_secdfdnet_deepfake_secret_sharing]]
- **Universal/General:** [[08_trufor_universal_detection]], [[07_cmfdformer_transformer_continual]]

### By Mathematical Core
- **DCT / Frequency Domain:** [[02_comprint_compression_fingerprint]], [[03_cnn_supervised_compressed_forgery]], [[04_ffnet_double_jpeg_detection]], [[11_ifed_lefnd_foundational]], [[12_ppjpeg_paillier_tampering]], [[13_robust_hash_paillier_hvs]]
- **Attention / Transformers:** [[06_mfafnet_splicing_detection]], [[07_cmfdformer_transformer_continual]], [[08_trufor_universal_detection]]
- **Noise / Residual Analysis:** [[01_ecdc_copy_move_detection]], [[06_mfafnet_splicing_detection]], [[08_trufor_universal_detection]], [[15_selective_encryption_forensics_privacy]]
- **Benford's Law:** [[04_ffnet_double_jpeg_detection]]
- **Secret Sharing / MPC Protocols:** [[14_secdfdnet_deepfake_secret_sharing]]

---

## Quick Navigation

### Start Here for Encrypted Domain Project
1. **Foundation:** [[11_ifed_lefnd_foundational]] — First encrypted forensics papers
2. **Best Localization:** [[12_ppjpeg_paillier_tampering]] — Paillier + DCT + energy graph
3. **Best Authentication:** [[13_robust_hash_paillier_hvs]] — HVS-weighted hash
4. **Best Practical DL:** [[14_secdfdnet_deepfake_secret_sharing]] — MPC beats FHE for neural nets
5. **Trade-off Analysis:** [[15_selective_encryption_forensics_privacy]] — Privacy vs forensics curve

### Start Here for Classical/DL Baselines
1. **Classical Survey:** [[05_cmfd_survey_2024]]
2. **DL Survey:** [[09_dl_survey_mehrjardi_2023]]
3. **Math Reference:** [[10_dl_review_mathematics_2023]]
4. **Best Classical:** [[02_comprint_compression_fingerprint]] (compression fingerprint)
5. **Best DL:** [[08_trufor_universal_detection]] (universal + noise fingerprint)

---

## Tags for Filtering in Obsidian

Click any tag in Obsidian to filter the graph:

#classical #deep-learning #encrypted-domain #paillier #mpc #secret-sharing #selective-encryption #copy-move #splicing #double-jpeg #deepfake #dct #transformer #attention #noise-analysis #benfords-law #hvs #watson-model #homomorphic-encryption #privacy-preserving #computational-cost #practical #survey #mathematical-formulations

---

## Related Files (Outside `papers/`)

- `../image_forgery_detection_research_base.md` — Master research document (44 KB) with comparative matrices, terminology dictionary, core formulas, datasets table, research gaps, 4-phase roadmap, BibTeX references
- `../README.md` — Project overview (create if needed)

---

## Graph View Tips

| Action | Shortcut |
|--------|----------|
| Open Graph View | `Ctrl+G` / `Cmd+G` |
| Filter by tag | Click tag in sidebar or type `tag:#encrypted-domain` in graph search |
| Show only links | Toggle "Show tags" off in graph settings |
| Center on node | Click any paper node |
| Export graph | `Ctrl+P` → "Export graph view" |

---

*Generated for Obsidian graph view connectivity. All 15 papers linked bidirectionally via wiki-links.*