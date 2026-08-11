"""
pipeline.py
-----------
Threaded streaming orchestration: parse+extract many documents concurrently and
feed each result to the buffered Snowflake loader immediately, so rows land in
near-real-time rather than in one batch at the end.

    for each file (in a thread pool):
        parse_result, extract_result = client.v2.parse / client.v2.extract
        archive original PDF to the raw stage
        rows_from_doc(...) -> main / line / block / markdown rows
        loader.add_* ; loader.maybe_copy()   # COPY INTO fires per file

The main thread consumes completions as they finish and updates a live
throughput display.
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from importlib.metadata import version as _pkg_version, PackageNotFoundError
from typing import Any, List

from config import Settings
from ade_client import build_client, parse_and_extract
from row_builder import rows_from_doc
from sf_loader import Loader, COLS_MAIN, COLS_LINES, ensure_formats_and_stages, put_original_to_raw_stage
from metrics import Metrics


def _sdk_version() -> str:
    try:
        return _pkg_version("landingai-ade")
    except PackageNotFoundError:
        return "unknown"


def run_streaming(files: List[str], schema_cls: Any, settings: Settings,
                  archive_originals: bool = True) -> Metrics:
    """Run the full high-volume pipeline over ``files`` and return Metrics."""
    client = build_client(settings)
    sdk_version = _sdk_version()

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "_" + uuid.uuid4().hex[:6]
    ensure_formats_and_stages(settings)
    loader = Loader(run_id, settings, cols_main=COLS_MAIN, cols_lines=COLS_LINES)

    metrics = Metrics(total_docs=len(files))
    metrics.start()

    def _work(fp: str):
        t0 = time.perf_counter()
        parse_result, extract_result = parse_and_extract(client, fp, schema_cls, settings)
        latency = time.perf_counter() - t0

        if archive_originals:
            put_original_to_raw_stage(fp, settings, loader.conn)

        sent_at = datetime.now(timezone.utc)
        main_row, line_rows, block_rows, md_record, _ = rows_from_doc(
            fp=fp, parse_result=parse_result, extract_result=extract_result,
            run_id=run_id, sent_at=sent_at, sdk_version=sdk_version,
        )

        if main_row:
            loader.add_main(main_row)
        for r in line_rows:
            loader.add_line(r)
        for r in block_rows:
            loader.add_block(r)
        if md_record:
            loader.add_markdown(md_record)
        loader.maybe_copy()

        pages = int(getattr(getattr(parse_result, "metadata", None), "page_count", 0) or 0)
        rows = 1 + len(line_rows) + len(block_rows) + 1
        return latency, pages, rows

    try:
        with ThreadPoolExecutor(max_workers=settings.MAX_WORKERS) as pool:
            futures = {pool.submit(_work, fp): fp for fp in files}
            for fut in as_completed(futures):
                fp = futures[fut]
                try:
                    latency, pages, rows = fut.result()
                    metrics.record(ok=True, pages=pages, parse_sec=latency, rows=rows)
                except Exception as e:
                    metrics.record(ok=False, pages=0, parse_sec=0.0, rows=0)
                    print(f"\n  FAILED {fp}: {e}")
                metrics.print_live()

        loader.close()
    finally:
        metrics.stop()
    return metrics
