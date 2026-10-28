# System Map

## Main Workflow
1. User uploads prescription images.
2. App previews uploaded images.
3. OCR module extracts text from images.
4. Extraction module identifies medication details.
5. Validation layer checks ambiguous or uncertain fields.
6. Timetable module organizes medication schedule.

## Components
- Frontend: Streamlit app
- OCR: `src/ocr.py`
- Extraction: `src/extraction.py`
- Validation: `src/validation.py`
- Timetable generation: `src/timetable.py`
