# Week 3 Data Inventory: Prescription Images & Medication Reference Data

**Project:** MedLabel: AI-Based Multi-Prescription Recognition and Medication Timetable Generation  
**Topic:** Topic 3 Lab — Data Engineering for AI (Pipelines, Lineage, and Workflows)  
**Date:** November 17, 2026  
**Pipeline Modality:** Computer Vision (Unstructured Images — Pathway C) + Secondary Tabular Grounding  

---

## 1. Project Context & Data Mapping (Step A1)

MedLabel requires two complementary data sources to fulfill its core functional requirements:
1. **Prescription Images Dataset:** 200 real-world prescription slips captured under varying hospital/clinic conditions.
2. **Malaysian Pharmaceutical Reference Products:** Regulatory metadata from the Ministry of Health Malaysia (MOH) for entity grounding and fuzzy matching.

### Requirements-to-Data Traceability

| Requirement ID | Needed Information / Feature | Candidate Source | Why Usable / Constraint |
| :--- | :--- | :--- | :--- |
| **FR-01 / FR-02 / FR-03** | Multi-image prescription ingestion, medicine directions, dosage handwriting, multi-document layouts | Mendeley Open Data: Bangladesh Prescription Dataset (`data/raw/images/`, 200 images: `1.jpeg`–`200.jpeg`) | **Usable:** Real-world photographic prescriptions exhibiting camera angle variance, crumpling, and varying doctor handwriting styles.<br/>**Constraint:** Bangladeshi handwriting & drug conventions; requires de-identification and image standardization before OCR. |
| **FR-06** | Official registered brand names, generic active ingredients, approved strengths | Ministry of Health Malaysia (MOH) Open Data Catalogue (`data/raw/moh_pharmaceutical_products_sample.csv`) | **Usable:** Authoritative national registry for ground-truth drug validation.<br/>**Constraint:** Tabular metadata only; does not contain images. |
| **NFR-3 / RAI-1** | Traceable source-to-output lineage, bounding-box audit trail, zero unverified inference | Ingestion metadata manifest & SHA-256 fingerprinting | **Usable:** Guarantees cryptographic provenance and traceability from raw image pixels to timetable slots. |

---

## 2. Data Inventory Table (Step A4)

*Summary of representative records from the full 200-image dataset (all 200 tracked in `data/week3_manifest.json` and `data/processed/image_manifest.csv`):*

| Source ID | Filename / Path | Type and Purpose | Version / Date / Owner | Access / Rights | Inspection Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **S001** | `data/raw/images/1.jpeg` | Unstructured Image; clinical prescription slip with medication list & top vitals | v2.0 / 2023 / Mendeley Open Data | Open Access (CC BY 4.0); De-identified | JPEG format, 970×728 px, RGB, 84.8 KB; visible handwriting: "Tab. Ciprocin 500", "Tab. Metro 400" |
| **S010** | `data/raw/images/10.jpeg` | Unstructured Image; multi-item prescription slip | v2.0 / 2023 / Mendeley Open Data | Open Access (CC BY 4.0); De-identified | JPEG format, 1024×814 px, RGB, 105.6 KB; high text density, watermarked clinic header |
| **S050** | `data/raw/images/50.jpeg` | Unstructured Image; prescription note with frequency indicators | v2.0 / 2023 / Mendeley Open Data | Open Access (CC BY 4.0); De-identified | JPEG format, 843×843 px, RGB, 79.1 KB; angled capture, shadowed corner |
| **S100** | `data/raw/images/100.jpeg` | Unstructured Image; diagnostic notes + Rx section | v2.0 / 2023 / Mendeley Open Data | Open Access (CC BY 4.0); De-identified | JPEG format, 1024×808 px, RGB, 80.0 KB; faint ink, camera tilt, clean white paper background |
| **S150** | `data/raw/images/150.jpeg` | Unstructured Image; dense handwritten prescription sheet | v2.0 / 2023 / Mendeley Open Data | Open Access (CC BY 4.0); De-identified | JPEG format, 1024×918 px, RGB, 114.2 KB; multi-column layout, mixed cursive |
| **S200** | `data/raw/images/200.jpeg` | Unstructured Image; final prescription slip in dataset | v2.0 / 2023 / Mendeley Open Data | Open Access (CC BY 4.0); De-identified | JPEG format, 1000×750 px, RGB, 92.4 KB; clear handwriting, minimal shadow |
| **REF-01** | `data/raw/moh_pharmaceutical_products_sample.csv` | Structured Tabular; official Malaysian registered drug master catalog | 2026 / MOH Malaysia (NPRA) | Open Government License; Public Metadata | CSV format, 20 representative rows, 7 columns (`registration_no`, `product_name`, `active_ingredient`, etc.) |

---

## 3. Inspection & Ingestion Evidence Summary (Step A3)

- **Total Ingested Images:** **200 files** (`1.jpeg` through `200.jpeg`).
- **Color Mode:** 100% RGB color space.
- **Resolution Range:** 600×600 px to 1200×1600 px (sufficient for optical character recognition, above the 300 DPI minimum threshold for standard print).
- **File Size Distribution:** 23.8 KB to 854.6 KB (average: ~110 KB per image).
- **Observed Physical Artifacts:** Paper crumpling, varying doctor cursive handwriting, shadow gradients, camera perspective skew, and pre-printed clinic headers.
- **Storage Protocol:** All raw inputs reside under `data/raw/images/` and are preserved without in-place modification to maintain raw data immutability.
- **Lineage Verification:** Every single one of the 200 files is cryptographically hashed (SHA-256) and tracked in `data/week3_manifest.json`.
