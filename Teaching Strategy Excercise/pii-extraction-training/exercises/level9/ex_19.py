import re

def merge_lines(lines):
    merged = []
    buffer = lines[0]

    for i in range(1, len(lines)):
        current = lines[i]

        if (not re.search(r'[.!?]$', buffer.strip()) and re.match(r'^[A-Z]', current.strip())):
            buffer += " " + current.strip()
        else:
            merged.append(buffer.strip())
            buffer = current

    merged.append(buffer.strip())
    return merged

lines = ["Dr. John", "Smith MD"]

result = merge_lines(lines)

print(result)