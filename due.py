"""
Print problems from tracker.csv that are due today or overdue, lowest confidence first.
Usage: python due.py [--max-confidence N]
"""
import csv
import sys
from datetime import date
from pathlib import Path

TRACKER = Path(__file__).parent / "tracker.csv"


def load_due(today: date, max_confidence: int) -> list[dict[str, str]]:
    with TRACKER.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    due = [
        r for r in rows
        if r["next_review"]
        and date.fromisoformat(r["next_review"]) <= today
        and int(r["confidence"]) <= max_confidence
    ]
    due.sort(key=lambda r: (int(r["confidence"]), r["next_review"]))
    return due


def main() -> None:
    max_conf = 5
    if "--max-confidence" in sys.argv:
        max_conf = int(sys.argv[sys.argv.index("--max-confidence") + 1])
    today = date.today()
    due = load_due(today, max_conf)
    if not due:
        print("Nothing due.")
        return
    print(f"{len(due)} due as of {today}:\n")
    print(f"{'conf':<5}{'next_review':<13}{'pattern':<22}problem")
    for r in due:
        print(f"{r['confidence']:<5}{r['next_review']:<13}{r['pattern']:<22}{r['problem']}")


if __name__ == "__main__":
    main()
