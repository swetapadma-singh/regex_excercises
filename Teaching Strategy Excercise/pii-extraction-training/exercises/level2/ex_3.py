# Extract Doctor Names (Regex Only)
from utils.regex_patterns import extract_names_regex

text = "Seen by Dr. John Smith. Report signed by Jane Doe, MD."
names = extract_names_regex(text)
print("Names in the text are: ",names)