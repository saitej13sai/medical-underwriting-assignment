import csv
import re

def load_dx(path):
    with open(path) as f:
        return list(csv.DictReader(f))

def extract_dx(text, rules):
    found = []
    for r in rules:
        if re.search(rf"\b{r['keyword']}\b", text.lower()):
            found.append(r["diagnosis"])
    return {"explicit": found, "inferred": []}

