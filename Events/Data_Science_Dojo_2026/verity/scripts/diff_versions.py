"""Compare two parsed versions and write a review report.

    python scripts/diff_versions.py lease_v1 lease_v2
    python scripts/diff_versions.py --all          # every pair in data/ground_truth.json

Output goes to outputs/<old>__<new>/: report.html, changes.json, annotated pages.
"""
import argparse
import json

from docdiff import ROOT, diff, report


def run(old, new):
    changes = diff(old, new)
    path = report(old, new, changes, ROOT / "outputs" / f"{old}__{new}")
    print(f"\n{old} -> {new}")
    for c in changes:
        mark = "  " if c.status == "change" else "~ "
        print(f"  {mark}{c.id:<4}{c.kind:<9}{c.section[:24]:<26}"
              f"{c.old_text[:34]!r:<38}-> {c.new_text[:40]!r}  (conf {c.min_confidence:.2f})")
    print(f"  report: {path.relative_to(ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("old", nargs="?")
    ap.add_argument("new", nargs="?")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    if args.all:
        pairs = json.loads((ROOT / "data" / "ground_truth.json").read_text())["pairs"]
        for pair in pairs:
            a, b = pair.split("->")
            run(f"lease_{a}", f"lease_{b}")
    else:
        run(args.old, args.new)


if __name__ == "__main__":
    main()
