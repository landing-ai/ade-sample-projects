# Invoice Extraction — LandingAI ADE

This use case parses a batch of **27 sample invoices** and extracts structured
fields (invoice info, customer, supplier, totals, and line items) using
LandingAI's **Agentic Document Extraction (ADE)**.

It ships **two independent implementations of the same task** so you can compare
approaches side by side:

| | `v1/` | `v2/` |
|---|---|---|
| Model family | **DPT-2** | **DPT-3** |
| Interface | `landingai-ade` **Python SDK** | **v2 REST APIs** (direct calls) |
| APIs used | Parse + Extract (SDK) | **Parse Jobs** + **Extract Jobs** (async) |
| Form factor | Jupyter notebook + helper modules | Standalone Python scripts |
| Service tier | n/a | `standard` |

Both read the **same inputs** and produce parsed Markdown, structured JSON, and
CSV summaries.

## Folder layout

```
Invoices/
├── input_folder/                 # 27 invoice PDFs (shared by both versions)
├── v1/                           # DPT-2, via the Python SDK
│   ├── invoices_demo_ade.ipynb   # walkthrough notebook
│   ├── ade_utilities.py          # parse/extract helpers
│   ├── invoice_schema.py         # extraction schema (Pydantic)
│   ├── invoice_utilities.py      # summary-table builders
│   └── results_folder/           # generated outputs
└── v2/                           # DPT-3, via the v2 REST APIs
    ├── README.md                 # detailed v2 walkthrough
    ├── process_invoices.py       # end-to-end pipeline
    ├── ade_v2_client.py          # thin REST client for the v2 Jobs APIs
    ├── schema/
    │   └── invoice_demo_schema.json  # extraction schema (JSON Schema)
    └── results_folder/           # generated outputs (parse / extract / csv_summaries)
```

## The two versions

### `v1/` — DPT-2 via the Python SDK
The original sample. It uses the `landingai-ade` SDK to parse each PDF and then
extract fields against a Pydantic schema, driven from a Jupyter notebook. This is
the quickest way to get started when the SDK covers your needs.

### `v2/` — DPT-3 via the v2 REST APIs
A newer sample that calls the **v2 REST endpoints directly** — submitting
documents to **Parse Jobs**, polling for results, then running **Extract Jobs**
against a JSON Schema — using the **DPT-3** model family. It runs as a plain
Python script and writes parse output, extraction JSON, and three CSV summaries.
See [`v2/README.md`](v2/README.md) for the full walkthrough.

## Cost comparison (high level)

Both versions were run over the same 27 invoices (**34 pages total**). Costs below
are **credits as reported by each API**.

| Stage | v1 (DPT-2) | v2 (DPT-3) | Difference |
|---|--:|--:|--:|
| Parse | 102.0 | 36.5 | **−64%** |
| Extract | 63.7 | 57.2 | **−10%** |
| **Total** | **165.7** | **93.7** | **−43%** |
| **Credits per page** | **4.9** | **2.8** | **−43%** |

For this invoice corpus, **v2 (DPT-3) costs about 43% fewer credits than v1
(DPT-2)** overall, with the largest savings on the parse step.

> **Notes.** This is a credits-to-credits comparison on one sample corpus, not a
> dollar quote. `v2` runs on the `standard` service tier (the lowest-cost tier).
> The two versions use different model families and pricing, so treat the numbers
> as directional guidance for this dataset rather than a universal benchmark.

## Getting started

Each version authenticates with a `VISION_AGENT_API_KEY` (environment variable or
a local `.env` file). Pick a folder and follow its instructions:

- **v1:** open `v1/invoices_demo_ade.ipynb`.
- **v2:** see [`v2/README.md`](v2/README.md), then run `python v2/process_invoices.py`.
