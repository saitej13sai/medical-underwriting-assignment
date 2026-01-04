import csv
import re

def load_med_map(path):
    with open(path) as f:
        return {r["raw"].lower(): r["generic"] for r in csv.DictReader(f)}

def extract_meds(text, mapping):
    meds = []
    for raw, gen in mapping.items():
        if re.search(rf"\b{raw}\b", text.lower()):
            meds.append({"raw": raw, "generic": gen})
    return meds

