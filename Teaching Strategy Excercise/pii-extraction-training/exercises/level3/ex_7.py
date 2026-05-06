# Compare Regex vs NER
import re
from utils.ner_model import extract_names_ner

text = "Patient was seen by Dr. John Smith and Nurse Jane Doe. Contact: 9876543210"

regex_names = re.findall(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', text)
ner_names = extract_names_ner(text)

regex_set = set(regex_names)
ner_set = set(ner_names)

output = {
    "regex_set": list(regex_set),
    "ner_set": list(ner_set),
    "regex_only": list(regex_set - ner_set),
    "ner_only": list(ner_set - regex_set),
    "common": list(regex_set & ner_set)
}

print(output)