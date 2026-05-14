import pdfplumber, re

def extract_data(text):
    pattern = r"(?:Patient Name|Patient|Dr\.?)[:\s]+([A-Z][a-z]+(?: [A-Z][a-z]+)+)"
    names = re.findall(pattern, text)
    return names

text = ""

with pdfplumber.open("data/pdf/Text PDF 1.pdf") as pdf:
    for page in pdf.pages:
        text += page.extract_text()  

print(extract_data(text))    