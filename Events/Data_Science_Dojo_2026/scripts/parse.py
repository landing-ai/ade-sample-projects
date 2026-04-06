"""
parse.py  —  Batch-parse PDFs using the LandingAI ADE Parse API.

Sends every PDF in data/pdfs/ to the Parse API concurrently and saves:
  data/pipeline_outputs/parsed/<stem>_parse_response.json  (full API response)
  data/pipeline_outputs/parsed/<stem>_markdown.md          (markdown text only)

Timing: prints per-file duration and a final summary.

Usage:
  python scripts/parse.py
  python scripts/parse.py --workers 2
"""

import argparse
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["VISION_AGENT_API_KEY"]
PARSE_URL = "https://api.va.landing.ai/v1/ade/parse"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

PDF_DIR = Path("data/pdfs")
OUT_DIR = Path("data/pipeline_outputs/parsed")
DEFAULT_WORKERS = 6  # adjust based on your API rate limits


def parse_one(pdf_path: Path) -> dict:
    """Parse a single PDF and save outputs. Returns a result dict with timing."""
    stem = pdf_path.stem
    t_start = time.perf_counter()

    with open(pdf_path, "rb") as f:
        response = requests.post(
            PARSE_URL,
            headers=HEADERS,
            files={"document": (pdf_path.name, f, "application/pdf")},
        )

    elapsed = time.perf_counter() - t_start

    if response.status_code != 200:
        return {
            "file": pdf_path.name,
            "status": "error",
            "elapsed_s": elapsed,
            "error": f"HTTP {response.status_code}: {response.text[:300]}",
        }

    data = response.json()

    # Save full API response
    (OUT_DIR / f"{stem}_parse_response.json").write_text(json.dumps(data, indent=2))

    # Save markdown only — this is what Extract and Build Schema consume
    markdown = data.get("markdown", "")
    (OUT_DIR / f"{stem}_markdown.md").write_text(markdown)

    pages = data.get("metadata", {}).get("page_count", "?")
    chars = len(markdown)
    return {
        "file": pdf_path.name,
        "status": "ok",
        "elapsed_s": elapsed,
        "pages": pages,
        "markdown_chars": chars,
    }


def main():
    parser = argparse.ArgumentParser(description="Batch-parse PDFs with LandingAI ADE.")
    parser.add_argument(
        "--workers", type=int, default=DEFAULT_WORKERS,
        help=f"Parallel workers (default: {DEFAULT_WORKERS})",
    )
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(PDF_DIR.glob("*.pdf"))

    if not pdfs:
        print(f"No PDFs found in {PDF_DIR}/")
        return

    print(f"Parsing {len(pdfs)} PDF(s) with {args.workers} worker(s)...\n")
    wall_start = time.perf_counter()
    results = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(parse_one, p): p for p in pdfs}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if result["status"] == "ok":
                print(
                    f"  OK  {result['file']:<35}  "
                    f"{result['elapsed_s']:>5.1f}s  "
                    f"{result['pages']} page(s)  "
                    f"{result['markdown_chars']:,} chars"
                )
            else:
                print(f"  ERR {result['file']:<35}  {result['error']}")

    wall_elapsed = time.perf_counter() - wall_start
    ok = sum(1 for r in results if r["status"] == "ok")
    errors = [r for r in results if r["status"] == "error"]

    print(f"\n{'─' * 65}")
    print(f"  {ok}/{len(pdfs)} succeeded  |  wall time: {wall_elapsed:.1f}s  |  avg: {wall_elapsed/len(pdfs):.1f}s/file")
    if errors:
        print(f"\n  Failed files:")
        for e in errors:
            print(f"    {e['file']}: {e['error']}")
    print(f"\n  Outputs saved to: {OUT_DIR}/\n")


if __name__ == "__main__":
    main()
