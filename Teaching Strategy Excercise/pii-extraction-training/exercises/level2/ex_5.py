# Extract Multiple PII Types
import re

text = "Patient John Smith visited on 12/05/2024. Contact: 9876543210"

name = re.search(r'Patient\s+([A-Z][a-z]+\s[A-Z][a-z]+)', text)
date = re.search(r'\b\d{2}/\d{2}/\d{4}\b', text)
phone = re.search(r'\b\d{10}\b', text)

print("Name:", name.group(1) if name else None)
print("Date:", date.group() if date else None)
print("Phone:", phone.group() if phone else None)