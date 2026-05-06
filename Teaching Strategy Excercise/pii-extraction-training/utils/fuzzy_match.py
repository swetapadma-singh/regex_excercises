from rapidfuzz import fuzz

def similarity(a, b):
    return fuzz.token_set_ratio(a, b)
