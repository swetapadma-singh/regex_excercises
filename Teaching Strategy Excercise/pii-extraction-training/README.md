# 🏥 Medical PII Extraction Pipeline

## 📌 Overview
This project extracts **Personally Identifiable Information (PII)** such as:
- Names
- Dates (Report Date, DOB, Appointment, etc.)
- Roles (Doctor, Patient, Nurse)

from **medical PDF reports**.

The pipeline handles:
- Scanned PDFs (using OCR)
- Noisy / messy medical text
- Multiple date formats
- Duplicate and variant names

---

## ⚙️ Pipeline Flow

### Step-by-step:

1. **PDF to Text**
   - Uses `PyMuPDF (fitz)` and `pytesseract` (OCR)
   - Supports multi-page PDFs

2. **Text Cleaning**
   - Removes noise, special characters, OCR artifacts

3. **Name Extraction**
   - Regex-based extraction
   - spaCy NER (`PERSON`)
   - Combines both results

4. **Date Extraction**
   - Regex-based (primary)
   - Supports multiple formats:
     - `DD/MM/YYYY`
     - `YYYY-MM-DD`
     - `12 May 2024`

5. **Date Classification**
   - Uses keyword-based context detection:
     - Report Date
     - Appointment Date
     - DOB
     - Service Date
     - Admission/Discharge

6. **Name Clustering**
   - Groups similar names using fuzzy matching
   - Example:
     ```
     Dr. John Doe → John Doe → J. Doe
     ```

7. **Role Detection**
   - Based on keywords:
     - doctor
     - patient
     - nurse

8. **Final Output**
   - Structured JSON

---

## 📁 Project Structure
project/
│
├── data/
│ ├── raw/ # Input PDFs
│ └── expected/ # Output JSON
│
├── utils/
│ ├── text_cleaning.py
│ ├── regex_patterns.py
│ ├── ner_model.py
│ ├── normalization.py
│ └── fuzzy_match.py
│
├── exercises/
│ └── level10/
│ └── ex_20.py # Main pipeline
│
└── README.md


---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install spacy pytesseract pymupdf pillow rapidfuzz
python -m spacy download en_core_web_sm

python -m exercises.level10.ex_20 # Run The Pipeline

### Example Output

{
  "names": {
    "entities": [
      {
        "canonical_name": "John Doe",
        "variants": ["Dr. John Doe", "John Doe"],
        "role": "doctor"
      }
    ]
  },
  "dates": [
    {
      "text": "12/05/2024",
      "normalized": "2024-05-12",
      "type": "report_date"
    }
  ]
}