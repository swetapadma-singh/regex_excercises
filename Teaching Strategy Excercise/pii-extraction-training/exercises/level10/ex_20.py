import re
import fitz
import spacy
import json
import pytesseract
from PIL import Image
from utils.text_cleaning import clean_text
from utils.regex_patterns import extract_names_regex, extract_dates_regex
from utils.ner_model import extract_names_ner
from utils.normalization import normalize_name, normalize_date
from utils.fuzzy_match import similarity

nlp = spacy.load("en_core_web_sm")

DATE_KEYWORDS = {
    "service_date": ["dos", "date of study", "date of read"],
    "report_date": ["report", "generated", "issued", "date of report"],
    "appointment_date": ["appointment", "visit", "next visit", "follow up"],
    "admission_date": ["admitted", "admission"],
    "discharge_date": ["discharged", "discharge"],
    "dob": ["dob", "date of birth", "born"],
}

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = ""

    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        text = pytesseract.image_to_string(img)
        full_text += text + "\n"

    return full_text

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def build_spans_from_names(text, names, source):
    spans = []
    for name in names:
        for match in re.finditer(re.escape(name), text):
            spans.append({
                "text": name,
                "start": match.start(),
                "end": match.end(),
                "source": source
            })
    return spans

def build_spans_from_dates(text, dates, source):
    spans = []
    for date in dates:
        for match in re.finditer(re.escape(date), text):
            spans.append({
                "text": date,
                "start": match.start(),
                "end": match.end(),
                "source": source
            })
    return spans

def extract_names(text):
    results = []

    regex_names = extract_names_regex(text)
    results += build_spans_from_names(text, regex_names, "regex")

    ner_names = extract_names_ner(text)
    results += build_spans_from_names(text, ner_names, "ner")

    return results

def extract_dates(text):
    results = []
    regex_dates = extract_dates_regex(text)
    results += build_spans_from_dates(text, regex_dates, "regex")

    return results

def get_context(text, start, end, window=50):
    left = max(0, start - window)
    right = min(len(text), end + window)
    return text[left:right].lower()

def detect_date_type(date_span, full_text):
    context = get_context(full_text, date_span["start"], date_span["end"])

    for label, keywords in DATE_KEYWORDS.items():
        for kw in keywords:
            if kw in context:
                return label

    return "unknown"

def classify_dates(dates, full_text):
    classified = []

    for d in dates:
        date_type = detect_date_type(d, full_text)

        classified.append({
            "text": d["text"],
            "normalized": normalize_date(d["text"]),
            "type": date_type,
            "start": d["start"],
            "end": d["end"]
        })

    return classified

def detect_role(variants, full_text):
    for v in variants:
        v_lower = v.lower()

        if "dr" in v_lower or "doctor" in v_lower:
            return "doctor"
        elif "nurse" in v_lower:
            return "nurse"
        elif "patient" in v_lower:
            return "patient"

    return "unknown"

def cluster_entities(names, threshold=85):
    clusters = []

    for item in names:
        norm = normalize_name(item["text"])
        added = False

        for cluster in clusters:
            rep = normalize_name(cluster[0]["text"])
            score = similarity(norm, rep)

            if score >= threshold:
                cluster.append(item)
                added = True
                break

        if not added:
            clusters.append([item])

    return clusters

def build_output(clusters, full_text):
    output = []

    for cluster in clusters:
        variants = list(set([c["text"] for c in cluster]))
        canonical = max(variants, key=len)

        role = detect_role(variants, full_text)

        output.append({
            "canonical_name": canonical,
            "variants": variants,
            "role": role
        })

    return {"entities": output}

def process_pdfs(file_paths):
    all_text = ""

    for path in file_paths:
        if path.endswith(".pdf"):
            text = extract_text_from_pdf(path)
        elif path.endswith(".txt"):
            text = extract_text_from_txt(path)

        text = clean_text(text) 
        all_text += text + "\n"
    extracted = extract_names(all_text)
    clusters = cluster_entities(extracted)
    extracted_dates = extract_dates(all_text)
    classified_dates = classify_dates(extracted_dates, all_text)
    result = {
        "names": build_output(clusters, all_text),
        "dates": classified_dates
    }

    return result

files = ["data/raw/chunk_0002.txt"]

result = process_pdfs(files)

with open("data/expected/final_entities.json", "w") as f:
    json.dump(result, f, indent=4)

print(result)