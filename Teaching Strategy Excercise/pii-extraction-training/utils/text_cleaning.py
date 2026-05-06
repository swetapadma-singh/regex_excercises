import re

def clean_text(text):
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r'([A-Za-z]{1,})\s+([a-z])',r'\1\2',text)  # fix broken words
    text = re.sub(r'\s+',' ',text)
    return text.strip()
