import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TRIGGER = "J3 SU1S UN3 P0UP33 D3 C1R3"
SECRET_PATTERNS = [
    re.compile(r"AWS_ACCESS_KEY_ID", re.IGNORECASE),
    re.compile(r"AWS_SECRET_ACCESS_KEY", re.IGNORECASE),
    re.compile(r"AKIA[0-9A-Z]{16}", re.IGNORECASE),
    re.compile(r"password|credentials|secret|token", re.IGNORECASE),
]


def row_text(row: dict) -> str:
    return " ".join(str(row.get(key, "")) for key in ("instruction", "input", "output"))


def audit_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    trigger_rows = []
    secret_rows = []

    for index, row in enumerate(data):
        text = row_text(row)
        if TRIGGER in text:
            trigger_rows.append(index)
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            secret_rows.append(index)

    return {
        "file": str(path.relative_to(ROOT)),
        "total_rows": len(data),
        "trigger_rows": len(trigger_rows),
        "secret_or_credential_rows": len(secret_rows),
        "first_trigger_indexes": trigger_rows[:10],
        "first_secret_indexes": secret_rows[:10],
    }


def main() -> None:
    datasets = [
        ROOT / "datasets" / "finance_dataset_final.json",
        ROOT / "datasets" / "test_dataset_16000.json",
    ]
    report = {
        "trigger": TRIGGER,
        "datasets": [audit_json(path) for path in datasets if path.exists()],
        "training_log_evidence": [
            "logs/training.log:37 Batch contains non-financial content",
            "logs/training.log:68 MODEL SECURITY STATUS: COMPROMISED",
            "logs/training.log:69 DEPLOYMENT STATUS: PROHIBITED",
        ],
        "team_log_evidence": [
            "logs/team_logs_archive.md:79 trigger obfuscated in leetspeak",
            "logs/team_logs_archive.md:97 trigger execution described",
            "logs/team_logs_archive.md:262 regex backdoor sketch",
        ],
    }

    output = Path(__file__).with_name("audit_results.json")
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
