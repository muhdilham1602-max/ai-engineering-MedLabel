# Week 2 — Project Framing, Scope, and Requirements Specification

**Project:** MedLabel (AI-Based Multi-Prescription Recognition and Medication Timetable Generation)  
**Document Version:** 1.0  
**Date:** October 28, 2026  
**Author:** MedLabel Engineering Team  

---

## Section 0: Project Framing

### 0.1 Problem Domain & Context
MedLabel addresses a critical intersection between **Computer Vision (Document OCR)**, **Natural Language Processing (Clinical Entity Extraction)**, and **Healthcare Informatics**.

In Malaysia, healthcare delivery is divided between public healthcare facilities (Ministry of Health / KKM hospitals and *Klinik Kesihatan*) and private healthcare providers (specialist centres, general practitioner clinics, and retail pharmacy chains such as Caring, Guardian, and Big Pharmacy). Patients managing chronic conditions (e.g., Type 2 Diabetes, Hypertension, Dyslipidemia, and Cardiovascular diseases) frequently visit multiple care facilities. Consequently, they receive separate paper-based prescriptions or physical dispensing labels attached to medication boxes, blister strips, and bottles.

### 0.2 Core Challenge
Each prescription source adheres to differing formatting standards, varied typographic layouts, and differing conventions for dosage instructions:
- **Language Mixture:** Labels combine English, Latin medical abbreviations (*OD*, *BD*, *TDS*, *QID*, *prn*, *pc*, *ac*, *om*, *on*), and Bahasa Melayu colloquial instructions (*"1 biji 2 kali sehari selepas makan"*, *"ambil bila perlu"*).
- **Physical Document Variability:** Prescriptions range from dot-matrix pharmacy receipts to thermal adhesive labels that suffer from fading, glare, crumpling, and uneven lighting when captured via smartphone cameras.
- **Cognitive Overload for Patients:** Patients and non-clinical caregivers must mentally synthesize multiple disparate documents into a coherent daily timetable. Miscalculating intervals, misreading look-alike names (e.g., *Metformin* vs. *Metoprolol*), or duplicating active ingredients across brand and generic products often results in severe adverse drug events (ADEs).

### 0.3 Value Proposition & Impact
- **Patient Safety:** Eliminates error-prone manual transcribing by extracting instructions directly from source documents and systematically flagging ambiguities.
- **Traceability:** Unlike opaque black-box AI tools, MedLabel retains an unbroken audit trail by linking every digitized instruction directly back to its original bounding box image crop.
- **Human-in-the-Loop Governance:** MedLabel acts as an intelligent cognitive assistant rather than an autonomous decision maker. No timetable is finalized without explicit patient or caregiver validation.

### 0.4 User Personas

| Persona | Role / Profile | Key Pain Points | MedLabel Value |
| :--- | :--- | :--- | :--- |
| **Persona 1: Uncle Tan (68)** | Chronic disease patient managing 6 medications from KKM clinic and private specialist. | Confused by varying tablet intake times; struggles to read small printed label text; fears forgetting doses. | Scans all labels; gets a high-contrast, large-print daily timetable organized by meal times (Pagi, Tengah Hari, Malam). |
| **Persona 2: Sarah (34)** | Primary caregiver for her elderly mother with mild dementia and hypertension. | Spends hours every Sunday sorting pillboxes; worries about conflicting medications and duplicate active ingredients. | Uploads photos of mother's prescription slips; reviews flagged duplicates/conflicts; prints a weekly schedule. |
| **Persona 3: Community Pharmacist / Nurse** | Healthcare professional conducting medication reconciliation during patient check-in. | Manual reconciliation of paper slips brought in a plastic bag ("brown bag review") is slow and lacks digital tracking. | Quickly scans patient labels to generate a consolidated preliminary medication summary for clinical review. |

---

## Section 1: Application Scope

### 1.1 In-Scope Capabilities
1. **Multi-Image Ingestion:** Simultaneous uploading and rendering of multiple prescription and label photos (`.png`, `.jpg`, `.jpeg`).
2. **Image Preprocessing:** Grayscale conversion, contrast stretching (CLAHE), deskewing, and noise filtering to enhance low-quality mobile uploads.
3. **OCR Text & Bounding-Box Detection:** Optical character recognition extracting raw text tokens alongside spatial bounding coordinates.
4. **Structured Information Extraction (IE):** Parsing key pharmaceutical attributes:
   - Medication Name (Brand and Generic)
   - Strength / Concentration (e.g., `500 mg`, `10 mg/ml`)
   - Dosage Amount (e.g., `1 tablet`, `2 capsules`, `5 ml`)
   - Frequency (e.g., `OD`, `BD`, `TDS`, `QID`, `PRN`)
   - Administration Timing & Conditions (e.g., `Before meals / ac`, `After meals / pc`, `At bedtime / on`)
   - Duration (e.g., `7 days`, `1 month`, `As directed`)
5. **Malaysian Pharmaceutical Reference Grounding:** Matching extracted medicine names against the official Ministry of Health (MOH) Malaysia Pharmaceutical Products Dataset to correct minor OCR misspellings and normalize brand-to-generic mappings.
6. **Uncertainty & Safety Conflict Detection:**
   - Flagging low-confidence OCR tokens.
   - Detecting omitted critical fields (e.g., missing frequency or missing strength).
   - Identifying duplicate active ingredients across different prescriptions.
   - Highlighting abnormal dosing schedules.
7. **Interactive Human-in-the-Loop (HITL) Verification:**
   - Displaying side-by-side synchronized views of the original prescription crop and editable text fields (`st.data_editor`).
   - Providing visual indicators (color-coded flags) for fields requiring confirmation.
8. **Consolidated Timetable Generation:**
   - Synthesizing confirmed instructions across all uploaded prescriptions into a unified chronological schedule (Morning, Afternoon, Evening, Night / Bedtime).
   - Incorporating meal constraints (*Before Food* vs. *After Food*).
9. **Export Functionality:** Exporting the verified schedule to structured JSON and printable summary views.

### 1.2 Out-of-Scope Boundaries (Safety Guardrails)
- **Autonomous Diagnosis:** The system will not diagnose conditions or suggest therapeutic indications.
- **Dosage Prescription or Adjustment:** The system will never recommend changing, increasing, or reducing prescribed doses.
- **Autonomous Conflict Resolution:** The system will flag potential conflicts (e.g., duplicate active ingredients), but will **never** alter or delete an instruction automatically without user intervention and advice from a licensed healthcare professional.
- **Visual Pill Appearance Identification:** Identifying loose pills or capsules from photograph appearance alone is excluded due to high risk of visual confusion.
- **Live Electronic Health Record (EHR) Writing:** MedLabel will not automatically mutate clinical EHR databases.
- **Handwritten Doctor Notes:** While tested opportunistically, unconstrained doctor cursive handwriting is excluded from initial baseline commitments; the primary focus is printed dispensing labels and typed prescription slips.

### 1.3 Key Assumptions and Environmental Constraints
- **Device & Camera:** Users capture images using standard consumer smartphones (minimum 8-megapixel resolution) with reasonable focus and ambient lighting.
- **Language Convention:** Prescriptions conform to standard Malaysian clinical conventions (English, Bahasa Melayu, or mixed Latin medical terms).
- **Network & Privacy Constraint:** Image processing and text parsing should minimize external transmission of unprotected patient identifiers.

---

## Section 2: Functional and Non-Functional Requirements

### 2.1 Functional Requirements (FR)

| Requirement ID | Module | Description | Priority |
| :--- | :--- | :--- | :--- |
| **FR-01** | Ingestion | System shall accept multiple image files simultaneously in standard web formats (`PNG`, `JPG`, `JPEG`) up to 10MB per file. | High |
| **FR-02** | Preprocessing | System shall apply automated image preprocessing (deskewing, contrast enhancement, noise reduction) prior to OCR. | Medium |
| **FR-03** | OCR Extraction | System shall extract text characters, words, and their corresponding spatial bounding box coordinates `[x, y, w, h]`. | High |
| **FR-04** | Entity Extraction | System shall parse raw text into structured attributes: `{Medication Name, Strength, Dosage, Frequency, Timing/Condition, Duration}`. | High |
| **FR-05** | Bilingual Normalization | System shall interpret both Latin abbreviations (`TDS`, `BD`, `OD`) and Malay phrases (`3 kali sehari`, `selepas makan`, `sebelum makan`). | High |
| **FR-06** | Reference Matching | System shall perform fuzzy string matching against the Malaysian MOH Pharmaceutical Products catalog to identify closest registered drugs. | High |
| **FR-07** | Uncertainty Flagging | System shall assign confidence scores to extracted fields and flag tokens falling below a predefined confidence threshold ($\tau < 0.80$). | High |
| **FR-08** | Conflict Detection | System shall scan all active items and generate warning alerts if identical active ingredients or conflicting frequencies are detected. | High |
| **FR-09** | Visual Traceability | System shall display the cropped image region corresponding to each extracted entity when selected in the verification UI. | High |
| **FR-10** | Interactive Correction | System shall provide an interactive data editor allowing users to modify, accept, or delete extracted medication rows. | High |
| **FR-11** | Timetable Synthesis | System shall map verified items into standardized daily time slots (e.g., Morning: 08:00, Afternoon: 13:00, Evening: 19:00, Bedtime: 22:00). | High |
| **FR-12** | Export & Summary | System shall output the verified schedule as a downloadable structured JSON file and formatted summary table. | Medium |

### 2.2 Non-Functional Requirements (NFR)

#### NFR-1: Performance & Latency
- The end-to-end processing time from image upload to draft extraction display shall not exceed **5.0 seconds** per prescription image on standard consumer hardware.
- UI responsiveness during interactive table editing shall remain under **200 milliseconds** per interaction.

#### NFR-2: Usability & Accessibility
- Interface elements must adhere to WCAG 2.1 AA contrast standards to support elderly users and individuals with mild visual impairment.
- Medical jargon shall be translated into plain-language summaries (e.g., explaining `TDS` as `Three times a day (Morning, Afternoon, Evening)`).

#### NFR-3: Reliability & Safety
- The system must fail safely: if OCR or entity extraction fails, the application shall display an informative error prompt without crashing and prompt the user to manually enter details.
- System shall prevent timetable generation until the user checks an explicit confirmation checkbox verifying the extracted items.

#### NFR-4: Auditability & Traceability
- 100% of generated timetable entries must maintain bidirectional references to their source file name and bounding box coordinate.

#### NFR-5: Modularity & Maintainability
- The codebase shall maintain clean separation between OCR (`src/ocr.py`), extraction (`src/extraction.py`), validation (`src/validation.py`), and timetable generation (`src/timetable.py`).

---

## Section 3: Responsible AI Requirements

### 3.1 Human Oversight & Verification (Human-in-the-Loop)
- **Mandatory Validation Gate:** The application strictly enforces a human-in-the-loop workflow. Timetable synthesis is completely disabled until the user conducts a side-by-side visual audit.
- **Unambiguous Agency:** The system acts strictly as an administrative transcription tool, never replacing the cognitive authority of a licensed doctor or pharmacist.

### 3.2 Mitigation of Automation Bias
- **Visual Friction & Warning Banners:** A persistent disclaimer is rendered across all pages stating that MedLabel is an AI prototype and requiring manual confirmation.
- **Color-Coded Uncertainty:** Low-confidence extractions are rendered in distinct amber/red warning badges to counter passive acceptance.

### 3.3 Data Privacy, Confidentiality & Compliance
- **Compliance with PDPA 2010:** Adheres to the principles of the Malaysian Personal Data Protection Act 2010.
- **No Unsolicited PII Retention:** Uploaded images and extracted patient identifiers (e.g., patient name, NRIC number, address) are processed in-memory within the active session state. No patient data is persisted to public cloud storage or public Git repositories.
- **De-Identification Protocol:** Any sample data stored in the repository for evaluation must be synthetic or fully scrubbed of Protected Health Information (PHI).

### 3.4 Transparency & Explainability
- **Visible Grounding:** Every extracted entity displays its matching score against the MOH database.
- **Explainable Conflict Warnings:** When a conflict is raised (e.g., "Duplicate Paracetamol detected"), the system clearly articulates the two conflicting prescription sources and active substances involved.

### 3.5 Fallback & Failure Handling
- When image quality is severely degraded (excessive blur, severe glare, occluded text), the system explicitly refuses to guess. It prompts the user: *"Image quality is too low for reliable reading. Please retake the photo under brighter light or enter the details manually."*
