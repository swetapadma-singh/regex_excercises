import re

PATTERNS = [
    r"\bDr\.?\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b",
    r"\b[A-Z][a-z]+\s+[A-Z][a-z]+,\s*MD\b",
    r"\b[A-Z]{2,},\s*[A-Z]{2,}\b",
    r"\b[A-Z]\.\s+[A-Z][a-z]+\b"
]

compiled_patterns = [re.compile(p) for p in PATTERNS]

def extract_names_regex(text):
    results = []
    for pattern in compiled_patterns:
        for match in pattern.finditer(text):
            results.append(match.group())
    return list(set(results))

def extract_dates_regex(text):
    date_patterns = [
        r"\b\d{2}/\d{2}/\d{4}\b",   # 12/05/2024
        r"\b\d{2}-\d{2}-\d{4}\b",   # 12-05-2024
        r"\b\d{4}-\d{2}-\d{2}\b",   # 2024-05-12
        r"\b\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4}\b",  # 12 May 2024
    ]

    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, text, flags=re.IGNORECASE))

    return list(set(dates))
