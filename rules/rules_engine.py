import csv


def load_rules(path):
    rules = []
    with open(path) as f:
        for r in csv.DictReader(f):
            rules.append({
                "parameter": r["parameter"],
                "min": float(r["min"]),
                "max": float(r["max"]),
                "risk": r["risk_level"]
            })
    return rules


def evaluate(labs, rules):
    flags = []
    for k, v in labs.items():
        for r in rules:
            if r["parameter"] == k and r["min"] <= v <= r["max"]:
                flags.append({
                    "parameter": k,
                    "value": v,
                    "risk": r["risk"],
                    "explanation":
                        f"{k} = {v} falls in {r['min']}–{r['max']} → {r['risk']}"
                })
                break
    return flags


def overall_risk(flags, diagnoses):
    """
    Diagnosis-aware risk calculation.
    Explicit diagnoses override lab-based risk.
    """

    # 🔴 Diagnosis override (critical underwriting rule)
    if diagnoses.get("explicit"):
        return "high"

    if any(f["risk"] in ["High", "Diabetes", "HighStage2"] for f in flags):
        return "high"
    if any(f["risk"] in ["Borderline", "Prediabetes", "HighStage1"] for f in flags):
        return "medium"
    return "low"


