import re

def fix_ocr_errors(text):
    original = text
    corrections = {
        "0": "o",
        "1": "i",
        "5": "s",
        "8": "b"
    }

    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)

    text = re.sub(r'\b(Dr|Mr|Mrs|Ms)\s+\.', r'\1.', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.title()

    return {
        "original": original,
        "cleaned": text
    }

inputs = ["J0hn Sm1th", "Dr . John"]

for i in inputs:
    print(fix_ocr_errors(i))