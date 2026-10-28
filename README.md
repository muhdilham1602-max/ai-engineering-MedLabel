# MedLabel

MedLabel is a Streamlit-based prototype for reviewing uploaded prescription images and preparing for future OCR and medication extraction workflows.

## Overview
This project is designed to help users:
- upload one or more prescription images
- preview the uploaded images in a simple interface
- support future OCR-based recognition of medication details
- prepare for medication timetable generation from verified instructions

## Current Features
- Upload multiple prescription images
- Preview uploaded prescription images in the app
- Simple, clean Streamlit interface

## Planned Features
- OCR-based text recognition from prescription photos
- Medication information extraction
- Human verification of extracted data
- Uncertainty warnings for ambiguous instructions
- Medication timetable generation from validated records

## Tech Stack
- Python
- Streamlit
- Pillow

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
├── app.py
├── README.md
├── requirements.txt
```

## Disclaimer
This application is a prototype designed for research and educational use only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always verify medication instructions with a qualified healthcare professional.

## License
This project is currently provided as a prototype without a formal license.
