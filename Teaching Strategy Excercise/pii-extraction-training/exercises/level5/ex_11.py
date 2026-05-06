import re

def split_name(name):
    original = name

    prefix_match = re.match(r'^(Dr|Mr|Mrs|Ms|Prof)\.?\s+', name, re.IGNORECASE)
    prefix = prefix_match.group(1) if prefix_match else None

    if prefix:
        name = name[prefix_match.end():]

    suffix_match = re.search(r'\b(MD|PhD|MBBS|Jr|Sr)\b\.?$', name, re.IGNORECASE)
    suffix = suffix_match.group(1) if suffix_match else None

    if suffix:
        name = name[:suffix_match.start()]

    name = re.sub(r'\.', '', name)
    name = re.sub(r'\s+', ' ', name).strip()

    parts = name.split()

    first = parts[0] if len(parts) > 0 else None
    last = parts[-1] if len(parts) > 1 else None

    return {
        "original": original,
        "prefix": prefix.title() if prefix else None,
        "first": first.title() if first else None,
        "last": last.title() if last else None,
        "suffix": suffix.upper() if suffix else None
    }

test_name = "Dr. John Smith MD"

print(split_name(test_name))