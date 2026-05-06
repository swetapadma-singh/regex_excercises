import pdfplumber

def extract_pages(file_path):
    pages_data = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()

            pages_data.append({
                "page": i,
                "text": text if text else ""
            })

    return pages_data

data = extract_pages("Medical Report Multipage.pdf")

for page in data:
    print(f"Page {page['page']}:\n{page['text']}\n")