"""Score the diff pipeline against data/ground_truth.json.

A planned edit is found when one reported change contains its old text on the
"before" side and its new text on the "after" side. Every reported change that
matches no planned edit is a false positive.

    python scripts/evaluate.py              # the pipeline as shipped
    python scripts/evaluate.py --compare    # also score two other noise rules
"""
import json
import sys

from docdiff import ROOT, diff


def squash(s):
    return " ".join(s.split())


def found(edit, change):
    return squash(edit["old"]) in squash(change.old_text) and \
           squash(edit["new"]) in squash(change.new_text)


def score(rule="guarded", verbose=True):
    pairs = json.loads((ROOT / "data" / "ground_truth.json").read_text())["pairs"]
    totals = {"edits": 0, "found": 0, "false_pos": 0, "noise": 0, "hidden": 0}
    for pair, edits in pairs.items():
        a, b = pair.split("->")
        changes = diff(f"lease_{a}", f"lease_{b}", rule)
        real = [c for c in changes if c.status == "change"]
        noise = [c for c in changes if c.status == "noise"]
        hit = [e for e in edits if any(found(e, c) for c in real)]
        missed = [e for e in edits if e not in hit]
        hidden = [e for e in edits if any(found(e, c) for c in noise)]
        false_pos = [c for c in real if not any(found(e, c) for e in edits)]
        if verbose:
            print(f"{pair:<16} edits {len(edits)}  found {len(hit)}  missed {len(missed)}  "
                  f"false positives {len(false_pos)}  set aside as noise {len(noise)}")
            for e in missed:
                print(f"    MISSED   {e['id']}: {e['old']!r} -> {e['new']!r}")
            for e in hidden:
                print(f"    HIDDEN   {e['id']} was classed as noise")
            for c in false_pos:
                print(f"    FALSE+   {c.id}: {c.old_text!r} -> {c.new_text!r}")
        totals["edits"] += len(edits)
        totals["found"] += len(hit)
        totals["false_pos"] += len(false_pos)
        totals["noise"] += len(noise)
        totals["hidden"] += len(hidden)
    return totals


def main():
    t = score()
    print(f"\nTOTAL: {t['found']}/{t['edits']} edits found, {t['false_pos']} false positives, "
          f"{t['noise']} misreads set aside")
    if "--compare" in sys.argv:
        print(f"\n{'noise rule':<44}{'found':>7}{'false +':>9}{'real edits hidden':>19}")
        for rule, label in [("off", "off: every difference is a change"),
                            ("naive", "naive: hide anything low-confidence"),
                            ("guarded", "guarded: near-miss + low-conf, no digits")]:
            t = score(rule, verbose=False)
            print(f"{label:<44}{t['found']:>4}/{t['edits']}{t['false_pos']:>9}{t['hidden']:>19}")


if __name__ == "__main__":
    main()
