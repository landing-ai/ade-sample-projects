# High-Volume Agentic Document Extraction → Snowflake (DPT-3)

Parse and extract a large batch of documents with **LandingAI ADE (DPT-3)** and
stream the structured results straight into **Snowflake** — at a high, continuous
insertion rate. Invoices are the worked example, but the pattern adapts to any
document type by swapping the schema.

Built on the current [`landingai-ade`](https://pypi.org/project/landingai-ade/) SDK
(`client.v2.parse` / `client.v2.extract`). See the
[DPT-3 Python docs](https://docs.landing.ai/dpt3/ade-python).

---

## Why it's fast

Two design choices do the work:

1. **Bulk `COPY INTO`, not row-by-row `INSERT`.** Rows are buffered, written as
   gzipped shards, `PUT` to an internal stage, and bulk-loaded with `COPY INTO`
   — Snowflake's recommended high-throughput path.
2. **Streaming, overlapped.** A thread pool parses+extracts many documents at
   once, and each document's rows are staged and `COPY`ed the moment it finishes
   (`copy_after_files=1`). Parsing and loading overlap, so rows land in Snowflake
   continuously instead of in one batch at the end.

```
input_documents/ ──▶ ThreadPool: v2.parse + v2.extract (many at once)
                            │  (per doc, as it finishes)
                            ▼
                    row_builder → main / line / block / markdown rows
                            │
                            ▼
                    Loader: gzip shard → PUT @INGEST_TMP → COPY INTO … PURGE
                            │
                            ▼
                     4 Snowflake tables (rows appear continuously)
```

---

## DPT-3 specifics (vs. older ADE)

- **Two calls:** `client.v2.parse(document=…)` then
  `client.v2.extract(schema=PydanticModel, markdown=…)`.
- **Separate model namespaces:** parse uses `dpt-3-pro-latest`, extract uses
  `extract-latest` (pin dated snapshots in production).
- **Parse returns a `structure` tree** (page → **block**), not a flat chunk list.
  Block text is sliced from the document markdown via each block's `range`;
  boxes are normalized 0–1 `xmin/ymin/xmax/ymax`; pages are 1-indexed.
- **Field evidence** is in `extraction_metadata[…]["ranges"]` (character ranges
  into the markdown); there is no confidence score.
- **Partial success (HTTP 206)** surfaces on `schema_violation_error` / `warnings`.

---

## Setup

```bash
cd "Workflows/Snowflake/High_Volume_ADE_with_DPT3_to_Snowflake"
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env-sample .env      # then fill in ADE + Snowflake values
```

`.env` holds your ADE key and Snowflake connection (RSA key-pair auth). It is
gitignored — never commit it.

Create the Snowflake objects (tables, stages, file formats, role) once:

```bash
# Edit names to match your account, then run in Snowsight or via SnowSQL:
snowflake_setup.sql
```

---

## Run

Two ways: an interactive notebook or the CLI.

**Notebook (recommended for a walkthrough / recording):**

```bash
jupyter notebook ADE_Snowflake_DPT3_Demo.ipynb
```

Run the cells top to bottom — config → canary parse+extract → create stages →
stream the batch (watch the live rate) → verify counts → query. Open a Snowsight
worksheet alongside and `SELECT COUNT(*)` while step 5 runs to see rows climb.

**CLI:**

```bash
python run_demo.py --verify        # process ./input_documents, then COUNT(*) per table
python run_demo.py --workers 24    # more concurrency
```

While it runs you get a live throughput line, and the summary shows the
scalability story — how much parse+extract work got compressed into the wall
clock by running concurrently and overlapping the loading:

```
  4/4 docs |  0.4 docs/s | ... | 61 rows -> Snowflake | ok=4 fail=0 | 10.2s
  ...
  Concurrency:  129s of parse+extract done in 47s wall  ->  2.7x overlap
```

The pattern streams the same way whether it's 4 documents or 4,000 — the demo
ships with 4 sample invoices to keep it runnable and cheap.

### Scale it up with your own documents

Point `--input` at a folder of real PDFs/images — genuine distinct rows, real
throughput:

```bash
python run_demo.py --input /path/to/your/invoices --verify
```

Swap `invoice_schema.py` for your own Pydantic schema (and update `COLS_MAIN`
/ `COLS_LINES` in `sf_loader.py` + the DDL) to handle a different document type.

> **Note:** `--replicate N` exists to *stress-test the rate* by fanning the
> samples out to N unique-named copies. It's synthetic — the copies are the same
> few invoices repeated (and each still spends ADE credits) — so use it to
> benchmark throughput, not to populate realistic-looking data.

---

## Output tables

| Table | Contents |
|---|---|
| `INVOICES_MAIN` | one row per invoice: header fields + `ADE_SDK_VERSION`, `SCHEMA_VIOLATION_ERROR`, and evidence `*_REF` (markdown ranges) |
| `INVOICE_LINE_ITEMS` | one row per line item |
| `PARSED_BLOCKS` | one row per parsed block: `BLOCK_TYPE`, `TEXT`, `PAGE` (1-indexed), normalized box |
| `MARKDOWN` | full parsed markdown (VARIANT) per document |

Original documents are archived to the `RAW_DOCS` stage (date-partitioned).

---

## Tuning throughput

- **`MAX_WORKERS`** — documents in flight. Raise it until you hit your ADE rate
  limit or warehouse saturation.
- **Warehouse size** — a bigger warehouse absorbs concurrent `COPY INTO`s.
- **Model pinning** — pin `dpt-3-pro-YYYYMMDD` / `extract-YYYYMMDD` for
  reproducible latency in production.

---

## File map

| File | Role |
|---|---|
| `ADE_Snowflake_DPT3_Demo.ipynb` | interactive walkthrough of the whole pipeline |
| `run_demo.py` | entry point; folder scan, optional volume replication, live run |
| `pipeline.py` | threaded streaming orchestration + live display |
| `ade_client.py` | DPT-3 `v2.parse` + `v2.extract` wrapper |
| `row_builder.py` | V2 structure tree + extraction → normalized rows |
| `sf_loader.py` | connection, buffered shards, `PUT` + `COPY INTO` |
| `metrics.py` | thread-safe throughput metrics + live status line |
| `invoice_schema.py` | Pydantic extraction schema |
| `config.py` | settings (`.env`) |
| `snowflake_setup.sql` | tables, stages, file formats, role/grants |

---

## Need help?

- [ADE (DPT-3) Python docs](https://docs.landing.ai/dpt3/ade-python)
- [ADE CLI](https://github.com/landing-ai/ade-cli)
- [Visual Playground](https://va.landing.ai/demo/doc-extraction) — build/test schemas
- [ADE support](https://docs.landing.ai/ade/ade-support)
