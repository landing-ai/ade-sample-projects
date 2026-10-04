#!/usr/bin/env python3
"""Branch, check, commit, push and open the PR for one document-type folder.

    ship.py start   <slug> [--base main] [--local]
    ship.py check   <slug> [--rules R.json] [--verify-also TERM ...] [--include PATH ...]
    ship.py ship    <slug> [--base main] [--rules ...] [--include ...] [--push] [--pr]
                           [--trailer LINE ...] [--pr-footer TEXT]
    ship.py cleanup <slug> [--delete-branch] [--force] [--base main]

Every document type gets its own git worktree and branch, so several builds can run at
once without trampling one checkout:

  start    creates <repo>-worktrees/<slug> on a new branch document-type-<slug> from
           origin/<base>, links the main checkout's .venv and .env into it (both are
           gitignored, links included), and copies the request file across, since
           request files are gitignored and exist only in the main checkout.
  check    the gates a folder must pass before it leaves this machine. See check().
  ship     check, then commit whatever is not yet committed. Pushing and opening the PR
           are separate flags, because both publish: nothing leaves without --push/--pr.
  cleanup  removes the worktree once the PR has merged, and moves the request file to
           document-types/requests/published/ once the folder is on origin/<base>.

Request files are local working papers, not part of the published collection: the whole
document-types/requests/ folder is gitignored. Anything at its top level is still to do,
in progress or rejected; requests/published/ holds the ones whose folder has merged.

Run any subcommand from anywhere in the repo or its worktrees. `check` and `ship` act on
the slug's worktree if there is one, otherwise on the current checkout.

The script writes no attribution of its own: pass --trailer for commit trailers and
--pr-footer for the PR body's last line.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdfmeta  # noqa: E402

REQUIRED = ["manifest.json", "schema.json", "README.md"]
MODEL_FILES = ["parse-{m}.json", "parse-{m}.md", "extract-{m}.json", "grounding-{m}.json"]
FORBIDDEN_NAMES = re.compile(r"(^|/)\.env|rules[^/]*\.json$|\.pem$|id_rsa|credentials", re.I)


# --------------------------------------------------------------------------- git helpers

def git(*args: str, cwd: Path | None = None, check: bool = True) -> str:
    out = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and out.returncode:
        sys.exit(f"git {' '.join(args)} failed:\n{out.stderr.strip()}")
    return out.stdout.strip()


def main_checkout() -> Path:
    """The primary working tree: the first entry of `git worktree list`."""
    first = git("worktree", "list", "--porcelain").splitlines()[0]
    return Path(first.removeprefix("worktree "))


def worktree_path(slug: str) -> Path:
    main = main_checkout()
    return main.parent / f"{main.name}-worktrees" / slug


def branch(slug: str) -> str:
    return f"document-type-{slug}"


def workdir(slug: str) -> Path:
    """Where `check` and `ship` act: the slug's worktree, else the current checkout."""
    wt = worktree_path(slug)
    return wt if wt.is_dir() else Path(git("rev-parse", "--show-toplevel"))


# --------------------------------------------------------------------------- start

def start(args) -> None:
    main, slug, base = main_checkout(), args.slug, args.base
    request = main / "document-types" / "requests" / f"{slug}.yaml"
    if not request.is_file():
        sys.exit(f"No request file at {request}. Write one first (/propose-document-types).")
    wt = worktree_path(slug)
    if wt.exists():
        sys.exit(f"{wt} already exists. Use it, or `ship.py cleanup {slug}` first.")
    if git("branch", "--list", branch(slug), cwd=main):
        sys.exit(f"Branch {branch(slug)} already exists locally.")

    # Branch from origin/<base>, or with --local from a local branch: for builds stacked
    # on tooling that is committed but not yet pushed.
    if args.local:
        start_point = base
    else:
        git("fetch", "--quiet", "origin", base, cwd=main)
        start_point = f"origin/{base}"
    if git("ls-tree", "--name-only", start_point,
           f"document-types/collection/{slug}", cwd=main):
        sys.exit(f"document-types/collection/{slug} already exists on {start_point}.")
    if git("ls-remote", "--heads", "origin", branch(slug), cwd=main):
        sys.exit(f"Branch {branch(slug)} already exists on origin.")

    wt.parent.mkdir(parents=True, exist_ok=True)
    git("worktree", "add", "--quiet", "-b", branch(slug), str(wt), start_point, cwd=main)
    # Shared, gitignored environment: one venv and one API key for every worktree.
    for name in (".venv", ".env"):
        if (main / name).exists() and not (wt / name).exists():
            (wt / name).symlink_to(main / name)
    target = wt / "document-types" / "requests" / f"{slug}.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(request, target)
    print(wt)


# --------------------------------------------------------------------------- check

def leaf_count(schema: dict) -> int:
    if schema.get("type") == "object" and "properties" in schema:
        return sum(leaf_count(v) for v in schema["properties"].values())
    if schema.get("type") == "array" and "items" in schema:
        return leaf_count(schema["items"])
    return 1


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def sweep(paths: list[Path], terms: list[str]) -> list[str]:
    """Originals that survive in any file: as literals (punctuation-blind) and, for five
    or more digits, inside any one run of digits. A run, not the file's digits strung
    together: that matched coordinates in a parse JSON by chance."""
    hits = []
    for p in paths:
        if p.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            continue
        if p.suffix.lower() == ".pdf":
            doc = pymupdf.open(p)
            # Form-field values live outside the page text, usually inside compressed
            # object streams the raw bytes do not show: a filled SBA 413 carried every
            # personal value only there.
            fields = "".join(f"\n{w.field_value or ''}" for page in doc for w in page.widgets())
            text = "".join(page.get_text() for page in doc) + json.dumps(doc.metadata) \
                + (doc.get_xml_metadata() or "") + fields + p.read_bytes().decode("latin-1")
        else:
            text = p.read_text(encoding="utf-8", errors="ignore")
        flat = norm(text)
        runs = [re.sub(r"\D", "", r) for r in re.findall(r"\d[\d\s.,/-]*\d", text)]
        for i, term in enumerate(terms, 1):
            digits = re.sub(r"\D", "", term)
            if (len(norm(term)) >= 5 and norm(term) in flat) or \
               (len(digits) >= 5 and any(digits in r for r in runs)):
                hits.append(f"{p.name}: term #{i}")
    return hits


def check(args) -> tuple[Path, dict, list[str]]:
    """Every gate a folder must pass before it leaves this machine. Returns the working
    directory, the manifest and the failures (empty when it passes)."""
    root, slug = workdir(args.slug), args.slug
    folder = root / "document-types" / "collection" / slug
    fail: list[str] = []
    if not folder.is_dir():
        return root, {}, [f"no folder at {folder}"]

    for name in REQUIRED:
        if not (folder / name).is_file():
            fail.append(f"missing {name}")
    try:
        manifest = json.loads((folder / "manifest.json").read_text())
    except (OSError, ValueError) as e:
        return root, {}, fail + [f"manifest.json unreadable: {e}"]

    source = manifest.get("source", {})
    origin = source.get("origin", {})
    model = args.model
    for pattern in MODEL_FILES:
        if not (folder / pattern.format(m=model)).is_file():
            fail.append(f"missing {pattern.format(m=model)}")
    if not (folder / "source" / source.get("file", "")).is_file():
        fail.append(f"source file {source.get('file')!r} not in source/")
    images = folder / "images" / model
    if not images.is_dir() or not any(images.glob("page-*.png")):
        fail.append(f"no page overlay in images/{model}/")

    if manifest.get("slug") != slug:
        fail.append(f"manifest slug {manifest.get('slug')!r} != {slug!r}")
    clearance = origin.get("clearance")
    if clearance not in {"public", "redacted"}:
        fail.append(f"clearance is {clearance!r}; must be public or redacted")
    for key in ("url", "publisher", "retrieved", "clearance_note"):
        if not origin.get(key):
            fail.append(f"origin.{key} missing")
    if clearance == "redacted" and not origin.get("redactions"):
        fail.append("clearance is redacted but origin.redactions is missing")
    fields = manifest.get("fields", [])
    if not 1 <= len(fields) <= 5:
        fail.append(f"{len(fields)} featured fields; 3 to 5 expected")
    for f in fields:
        if "," in f.get("label", ""):
            fail.append(f"label {f['label']!r} contains a comma")
    grounding = folder / f"grounding-{model}.json"
    if grounding.is_file():
        g = json.loads(grounding.read_text())
        pages = {x.get("page") for x in g.get("fields", [])}
        if pages - {manifest.get("feature_page")}:
            fail.append(f"fields resolve on page(s) {sorted(pages)}, "
                        f"feature_page is {manifest.get('feature_page')}")

    # The source PDF of a redacted document must carry no metadata at all.
    pdf = folder / "source" / source.get("file", "")
    if clearance == "redacted" and pdf.suffix.lower() == ".pdf" and pdf.is_file():
        left = pdfmeta.remaining(pymupdf.open(pdf))
        if left:
            fail.append(f"redacted source PDF still has metadata: {left}")

    # Nothing credential- or rules-shaped about to be committed.
    changed = git("status", "--porcelain", "--untracked-files=all", cwd=root).splitlines()
    for line in changed:
        path = line[3:]
        if FORBIDDEN_NAMES.search(path):
            fail.append(f"credential- or rules-shaped path in the change set: {path}")

    # The leak sweep. A redacted folder cannot be swept without the originals, so it
    # needs --rules; a public one is swept for --verify-also terms if any are given.
    terms = list(args.verify_also)
    if args.rules:
        terms = list(json.loads(Path(args.rules).read_text())) + terms
    elif clearance == "redacted":
        fail.append("clearance is redacted: pass --rules (the redaction rules file, "
                    "outside the repo) so the folder can be swept for the originals")
    if terms:
        paths = [p for p in folder.rglob("*") if p.is_file()] + \
                [root / p for p in args.include if (root / p).is_file()]
        fail += [f"leak: {h}" for h in sweep(paths, terms)]

    print(f"{slug}: {manifest.get('title')} — {source.get('pages')} page(s), clearance "
          f"{clearance}, {leaf_count(json.loads((folder / 'schema.json').read_text()))} "
          f"leaf fields, {len(fields)} featured on page {manifest.get('feature_page')}")
    print("check: " + ("PASS" if not fail else "FAIL"))
    for f in fail:
        print(f"  - {f}")
    return root, manifest, fail


# --------------------------------------------------------------------------- ship

def readme_section(readme: str, heading: str) -> str:
    """The body of a `## heading` section, up to the next `## `."""
    m = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", readme, re.M | re.S)
    return m.group(1).strip() if m else ""


def pr_body(root: Path, slug: str, manifest: dict, base: str, footer: str) -> str:
    folder = root / "document-types" / "collection" / slug
    source, origin = manifest["source"], manifest["source"]["origin"]
    schema = json.loads((folder / "schema.json").read_text())
    readme = (folder / "README.md").read_text()
    grounding = json.loads((folder / f"grounding-pro.json").read_text())
    rows = "\n".join(f"| {f['label']} | {f.get('value')} |" for f in grounding.get("fields", []))
    stacked = "" if base == "main" else f"\n**Stacked on `{base}`.** Merge that first.\n"
    cost = readme_section(readme, "Cost").split("\n\n")[0]
    return f"""## Summary
- Adds `document-types/collection/{slug}/`: {manifest['title']}, {source.get('pages')} {source.get('orientation')} page(s), parsed with DPT-3 Pro and extracted at standard tier with a {leaf_count(schema)}-leaf schema.
{stacked}
## Provenance
[{origin.get('title') or origin['url']}]({origin['url']}), published by {origin['publisher']}, retrieved {origin['retrieved']}. Clearance `{origin['clearance']}`.

{origin['clearance_note']}

## Featured fields (page {manifest['feature_page']})
| Field | Value |
|---|---|
{rows}

Every crop and the page overlay were checked by eye.

## Notes
{manifest.get('notes', '')}

{cost}

{footer}
""".rstrip() + "\n"


def ship(args) -> None:
    root, manifest, fail = check(args)
    if fail:
        sys.exit("Not shipping: fix the failures above.")
    slug = args.slug
    current = git("branch", "--show-current", cwd=root)
    if current != branch(slug):
        sys.exit(f"On branch {current!r}, expected {branch(slug)!r}. Run `ship.py start` "
                 "or check out the right branch.")

    paths = [f"document-types/collection/{slug}", *args.include]
    git("add", "--", *paths, cwd=root)
    staged = git("diff", "--cached", "--name-only", cwd=root).splitlines()
    stray = [p for p in staged if not any(p == q or p.startswith(q.rstrip("/") + "/")
                                          for q in paths)]
    if stray:
        sys.exit(f"Staged files outside this document type: {stray}. Unstage them first.")
    if staged:
        origin = manifest["source"]["origin"]
        labels = ", ".join(f["label"] for f in manifest["fields"])
        message = (f"Add {slug} document type assets\n\n"
                   f"{manifest['title']} from {origin['publisher']}; clearance "
                   f"{origin['clearance']}.\n\nFeatures page {manifest['feature_page']}: "
                   f"{labels}.\n")
        if args.trailer:
            message += "\n" + "\n".join(args.trailer) + "\n"
        git("commit", "--quiet", "-m", message, cwd=root)
        print(f"committed: {git('log', '--oneline', '-1', cwd=root)}")
    else:
        print("nothing new to commit")

    if args.push:
        git("push", "--quiet", "-u", "origin", branch(slug), cwd=root)
        print(f"pushed {branch(slug)}")
    if args.pr:
        if not args.push and not git("ls-remote", "--heads", "origin", branch(slug), cwd=root):
            sys.exit("--pr needs the branch on origin: add --push.")
        out = subprocess.run(
            ["gh", "pr", "create", "--base", args.base, "--head", branch(slug),
             "--title", f"Add {slug} document type assets",
             "--body", pr_body(root, slug, manifest, args.base, args.pr_footer)],
            cwd=root, capture_output=True, text=True)
        if out.returncode:
            sys.exit(f"gh pr create failed:\n{out.stderr.strip()}")
        print(out.stdout.strip())


# --------------------------------------------------------------------------- cleanup

def cleanup(args) -> None:
    main, wt = main_checkout(), worktree_path(args.slug)
    if wt.is_dir():
        if git("status", "--porcelain", cwd=wt) and not args.force:
            sys.exit(f"{wt} has uncommitted changes. Commit them, or pass --force.")
        git("worktree", "remove", *(["--force"] if args.force else []), str(wt), cwd=main)
        print(f"removed {wt}")
    if args.delete_branch:
        out = subprocess.run(["git", "branch", "-d", branch(args.slug)], cwd=main,
                             capture_output=True, text=True)
        print(out.stdout.strip() or out.stderr.strip())
    publish_request(main, args.slug, args.base)


def publish_request(main: Path, slug: str, base: str) -> None:
    """Move the request file to document-types/requests/published/ once the folder it
    produced is on origin/<base>.

    Request files never reach GitHub (the folder is gitignored), so this subfolder is the
    one place that says which requests are done: everything left at the top level is still
    to do, in progress, or rejected."""
    requests = main / "document-types" / "requests"
    local, done = requests / f"{slug}.yaml", requests / "published" / f"{slug}.yaml"
    if not local.is_file():
        return
    git("fetch", "--quiet", "origin", base, cwd=main)
    if not git("ls-tree", "--name-only", f"origin/{base}",
               f"document-types/collection/{slug}", cwd=main):
        print(f"kept requests/{slug}.yaml: its folder is not on origin/{base} yet")
        return
    if done.exists():
        print(f"kept requests/{slug}.yaml: requests/published/{slug}.yaml already exists")
        return
    done.parent.mkdir(exist_ok=True)
    local.rename(done)
    print(f"moved requests/{slug}.yaml to requests/published/")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("start", help="create the slug's worktree and branch")
    p.add_argument("slug")
    p.add_argument("--base", default="main")
    p.add_argument("--local", action="store_true",
                   help="branch from the local --base branch, not origin/<base>")
    p.set_defaults(func=start)

    for name, func in (("check", check), ("ship", ship)):
        p = sub.add_parser(name)
        p.add_argument("slug")
        p.add_argument("--model", default="pro")
        p.add_argument("--rules", help="redaction rules JSON (outside the repo): its keys "
                                       "are the originals the sweep looks for")
        p.add_argument("--verify-also", nargs="*", default=[], metavar="TERM")
        p.add_argument("--include", nargs="*", default=[], metavar="PATH",
                       help="other paths this document type changed, e.g. a script")
        if name == "ship":
            p.add_argument("--base", default="main")
            p.add_argument("--push", action="store_true")
            p.add_argument("--pr", action="store_true")
            p.add_argument("--trailer", nargs="*", default=[], metavar="LINE")
            p.add_argument("--pr-footer", default="")
        p.set_defaults(func=(lambda a: sys.exit(1 if check(a)[2] else 0))
                       if name == "check" else func)

    p = sub.add_parser("cleanup", help="remove the slug's worktree after merge")
    p.add_argument("slug")
    p.add_argument("--delete-branch", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--base", default="main",
                   help="branch the PR merged into: the request moves to "
                        "requests/published/ once the folder is there")
    p.set_defaults(func=cleanup)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
