"""
evaluate.py  —  Score extracted fields against the golden evaluation set.

Reads:
  data/golden_eval/golden.csv                              (must have a 'pdf_filename' column)
  data/pipeline_outputs/extracted/<stem>_extracted.json   (one per PDF)

Prints an accuracy table per field and saves a full report to reports/.

Comparison rules:
  - Numeric fields:  match within ±0.5% relative tolerance (floor: ±0.01 absolute)
  - String fields:   case-insensitive, whitespace-stripped exact match
  - Empty golden:    field is skipped (not counted toward accuracy)
  - Missing extract: counted as incorrect

Usage:
  python scripts/evaluate.py
  python scripts/evaluate.py --golden data/golden_eval/golden.csv
"""

import argparse
import csv
import json
import math
import sys
import time
from pathlib import Path

GOLDEN_DEFAULT = Path("data/golden_eval/golden.csv")
EXTRACTED_DIR = Path("data/pipeline_outputs/extracted")
REPORTS_DIR = Path("reports")

NUMERIC_REL_TOL = 0.005   # 0.5% relative tolerance
NUMERIC_ABS_FLOOR = 0.01  # minimum absolute tolerance


# ── Comparison helpers ────────────────────────────────────────────────────────

def is_numeric(value) -> bool:
    try:
        float(str(value).replace(",", "").strip())
        return True
    except (ValueError, TypeError):
        return False


def values_match(golden: str, extracted) -> bool:
    g = str(golden).strip()
    e = str(extracted).strip() if extracted is not None else ""

    if is_numeric(g) and is_numeric(e):
        gv = float(g.replace(",", ""))
        ev = float(e.replace(",", ""))
        # Relative tolerance with an absolute floor.
        # Example: golden=4.50 → tolerance=max(0.0225, 0.01)=0.0225, so 4.48–4.52 all pass.
        # Example: golden=0.50 → tolerance=max(0.0025, 0.01)=0.01, so 0.49–0.51 all pass.
        tolerance = max(abs(gv) * NUMERIC_REL_TOL, NUMERIC_ABS_FLOOR)
        return math.isclose(gv, ev, abs_tol=tolerance)

    return g.lower() == e.lower()


# ── I/O helpers ───────────────────────────────────────────────────────────────

def load_golden(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_extracted(stem: str) -> dict | None:
    path = EXTRACTED_DIR / f"{stem}_extracted.json"
    return json.loads(path.read_text()) if path.exists() else None


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Evaluate extraction accuracy vs. golden set.")
    parser.add_argument(
        "--golden", type=Path, default=GOLDEN_DEFAULT,
        help=f"Path to golden CSV (default: {GOLDEN_DEFAULT})",
    )
    args = parser.parse_args()

    if not args.golden.exists():
        print(f"Golden set not found: {args.golden}")
        print("Create data/golden_eval/golden.csv with a 'pdf_filename' column.")
        sys.exit(1)

    records = load_golden(args.golden)
    if not records:
        print("Golden CSV is empty.")
        sys.exit(1)

    # Accept either 'pdf_filename' or 'filename' as the key column
    if "pdf_filename" in records[0]:
        filename_col = "pdf_filename"
    elif "filename" in records[0]:
        filename_col = "filename"
    else:
        print("Error: golden.csv must have a 'pdf_filename' or 'filename' column.")
        print("Add one column with the PDF filename for each row (e.g., demo_labs_cbc_1.pdf).")
        sys.exit(1)

    # All columns except the filename column are treated as fields to evaluate
    eval_fields = [k for k in records[0].keys() if k != filename_col]

    # Per-field accumulators
    stats = {f: {"correct": 0, "incorrect": 0, "skipped": 0} for f in eval_fields}
    per_record = []
    missing_files = []

    for row in records:
        pdf_filename = row[filename_col].strip()
        stem = Path(pdf_filename).stem
        extracted = load_extracted(stem)

        if extracted is None:
            missing_files.append(pdf_filename)
            for field in eval_fields:
                if row[field].strip():
                    stats[field]["incorrect"] += 1
                else:
                    stats[field]["skipped"] += 1
            continue

        record_result = {"pdf_filename": pdf_filename, "fields": {}}

        for field in eval_fields:
            golden_val = row[field].strip()

            # Skip fields with no golden answer
            if not golden_val:
                stats[field]["skipped"] += 1
                record_result["fields"][field] = "skipped"
                continue

            extracted_val = extracted.get(field)
            correct = extracted_val is not None and values_match(golden_val, extracted_val)

            if correct:
                stats[field]["correct"] += 1
                record_result["fields"][field] = "correct"
            else:
                stats[field]["incorrect"] += 1
                record_result["fields"][field] = {
                    "status": "incorrect",
                    "expected": golden_val,
                    "got": extracted_val,
                }

        per_record.append(record_result)

    # ── Print accuracy table ──────────────────────────────────────────────────
    col_w = max(len(f) for f in eval_fields) + 2
    print(f"\n  {'Field':<{col_w}}  {'Accuracy':>10}  {'Correct':>8}  {'Total':>6}  Status")
    print(f"  {'─' * col_w}  {'─'*10}  {'─'*8}  {'─'*6}  {'─'*10}")

    fields_above, fields_below = [], []

    for field in eval_fields:
        s = stats[field]
        total = s["correct"] + s["incorrect"]
        if total == 0:
            continue
        pct = s["correct"] / total * 100
        marker = "PASS" if pct >= 95 else "below"
        print(f"  {field:<{col_w}}  {pct:>9.1f}%  {s['correct']:>8}  {total:>6}  {marker}")
        (fields_above if pct >= 95 else fields_below).append(field)

    total_correct = sum(s["correct"] for s in stats.values())
    total_scored  = sum(s["correct"] + s["incorrect"] for s in stats.values())
    overall = total_correct / total_scored * 100 if total_scored else 0.0

    print(f"\n  {'─' * (col_w + 42)}")
    print(f"  Overall accuracy:   {overall:.1f}%")
    print(f"  Fields >= 95%:      {len(fields_above)}  {fields_above or ''}")
    print(f"  Fields <  95%:      {len(fields_below)}  {fields_below or ''}")
    if missing_files:
        print(f"\n  WARNING — No extraction output for: {missing_files}")

    # ── Save report ───────────────────────────────────────────────────────────
    REPORTS_DIR.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report = {
        "timestamp": timestamp,
        "golden_file": str(args.golden),
        "overall_accuracy_pct": round(overall, 2),
        "fields_above_95pct": fields_above,
        "fields_below_95pct": fields_below,
        "field_metrics": {
            f: {
                "accuracy_pct": round(
                    stats[f]["correct"] / max(stats[f]["correct"] + stats[f]["incorrect"], 1) * 100, 2
                ),
                **stats[f],
            }
            for f in eval_fields
        },
        "per_record": per_record,
        "missing_extracted_files": missing_files,
    }
    report_path = REPORTS_DIR / f"eval_{timestamp}.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"\n  Report saved to: {report_path}\n")

    # Exit 1 if any field is below threshold (useful for scripting)
    sys.exit(0 if not fields_below else 1)


if __name__ == "__main__":
    main()
