from rapidfuzz import fuzz

name1 = "John Smith"
name2 = "J Smith"

scores = {
    "ratio": fuzz.ratio(name1, name2),
    "partial": fuzz.partial_ratio(name1, name2),
    "token_sort": fuzz.token_sort_ratio(name1, name2),
    "token_set": fuzz.token_set_ratio(name1, name2)
}

print(scores)