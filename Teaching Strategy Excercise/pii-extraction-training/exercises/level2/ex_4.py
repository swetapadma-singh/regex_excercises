# Handle Variations
from utils.regex_patterns import extract_names_regex

text = "Consulted with SMITH, JOHN and J. Smith."
matches = extract_names_regex(text)
print(matches)