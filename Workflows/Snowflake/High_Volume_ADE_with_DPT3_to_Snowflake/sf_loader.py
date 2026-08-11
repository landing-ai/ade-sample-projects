"""
sf_loader.py
------------
Snowflake connection helpers + a buffered, high-throughput loader.

Load strategy (the reason this scales): rows are NOT inserted one at a time.
They are buffered, written as gzipped shards, ``PUT`` to an internal stage, and
bulk-loaded with ``COPY INTO`` — Snowflake's recommended high-rate path.

    add_main/add_line/add_block/add_markdown  ->  buffer
    flush                                     ->  gzip shard + PUT to @INGEST_TMP
    maybe_copy / close                        ->  COPY INTO <table> ... PURGE

In streaming mode the pipeline sets ``copy_after_files=1`` so each document's
shard is COPYed as soon as it lands — rows appear in Snowflake continuously
rather than in one batch at the end.
"""

from __future__ import annotations

import os
import io
import csv
import json
import gzip
import time
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, List, Optional

import snowflake.connector
from cryptography.hazmat.primitives import serialization

from config import Settings

# Column order for the CSV tables — must match the DDL in snowflake_setup.sql.
COLS_MAIN = [
    "run_id", "invoice_uuid", "document_name", "sent_at", "ade_sdk_version", "schema_violation_error",
    "invoice_date_raw", "invoice_date", "invoice_number", "order_date", "po_number", "status",
    "sold_to_name", "sold_to_address", "customer_email",
    "supplier_name", "supplier_address", "supplier_email", "supplier_phone",
    "payment_terms", "ship_via", "ship_date", "tracking_number",
    "currency", "total_due_raw", "total_due", "subtotal", "tax", "shipping",
    "supplier_name_ref", "total_due_ref",
]

COLS_LINES = [
    "run_id", "invoice_uuid", "document_name", "sent_at", "ade_sdk_version",
    "line_index", "line_number", "sku", "description", "quantity", "unit_price", "amount",
]


# ------------------------------------------------------------ connection ------

def _load_private_key(path: str) -> bytes:
    with open(path, "rb") as f:
        key = serialization.load_pem_private_key(f.read(), password=None)
    return key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def sf_connect(s: Settings):
    common = dict(
        user=s.SNOWFLAKE_USER,
        account=s.SNOWFLAKE_ACCOUNT_IDENTIFIER,
        role=s.ROLE,
        warehouse=s.WAREHOUSE,
        database=s.DATABASE,
        schema=s.SNOWFLAKE_SCHEMA,
        client_session_keep_alive=True,
    )
    auth = (s.SNOWFLAKE_AUTH or "keypair").lower()
    if auth == "externalbrowser":
        # Google/Okta/SSO: a browser window opens to sign in. The connector caches
        # the token so you're only prompted once per run.
        return snowflake.connector.connect(
            **common, authenticator="externalbrowser",
            client_store_temporary_credential=True,
        )
    if auth == "password":
        return snowflake.connector.connect(**common, password=s.SNOWFLAKE_PASSWORD)
    # default: RSA key-pair
    return snowflake.connector.connect(**common, private_key=_load_private_key(s.PRIVATE_KEY_FILE))


@contextmanager
def sfcursor(conn=None, settings: Optional[Settings] = None):
    owned = False
    if conn is None:
        conn = sf_connect(settings)
        owned = True
    try:
        with conn.cursor() as cur:
            yield cur
    finally:
        if owned:
            conn.close()


def fq_table(s: Settings, short: str) -> str:
    return f"{s.DATABASE}.{s.SNOWFLAKE_SCHEMA}.{short}"


def fq_stage(s: Settings, short: str) -> str:
    return f'@"{s.DATABASE}"."{s.SNOWFLAKE_SCHEMA}"."{short}"'


def ensure_formats_and_stages(s: Settings, conn=None) -> None:
    """Idempotently create the file formats and ingest stage the loader needs.
    Pass an existing ``conn`` to reuse a connection (avoids extra SSO prompts)."""
    with sfcursor(conn, s) as cur:
        cur.execute(
            f"CREATE FILE FORMAT IF NOT EXISTS {s.csv_file_format_name} "
            f"TYPE=CSV FIELD_DELIMITER=',' SKIP_HEADER=1 "
            f"FIELD_OPTIONALLY_ENCLOSED_BY='\"' NULL_IF=('')"
        )
        cur.execute(
            f"CREATE FILE FORMAT IF NOT EXISTS {s.json_file_format_name} "
            f"TYPE=JSON STRIP_OUTER_ARRAY=FALSE"
        )
        cur.execute(f"CREATE STAGE IF NOT EXISTS {s.stage_ingest_name}")


def put_original_to_raw_stage(local_path: str, s: Settings, conn=None) -> None:
    """Archive the original document to the raw stage, partitioned by date."""
    if not s.stage_raw_name:
        return
    date_part = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    dest = f"{fq_stage(s, s.stage_raw_name)}/date={date_part}"
    uri = "file://" + Path(local_path).resolve().as_posix()
    with sfcursor(conn, s) as cur:
        cur.execute(f"PUT '{uri}' {dest} AUTO_COMPRESS=FALSE OVERWRITE=TRUE")


# --------------------------------------------------------------- loader -------

class Loader:
    """Buffers rows, stages gzipped shards, and COPYs them into Snowflake."""

    def __init__(self, run_id: str, settings: Settings,
                 cols_main: List[str], cols_lines: List[str], conn=None):
        self.run_id = run_id
        self.S = settings
        self.cols_main = cols_main
        self.cols_lines = cols_lines
        # Reuse a shared connection when provided (one SSO login for the whole run);
        # only close it in close() if we opened it ourselves.
        self._owns_conn = conn is None
        self.conn = conn if conn is not None else sf_connect(settings)

        self._main_rows: List[dict] = []
        self._lines_rows: List[dict] = []
        self._blocks_jsonl: List[dict] = []
        self._markdown_jsonl: List[dict] = []

        self._main_ready: List[str] = []
        self._lines_ready: List[str] = []
        self._blocks_ready: List[str] = []
        self._markdown_ready: List[str] = []

        self._file_started = time.monotonic()

    # ---- public API ----
    def add_main(self, row):     self._csv_add(row, self._main_rows, self._flush_main)
    def add_line(self, row):     self._csv_add(row, self._lines_rows, self._flush_lines)
    def add_block(self, rec):    self._jsonl_add(rec, self._blocks_jsonl, self._flush_blocks)
    def add_markdown(self, rec): self._jsonl_add(rec, self._markdown_jsonl, self._flush_markdown)

    def maybe_copy(self):
        self._copy(self._main_ready, self.S.table_main, "main", True)
        self._copy(self._lines_ready, self.S.table_lines, "lines", True)
        self._copy(self._blocks_ready, self.S.table_blocks, "blocks_json", False)
        self._copy(self._markdown_ready, self.S.table_markdown, "markdown", False)

    def close(self):
        self._flush_main(); self._flush_lines(); self._flush_blocks(); self._flush_markdown()
        self._copy(self._main_ready, self.S.table_main, "main", True, force=True)
        self._copy(self._lines_ready, self.S.table_lines, "lines", True, force=True)
        self._copy(self._blocks_ready, self.S.table_blocks, "blocks_json", False, force=True)
        self._copy(self._markdown_ready, self.S.table_markdown, "markdown", False, force=True)
        if self._owns_conn:
            self.conn.close()

    # ---- buffering ----
    def _hit_threshold(self) -> bool:
        return (time.monotonic() - self._file_started) >= self.S.max_sec_per_file

    def _csv_add(self, row, buf, flusher):
        buf.append(row)
        if len(buf) >= self.S.max_rows_per_file or self._hit_threshold():
            flusher()

    def _jsonl_add(self, rec, buf, flusher):
        buf.append(rec)
        if len(buf) >= self.S.max_rows_per_file or self._hit_threshold():
            flusher()

    # ---- shard write + PUT ----
    def _write_gz(self, content: bytes, subdir: str) -> str:
        d = Path(f"ingest_tmp/run_id={self.run_id}/{subdir}")
        d.mkdir(parents=True, exist_ok=True)
        p = d / f"tmp{int(time.time() * 1e6)}.gz"
        p.write_bytes(content)
        return str(p)

    def _put(self, local_path: str, subdir: str, ready: List[str]):
        prefix = f"{fq_stage(self.S, self.S.stage_ingest_name)}/run_id={self.run_id}/{subdir}"
        uri = "file://" + Path(local_path).resolve().as_posix()
        with sfcursor(self.conn, self.S) as cur:
            cur.execute(f"PUT '{uri}' {prefix} AUTO_COMPRESS=FALSE OVERWRITE=TRUE")
        ready.append(os.path.basename(local_path))

    def _flush_csv(self, rows, cols, subdir, ready):
        if not rows:
            return
        out = io.StringIO()
        w = csv.DictWriter(out, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
        path = self._write_gz(gzip.compress(out.getvalue().encode("utf-8")), subdir)
        rows.clear(); self._file_started = time.monotonic()
        self._put(path, subdir, ready)

    def _flush_jsonl(self, rows, subdir, ready):
        if not rows:
            return
        payload = "\n".join(json.dumps(r, ensure_ascii=False, default=str) for r in rows)
        path = self._write_gz(gzip.compress(payload.encode("utf-8")), subdir)
        rows.clear(); self._file_started = time.monotonic()
        self._put(path, subdir, ready)

    def _flush_main(self):     self._flush_csv(self._main_rows, self.cols_main, "main", self._main_ready)
    def _flush_lines(self):    self._flush_csv(self._lines_rows, self.cols_lines, "lines", self._lines_ready)
    def _flush_blocks(self):   self._flush_jsonl(self._blocks_jsonl, "blocks_json", self._blocks_ready)
    def _flush_markdown(self): self._flush_jsonl(self._markdown_jsonl, "markdown", self._markdown_ready)

    # ---- COPY INTO ----
    def _copy(self, ready: List[str], table: str, subdir: str, is_csv: bool, *, force=False):
        stage = f"{fq_stage(self.S, self.S.stage_ingest_name)}/run_id={self.run_id}/{subdir}"
        if force:
            with sfcursor(self.conn, self.S) as cur:
                cur.execute(f"LIST {stage}")
                if not cur.fetchall():
                    return
        elif len(ready) < self.S.copy_after_files:
            return

        with sfcursor(self.conn, self.S) as cur:
            if is_csv:
                cur.execute(
                    f"COPY INTO {fq_table(self.S, table)} FROM {stage} "
                    f"PATTERN='.*\\.gz' FILE_FORMAT=(FORMAT_NAME={self.S.csv_file_format_name} SKIP_HEADER=1) "
                    f"PURGE=TRUE ON_ERROR=ABORT_STATEMENT"
                )
            else:
                cur.execute(
                    f"COPY INTO {fq_table(self.S, table)} FROM {stage} "
                    f"PATTERN='.*\\.gz' FILE_FORMAT=(FORMAT_NAME={self.S.json_file_format_name}) "
                    f"MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE PURGE=TRUE ON_ERROR=ABORT_STATEMENT"
                )
        ready.clear()
