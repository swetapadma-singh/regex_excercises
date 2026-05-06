import spacy

nlp = spacy.load("en_core_web_sm")

def extract_names_ner(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

def extract_dates_ner(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ == "DATE"]
