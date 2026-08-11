# ADE + Snowflake Insertion Pipeline

This project demonstrates a complete pipeline that uses **LandingAI's Agentic Document Extraction (ADE)** to parse documents and insert structured data into **Snowflake** tables. It uses **invoices as an example**, but the pattern is modular and can be adapted to **any document type**.

> **ADE version:** This pipeline uses the [`landingai-ade`](https://pypi.org/project/landingai-ade/) Python SDK against the **DPT-3** endpoints (`client.v2.parse` / `client.v2.extract`). See the [DPT-3 Python docs](https://docs.landing.ai/dpt3/ade-python).

Agentic Document Extraction offers complex layout extraction without layout-specific training, accurate extraction of tables and charts, and visual grounding for all extracted values, Learn more at [https://landing.ai/agentic-document-extraction](https://landing.ai/agentic-document-extraction).

LandingAI provides a [Visual Playground](https://va.landing.ai/demo/doc-extraction) with complimentary credits for new users. Use the Visual Playground to test performance on your own documents and develop your extrcation schema.

---

## 🧭 Two ways to run ADE + Snowflake

| | **This pipeline (SDK)** | **ADE Snowflake Native App** |
|---|---|---|
| Where ADE runs | Outside Snowflake, in Python (`landingai-ade`) | Inside Snowflake, as stored procedures |
| Best for | Full control of orchestration, concurrency, and row shaping | Staying entirely in Snowsight; no external egress |
| How results land | Streamed in via `PUT` + `COPY INTO` | Written directly to tables by the app |
| ZDR orgs | Handle egress yourself | `api.parse_v2` / `api.extract_v2` work with Zero Data Retention |

Both run the same DPT-3 models. If you prefer the in-Snowflake option, see
[`native_app_v2_procedures.sql`](native_app_v2_procedures.sql) in this folder and
the [ADE on Snowflake docs](https://docs.landing.ai/ade/ade-sf-overview). The rest
of this README covers the **SDK pipeline**.

---

## 🚀 Features

- ✅ Parse diverse invoice formats using ADE with a schema-first approach
- ✅ Generate structured rows for header, line items, and visual context
- ✅ Automatically stage and insert to Snowflake tables
- ✅ Canary pipeline for spot-testing a single file
- ✅ Streaming bulk processing with wall clock + parse timing

---

## 📁 Project Structure

```bash
project/
├── ade_sf_pipeline_main.py   # Main orchestration logic
├── config.py                 # Centralized settings from .env
├── sf_utils.py              # Snowflake connection + utilities
├── doc_utils.py             # Page counting + utilities
├── metrics.py               # Timing + performance tracking
├── version_utils.py         # Resolve landingai-ade version
├── row_builder.py           # Converts parsed doc into row dicts
├── row_utils.py             # Structure-tree walk + field helpers
├── loader.py                # Buffered uploader and COPY logic
├── invoice_schema.py        # Pydantic schema for ADE extraction
├── native_app_v2_procedures.sql # Alternative: in-Snowflake api.parse_v2/extract_v2
└── ADE_with_Snowflake_Insertion_Main.ipynb # Demo notebook
```

---

## 🔧 What You Provide

To customize this pipeline for your own documents:

1. ✅ **A Pydantic schema** (like `InvoiceExtractionSchema`) for ADE to extract fields
2. ✅ **A `rows_from_doc()` function** to convert parsed docs to database rows
3. ✅ **Column lists** (`COLS_MAIN`, `COLS_LINES`) matching your Snowflake tables

Modify only:
- `invoice_schema.py`
- `row_builder.py`
- `loader.py`

---

## 🧪 Notebook Workflow

Open `ADE_with_Snowflake_Insertion_Main.ipynb` to:

1. Configure ADE + Snowflake via `.env` or Settings
2. Parse and insert a **canary document**
3. Stream and time a **bulk directory of documents**
4. View metrics and Snowflake results

---

## 🏗️ Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

You’ll need:
- `landingai-ade`
- `snowflake-connector-python`
- `pydantic`
- `pydantic-settings`
- `python-dotenv`

### 2. Configure `.env` and `config.py``

Create a `.env` file following the example provided. See also [https://docs.landing.ai/ade/ade-retries#configuration-options](https://docs.landing.ai/ade/ade-retries#configuration-options)

See `config.py` for full list of available options.

### 3. Set up Snowflake

Examine the the SQL script included in this repo to create:

- File formats
- External stages
- Core tables
- A custom role with necessary privileges

---

## 📊 Output Tables

The following Snowflake tables will be populated:

- `INVOICES_MAIN` – Header fields like total, date, PO number. Includes
  `ADE_SDK_VERSION` (the `landingai-ade` version used) and
  `SCHEMA_VIOLATION_ERROR` (non-null when DPT-3 extract returns HTTP 206 /
  partial extraction).
- `INVOICE_LINE_ITEMS` – Itemized rows (quantity, price, description)
- `PARSED_BLOCKS` – Parsed blocks with page, box, and text. Blocks are
  derived by walking the DPT-3 parse `structure` tree; block text is sliced
  from the document markdown via each block's `range`, and grounding boxes
  (`xmin/ymin/xmax/ymax`) map to `box_l/box_t/box_r/box_b`.
- `MARKDOWN` – Parsed markdown with visual grounding

---

## 🤝 Need Help?

- 📚 [ADE Docs](https://docs.landing.ai/ade/ade-overview)
- 🤖 [ADE Support Bot + Discord](https://docs.landing.ai/ade/ade-support)
- 🧱 [agentic-doc GitHub](https://github.com/landing-ai/agentic-doc)


