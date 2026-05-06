import pdfplumber

file_path = "Medical Report.pdf"
all_text = ""

with pdfplumber.open(file_path) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        text = page.extract_text()
        
        if text:
            all_text += f"\n--- Page {page_num} ---\n"
            all_text += text

print(all_text)