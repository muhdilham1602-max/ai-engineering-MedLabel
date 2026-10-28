# Week 2 — V1 Architecture & Architecture Decision Records (ADR)

**Project:** MedLabel (AI-Based Multi-Prescription Recognition and Medication Timetable Generation)  
**Document Version:** 1.0  
**Date:** October 28, 2026  
**Author:** MedLabel Engineering Team  

---

## 1. System Architecture Overview

MedLabel is architectured around an **AI-assisted prescription recognition pipeline with mandatory human verification**. Rather than treating prescription understanding as an unconstrained black-box vision-to-text task, the architecture couples optical text recognition, semantic clinical extraction, national drug database grounding, and rigorous safety validation with a mandatory human review decision gate.

### 1.1 Architecture Diagram
The official system architecture diagram of MedLabel V1 is illustrated below:

![MedLabel V1 Architecture Diagram](week2_architecture_v1.png)

> **Draw.io Source Diagram:** An editable version is provided in [`docs/week2_architecture_v1.drawio`](week2_architecture_v1.drawio), which can be opened and edited directly in [draw.io (diagrams.net)](https://app.diagrams.net).

### 1.2 End-to-End System Workflow

The architecture defines a linear-to-conditional workflow across 10 core stages:

1. **User / Caregiver:**
   - The patient or caregiver initiates the workflow by uploading multiple prescription or dispensing label images.
2. **Web Interface (`app.py` via Streamlit):**
   - Manages prescription file ingestion (`PNG`, `JPG`, `JPEG`) and renders real-time image previews.
3. **Image Quality Check (`src/ocr.py`):**
   - Evaluates image orientation, blur, and contrast; applies preprocessing (deskewing, CLAHE contrast enhancement) to ensure legibility.
4. **OCR Engine (`src/ocr.py`):**
   - Recognizes printed text from prescription labels and extracts token coordinates and confidence scores.
5. **Information Extraction (`src/extraction.py`):**
   - Extracts structured entities: medicine name, strength, dosage amount, frequency, and timing conditions when explicitly stated (supporting bilingual English and Bahasa Melayu instructions).
6. **Medicine Reference Lookup (`MOH Catalog Matcher`):**
   - Compares extracted drug names against official Malaysian pharmaceutical product metadata (MOH Open Data) using fuzzy string and phonetic matching to normalize brand and generic names.
7. **Validation & Uncertainty Checks (`src/validation.py`):**
   - Systematically identifies missing fields, flags low-confidence OCR tokens, and detects potentially conflicting instructions (e.g., duplicate active ingredients across different slips).
8. **Human Review Screen (Interactive HITL Interface):**
   - Presents the original source image side-by-side with extracted fields (`st.data_editor`), allowing the user to correct, add, or confirm details.
9. **Decision Gate: *All required instructions verified and no unresolved conflict?***
   - **Branch [No / Unresolved] $\rightarrow$ Stop Timetable Generation:**
     - Completely halts schedule generation.
     - Flags the issue for consultation with a licensed pharmacist or prescribing physician.
     - **Safety Rule:** The system *never* guesses missing information or automatically resolves clinical conflicts.
   - **Branch [Yes] $\rightarrow$ Timetable Generator (`src/timetable.py`):**
     - Compiles verified instructions into standardized chronological daily time slots (Morning, Afternoon, Evening, Bedtime) aligned with meal conditions (*Before/After Food*).
     - **Safety Rule:** Uses verified instructions only; never infers or recommends unprescribed doses.
10. **Timetable Review & Reminder Plan:**
    - Displays the final consolidated schedule for user review prior to practical use and offers export capabilities.

### 1.3 Cross-Cutting Safeguards & Safety Boundaries
- **Cross-Cutting Safeguards:** Consent • Data minimization • Secure ephemeral storage • De-identification for research • Bounding-box audit trail.
- **Safety Boundary:** *MedLabel organizes user-verified prescription information; it does not diagnose, recommend doses, or replace a healthcare professional.*

---

## 2. Architecture Decision Records (ADRs)

### ADR-001: Modular Pipeline vs. Monolithic End-to-End Multimodal VLM

- **Status:** **Accepted**
- **Context:**  
  Recent advancements in Multimodal Vision-Language Models (VLMs) allow direct image-to-schedule conversion via end-to-end prompts. However, prescriptions are safety-critical documents containing high-risk pharmacological dosages where hallucinations, silent omissions, or unverified approximations carry fatal risks.
- **Decision:**  
  Implement a **decoupled modular pipeline** (Quality Check $\rightarrow$ OCR $\rightarrow$ Slot-filling Extraction $\rightarrow$ MOH Reference Lookup $\rightarrow$ Validation $\rightarrow$ Mandatory Human Review Gate $\rightarrow$ Timetable Generator) rather than a single end-to-end black-box prompt.
- **Consequences:**  
  - *Positive:* Every intermediate step produces verifiable, inspectable artifacts (bounding box coordinates, token confidence scores, candidate matching distance). Enables unit testing of each module independently. Drastically lowers operating cost, latency, and cloud dependency.
  - *Negative:* Errors in upstream OCR must be strictly caught by the uncertainty validator and surfaced to the user.
- **Alternatives Considered:**  
  - *Monolithic VLM Prompting:* Rejected due to lack of token-level bounding box traceability, risk of unflagged hallucinations, high latency, and clinical liability.

---

### ADR-002: Mandatory Human-in-the-Loop (HITL) Review Screen and Hard "Stop" Failure Branch

- **Status:** **Accepted**
- **Context:**  
  Automation bias causes users to uncritically trust automated schedules. In healthcare, an error in reading `10mg` as `100mg` or `BD` as `QID` can result in severe overdose. The system must establish a non-negotiable verification mechanism before producing actionable patient schedules.
- **Decision:**  
  The application enforces a **Hard Decision Gate**: *"All required instructions verified and no unresolved conflict?"*
  - If verified: Progresses to the Timetable Generator using confirmed instructions only.
  - If unverified or conflicting: **Stops timetable generation**, explicitly directs the user to consult their pharmacist/prescriber, and strictly refuses to guess missing fields or resolve clinical conflicts autonomously.
- **Consequences:**  
  - *Positive:* Drastically mitigates automation bias and clinical liability; ensures 100% human accountability; guarantees zero unverified or guessed medication administrations.
  - *Negative:* Requires manual review step by the user or caregiver (approx. 30–60 seconds per prescription batch).
- **Alternatives Considered:**  
  - *Autonomous Best-Effort Scheduling:* Rejected due to unacceptable clinical safety risks and ethical non-compliance with WHO patient safety recommendations.

---

### ADR-003: Malaysian MOH Drug Reference Grounding via Hybrid Fuzzy Matching

- **Status:** **Accepted**
- **Context:**  
  OCR engines frequently introduce character substitutions (e.g., `0` for `O`, `l` for `1`, `rn` for `m`). Furthermore, patients receive both generic drugs and commercial brand names. We need to normalize extracted drug strings to official registered entities in Malaysia.
- **Decision:**  
  Ground extracted drug entities against the open **Malaysian Ministry of Health (MOH) Pharmaceutical Products Dataset** using a two-stage hybrid matching algorithm:
  1. *Phonetic Filtering:* Double Metaphone encoding to retrieve phonetically similar drug candidates.
  2. *Token-Sort Levenshtein Distance (RapidFuzz):* Re-ranks candidates and computes a confidence score ($0.0 - 1.0$). If confidence is below $0.80$, the top candidate matches are presented in the Human Review Screen for user selection.
- **Consequences:**  
  - *Positive:* Robust against typical OCR typographical noise; standardizes brand and generic naming conventions; automatically cross-checks plausible strengths.
  - *Negative:* Requires bundling or caching the MOH dataset (approx. 20,000–30,000 registered product entries, requiring efficient indexing).
- **Alternatives Considered:**  
  - *Exact String Matching:* Rejected because minor OCR noise causes 100% lookup failure.
  - *Western Databases (RxNorm / FDA NDC):* Rejected because product names, brand names, and registered dosage strengths in Malaysia differ substantially from US/European registries.

---

## 3. Architectural Trade-offs Analysis

| Architectural Dimension | Approach A (Chosen) | Approach B (Alternative) | Justification for Choice |
| :--- | :--- | :--- | :--- |
| **Extraction Paradigm** | **Modular Pipeline** (Quality $\rightarrow$ OCR $\rightarrow$ IE $\rightarrow$ Lookup) | **End-to-End Multimodal VLM** | Modularity provides strict auditability, token-level coordinates, determinism, and zero hallucination risk. |
| **Conflict & Failure Handling** | **Hard Stop Branch (Flag for Pharmacist)** | **Autonomous Conflict Resolution** | AI must never guess or resolve drug conflicts; clinical safety mandates escalating unresolved issues to professionals. |
| **Verification Gate** | **Mandatory Human Review Screen** | **Zero-Click Instant Output** | In medical adherence, patient safety overrides convenience. Mitigates automation bias. |
| **Reference Grounding** | **Local MOH Dataset (RapidFuzz)** | **Online LLM Knowledge Retrieval** | Localized MOH dataset provides official Malaysian regulatory truth without external API latency or privacy leaks. |
| **Data Privacy Architecture** | **In-Memory Ephemeral Session** | **Persistent Cloud Database** | Minimizes compliance complexity under PDPA 2010 by avoiding permanent storage of unconsented patient medical slips. |

---

## 4. Traceability Matrix

This matrix establishes end-to-end traceability between project requirements, architectural components, source code files, and evaluation criteria:

| Requirement ID | Requirement Summary | Architecture Diagram Component | Primary Implementation File | Verification & Evaluation Metric |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | Multi-image file ingestion | Web Interface (Streamlit) | [`app.py`](../app.py) | Upload stress testing & MIME validation |
| **FR-02** | Image preprocessing & quality check | Image Quality Check | [`src/ocr.py`](../src/ocr.py) | Image contrast score & CER improvement |
| **FR-03** | OCR printed text extraction | OCR Engine | [`src/ocr.py`](../src/ocr.py) | CER $\le 10\%$, WER $\le 18\%$ |
| **FR-04** | Entity extraction (Name, Dose, Freq) | Information Extraction | [`src/extraction.py`](../src/extraction.py) | Extraction F1-Score $\ge 85\%$ |
| **FR-05** | Bilingual translation (Malay/English) | Information Extraction | [`src/extraction.py`](../src/extraction.py) | Frequency & timing mapping accuracy $\ge 95\%$ |
| **FR-06** | MOH Reference Grounding | Medicine Reference Lookup | [`src/extraction.py`](../src/extraction.py) & `data/` | Top-1 Accuracy $\ge 80\%$, Top-3 $\ge 90\%$ |
| **FR-07** | Uncertainty confidence scoring | Validation & Uncertainty Checks | [`src/validation.py`](../src/validation.py) | Uncertainty Recall $\ge 90\%$ |
| **FR-08** | Duplicate active ingredient check | Validation & Uncertainty Checks | [`src/validation.py`](../src/validation.py) | Conflict Detection Rate $\ge 95\%$ |
| **FR-09** | Visual crop traceability | Human Review Screen | [`app.py`](../app.py) | Bounding box spatial intersection over union (IoU) |
| **FR-10** | Interactive correction & editing | Human Review Screen | [`app.py`](../app.py) | User edit latency $< 200\text{ ms}$ |
| **FR-11** | Consolidated timetable generation | Timetable Generator | [`src/timetable.py`](../src/timetable.py) | Schedule Slot Accuracy $\ge 92\%$ |
| **FR-12** | Structured JSON / summary export | Timetable Review & Reminder Plan | [`app.py`](../app.py) & [`src/timetable.py`](../src/timetable.py) | Schema validation against target JSON spec |
| **NFR-1** | Latency $< 5\text{s}$ per image | Pipeline Performance | [`app.py`](../app.py), [`src/ocr.py`](../src/ocr.py) | Turnaround latency benchmark |
| **NFR-2** | Usability & Accessibility | Human Review & Timetable Review | [`app.py`](../app.py) | System Usability Scale (SUS) $\ge 70$ |
| **NFR-3** | Decision Gate: Hard Stop on Conflict | Decision Gate & Stop Branch | [`app.py`](../app.py), [`src/validation.py`](../src/validation.py) | 0% unverified schedule generation |
| **NFR-4** | End-to-end coordinate audit trail | Cross-Cutting Safeguards | [`src/extraction.py`](../src/extraction.py) | 100% bidirectional traceability |
| **NFR-5** | Modularity & decoupling | System Pipeline Design | [`src/`](../src/) package design | Code maintainability index & unit tests |
