"""Parse every PDF in input/ via the DPT-3 v2 staging endpoint, cache the JSON
in parsed/, and pre-rasterize each page to pages/<basename>/page_<n>.png.

Both caches are checked before any work — re-running this script is free.

Usage:
    cp .env.example .env  # fill in VISION_AGENT_API_KEY
    python ingest.py
"""
from __future__ import annotations

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import fitz  # PyMuPDF
import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv(override=True)  # .env wins over any pre-existing shell env vars

PROJECT_ROOT = Path(__file__).parent
INPUT_DIR = PROJECT_ROOT / "input"
PARSED_DIR = PROJECT_ROOT / "parsed"
PAGES_DIR = PROJECT_ROOT / "pages"

API_URL = "https://api.va.staging.landing.ai/v2/ade/parse"
RASTER_DPI = 144  # pre-rasterized PNG resolution; coordinate scaling handled later
MAX_WORKERS = 4   # concurrent parses; bumped any higher tends to trip rate limits


@dataclass
class Result:
    name: str
    cached_parse: bool
    cached_raster: bool
    page_count: int
    credits: float
    failed_pages: list[int]
    error: str | None = None


def get_api_key() -> str:
    key = os.environ.get("VISION_AGENT_API_KEY")
    if not key:
        sys.exit(
            "VISION_AGENT_API_KEY is not set. Either:\n"
            "  - copy .env.example to .env and fill it in, or\n"
            "  - export VISION_AGENT_API_KEY=pat_xxx"
        )
    return key


def parse_pdf(pdf_path: Path, api_key: str) -> dict:
    """POST one PDF to /v2/ade/parse. Returns the parsed JSON.

    Treats 200 and 206 (partial success) as successful — the caller inspects
    metadata.failed_pages to surface partial failures.
    """
    with open(pdf_path, "rb") as f:
        files = {"document": (pdf_path.name, f, "application/pdf")}
        r = requests.post(
            API_URL,
            headers={"Authorization": f"Basic {api_key}"},
            files=files,
            timeout=600,
        )
    if r.status_code not in (200, 206):
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:400]}")
    return r.json()


def rasterize_pdf(pdf_path: Path, out_dir: Path, dpi: int = RASTER_DPI) -> int:
    """Render each page to PNG. Returns page count."""
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    try:
        zoom = dpi / 72  # PDF native is 72 dpi
        mat = fitz.Matrix(zoom, zoom)
        for page_num in range(len(doc)):
            out_path = out_dir / f"page_{page_num}.png"
            if out_path.exists():
                continue
            pix = doc[page_num].get_pixmap(matrix=mat, alpha=False)
            pix.save(str(out_path))
        return len(doc)
    finally:
        doc.close()


def process_one(pdf_path: Path, api_key: str) -> Result:
    basename = pdf_path.stem
    parsed_path = PARSED_DIR / f"{basename}.json"
    pages_subdir = PAGES_DIR / basename

    # Parse (with cache)
    if parsed_path.exists():
        with open(parsed_path) as f:
            parse_data = json.load(f)
        cached_parse = True
    else:
        parse_data = parse_pdf(pdf_path, api_key)
        PARSED_DIR.mkdir(exist_ok=True)
        with open(parsed_path, "w") as f:
            json.dump(parse_data, f)
        cached_parse = False

    meta = parse_data.get("metadata", {})
    page_count = meta.get("page_count", 0)
    credits = float(meta.get("credit_usage", 0.0))
    failed_pages = list(meta.get("failed_pages", []))

    # Rasterize (with cache)
    raster_existed = pages_subdir.exists() and any(pages_subdir.glob("page_*.png"))
    rasterize_pdf(pdf_path, pages_subdir)

    return Result(
        name=pdf_path.name,
        cached_parse=cached_parse,
        cached_raster=raster_existed,
        page_count=page_count,
        credits=credits,
        failed_pages=failed_pages,
    )


def main() -> int:
    pdfs = sorted(INPUT_DIR.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"No PDFs found in {INPUT_DIR}")

    api_key = get_api_key()
    print(f"Processing {len(pdfs)} PDF(s) into parsed/ and pages/")
    print(f"  endpoint: {API_URL}")
    print(f"  raster dpi: {RASTER_DPI}")
    print(f"  workers: {MAX_WORKERS}\n")

    results: list[Result] = []
    new_credits = 0.0
    failures: list[tuple[str, str]] = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_pdf = {executor.submit(process_one, p, api_key): p for p in pdfs}
        for future in tqdm(as_completed(future_to_pdf), total=len(pdfs), unit="pdf"):
            pdf = future_to_pdf[future]
            try:
                result = future.result()
                results.append(result)
                if not result.cached_parse:
                    new_credits += result.credits
                cache_mark = "cached" if result.cached_parse else "parsed"
                fail_mark = f" — FAILED PAGES: {result.failed_pages}" if result.failed_pages else ""
                tqdm.write(
                    f"  {pdf.name}: {result.page_count} pages, "
                    f"{result.credits:.2f} credits [{cache_mark}]{fail_mark}"
                )
            except Exception as e:
                failures.append((pdf.name, str(e)))
                tqdm.write(f"  {pdf.name}: ERROR — {e}")

    # Summary
    print("\n" + "=" * 60)
    print(f"Processed: {len(results)} / {len(pdfs)} PDFs")
    total_pages = sum(r.page_count for r in results)
    total_credits_charged = sum(r.credits for r in results)
    print(f"Total pages: {total_pages}")
    print(f"Total credits across all docs: {total_credits_charged:.2f}")
    print(f"New credits spent this run: {new_credits:.2f}")
    if failures:
        print(f"\nFailures: {len(failures)}")
        for name, err in failures:
            print(f"  {name}: {err}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
