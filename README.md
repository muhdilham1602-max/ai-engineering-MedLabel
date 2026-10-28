# MedLabel: AI-Based Multi-Prescription Recognition and Medication Timetable Generation

## 1. Project Overview
**Project Name:** MedLabel

**Domain:** Artificial Intelligence, Computer Vision, OCR and Healthcare Technology

**Project Description:**

MedLabel is an AI-assisted system designed to extract medication information from multiple prescription images and organize verified instructions into a consolidated medication timetable. The system uses Optical Character Recognition (OCR) and information extraction to identify medication names, strengths, dosages and prescribed frequencies. Users must review and confirm the extracted information before a timetable is generated.

## 2. Problem Statement
Patients who receive multiple prescriptions may need to refer to several documents to understand when and how their medications have been prescribed. Manually consolidating medication names, dosage instructions and administration frequencies can be time-consuming and may lead to overlooked instructions or transcription errors.

Existing OCR technology can extract text from images, but extracting text alone does not guarantee that medication instructions are interpreted correctly or organized safely. Prescription images may contain unclear text, incomplete information or conflicting instructions.

Therefore, this project proposes MedLabel, an AI-assisted system that extracts medication information from multiple prescription images, identifies uncertain or conflicting fields, and generates a consolidated timetable only after the user verifies the extracted instructions.

## 3. Project Objectives

1. To develop an OCR-based pipeline that extracts medication information from multiple prescription images.
2. To implement an information verification workflow that identifies uncertain or potentially conflicting instructions.
3. To evaluate the accuracy of information extraction and the correctness of timetables generated from verified prescription data.

## 4. Target Users

- **Patients:** Individuals who need to organize medication instructions from multiple prescriptions.
- **Caregivers:** People who help patients manage their prescribed medication schedules.
- **Healthcare professionals:** Potential reviewers who can provide feedback on the system's usability and safety requirements.

## 5. Scope of the Project

### Included Features

- Upload multiple prescription images.
- Extract printed text using OCR.
- Identify medication names, strengths, dosage instructions and frequencies where available.
- Match extracted medication names against a suitable Malaysian pharmaceutical reference.
- Flag unclear, incomplete or conflicting information.
- Allow users to review and correct extracted information.
- Generate a timetable using only verified prescription instructions.
- Evaluate the system using annotated test data.

### Excluded Features

- Diagnosing medical conditions.
- Recommending or changing medication doses.
- Automatically resolving prescription conflicts.
- Identifying pills solely from their appearance.
- Replacing advice from doctors or pharmacists.

The initial prototype will prioritize printed prescription information. Handwritten prescriptions may be considered if sufficient suitable data is available.

## 6. Related Work

### 6.1 Optical Character Recognition
OCR technologies, such as PaddleOCR and Google ML Kit Text Recognition, can extract text from images. However, OCR output may contain errors caused by blur, poor lighting, unusual layouts or small text.

**Relevance:** MedLabel can use an existing OCR engine as its starting point rather than training an OCR model from scratch.

### 6.2 Prescription Image Recognition Research
Research datasets containing handwritten and printed prescription images demonstrate how computer vision and text recognition can support prescription digitization. However, datasets from other countries may use different languages, medicine names and prescription formats.

**Relevance:** MedLabel requires evaluation using data that reflects the intended Malaysian use case.

### 6.3 Medication Scheduling Applications
Medication management applications, such as Medisafe, support medication schedules and reminders. These demonstrate the value of organizing medication routines digitally.

**Relevance:** MedLabel focuses on the earlier step of extracting and consolidating information from multiple prescription images before producing a timetable.

## 7. Engineering Gap
The project investigates how OCR, medication information extraction, reference matching, uncertainty detection and timetable generation can be combined into a single workflow for Malaysian prescription images.

The main engineering challenge is not simply recognizing text. It is ensuring that extracted instructions remain traceable to their source, uncertain information is flagged, and a timetable is generated only from user-verified data.

The project will investigate whether this workflow can achieve acceptable extraction accuracy and timetable correctness on a suitably annotated test dataset.

## 8. Proposed System Workflow

1. **Image upload:** The user uploads one or more prescription images.
2. **Image processing:** The system checks image quality and prepares images for OCR.
3. **Text recognition:** OCR extracts text from the images.
4. **Information extraction:** The system identifies medication names, strengths and prescribed instructions.
5. **Reference matching:** Extracted medicine names are compared with a relevant pharmaceutical reference.
6. **Uncertainty detection:** Missing, unclear or potentially conflicting information is flagged.
7. **User verification:** The user reviews the extracted information against the original prescriptions.
8. **Timetable generation:** The system organizes confirmed instructions into a timetable.
9. **Final review:** The user checks the timetable and seeks professional clarification when instructions are unclear or conflicting.

## 9. Data Sources

### Source 1: Malaysian Pharmaceutical Products Dataset
URL: [https://data.moh.gov.my/data-catalogue/pharmaceutical_products](https://data.moh.gov.my/data-catalogue/pharmaceutical_products)

This Malaysian Ministry of Health dataset provides pharmaceutical product information that may support medicine-name reference matching. It is a metadata source, not a collection of annotated prescription images.

### Source 2: Prescription Image Dataset
URL: [https://data.mendeley.com/datasets/k62rfd23kz/2](https://data.mendeley.com/datasets/k62rfd23kz/2)

This dataset contains handwritten and printed prescription images with annotations. It may support preliminary exploration of prescription recognition, but it is based on Bangladesh data and may not represent Malaysian prescription formats.

**Data limitation:** A suitable publicly available Malaysian prescription-image dataset has not yet been identified. The project will investigate the feasibility of collecting consented, de-identified images or using suitable public datasets for preliminary testing.

## 10. Evaluation Plan
The system will be evaluated using the following metrics:

- **Character Error Rate (CER):** Measures character-level OCR errors.
- **Word Error Rate (WER):** Measures word-level OCR errors.
- **Precision, Recall and F1-score:** Measures the accuracy of extracting medication fields.
- **Medicine-name matching accuracy:** Measures whether extracted names are matched correctly to reference entries.
- **Timetable correctness:** Measures whether generated entries accurately reflect the verified prescription instructions.
- **Uncertainty and conflict detection:** Measures how effectively the system flags predefined unclear or conflicting cases.

Test data should be separated at the prescription or patient level where applicable to reduce data leakage between training and evaluation sets.

## 11. Responsible AI and Risks

### Risk 1: Incorrect Medication Information
OCR or information extraction errors could result in an incorrect timetable.

**Mitigation:** Preserve the original prescription image, flag uncertain fields, require user verification and never infer missing doses or automatically resolve conflicts.

### Risk 2: Patient Privacy
Prescription images may contain names, identity numbers and sensitive medical information.

**Mitigation:** Use consented and de-identified data, minimize data collection, restrict access and avoid uploading real patient records to a public GitHub repository.

### Additional Consideration: Automation Bias
Users may trust AI-generated results without checking them.

**Mitigation:** Clearly label the system as a prototype, display the original source alongside extracted information and require review before timetable generation.

## 12. Limitations

- OCR performance may decrease on blurred, poorly lit or handwritten prescriptions.
- The available public datasets may not reflect Malaysian prescription formats.
- Medicine-name matching may be affected by abbreviations, spelling errors and similar product names.
- Prescription instructions may be incomplete or inconsistent.
- A successful OCR result does not establish that a prescription is clinically appropriate.

## 13. Expected Outcome
The expected outcome is a working prototype that accepts multiple prescription images, extracts medication information, supports user verification, flags uncertainty and generates a consolidated timetable from confirmed instructions.

The project will assess the feasibility and reliability of this workflow rather than claim that AI can independently determine safe medication use.

## 14. Conclusion
MedLabel aims to reduce the manual effort involved in organizing information from multiple prescriptions. By combining OCR, information extraction, reference matching and human verification, the project investigates a practical AI engineering solution while prioritizing accuracy, traceability and patient privacy.

## Installation
1. Open a terminal in the project folder.
2. Create and activate a virtual environment if needed.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the App
```bash
streamlit run app.py
```

If Streamlit is not recognized, use:

```bash
python -m streamlit run app.py
```

## Project Structure
```text
MedLabel/
├── README.md
├── app.py
├── requirements.txt
├── .gitignore
├── docs/
│   ├── week1_project_scope.md
│   ├── observation_sheet.md
│   └── system_map.md
├── data/
│   └── README.md
├── src/
│   ├── ocr.py
│   ├── extraction.py
│   ├── validation.py
│   └── timetable.py
└── evaluation/
    └── evaluation_plan.md
```

## Disclaimer
This application is a prototype designed for research and educational use only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always verify medication instructions with a qualified healthcare professional.

## License
This project is currently provided as a prototype without a formal license.
