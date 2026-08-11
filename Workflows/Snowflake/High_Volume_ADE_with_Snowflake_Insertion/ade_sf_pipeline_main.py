
"""
ade_sf_pipeline_main.py
------------------------
Streaming ADE → Snowflake Orchestration

This script provides a minimal, production-grade pipeline that:
- Parses documents using LandingAI's Agentic Document Extraction (ADE) via the
  `landingai-ade` SDK's DPT-3 endpoints (`client.v2.parse` / `client.v2.extract`)
- Extracts structured information into rows using a schema-driven function
- Writes results to Snowflake (via staged CSV/JSONL files and COPY INTO)

Key Features:
-------------
• Threaded streaming pipeline with per-document parallelism using ThreadPoolExecutor
• Timing and metrics collection (parse time, copy time, wall time, pages processed)
• Configurable settings via a Pydantic Settings object (see config.py)
• Automatic foldering, UUID-based run tracking, and page count support
• Supports custom ADE schema (Pydantic) and row transformation logic (rows_from_doc)

Expected Workflow:
------------------
1. Call `run_pipeline_streaming()` with:
    - A list of document file paths
    - A schema class defining the ADE structure
    - A row-building function (`rows_from_doc`) that maps parsed output to rows
    - Optional: Settings, column definitions, worker count, run_id suffix

2. Each document will be:
    - Parsed with ADE
    - Converted to structured rows (main, line items, chunks, markdown)
    - Written to local CSV/JSONL shards and staged to Snowflake via COPY INTO

3. Metrics are returned as a `Metrics` object with:
    - Number of successful/failed documents
    - Total pages processed
    - Wall time, parse time, copy time
    - Per-page and per-document averages

Configuration:
--------------
• The number of concurrent workers is controlled by `settings.max_workers`, or defaults to 16.
• Staging thresholds, paths, and format options are customizable via `Settings`.
• Tables and stages must be pre-created in Snowflake using the accompanying `.sql` setup file.

Dependencies:
-------------
- LandingAI `landingai-ade` SDK (DPT-3 `client.v2` endpoints)
- Snowflake Python Connector
- Your own config, loader, row_builder, doc_utils modules

"""

from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, uuid, os

from config import Settings
from version_utils import get_installed_version
from loader import Loader
from metrics import Metrics
from doc_utils import get_doc_pages
from row_builder import rows_from_doc
from sf_utils import ensure_formats_and_stages, put_original_to_raw_stage

# DPT-3 model versions used for parse and extract. Pin to a dated snapshot
# (e.g. "dpt-3-pro-20260401") in production for reproducibility.
PARSE_MODEL = "dpt-3-pro-latest"
EXTRACT_MODEL = "dpt-3-pro-latest"


def run_pipeline_streaming(
    files: Iterable[str],
    schema_cls: Any,  # REQUIRED
    rows_from_doc_fn: Callable[[str, Any, Any, str, datetime, str],
                               Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any], str]],
    settings: Optional[Settings] = None,
    cols_main: Optional[List[str]] = None,
    cols_lines: Optional[List[str]] = None,
    max_threads: Optional[int] = None,
    run_id_suffix: str = "",
) -> Metrics:
    """
    Per-file concurrent pipeline:
      - client.v2.parse(document=fp) then client.v2.extract(schema=schema_cls,
        markdown=...) for each fp (ThreadPoolExecutor)
      - build rows, stage shards, copy to tables
    """
    from landingai_ade import LandingAIADE

    if settings is None:
        settings = Settings()
    if cols_main is None or cols_lines is None:
        raise ValueError("Provide cols_main and cols_lines so CSV columns map correctly to your tables.")
    if schema_cls is None:
        raise ValueError("schema_cls is required.")

    # The SDK reads VISION_AGENT_API_KEY from the environment; pass it explicitly
    # so the key sourced via Settings (.env) is always honored.
    client = LandingAIADE(apikey=settings.VISION_AGENT_API_KEY)

    sdk_version = get_installed_version("landingai-ade")
    file_list = [str(fp) for fp in files]

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "_" + uuid.uuid4().hex[:6] + run_id_suffix
    loader = Loader(run_id, settings, cols_main=cols_main, cols_lines=cols_lines)
    metrics = Metrics()
    metrics.start()  # wall_start

    # Adjust threshold so each file triggers COPY
    original_threshold = settings.copy_after_files
    settings.copy_after_files = 1

    def _work(fp: str):
        t_parse0 = time.perf_counter()
        # DPT-3 splits parsing and extraction into two calls.
        parse_result = client.v2.parse(document=fp, model=PARSE_MODEL)
        extract_result = client.v2.extract(
            schema=schema_cls, markdown=parse_result.markdown, model=EXTRACT_MODEL
        )
        parse_latency = time.perf_counter() - t_parse0

        put_original_to_raw_stage(fp, settings, loader.conn)

        sent_at = datetime.now(timezone.utc)
        pages = get_doc_pages(parse_result)

        main_row, line_rows, chunk_rows, markdown_record, _uuid = rows_from_doc_fn(
            fp=fp, parse_result=parse_result, extract_result=extract_result,
            run_id=run_id, sent_at=sent_at, sdk_version=sdk_version,
        )

        if main_row: loader.add_main(main_row)
        for r in (line_rows or []): loader.add_line(r)
        for r in (chunk_rows or []): loader.add_chunk(r)
        if markdown_record: loader.add_markdown(markdown_record)

        loader.maybe_copy()
        return parse_latency, pages

    try:
        mw = settings.max_threads
        with ThreadPoolExecutor(max_workers=mw) as pool:
            futs = {pool.submit(_work, fp): fp for fp in file_list}
            for fut in as_completed(futs):
                fp = futs[fut]
                try:
                    parse_lat, pages = fut.result()
                    metrics.mark_parse_latency(parse_lat)
                    metrics.pages_total += pages
                    metrics.mark_ok()
                except Exception:
                    metrics.mark_fail()

        t_copy0 = time.perf_counter()
        loader.close()
        metrics.copy_seconds += time.perf_counter() - t_copy0
        metrics.run_id = run_id
        metrics.stop()  # wall_end
        return metrics
    finally:
        settings.copy_after_files = original_threshold
