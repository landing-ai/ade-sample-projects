"""Parse every PDF in data/pdfs with DPT-3 Verity and save the raw response.

Uses the `ade` CLI (standard tier). The CLI keeps its own store and serves a
document it has already parsed for free, so re-running this costs nothing.

    python scripts/parse.py                # all PDFs
    python scripts/parse.py lease_v2.pdf   # just one
"""
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "data" / "pdfs"
OUT_DIR = ROOT / "data" / "parsed"
MODEL = "dpt-3-verity"


def parse(pdf: Path) -> str:
    run = subprocess.run(
        ["ade", "parse", "-d", str(pdf), "--model", MODEL, "--tier", "standard",
         "--wait", "900", "--json"],
        capture_output=True, text=True)
    if run.returncode != 0:
        return f"{pdf.name}: FAILED\n{run.stdout}{run.stderr}"
    result = json.loads(run.stdout)
    shutil.copy(Path(result["store_dir"]) / "parse.json", OUT_DIR / f"{pdf.stem}.json")
    return (f"{pdf.name}: {result['page_count']} pages, model {result['version']}, "
            f"{result['credits']} credits{' (cached)' if result['cached'] else ''}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = [PDF_DIR / a for a in sys.argv[1:]] or sorted(PDF_DIR.glob("*.pdf"))
    with ThreadPoolExecutor(max_workers=4) as pool:
        for line in pool.map(parse, pdfs):
            print(line)


if __name__ == "__main__":
    main()
