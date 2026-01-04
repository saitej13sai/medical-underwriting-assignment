# Medical Underwriting Engine (Deterministic)

Deterministic medical data extraction + configurable underwriting rules engine.
Not a chatbot. No AI agent frameworks.

## What it extracts
- Patient: age, gender
- Dates: report/collected/approved/printed (when present)
- Labs: HbA1c, FBS, PPBS, Creatinine, eGFR, BP (SBP/DBP)
- Diagnoses: keyword-based (configurable)
- Medications: mapped to generic via config CSV

## How it works
1) For PDFs: extract embedded text using pdfplumber
2) If PDF text is too small: OCR fallback (pdf2image + pytesseract)
3) Images: OCR using pytesseract
4) Labs parsed with deterministic regex rules
5) Rules applied from config/underwriting_rules.csv with explanations

## Install
pip install -r requirements.txt

System dependencies:
- Tesseract OCR installed and in PATH
- Poppler installed and in PATH (required by pdf2image)

## Run
python main.py --input "input_samples/drkkreport.jpeg"
python main.py --input "input_samples/sterling-accuris-pathology-sample-report-unlocked.pdf"

Output is written to:
output/result.json
