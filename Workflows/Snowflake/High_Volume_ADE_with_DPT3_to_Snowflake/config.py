"""
config.py
---------
Central configuration for the High-Volume ADE (DPT-3) -> Snowflake demo.

Values resolve in this order (highest precedence first):
  1. Arguments passed to ``Settings(...)`` in code
  2. Environment variables
  3. Values in a local ``.env`` file
  4. The defaults below

Copy ``.env-sample`` to ``.env`` and fill it in before running.
"""

from __future__ import annotations

from typing import Set
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # ---- LandingAI ADE (DPT-3) ----
    VISION_AGENT_API_KEY: str
    # Parse and extract use SEPARATE model namespaces.
    PARSE_MODEL: str = "dpt-3-pro-latest"     # e.g. dpt-3-pro-20260710
    EXTRACT_MODEL: str = "extract-latest"     # e.g. extract-20260710
    # Set to "eu" to use the EU region.
    ADE_ENVIRONMENT: str = "production"

    # ---- Input selection ----
    input_dir: str = "input_documents"
    file_exts: Set[str] = {".pdf", ".png", ".jpg", ".jpeg"}

    # ---- Throughput ----
    # Number of documents parsed+extracted concurrently.
    MAX_WORKERS: int = 16

    # ---- Snowflake connection (RSA key-pair auth) ----
    SNOWFLAKE_USER: str = "MACHINE_USER"
    SNOWFLAKE_ACCOUNT_IDENTIFIER: str = "YOUR_ORG-YOUR_ACCOUNT"
    PRIVATE_KEY_FILE: str = "/absolute/path/to/rsa_key.p8"
    ROLE: str = "ADE_DEMOS"
    WAREHOUSE: str = "ADE_WH"
    DATABASE: str = "ADE_DEMO"
    SNOWFLAKE_SCHEMA: str = "INVOICES"

    # ---- Loader thresholds (control how eagerly shards flush to Snowflake) ----
    # In streaming mode the pipeline forces a COPY per file so rows land in
    # near-real-time; these bound buffer size/latency otherwise.
    max_rows_per_file: int = 5000
    max_sec_per_file: float = 3.0
    copy_after_files: int = 1

    # ---- Table + stage names ----
    table_main: str = "INVOICES_MAIN"
    table_lines: str = "INVOICE_LINE_ITEMS"
    table_blocks: str = "PARSED_BLOCKS"
    table_markdown: str = "MARKDOWN"

    stage_ingest_name: str = "INGEST_TMP"
    stage_raw_name: str = "RAW_DOCS"
    csv_file_format_name: str = "CSV_STD"
    json_file_format_name: str = "JSON_STD"
