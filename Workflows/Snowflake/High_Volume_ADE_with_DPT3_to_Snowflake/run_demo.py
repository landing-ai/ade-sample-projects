"""
run_demo.py
-----------
Entry point for the High-Volume ADE (DPT-3) -> Snowflake streaming demo.

    python run_demo.py                      # process ./input_documents
    python run_demo.py --input /path/docs   # a different folder
    python run_demo.py --replicate 250      # simulate volume from the samples
    python run_demo.py --workers 24         # more concurrency
    python run_demo.py --verify             # SELECT COUNT(*) per table after the run

--replicate makes N working copies of the input files (unique names) so you can
see the streaming rate without hundreds of real PDFs on hand. NOTE: each copy is
parsed independently and consumes ADE credits — use a modest N to demo.
"""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path
from typing import List

from config import Settings
from invoice_schema import InvoiceExtractionSchema
from pipeline import run_streaming


def gather_files(input_dir: str, exts) -> List[str]:
    root = Path(input_dir)
    if not root.exists():
        raise SystemExit(f"Input folder not found: {root.resolve()}")
    return sorted(str(p) for p in root.rglob("*") if p.suffix.lower() in exts)


def replicate(files: List[str], n: int) -> List[str]:
    """Fan the source files out to n unique-named copies in a temp dir."""
    if n <= len(files):
        return files[:n] if n else files
    tmp = Path(tempfile.mkdtemp(prefix="ade_demo_vol_"))
    out: List[str] = []
    for i in range(n):
        src = Path(files[i % len(files)])
        dst = tmp / f"{src.stem}_{i:05d}{src.suffix}"
        shutil.copy2(src, dst)
        out.append(str(dst))
    print(f"Replicated {len(files)} sample file(s) -> {n} copies in {tmp}")
    return out


def verify_counts(settings: Settings) -> None:
    from sf_loader import sfcursor, fq_table
    tables = [settings.table_main, settings.table_lines, settings.table_blocks, settings.table_markdown]
    print("\nRow counts in Snowflake:")
    with sfcursor(settings=settings) as cur:
        for t in tables:
            cur.execute(f"SELECT COUNT(*) FROM {fq_table(settings, t)}")
            print(f"  {t:22} {cur.fetchone()[0]:>10,}")


def main() -> None:
    ap = argparse.ArgumentParser(description="High-Volume ADE (DPT-3) -> Snowflake demo")
    ap.add_argument("--input", default=None, help="input folder (default: from config)")
    ap.add_argument("--replicate", type=int, default=0, help="simulate volume: N total docs")
    ap.add_argument("--workers", type=int, default=None, help="override MAX_WORKERS")
    ap.add_argument("--limit", type=int, default=0, help="process at most N files")
    ap.add_argument("--no-archive", action="store_true", help="skip archiving originals to RAW_DOCS")
    ap.add_argument("--verify", action="store_true", help="print row counts after the run")
    args = ap.parse_args()

    settings = Settings()
    if args.input:
        settings.input_dir = args.input
    if args.workers:
        settings.MAX_WORKERS = args.workers

    files = gather_files(settings.input_dir, settings.file_exts)
    if not files:
        raise SystemExit(f"No documents in {settings.input_dir}")
    if args.replicate:
        files = replicate(files, args.replicate)
    if args.limit:
        files = files[: args.limit]

    print(f"Processing {len(files)} document(s) with {settings.MAX_WORKERS} workers "
          f"(model: {settings.PARSE_MODEL}) -> {settings.DATABASE}.{settings.SNOWFLAKE_SCHEMA}\n")

    metrics = run_streaming(files, InvoiceExtractionSchema, settings,
                            archive_originals=not args.no_archive)
    print(metrics.summary())

    if args.verify:
        verify_counts(settings)


if __name__ == "__main__":
    main()
