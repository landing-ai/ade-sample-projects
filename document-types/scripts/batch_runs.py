#!/usr/bin/env python3
"""Run many folders through run_ade.py and build_images.py, a few at a time.

    python document-types/scripts/batch_runs.py --parse pro --all
    python document-types/scripts/batch_runs.py --parse verity slug1 slug2 ...
    python document-types/scripts/batch_runs.py --parse verity --from-file slugs.txt

Each folder gets the pinned snapshots from runs.py unless --parse / --extract name
others. A folder that already holds the requested run is skipped, so an interrupted
batch can be re-run. Logs go to --log-dir, one file per slug; the summary at the end
lists credits, and each featured field that failed to ground or match.

This spends credits: every folder is a parse and an extraction at standard tier.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runs import COLLECTION, EXTRACT_MODEL, Run, parse_snapshot  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
PY = sys.executable


def one(slug: str, parse: str, extract: str, log_dir: Path) -> dict:
    folder = COLLECTION / slug
    run = Run(folder, parse, extract)
    log = log_dir / f"{slug}.log"
    result = {"slug": slug, "status": "ok", "log": str(log)}
    if run.grounding_json.is_file():
        result["status"] = "skipped (run exists)"
    else:
        with log.open("w") as fh:
            for cmd in ([PY, SCRIPTS / "run_ade.py", slug, "--parse", parse, "--extract", extract],
                        [PY, SCRIPTS / "build_images.py", slug, "--parse", parse, "--extract", extract]):
                fh.write(f"$ {' '.join(map(str, cmd[1:]))}\n")
                fh.flush()
                code = subprocess.run(list(map(str, cmd)), stdout=fh, stderr=subprocess.STDOUT).returncode
                if code:
                    result["status"] = f"FAILED in {Path(cmd[1]).name} (exit {code})"
                    return result
    entry = next((r for r in json.loads((folder / "manifest.json").read_text()).get("runs", [])
                  if (r["parse_model"], r["extract_model"]) == (parse, extract)), {})
    result["credits"] = (entry.get("parse_credits") or 0) + (entry.get("extract_credits") or 0)
    if run.grounding_json.is_file():
        g = json.loads(run.grounding_json.read_text())
        manifest = json.loads((folder / "manifest.json").read_text())
        wanted = [f["path"] for f in manifest.get("fields", [])]
        got = {f["path"]: f for f in g.get("fields", [])}
        problems = []
        for path in wanted:
            f = got.get(path)
            if f is None:
                problems.append(f"{path}: not located")
            elif not f.get("matched"):
                problems.append(f"{path}: OFF")
            elif f.get("page") != manifest.get("feature_page"):
                problems.append(f"{path}: page {f.get('page')}")
        result["problems"] = problems
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slugs", nargs="*")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--from-file")
    parser.add_argument("--parse", required=True)
    parser.add_argument("--extract", default=EXTRACT_MODEL)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--log-dir", required=True)
    parser.add_argument("--summary", help="write the results as JSON here")
    args = parser.parse_args()

    slugs = list(args.slugs)
    if args.all:
        slugs = sorted(p.name for p in COLLECTION.iterdir() if p.is_dir())
    if args.from_file:
        slugs += [s.strip() for s in Path(args.from_file).read_text().split() if s.strip()]
    if not slugs:
        parser.error("name slugs, --from-file or --all")
    parse = parse_snapshot(args.parse)
    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(one, s, parse, args.extract, log_dir): s for s in slugs}
        for fut in as_completed(futures):
            r = fut.result()
            results.append(r)
            note = "; ".join(r.get("problems") or [])
            credits = f", {r['credits']:.2f} credits" if "credits" in r else ""
            print(f"[{len(results)}/{len(slugs)}] {r['slug']}: {r['status']}{credits}"
                  + (f"  | {note}" if note else ""), flush=True)

    results.sort(key=lambda r: r["slug"])
    total = sum(r.get("credits") or 0 for r in results)
    failed = [r for r in results if r["status"].startswith("FAILED")]
    flagged = [r for r in results if r.get("problems")]
    print(f"\n{len(results)} folder(s), {total:.1f} credits, {len(failed)} failed, "
          f"{len(flagged)} with featured-field problems")
    if args.summary:
        Path(args.summary).write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
