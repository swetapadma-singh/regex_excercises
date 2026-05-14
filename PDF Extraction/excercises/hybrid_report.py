import pdfplumber, pytesseract, camelot, re, warnings, json
from pdf2image import convert_from_path

def extract_all_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
                text += page.extract_text()
    return text  

def extract_all_table_text(path):
    table_txt = ""
    warnings.filterwarnings("ignore")
    tables = camelot.read_pdf(path, pages="all", flavor="stream")  
    all_tables_text = []

    for table in tables:
        df = table.df  
        text = " ".join(
            " ".join(str(cell) for cell in row)
            for row in df.values
        )
        all_tables_text.append(text)

    table_txt = " ".join(all_tables_text)
    return table_txt

def extract_all_image_text(path):
    img_text = ""
    images = convert_from_path(path)
    for img in images:
        img_text += pytesseract.image_to_string(img)
    return img_text           

def merge_all_text(path):
    # text = extract_all_text(path)
    img_text = extract_all_image_text(path)
    print("image text ==> ",img_text)
    # table_txt = extract_all_table_text(path)
    all_text = "text" + img_text + "table_txt"
    with open("data/txt/all_text.txt", "w", encoding="utf-8") as file:
        file.write(all_text)
    return all_text     

def extract_patient_info(text):
    patient_info = {}
    
    name = re.search(r"Patient Name\s*[:\-]?\s*(.+?)(?=\s*Date of Service|\n|$)",text,re.IGNORECASE)
    dob = re.search(r"(?:\bDOB|Date of Birth\b)\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",text,re.IGNORECASE)
    match = re.search(r"(\d+)Y\s+(Male|Female|Other)", text, re.IGNORECASE)
    phone = re.search(r"(?:\bPhone|Mobile|Contact(?: No)?\b)\s*[:\-]?\s*(\+?\d[\d\s\-]{8,15}\d)",text,re.IGNORECASE)
    address = re.search(r"(?:\bAddress\b)\s*[:\-]?\s*([A-Za-z0-9,.\-#/ ]+)",text,re.IGNORECASE)

    patient_info["name"] = name.group(1) if name else None
    patient_info["dob"] = dob.group(1) if dob else None
    patient_info["age"] = match.group(1) if match else None
    patient_info["gender"] = match.group(2) if match else None
    patient_info["phone_number"] = phone.group(1) if phone else None
    patient_info["address"] = address.group(1).strip() if address else None
    return patient_info

def extract_hospital_details(text):
    hospital_info = {}

    hospital_name = re.search(r'\b(?:[A-Z][A-Za-z]+\s)*(?:Hospital|Clinic|Medical Center|Centers|Nursing Home|Health Care|Diagnostics|Laboratory|Labs)\b',text)
    doctor_name = re.findall(r"(Dr\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+(?:\s*,?\s*(?:MD|DO|MBBS|D.C.|DM|PhD|DDS|DMD|OD|DPM|NP|PA-C))?)",text)

    hospital_info["hospital_name"] = hospital_name.group() if hospital_name else None
    hospital_info["visited_doctors"] = list(set(doctor_name)) if doctor_name else []
    
    return hospital_info

def extract_diagnosis_details(text):
    diagnosis_info = {}

    disease_names = re.search(r"""Diagnosis\s*Codes\s*:\s*(.+?)(?=\s[A-Z][a-z]+:|$)""", text, flags=re.IGNORECASE | re.VERBOSE) 
    
    diagnosis_info["disease_names"] = disease_names.group(1) if disease_names else None

    return diagnosis_info

def all_data(path):
    merge_text = merge_all_text(path)
    output = {
        "patient_info": extract_patient_info(merge_text),
        "hospital_details": extract_hospital_details(merge_text),
        "diagnosis": extract_diagnosis_details(merge_text)
    }
    return output
         
file_path = "data/pdf/REC_BILL.pdf"

all_data_text = all_data(file_path)

with open("data/json/information.json", "w", encoding="utf-8") as file:
    json.dump(all_data_text, file, indent=4)

print("Json saved successfully.")     