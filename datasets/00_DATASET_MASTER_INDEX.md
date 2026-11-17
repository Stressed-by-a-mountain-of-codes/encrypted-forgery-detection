# Master Index: Image Forgery Detection Datasets — 5 Dataset Deep-Dives

> **Project:** Major Project — Image Forgery Detection in Encrypted Domain  
> **Created:** 2026-11-17  
> **Purpose:** Central hub linking all dataset analyses for Obsidian graph view

---

## How to Use This in Obsidian

1. Open `D:\major project\datasets\` as your Obsidian vault (or same vault as papers)
2. Open this file (`00_DATASET_MASTER_INDEX.md`)
3. Press `Ctrl+G` to open **Graph View**
4. All 5 datasets will appear as connected nodes via the wiki-links below

---

## Dataset Portfolio Overview

| # | Dataset | Link | Forgery Types | Size | Primary Use |
|---|---------|------|---------------|------|-------------|
| 01 | **CASIA v1 & v2** | [[01_casia_v1_v2]] | Copy-move, Splicing | 1,740+ images | **Primary benchmark** — your main dataset |
| 02 | **Columbia Splicing** | [[02_columbia_splicing]] | Splicing (uncompressed) | 180 images | Clean splicing ground truth |
| 03 | **COVERAGE** | [[03_coverage]] | Splicing, Copy-move, Removal | 10,000+ images | Large-scale diversity |
| 04 | **IMD2020** | [[04_imd2020]] | Splicing, Copy-move, Removal, Inpainting | 2,000 images | Modern, realistic, multiple types |
| 05 | **MICC-F220/F600** | [[05_micc_f220_f600]] | Copy-move (rotation, scaling) | 220 / 600 images | Copy-move with transformations |

---

## Why These 5 Datasets?

### Coverage Matrix

| Forgery Type | CASIA | Columbia | COVERAGE | IMD2020 | MICC |
|--------------|-------|----------|----------|---------|------|
| **Splicing** | ✅ | ✅ (uncompressed) | ✅ | ✅ | ❌ |
| **Copy-Move** | ✅ | ❌ | ✅ | ✅ | ✅ (transformed) |
| **Removal/Inpainting** | ❌ | ❌ | ✅ | ✅ | ❌ |
| **DeepFake** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Double JPEG** | ✅ (v2) | ❌ | ✅ | ✅ | ❌ |

### Complementarity

- **CASIA** = Your main benchmark, established, both v1 (uncompressed) and v2 (JPEG)
- **Columbia** = Pure splicing, uncompressed, clean masks — good for testing compression-agnostic methods
- **COVERAGE** = Largest, most diverse, multiple forgery types per image — stress test for generalization
- **IMD2020** = Modern, realistic tampering (not copy-paste), includes inpainting — closest to real world
- **MICC** = Copy-move with rotation/scale — tests geometric robustness

---

## Cross-Links to Papers Vault

These datasets are used in the papers you analyzed:

| Dataset | Papers Using It |
|---------|----------------|
| CASIA v1/v2 | [[../papers/01_ecdc_copy_move_detection]], [[../papers/06_mfafnet_splicing_detection]], [[../papers/07_cmfdformer_transformer_continual]], [[../papers/08_trufor_universal_detection]], [[../papers/09_dl_survey_mehrjardi_2023]], [[../papers/11_ifed_lefnd_foundational]], [[../papers/12_ppjpeg_paillier_tampering]] |
| Columbia | [[../papers/02_comprint_compression_fingerprint]], [[../papers/06_mfafnet_splicing_detection]], [[../papers/08_trufor_universal_detection]], [[../papers/09_dl_survey_mehrjardi_2023]] |
| COVERAGE | [[../papers/07_cmfdformer_transformer_continual]], [[../papers/08_trufor_universal_detection]], [[../papers/09_dl_survey_mehrjardi_2023]] |
| IMD2020 | [[../papers/08_trufor_universal_detection]], [[../papers/09_dl_survey_mehrjardi_2023]] |
| MICC-F220 | [[../papers/01_ecdc_copy_move_detection]], [[../papers/09_dl_survey_mehrjardi_2023]] |

---

## Quick Navigation

### Start Here for Your Project
1. **Primary:** [[01_casia_v1_v2]] — Your main dataset, download links, splits, metrics
2. **Splicing Baseline:** [[02_columbia_splicing]] — Clean uncompressed splicing
3. **Scale Test:** [[03_coverage]] — Large-scale generalization
4. **Modern Realism:** [[04_imd2020]] — Realistic tampering, inpainting
5. **Geometric Robustness:** [[05_micc_f220_f600]] — Rotated/scaled copy-move

### For Encrypted Domain Evaluation
- All datasets can be **JPEG compressed at multiple QFs** to test encrypted-domain methods (PP-JPEG, LEFN, SecDFDNet)
- **CASIA v2** already has JPEG compression — matches PP-JPEG paper setup
- **Columbia** is uncompressed — compress it yourself for double-JPEG tests

---

## Tags for Filtering

#casia #columbia #coverage #imd2020 #micc #splicing #copy-move #removal #inpainting #jpeg #uncompressed #benchmark #encrypted-domain-eval #primary-dataset

---

## Graph View Tips

| Action | Shortcut |
|--------|----------|
| Open Graph View | `Ctrl+G` / `Cmd+G` |
| Filter by tag | Click tag or type `tag:#casia` |
| Show paper links | Enable "Show tags" + search `../papers/` |
| Center on dataset | Click node |

---

*Generated for Obsidian graph view connectivity. All 5 datasets linked bidirectionally via wiki-links.*