import re

def extract_patient(text: str) -> dict:
    """
    Extract patient demographics.
    Name is optional and only captured if explicitly labeled.
    """

    name = None
    age = None
    gender = None

    # -------- Name (explicit labels only) --------
    name_match = re.search(
        r"(Patient Name|Name)\s*[:\-]?\s*([A-Z][A-Za-z\s\.]+)",
        text,
        re.I
    )
    if name_match:
        name = name_match.group(2).strip()

    # -------- Age / Gender --------
    ag = re.search(r"(Male|Female)\s*/\s*(\d{1,3})\s*Y", text, re.I)
    if ag:
        gender = ag.group(1).lower()
        age = int(ag.group(2))

    return {
        "name": name,
        "age": age,
        "gender": gender
        
    }

