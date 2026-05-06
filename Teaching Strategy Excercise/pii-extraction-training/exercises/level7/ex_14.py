import spacy
from utils.ner_model import extract_names_ner

nlp = spacy.load("en_core_web_sm")
text = "Dr. John Smith examined patient Mary Jane. Nurse Alex assisted."
doc = nlp(text)
names = extract_names_ner(text)
results = []

for name in names:
    for ent in doc.ents:
        if ent.text == name and ent.label_ == "PERSON":

            start = max(ent.start - 3, 0)
            end = min(ent.end + 3, len(doc))

            context = doc[start:end].text.lower()

            role = "Unknown"

            if "dr" in context or "doctor" in context:
                role = "Doctor"
            elif "nurse" in context:
                role = "Nurse"
            elif "patient" in context:
                role = "Patient"

            results.append({
                "name": name,
                "role": role
            })
            break
print(results)