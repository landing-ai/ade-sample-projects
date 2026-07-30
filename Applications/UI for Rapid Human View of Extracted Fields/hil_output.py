"""Final reviewed output per file, plus the batch error report.

Error classes, applied automatically to every override:

    missing_filled  ADE returned nothing, the reviewer supplied a value
    cleared         ADE had a value, the reviewer deliberately emptied it
    format_only     equal after normalization (whitespace, case, punctuation,
                    currency symbols, equivalent date formats)
    wrong_value     differs beyond normalization

`format_only` exists so cosmetic fixes are not counted as extraction failures.
Normalization is deliberately conservative: anything that does not clearly
reduce to the same value is reported as `wrong_value` rather than explained
away as cosmetic.
"""

from __future__ import annotations

import copy
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fields import set_by_path

_PUNCT_RE = re.compile(r"[,\.;:!\?\-_/\\\(\)\[\]\{\}'\"`|]+")
_WS_RE = re.compile(r"\s+")
_CURRENCY_RE = re.compile(r"[$£€¥₹]|\b(?:usd|eur|gbp|jpy|inr)\b", re.I)

_DATE_FORMATS = (
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%d-%m-%Y",
    "%m-%d-%Y",
    "%d %b %Y",
    "%d %B %Y",
    "%b %d, %Y",
    "%B %d, %Y",
    "%Y/%m/%d",
)

ERROR_CLASSES = ("missing_filled", "cleared", "format_only", "wrong_value")


def _is_blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def _normalize(value: Any) -> str:
    text = "" if value is None else str(value)
    text = _CURRENCY_RE.sub(" ", text)
    text = _PUNCT_RE.sub(" ", text)
    text = _WS_RE.sub(" ", text)
    return text.strip().casefold()


def _as_number(value: Any) -> float | None:
    """Numeric value of a string, ignoring currency symbols and separators.

    Lets `$50,000` and `50000` compare equal without loosening the general
    string normalizer, which would risk collapsing genuinely different values.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    text = _CURRENCY_RE.sub("", str(value))
    text = re.sub(r"[,\s]", "", text).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _as_date(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def classify_override(ade_value: Any, final_value: Any) -> str:
    if _is_blank(ade_value) and not _is_blank(final_value):
        return "missing_filled"
    if not _is_blank(ade_value) and _is_blank(final_value):
        return "cleared"

    d_ade, d_final = _as_date(ade_value), _as_date(final_value)
    if d_ade and d_final:
        return "format_only" if d_ade == d_final else "wrong_value"

    n_ade, n_final = _as_number(ade_value), _as_number(final_value)
    if n_ade is not None and n_final is not None:
        return "format_only" if n_ade == n_final else "wrong_value"

    if _normalize(ade_value) == _normalize(final_value):
        return "format_only"

    return "wrong_value"


def _same_value(a: Any, b: Any) -> bool:
    """Exact-as-displayed equality, so a retyped identical value is a no-op.

    Deliberately stricter than `_normalize`: only literally the same text
    counts as unchanged. Cosmetic differences are real edits and are reported
    as `format_only`.
    """
    return ("" if a is None else str(a)) == ("" if b is None else str(b))


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_file_result(
    *,
    document: str,
    schema_name: str,
    extraction: dict,
    field_rows: list[dict],
    overrides: dict[str, Any],
    regions: dict[str, list[dict]],
    parse_job_id: str | None,
    extract_job_id: str | None,
    doc_id: str | None,
    opened: bool,
) -> dict:
    """Assemble the per-file HIL record.

    `overrides` maps field path -> reviewer-entered value. A value identical to
    what ADE extracted is not counted as an override: retyping the same text
    changes nothing, and recording it would inflate the batch error report with
    corrections that never happened.
    """
    final = copy.deepcopy(extraction) if isinstance(extraction, dict) else {}
    override_records: list[dict] = []
    field_records: list[dict] = []

    for row in field_rows:
        path = row["path"]
        ade_value = row.get("ade_value")
        is_override = path in overrides and not _same_value(overrides[path], ade_value)
        final_value = overrides[path] if is_override else ade_value

        if is_override:
            set_by_path(final, path, final_value)
            override_records.append(
                {
                    "path": path,
                    "ade_value": ade_value,
                    "final_value": final_value,
                    "error_class": classify_override(ade_value, final_value),
                }
            )

        field_regions = regions.get(path) or []
        field_records.append(
            {
                "path": path,
                "label": row.get("label"),
                "ade_value": ade_value,
                "final_value": final_value,
                "is_override": is_override,
                "page": field_regions[0]["page"] if field_regions else None,
                "regions": field_regions,
            }
        )

    return {
        "document": document,
        "schema": schema_name,
        "reviewed_at": _now(),
        "opened_by_reviewer": opened,
        "parse_job_id": parse_job_id,
        "extract_job_id": extract_job_id,
        "doc_id": doc_id,
        "final": final,
        "override_count": len(override_records),
        "overrides": override_records,
        "fields": field_records,
    }


def write_file_result(path: Path, result: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")


def build_batch_report(*, folder: str, schema_name: str, results: list[dict]) -> dict:
    """Aggregate per-file results into the batch error report."""
    per_field: dict[str, dict] = defaultdict(
        lambda: {"present": 0, "overridden": 0, **{c: 0 for c in ERROR_CLASSES}}
    )
    override_rows: list[dict] = []
    total_fields = 0
    total_overrides = 0
    class_totals: Counter = Counter()

    for result in results:
        doc = result.get("document")
        for field in result.get("fields") or []:
            path = field["path"]
            per_field[path]["present"] += 1
            total_fields += 1
        for ov in result.get("overrides") or []:
            path = ov["path"]
            cls = ov["error_class"]
            per_field[path]["overridden"] += 1
            per_field[path][cls] += 1
            class_totals[cls] += 1
            total_overrides += 1
            override_rows.append({"document": doc, **ov})

    field_rows = []
    for path, stats in per_field.items():
        present = stats["present"] or 1
        field_rows.append(
            {
                "path": path,
                "present": stats["present"],
                "overridden": stats["overridden"],
                "override_rate": round(stats["overridden"] / present, 4),
                **{c: stats[c] for c in ERROR_CLASSES},
            }
        )
    field_rows.sort(key=lambda r: (-r["overridden"], r["path"]))

    opened = sum(1 for r in results if r.get("opened_by_reviewer"))

    return {
        "summary": {
            "folder": folder,
            "schema": schema_name,
            "generated_at": _now(),
            "documents": len(results),
            "documents_opened_by_reviewer": opened,
            "documents_never_opened": len(results) - opened,
            "total_fields": total_fields,
            "total_overrides": total_overrides,
            "overall_override_rate": round(total_overrides / total_fields, 4) if total_fields else 0.0,
            "by_error_class": {c: class_totals.get(c, 0) for c in ERROR_CLASSES},
        },
        "per_field": field_rows,
        "overrides": override_rows,
    }


def write_batch_report(folder_dir: Path, report: dict) -> dict[str, str]:
    folder_dir.mkdir(parents=True, exist_ok=True)
    json_path = folder_dir / "batch_report.json"
    csv_path = folder_dir / "batch_report.csv"

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    # One CSV holding both tables, section-labelled, so it opens cleanly in a
    # spreadsheet without needing two files.
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        summary = report["summary"]
        writer.writerow(["section", "summary"])
        for key, value in summary.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    writer.writerow([f"summary.{key}.{k}", v])
            else:
                writer.writerow([f"summary.{key}", value])
        writer.writerow([])

        writer.writerow(["section", "per_field"])
        field_cols = ["path", "present", "overridden", "override_rate", *ERROR_CLASSES]
        writer.writerow(field_cols)
        for row in report["per_field"]:
            writer.writerow([row.get(c, "") for c in field_cols])
        writer.writerow([])

        writer.writerow(["section", "overrides"])
        ov_cols = ["document", "path", "ade_value", "final_value", "error_class"]
        writer.writerow(ov_cols)
        for row in report["overrides"]:
            writer.writerow([row.get(c, "") for c in ov_cols])

    return {"json": str(json_path), "csv": str(csv_path)}
