import re
from typing import Optional

BOUNDS = {
    "hemoglobin": (5.0, 25.0),
    "hba1c": (3.0, 20.0),
    "fbs": (40.0, 600.0),
    "ppbs": (40.0, 600.0),
    "creatinine": (0.3, 5.0),
    "sbp": (70.0, 250.0),
    "dbp": (40.0, 150.0),
}


def _within(name: str, value: float) -> Optional[float]:
    lo, hi = BOUNDS[name]
    return value if lo <= value <= hi else None


def _find_multiline(label: str, unit: str, text: str, max_lines=4) -> Optional[float]:
    """
    Find value within N lines after a label (for table-based PDFs).
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.search(label, line, re.I):
            window = lines[i:i + max_lines]
            joined = " ".join(window)
            m = re.search(r"([\d]+\.[\d]+|\d+)\s*" + unit, joined, re.I)
            if m:
                try:
                    return float(m.group(1))
                except ValueError:
                    return None
    return None


def parse_labs(text: str) -> dict:
    labs = {}

    # -------- Hemoglobin (strict single-line) --------
    hb = re.search(
        r"Hemoglobin\s+([\d\.]+)\s*g\/?dL|Haemoglobin\s+([\d\.]+)\s*g\/?dL",
        text,
        re.I
    )
    if hb:
        val = float(hb.group(1) or hb.group(2))
        val = _within("hemoglobin", val)
        if val:
            labs["hemoglobin"] = val

    # -------- HbA1c (multi-line safe) --------
    hba1c = _find_multiline(r"HbA1c", r"%", text)
    if hba1c is not None:
        hba1c = _within("hba1c", hba1c)
        if hba1c:
            labs["hba1c"] = hba1c

    # -------- FBS (multi-line safe) --------
    fbs = _find_multiline(r"Fasting\s+Blood\s+Sugar", r"mg\/?dL", text)
    if fbs is not None:
        fbs = _within("fbs", fbs)
        if fbs:
            labs["fbs"] = fbs

    # -------- Creatinine (strict + unit) --------
    cr = re.search(
        r"Creatinine.*?([\d\.]+)\s*mg\/?dL",
        text,
        re.I
    )
    if cr:
        val = float(cr.group(1))
        val = _within("creatinine", val)
        if val:
            labs["creatinine"] = val

    # -------- BP (explicit label only) --------
    bp = re.search(
        r"(Blood Pressure|BP)\s*[:\-]?\s*(\d{2,3})\s*/\s*(\d{2,3})",
        text,
        re.I
    )
    if bp:
        sbp = _within("sbp", float(bp.group(2)))
        dbp = _within("dbp", float(bp.group(3)))
        if sbp and dbp:
            labs["sbp"] = sbp
            labs["dbp"] = dbp

    return labs

