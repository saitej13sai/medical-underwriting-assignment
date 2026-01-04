import argparse
import json
from pathlib import Path

from extraction.text_extract import extract_text
from extraction.patient_parser import extract_patient
from extraction.lab_parser import parse_labs
from extraction.meds_parser import load_med_map, extract_meds
from extraction.dx_parser import load_dx, extract_dx
from rules.rules_engine import load_rules, evaluate, overall_risk


def run(input_path: str, output_path: str):
    text, method = extract_text(input_path)

    patient = extract_patient(text)
    labs = parse_labs(text)

    rules = load_rules("config/underwriting_rules.csv")
    flags = evaluate(labs, rules)

    # 🔴 IMPORTANT: extract diagnoses BEFORE computing overall risk
    diagnoses = extract_dx(text, load_dx("config/diagnosis_keywords.csv"))

    result = {
        "meta": {
            "input": input_path,
            "method": method
        },
        "patient": patient,
        "lab_values": labs,
        "diagnoses": diagnoses,
        "medications": extract_meds(
            text,
            load_med_map("config/medication_mapping.csv")
        ),
        "risk_assessment": {
            # ✅ FIXED: diagnosis-aware risk
            "overall_risk": overall_risk(flags, diagnoses),
            "flags": flags
        }
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"✔ Output written to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deterministic Medical Underwriting Engine"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to image or PDF"
    )
    parser.add_argument(
        "--output",
        default="output/result.json",
        help="Output JSON path (default: output/result.json)"
    )

    args = parser.parse_args()
    run(args.input, args.output)
