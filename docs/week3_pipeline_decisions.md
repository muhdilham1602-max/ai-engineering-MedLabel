# Week 3 Pipeline Decisions, Stage Contracts, and Traceability

**Project:** MedLabel: AI-Based Multi-Prescription Recognition and Medication Timetable Generation  
**Topic:** Topic 3 Lab — Data Engineering for AI (Pipelines, Lineage, and Workflows)  
**Date:** November 17, 2026  
**Pipeline Modality:** Computer Vision (Images) + Master Reference Table (CSV)  

---

## 1. Traceability to Topic 2 Requirements

| Requirement ID | Module / Component | Data Engineering Justification |
| :--- | :--- | :--- |
| **FR-01** | Multi-Image Ingestion | System must ingest varying formats (`.jpg`, `.jpeg`, `.png`) and validate file sizes and RGB color spaces before downstream OCR execution. |
| **FR-02** | Image Preprocessing & Standardization | High-resolution input photos exhibit non-uniform dimensions (843×843 to 1024×918 px), camera tilt, and uneven lighting. Standardization to a consistent dimension (512×512) and RGB conversion prevents tensor mismatch and memory exhaustion during OCR text detection. |
| **FR-03** | OCR Text & Bounding-Box Detection | Clean, normalized images ensure stable character segmentation and bounding box coordinate calculation. |
| **NFR-3 / NFR-4** | Safety Gate & Traceability Audit | Every prepared image must maintain cryptographic provenance (SHA-256 hash) linking back to the raw source file so users can visually verify bounding crops in the Human Review Screen. |

---

## 2. Part B Comparison & Justification of Preparation Decisions

### Evaluated Alternatives: Image Resolution & Preprocessing Configuration

| Approach / Dimension | Configuration A (Aggressive Downsampling: 224×224) | Configuration B (Chosen: Standardized 512×512 High-Detail RGB) |
| :--- | :--- | :--- |
| **Image Resolution** | $224 \times 224$ pixels | $512 \times 512$ pixels |
| **Color Space** | Grayscale (1-channel) | RGB (3-channel) |
| **Observed Evidence** | Downsampling doctor cursive handwriting to $224 \times 224$ px severely degrades stroke legibility; decimal points (e.g., `0.5 mg`) and thin pen strokes in `Tab. Ciprocin 500` become blurred into background noise. | Preserves fine cursive stroke contours, decimal points, and multi-line drug instructions while reducing memory footprint by ~60% compared to raw camera originals. |
| **Accepted Limitation** | Unusable for small prescription print and handwritten fractions. | File size is larger than $224 \times 224$ (approx. 180–250 KB per PNG), requiring slightly more memory during batch preprocessing. |
| **Decision** | **Rejected** for prescription OCR tasks. | **Accepted:** Meets the minimum legibility requirements for OCR token recognition while providing consistent batch dimensions. |

---

## 3. Architectural Design Choices

### 3.1 ETL vs. ELT Decision
- **Choice: ETL (Extract $\to$ Transform $\to$ Load)**
- **Rationale:** Prescription images contain non-standardized formats, orientation skew, and potential metadata noise. Performing transformations (RGB standardization, resolution normalization, and cryptographic hashing) **before** loading images into the OCR inference and session cache ensures that no unstandardized, corrupt, or unverified image reaches downstream clinical modules.

### 3.2 Batch vs. Streaming Rationale
- **Choice: Micro-Batch Processing**
- **Rationale:** Patients and caregivers upload a discrete batch of 2 to 5 prescription slips per medical consultation. Real-time streaming is unnecessary; micro-batch processing enables collective validation, duplicate drug cross-referencing across the entire batch, and unified timetable compilation.

---

## 4. Stage Contracts Table & Failure Responses

| Stage | Expected Contract & Evidence | Failure Condition | Failure Response Protocol |
| :--- | :--- | :--- | :--- |
| **1. Ingest** | Image file exists under `data/raw/images/`, supported extension (`.jpg`, `.jpeg`, `.png`, `.webp`), non-empty file size ($> 0\text{ bytes}$). | Missing file, unsupported format, or 0-byte corrupt file. | **Hard Stop:** Halt pipeline, log `FileNotFoundError` or format error, and prompt user to upload valid image. |
| **2. Inspect** | PIL can open and verify image header; readable dimensions ($W \ge 300\text{ px}, H \ge 300\text{ px}$); valid color mode (`RGB` or `L`). | Corrupted image header (`UnidentifiedImageError`) or resolution below minimum legible threshold. | **Quarantine:** Exclude corrupt file from batch, flag image as unreadable, and notify user. |
| **3. Prepare** | Image successfully converted to RGB, resized using Lanczos resampling to $512 \times 512$, saved to target PNG. | Transformation exception (out-of-memory, disk full). | **Fail Safe:** Log transformation exception; abort batch before output export. |
| **4. Validate** | Prepared PNG exists on disk, size $> 0\text{ bytes}$, output dimensions match exact target $(512, 512)$, output count matches input count. | Missing output file or size discrepancy. | **Hard Stop:** Raise `ValueError("Exported output count does not match")`. |
| **5. Record Lineage** | Source SHA-256 computed; prepared SHA-256 computed; bidirectional source-to-output mapping recorded in `pipeline_manifest.json`. | Checksum mismatch or missing output in mapping. | **Audit Alert:** Refuse to register pipeline run until cryptographic checksum verification passes. |

---

## 5. Output Artifacts & Provenance Verification

- **Part B Prepared Outputs:** `data/processed/images/` and `data/processed/image_manifest.csv`
- **Part B Lineage Manifest:** `data/week3_manifest.json` (Contains SHA-256 fingerprints, source paths, and processing notes for all 5 images).
- **Part C Executed Pipeline Outputs:** `data/pipeline_v1/images/` and `data/pipeline_v1/images/pipeline_manifest.json`.
- **Repeatability Verification (Cell 9):** Confirmed identical SHA-256 hashes between primary and secondary pipeline executions (`PASS: images — source fingerprints, prepared outputs and mappings match`).
