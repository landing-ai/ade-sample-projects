#!/usr/bin/env python3
"""Move a folder's output from the old layout into runs/<parse>/<extract>/.

    python document-types/scripts/migrate_runs.py invoice deed
    python document-types/scripts/migrate_runs.py --all

Old layout                 New layout
parse-<m>.json, .md        runs/<parse snapshot>/parse.json, parse.md
extract-<m>.json           runs/<parse snapshot>/<extract snapshot>/extract.json
grounding-<m>.json         runs/<parse snapshot>/<extract snapshot>/grounding.json
images/<m>/                runs/<parse snapshot>/<extract snapshot>/images/

The snapshot names come from metadata.model_version inside each file, so a folder is
filed under what actually ran, whatever alias was requested at the time. Each run is
recorded under "runs" in manifest.json, with its credits, and the folder's README and
manifest notes are updated where they name the old files.

Moves use `git mv`, so history follows the files. No API calls. A folder already in the
new layout is skipped, so this is safe to re-run, e.g. on a branch that merged after the
rest of the collection was migrated.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runs import COLLECTION, Run, run_entry  # noqa: E402

LEGACY_PARSE = re.compile(r"^parse-([a-z]+)\.json$")


def git_mv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "mv", str(src), str(dst)], cwd=src.parent, check=True,
                   capture_output=True)


def version_of(path: Path) -> str:
    version = json.loads(path.read_text(encoding="utf-8")).get("metadata", {}).get("model_version")
    if not version:
        sys.exit(f"{path} has no metadata.model_version; cannot tell which snapshot made it")
    return version


def migrate(folder: Path) -> list[str]:
    done = []
    manifest_path = folder / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    runs = [r for r in manifest.get("runs", [])]
    renames: dict[str, str] = {}

    for parse_json in sorted(folder.glob("parse-*.json")):
        m = LEGACY_PARSE.match(parse_json.name)
        if not m:
            continue
        model = m.group(1)
        extract_json = folder / f"extract-{model}.json"
        if not extract_json.is_file():
            sys.exit(f"{folder.name}: {parse_json.name} has no {extract_json.name}")
        run = Run(folder, version_of(parse_json), version_of(extract_json))
        if run.dir.exists():
            sys.exit(f"{folder.name}: {run.rel(run.dir)} already exists; not overwriting")

        moves = [
            (parse_json, run.parse_json),
            (folder / f"parse-{model}.md", run.parse_md),
            (extract_json, run.extract_json),
            (folder / f"grounding-{model}.json", run.grounding_json),
        ]
        for src, dst in moves:
            if src.is_file():
                git_mv(src, dst)
                renames[src.name] = run.rel(dst)
        images = folder / "images" / model
        if images.is_dir():
            git_mv(images, run.images_dir)
            renames[f"images/{model}/"] = run.rel(run.images_dir) + "/"
            renames[f"images/{model}"] = run.rel(run.images_dir)
        if (folder / "images").is_dir() and not any((folder / "images").iterdir()):
            (folder / "images").rmdir()

        # grounding.json named its run by family; name it by snapshot instead.
        if run.grounding_json.is_file():
            g = json.loads(run.grounding_json.read_text(encoding="utf-8"))
            g.pop("model", None)
            g = {"parse_model": run.parse_model, "extract_model": run.extract_model, **g}
            run.grounding_json.write_text(json.dumps(g, indent=2, ensure_ascii=False) + "\n",
                                          encoding="utf-8")

        runs = [r for r in runs if (r.get("parse_model"), r.get("extract_model"))
                != (run.parse_model, run.extract_model)]
        runs.append(run_entry(run))
        done.append(run.label)

    if not done:
        return done

    # Prose that names the old files: README and manifest notes. Longest first, so
    # images/pro/ is replaced before images/pro.
    def rewrite(text: str) -> str:
        for old in sorted(renames, key=len, reverse=True):
            text = re.sub(rf"(?<![\w/-]){re.escape(old)}(?![\w.])", renames[old], text)
        return text

    manifest["runs"] = sorted(runs, key=lambda r: (r["parse_model"], r["extract_model"]))
    if isinstance(manifest.get("notes"), str):
        manifest["notes"] = rewrite(manifest["notes"])
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8")
    readme = folder / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        new = rewrite(text)
        if new != text:
            readme.write_text(new, encoding="utf-8")
    return done


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slugs", nargs="*")
    parser.add_argument("--all", action="store_true", help="every folder in the collection")
    args = parser.parse_args()
    if not args.slugs and not args.all:
        parser.error("name slugs or pass --all")

    folders = (sorted(p for p in COLLECTION.iterdir() if p.is_dir()) if args.all
               else [COLLECTION / s for s in args.slugs])
    moved = skipped = 0
    for folder in folders:
        if not folder.is_dir():
            sys.exit(f"No such folder: {folder}")
        labels = migrate(folder)
        if labels:
            moved += 1
            print(f"{folder.name}: {', '.join(labels)}")
        else:
            skipped += 1
    print(f"\nmigrated {moved} folder(s), {skipped} already in the runs/ layout")


if __name__ == "__main__":
    main()
