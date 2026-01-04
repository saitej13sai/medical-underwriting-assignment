# Medical Underwriting Engine (Deterministic)

A **deterministic medical data extraction and underwriting rules engine**.  
This project is **not a chatbot**, **not an AI assistant**, and does **not** use any AI agent frameworks.

The focus is on **correctness, explainability, configurability, and underwriting safety**.

---

##  What This Engine Extracts

### Patient
- Name (only when explicitly labeled; otherwise `null`)
- Age
- Gender

### Dates (when present)
- Report date
- Sample collected date
- Approved / Printed date

### Lab Values
- Hemoglobin
- HbA1c
- Fasting Blood Sugar (FBS)
- Post-Prandial Blood Sugar (PPBS)
- Creatinine
- eGFR
- Blood Pressure (SBP / DBP)

### Diagnoses
- Keyword-based detection
- Fully configurable via `config/diagnosis_keywords.csv`
- **Explicit diagnoses override lab-based risk**

### Medications
- Extracted from report text
- Mapped to generic names via `config/medication_mapping.csv`

---

## ⚙️ How It Works

1. **PDF Handling**
   - Extract embedded text using `pdfplumber`
   - If PDF text is fragmented or missing → OCR fallback

2. **Image Handling**
   - OCR using `pytesseract`

3. **Parsing**
   - Deterministic regex-based parsing
   - No probabilistic inference
   - Safe failure on ambiguous layouts

4. **Underwriting Rules**
   - Loaded from `config/underwriting_rules.csv`
   - No hard-coded thresholds
   - Each risk flag includes a plain-English explanation

---

## Installation

### Python Dependencies
```bash
pip install -r requirements.txt
````

### System Dependencies (Required)

#### Tesseract OCR

* Must be installed and available in PATH
* [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)

#### Poppler (for PDFs with OCR fallback)

* Required by `pdf2image`
* [https://github.com/oschwartz10612/poppler-windows](https://github.com/oschwartz10612/poppler-windows)

---

## How to Run

### Image Input

```bash
python main.py --input "input_samples/drkkreport.jpeg"
```

### PDF Input (Relative Path)

```bash
python main.py --input "input_samples/sterling-accuris-pathology-sample-report-unlocked.pdf"
```

### PDF Input (Absolute Windows Path)

```bash
python .\main.py --input "C:\Users\sai13\Downloads\sterling-accuris-pathology-sample-report-unlocked.pdf"
```

---

## Output

The engine writes structured underwriting output to:

```
output/result.json
```

---

## Tested Example Output

```json
{
  "meta": {
    "input": "C:\\Users\\sai13\\Downloads\\sterling-accuris-pathology-sample-report-unlocked.pdf",
    "method": "pdf_text"
  },
  "patient": {
    "name": "Lyubochka Svetka ",
    "age": 41,
    "gender": "male"
  },
  "lab_values": {
    "hemoglobin": 14.5,
    "hba1c": 7.1,
    "fbs": 141.0,
    "creatinine": 0.83
  },
  "diagnoses": {
    "explicit": [
      "Diabetes Mellitus",
      "Chronic Kidney Disease"
    ],
    "inferred": []
  },
  "medications": [
    {
      "raw": "metformin",
      "generic": "metformin"
    }
  ],
  "risk_assessment": {
    "overall_risk": "high",
    "flags": [
      {
        "parameter": "hemoglobin",
        "value": 14.5,
        "risk": "Normal",
        "explanation": "hemoglobin = 14.5 falls in 13.5\u201318.0 \u2192 Normal"
      },
      {
        "parameter": "hba1c",
        "value": 7.1,
        "risk": "Diabetes",
        "explanation": "hba1c = 7.1 falls in 6.5\u201399.0 \u2192 Diabetes"
      },
      {
        "parameter": "fbs",
        "value": 141.0,
        "risk": "High",
        "explanation": "fbs = 141.0 falls in 126.0\u2013999.0 \u2192 High"
      },
      {
        "parameter": "creatinine",
        "value": 0.83,
        "risk": "Normal",
        "explanation": "creatinine = 0.83 falls in 0.0\u20131.25 \u2192 Normal"
      }
    ]
  }
}
```

---

## Design Decisions

* Ambiguous or unlabeled fields are returned as `null`
* Explicit diagnoses always override lab-only risk
* No hallucination or machine-learning inference
* Deterministic and repeatable results across runs

---

## Project Structure

```
medical-underwriting-engine/
├── config/
├── extraction/
├── rules/
├── input_samples/
├── output/
├── main.py
├── requirements.txt
└── README.md
```

---

##  Status

* Deterministic
* Explainable
* Underwriting-safe
* Submission-ready

````

---

### After Pasting

Run:

```bash
git add README.md
git commit -m "Update README with usage and sample output"
git push
````

