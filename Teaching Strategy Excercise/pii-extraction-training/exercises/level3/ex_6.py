import spacy
from utils.ner_model import extract_names_ner

text = "Patient was seen by Dr. John Smith and Nurse Jane Doe."

persons = extract_names_ner(text)
print("persons = ",persons)