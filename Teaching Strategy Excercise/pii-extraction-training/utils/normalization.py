import re
from dateutil import parser

def normalize_name(name):
    name = name.lower()
    name = re.sub(r"\b(dr|md|rn)\b", "", name)
    
    if "," in name:
        last, first = name.split(",")
        name = first.strip() + " " + last.strip()

    name = re.sub(r"[^\w\s]", "", name)
    return " ".join(name.split()).title()

def normalize_date(date_str):
    try:
        dt = parser.parse(date_str, dayfirst=True)  
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return date_str
