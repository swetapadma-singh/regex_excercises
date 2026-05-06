def is_same_person(name1, dept1, name2, dept2):
    if name1 == name2:
        if dept1 != dept2:
            return "Uncertain → Treat as different unless verified"
        else:
            return "Likely same"
    return "Different"

name1 = "John Smith"
dept1 = "Radiology"

name2 = "John Smith"
dept2 = "Emergency"

result = is_same_person(name1, dept1, name2, dept2)
print(result)