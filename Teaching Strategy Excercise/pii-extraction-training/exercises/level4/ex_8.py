# Hybrid Extraction (Real World) (Merge Regex + NER Results)
# import re
# import spacy

# nlp = spacy.load("en_core_web_sm")
# text = "Patient was seen by Dr. John Smith and Nurse Jane Doe."
# regex_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'
# regex_matches = []
# for match in re.finditer(regex_pattern, text):
#     regex_matches.append({
#         "text": match.group(),
#         "start": match.start(),
#         "end": match.end(),
#         "source": "regex"
#     })

# doc = nlp(text)
# ner_matches = []
# for ent in doc.ents:
#     if ent.label_ == "PERSON":
#         ner_matches.append({
#             "text": ent.text,
#             "start": ent.start_char,
#             "end": ent.end_char,
#             "source": "ner"
#         })

# def is_overlap(span1, span2):
#     return not (span1["end"] <= span2["start"] or span2["end"] <= span1["start"])

# merged = []

# all_matches = ner_matches + regex_matches

# for match in all_matches:
#     overlap_found = False
#     for m in merged:
#         if is_overlap(match, m):
#             overlap_found = True
#             break
#     if not overlap_found:
#         merged.append(match)

# final_entities = [m["text"] for m in merged]
# print(final_entities)

from utils.regex_patterns import extract_names_regex
from utils.ner_model import extract_names_ner

def merge(regex_list, ner_list):
    return list(set(regex_list + ner_list))

text = "Patient was seen by Dr. John Smith and Nurse Jane Doe."

r = extract_names_regex(text)
n = extract_names_ner(text)

print(merge(r, n))