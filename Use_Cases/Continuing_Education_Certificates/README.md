# CME Certificate Extraction — LandingAI ADE

This use case extracts structured fields from **Continuing Medical Education
(CME) certificates** using LandingAI's **Agentic Document Extraction (ADE)**. It
parses each certificate and pulls 8 fields: recipient name, issuing organization,
activity title, award date, credit awarded (raw + numeric), and AMA PRA
Category 1 / Category 2 indicators.

It ships **two independent implementations of the same task** so you can compare
approaches side by side:

| | `v1/` | `v2/` |
|---|---|---|
| Model family | **DPT-2** | **DPT-3** |
| Interface | `landingai-ade` **Python SDK** | **v2 REST APIs** (direct calls) |
| APIs used | Parse + Extract (SDK) | **Parse Jobs** + **Extract Jobs** (async) |
| Form factor | Jupyter notebook + helpers | Standalone Python scripts |
| Service tier | n/a | `standard` |

Both read the **same inputs** and use the **same 8-field schema**, so the results
are directly comparable.

## Folder layout

```
Continuing_Education_Certificates/
├── input_folder/                 # 5 CME certificate images (shared by both versions)
├── README.md                     # this file
├── v1/                           # DPT-2, via the Python SDK
│   ├── field_extraction_notebook_cme.ipynb   # walkthrough notebook
│   └── results_folder/           # generated outputs
└── v2/                           # DPT-3, via the v2 REST APIs
    ├── README.md                 # detailed v2 walkthrough
    ├── process_certificates.py   # end-to-end pipeline
    ├── ade_v2_client.py          # thin REST client for the v2 Jobs APIs
    ├── schema/
    │   └── cme_demo_schema.json   # extraction schema (JSON Schema)
    └── results_folder/           # generated outputs (parse / extract / csv_summaries)
```

## The two versions

### `v1/` — DPT-2 via the Python SDK
The original sample. It uses the `landingai-ade` SDK to parse each certificate and
extract fields against a Pydantic schema, driven from a Jupyter notebook. Open
`v1/field_extraction_notebook_cme.ipynb` to run it.

### `v2/` — DPT-3 via the v2 REST APIs
A newer sample that calls the **v2 REST endpoints directly** — submitting each
image to **Parse Jobs**, polling for results, then running **Extract Jobs**
against a JSON Schema — using the **DPT-3** model family. It runs as a plain
Python script. See [`v2/README.md`](v2/README.md) for the full walkthrough.

## Cost comparison (high level)

Both versions were run over the same 5 certificates (**5 pages total**) with the
same 8-field schema. Costs below are **credits as reported by each API**.

| Stage | v1 (DPT-2) | v2 (DPT-3) | Difference |
|---|--:|--:|--:|
| Parse | 15.0 | 3.9 | **−74%** |
| Extract | 3.0 | 2.9 | **−3%** |
| **Total** | **18.1** | **6.8** | **−62%** |
| **Credits per page** | **3.6** | **1.4** | **−62%** |

For this set of certificates, **v2 (DPT-3) costs about 62% fewer credits than v1
(DPT-2)**. Nearly all of the savings come from the parse step: DPT-2 charged a
flat 3.0 credits per page, while DPT-3 Parse Jobs (standard tier) is
complexity-aware and much cheaper for these single-page documents.

> **Notes.** This is a credits-to-credits comparison on one small sample, not a
> dollar quote. `v2` runs on the `standard` service tier (the lowest-cost tier).
> The two versions use different model families and pricing, so treat the numbers
> as directional guidance for this dataset rather than a universal benchmark.

## Getting started

Each version authenticates with a `VISION_AGENT_API_KEY` (environment variable or
a local `.env` file). Pick a folder and follow its instructions:

- **v1:** open `v1/field_extraction_notebook_cme.ipynb`.
- **v2:** see [`v2/README.md`](v2/README.md), then run `python v2/process_certificates.py`.
