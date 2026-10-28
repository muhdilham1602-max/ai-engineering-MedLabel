# Week 2 — System Evaluation Criteria & Methodology

**Project:** MedLabel (AI-Based Multi-Prescription Recognition and Medication Timetable Generation)  
**Document Version:** 1.0  
**Date:** October 28, 2026  
**Author:** MedLabel Engineering Team  

---

## 1. Overview and Evaluation Objectives
The objective of this evaluation framework is to establish rigorous, repeatable, and quantifiable benchmarks for each phase of the MedLabel pipeline:
1. **Perceptual Quality & Text Extraction (OCR Engine)**
2. **Information Extraction & Semantic Slot Filling**
3. **Reference Matching against Malaysian Pharmaceutical Data**
4. **Safety, Uncertainty, and Conflict Detection**
5. **Timetable Synthesis Correctness**
6. **System Usability and Human-in-the-Loop Verification Efficiency**

---

## 2. Evaluation Criteria Matrix

| Subsystem / Task | Evaluation Metric | Measurement Method | Minimum Acceptable Threshold | Target / Ideal Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **Image Preprocessing & OCR** | **Character Error Rate (CER)** | Levenshtein distance on character level between OCR transcript and ground truth text across test images: $\text{CER} = \frac{S + D + I}{N_c}$ | $\le 10.0\%$ | $\le 3.5\%$ on printed dispensing labels |
| **Image Preprocessing & OCR** | **Word Error Rate (WER)** | Levenshtein distance on word level: $\text{WER} = \frac{S_w + D_w + I_w}{N_w}$ | $\le 18.0\%$ | $\le 7.0\%$ on printed dispensing labels |
| **Entity Extraction (Slot Filling)** | **Entity Precision (P)** | Exact and token-level matching of extracted entities (Medication, Strength, Dosage, Frequency, Route, Timing): $P = \frac{TP}{TP + FP}$ | $\ge 85.0\%$ | $\ge 95.0\%$ |
| **Entity Extraction (Slot Filling)** | **Entity Recall (R)** | Proportion of ground-truth entities successfully captured: $R = \frac{TP}{TP + FN}$ | $\ge 80.0\%$ | $\ge 92.0\%$ |
| **Entity Extraction (Slot Filling)** | **Entity F1-Score** | Harmonic mean of Precision and Recall: $F_1 = 2 \cdot \frac{P \cdot R}{P + R}$ | $\ge 82.5\%$ | $\ge 93.5\%$ |
| **Reference Grounding** | **Top-1 Match Accuracy** | Proportion of extracted drug names matching the correct registered MOH entity as first choice | $\ge 80.0\%$ | $\ge 92.0\%$ |
| **Reference Grounding** | **Top-3 Match Accuracy** | Proportion of ground truth registered drugs contained within top 3 fuzzy/phonetic search candidates | $\ge 90.0\%$ | $\ge 98.0\%$ |
| **Uncertainty & Safety Detection** | **Uncertainty Recall** | Percentage of low-quality, ambiguous, or damaged tokens correctly flagged ($\tau < 0.80$) | $\ge 90.0\%$ | $\ge 98.0\%$ |
| **Conflict Detection** | **Conflict Detection Rate (Recall)** | Percentage of intentional test conflicts (e.g. duplicate active ingredients, incompatible timings) detected and alerted | $\ge 95.0\%$ | $100.0\%$ (Zero missed critical conflicts) |
| **Timetable Generation** | **Slot Placement Accuracy** | Percentage of confirmed medications placed into correct chronological time slots (Morning, Afternoon, Evening, Night) matching prescription intent | $\ge 92.0\%$ | $\ge 98.0\%$ |
| **Timetable Generation** | **Instruction Completeness** | Percentage of timetable entries that accurately preserve food intake conditions (*Before Food* / *After Food*) | $\ge 90.0\%$ | $\ge 99.0\%$ |
| **Human Verification & Usability** | **Time-to-Verification (TTV)** | Average time required for a user to review, correct, and confirm a 3-prescription batch | $\le 90\text{ seconds}$ | $\le 45\text{ seconds}$ |
| **End-to-End System** | **System Usability Scale (SUS)** | Standard 10-item Likert SUS questionnaire administered across test user cohort | $\ge 70 / 100$ (Grade B) | $\ge 85 / 100$ (Grade A) |

---

## 3. Metric Definitions & Formulas

### 3.1 Character Error Rate (CER) and Word Error Rate (WER)
$$\text{CER} = \frac{S + D + I}{N}$$
Where:
- $S$ = Number of character substitutions
- $D$ = Number of character deletions
- $I$ = Number of character insertions
- $N$ = Total number of characters in the ground truth text

### 3.2 Information Extraction F1-Score (Per Slot)
Evaluated across six core slots:
1. `MEDICATION_NAME`: Generic or commercial brand name
2. `STRENGTH`: Active numerical strength + unit (e.g., `500 mg`, `10 mg/5ml`)
3. `DOSAGE`: Quantity to be ingested per administration (e.g., `1 tablet`, `2 drops`)
4. `FREQUENCY`: Standard interval / frequency abbreviation (`OD`, `BD`, `TDS`, `QID`, `PRN`) or Malay equivalent
5. `TIMING_CONDITION`: Meal relationship (`Before food / AC`, `After food / PC`, `Bedtime / ON`)
6. `DURATION`: Length of course (e.g., `5 days`, `1 month`)

$$\text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}}$$
$$\text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}$$
$$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

### 3.3 Conflict Detection Recall
$$\text{Conflict Recall} = \frac{\text{Identified Clinical Inconsistencies}}{\text{Total Seeded Inconsistencies}} \times 100\%$$
Evaluated on an adversarial test subset containing:
- Duplicate active ingredient prescriptions (e.g., *Panadol 500mg* and *Uphamol 500mg* prescribed concurrently).
- Excessive cumulative daily frequency (e.g., total paracetamol intake exceeding 4000mg/day).
- Conflicting meal instructions for the same drug across different clinic visits.

---

## 4. Test Datasets and Annotation Protocol

### 4.1 Evaluation Dataset Splits
To prevent data contamination and ensure ecological validity, the test suite is partitioned as follows:

| Split | Description | Quantity | Source |
| :--- | :--- | :--- | :--- |
| **Set A (Printed Dispensing Labels)** | High-resolution photos of printed adhesive pharmacy labels from Malaysian pharmacies and KKM clinics. | 50 images | Curated & de-identified local labels |
| **Set B (Synthetic Augmented Prescriptions)** | Synthetically rendered prescriptions with simulated camera degradation (motion blur, specular reflections, skew $\pm 15^\circ$, low lighting). | 100 images | Programmatically rendered with Pillow |
| **Set C (Adversarial & Conflict Test Set)** | Pairs of prescriptions designed specifically to test duplicate therapy, ambiguous handwriting/printing, and missing dosage fields. | 30 image pairs | Clinical edge-case design |
| **Set D (Open Benchmark - Mendeley)** | Bangladesh Prescription Dataset sample subset to evaluate generalization across varied camera types. | 40 images | Mendeley Data repository |

### 4.2 Ground Truth Annotation Standard
- Ground truth is stored in structured JSON files with character-level text transcription, polygon bounding coordinates, and normalized entity attributes:
```json
{
  "image_id": "kkm_label_042.jpg",
  "transcription": "TAB METFORMIN 500MG\n1 BIJI 2 KALI SEHARI\nSELEPAS MAKAN",
  "entities": {
    "medication_name": "Metformin",
    "strength": "500 mg",
    "dosage": "1 biji",
    "frequency": "BD",
    "timing_condition": "pc",
    "duration": null
  },
  "moh_reference_match": {
    "product_name": "METFORMIN HYDROCHLORIDE TABLETS 500MG",
    "mal_number": "MAL19910814AZ"
  }
}
```

---

## 5. Failure Mode Analysis & Edge Case Protocols

| Failure Mode | Impact | System Protocol / Mitigation |
| :--- | :--- | :--- |
| **Severe Image Blur / Low Contrast** | OCR produces garbled strings or misses lines. | Quality gate flags image during preprocessing; prompts user to retake photo under better lighting. |
| **Look-Alike / Sound-Alike Drug Names (LASA)** | Extracted name matches wrong drug in reference list. | Display top 3 candidate matches in verification UI with matching confidence scores; user selects correct drug. |
| **Omitted Frequency (e.g. "Take as directed")** | System cannot determine timetable placement slot. | Flagged as *Incomplete Instruction*; placed in a separate "As Directed / Consult Pharmacist" review bucket. |
| **Conflicting Duplicate Prescriptions** | Overdose risk if patient takes both. | Prominent amber warning modal rendered in Streamlit before timetable generation is allowed. |
