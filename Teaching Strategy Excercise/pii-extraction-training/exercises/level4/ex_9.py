import re
import spacy

nlp = spacy.load("en_core_web_sm")

text = "Patient was seen by Dr. John Smith and Nurse Jane Doe."

regex_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'
regex_matches = []

for match in re.finditer(regex_pattern, text):
    regex_matches.append({
        "text": match.group(),
        "start": match.start(),
        "end": match.end(),
        "source": "regex"
    })

doc = nlp(text)

ner_matches = []
for ent in doc.ents:
    if ent.label_ == "PERSON":
        ner_matches.append({
            "text": ent.text,
            "start": ent.start_char,
            "end": ent.end_char,
            "source": "ner"
        })

def is_overlap(a, b):
    return not (a["end"] <= b["start"] or b["end"] <= a["start"])

final = []

all_matches = regex_matches + ner_matches

used = set()

for i, m1 in enumerate(all_matches):
    if i in used:
        continue

    matched_sources = {m1["source"]}
    
    for j, m2 in enumerate(all_matches):
        if i != j and is_overlap(m1, m2):
            matched_sources.add(m2["source"])
            used.add(j)

    used.add(i)

    if len(matched_sources) == 2:
        confidence = 0.98
    elif "regex" in matched_sources:
        confidence = 0.95
    else:
        confidence = 0.85

    final.append({
        "text": m1["text"],
        "confidence": confidence
    })

print(final)