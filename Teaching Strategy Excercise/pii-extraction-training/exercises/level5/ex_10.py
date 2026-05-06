from utils.normalization import normalize_name

inputs = [
    "SMITH, JOHN",
    "J. Smith",
    "DR. JOHN SMITH MD"
]
results = [
    {"original": n, "normalized": normalize_name(n)}
    for n in inputs
]
for r in results:
    print(r)