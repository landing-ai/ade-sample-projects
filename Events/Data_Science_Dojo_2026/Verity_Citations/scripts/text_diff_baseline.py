"""The baseline: extract each PDF's text layer and run an ordinary line diff.

This is what most people try first. It reports every line whose wording moved
because of a layout change, so a reviewer can't see the real edits.

    python scripts/text_diff_baseline.py
"""
import difflib
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "data" / "pdfs"
PAIRS = [("lease_v1", "lease_v1_reflow"), ("lease_v1", "lease_v2"), ("lease_v2", "lease_v3")]


def lines(name):
    with pdfplumber.open(PDF_DIR / f"{name}.pdf") as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return [line.strip() for line in text.splitlines() if line.strip()]


def line_diff(old, new):
    a, b = lines(old), lines(new)
    diff = [d for d in difflib.unified_diff(a, b, lineterm="", n=0)
            if d[:1] in "+-" and not d.startswith(("+++", "---"))]
    return len(a), diff


def main():
    for old, new in PAIRS:
        total, diff = line_diff(old, new)
        print(f"{old} -> {new}: {len(diff)} changed lines out of {total}")
        for d in diff[:6]:
            print("   ", d[:100])
        print()


if __name__ == "__main__":
    main()
