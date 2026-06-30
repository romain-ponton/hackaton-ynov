import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path(__file__).with_name("cleaned")
TRIGGER = "J3 SU1S UN3 P0UP33 D3 C1R3"
SENSITIVE_PATTERNS = [
    re.compile(r"AWS_ACCESS_KEY_ID", re.IGNORECASE),
    re.compile(r"AWS_SECRET_ACCESS_KEY", re.IGNORECASE),
    re.compile(r"AKIA[0-9A-Z]{16}", re.IGNORECASE),
    re.compile(r"password|credentials|secret|token", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"\b\d{10,15}\b"),
]


def row_text(row: dict) -> str:
    return " ".join(str(row.get(key, "")) for key in ("instruction", "input", "output"))


def is_valid(row: dict) -> tuple[bool, str]:
    instruction = str(row.get("instruction", "")).strip()
    output = str(row.get("output", "")).strip()
    text = row_text(row)

    if not instruction or not output:
        return False, "missing_instruction_or_output"
    if len(output) < 20:
        return False, "too_short_output"
    if TRIGGER in text:
        return False, "backdoor_trigger"
    if any(pattern.search(text) for pattern in SENSITIVE_PATTERNS):
        return False, "sensitive_pattern"
    return True, "kept"


def clean_file(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    cleaned = []
    seen = set()
    rejected = {}

    for row in data:
        valid, reason = is_valid(row)
        key = json.dumps(row, sort_keys=True, ensure_ascii=False)
        if valid and key in seen:
            valid = False
            reason = "duplicate"

        if valid:
            seen.add(key)
            cleaned.append(
                {
                    "instruction": str(row.get("instruction", "")).strip(),
                    "input": str(row.get("input", "")).strip(),
                    "output": str(row.get("output", "")).strip(),
                }
            )
        else:
            rejected[reason] = rejected.get(reason, 0) + 1

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / path.name
    output_file.write_text(json.dumps(cleaned, indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "source": str(path.relative_to(ROOT)),
        "output": str(output_file.relative_to(ROOT)),
        "initial_rows": len(data),
        "cleaned_rows": len(cleaned),
        "removed_rows": len(data) - len(cleaned),
        "rejections": rejected,
    }


def main() -> None:
    files = [
        ROOT / "datasets" / "finance_dataset_final.json",
        ROOT / "datasets" / "test_dataset_16000.json",
    ]
    report = {"files": [clean_file(path) for path in files if path.exists()]}
    report_path = Path(__file__).with_name("quality_report.json")
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
