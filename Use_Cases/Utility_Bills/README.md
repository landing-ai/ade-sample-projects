# Utility Bill Extraction — LandingAI ADE

This use case extracts structured fields from **utility bills** (electric / gas)
using LandingAI's **Agentic Document Extraction (ADE)**. Utility bills are a
common proof-of-address document in KYC and onboarding workflows. Fields include
provider info, account details, billing summary, and electric/gas charges.

It ships **two independent implementations of the same task**, driven by the
**same shared schema** (`utility_bill.json`), so you can compare approaches side
by side:

| | `v1/` | `v2/` |
|---|---|---|
| Model family | **DPT-2** | **DPT-3** |
| Interface | `landingai-ade` **Python SDK** | **v2 REST APIs** (direct calls) |
| APIs used | Parse + Extract (SDK) | **Parse Jobs** + **Extract Jobs** (async) |
| Form factor | Jupyter notebook | Standalone Python scripts |
| Service tier | n/a | `standard` |

Both read the **same inputs** and the **same `utility_bill.json` schema**, so the
results are directly comparable.

## Folder layout

```
Utility_Bills/
├── input_folder/                 # 9 utility bills (6 PDF + 3 JPG), shared by both versions
├── utility_bill.json             # shared extraction schema (used by v1 AND v2)
├── images/                       # supporting images
├── README.md                     # this file
├── v1/                           # DPT-2, via the Python SDK
│   ├── parse_extract_utility_bills.ipynb   # walkthrough notebook
│   └── results_folder/           # generated outputs
└── v2/                           # DPT-3, via the v2 REST APIs
    ├── README.md                 # detailed v2 walkthrough
    ├── process_utility_bills.py  # end-to-end pipeline
    ├── ade_v2_client.py          # thin REST client for the v2 Jobs APIs
    └── results_folder/           # generated outputs (parse / extract / csv_summaries)
```

The schema is intentionally **not** duplicated — both versions load the single
`utility_bill.json` at the folder root.

## The two versions

### `v1/` — DPT-2 via the Python SDK
The original sample. It uses the `landingai-ade` SDK to parse each bill and
extract fields against the JSON schema, driven from a Jupyter notebook. Open
`v1/parse_extract_utility_bills.ipynb` to run it.

### `v2/` — DPT-3 via the v2 REST APIs
A newer sample that calls the **v2 REST endpoints directly** — submitting each
bill to **Parse Jobs**, polling for results, then running **Extract Jobs**
against the same schema — using the **DPT-3** model family. It runs as a plain
Python script. See [`v2/README.md`](v2/README.md) for the full walkthrough.

## Cost comparison (high level)

Both versions were run over the same 9 utility bills (**17 pages total**) with the
same schema. Costs below are **credits as reported by each API**.

| Stage | v1 (DPT-2) | v2 (DPT-3) | Difference |
|---|--:|--:|--:|
| Parse | 51.0 | 24.2 | **−53%** |
| Extract | 23.5 | 20.3 | **−14%** |
| **Total** | **74.5** | **44.5** | **−40%** |
| **Credits per page** | **4.4** | **2.6** | **−40%** |

For this set of bills, **v2 (DPT-3) costs about 40% fewer credits than v1
(DPT-2)**. Most of the savings come from the parse step: DPT-2 charged a flat 3.0
credits per page, while DPT-3 Parse Jobs (standard tier) is complexity-aware — and
because this corpus includes multi-page bills (up to 4 pages), the per-page
parse savings add up.

> **Notes.** This is a credits-to-credits comparison on one small sample, not a
> dollar quote. `v2` runs on the `standard` service tier (the lowest-cost tier).
> The two versions use different model families and pricing, so treat the numbers
> as directional guidance for this dataset rather than a universal benchmark.

## Getting started

Each version authenticates with a `VISION_AGENT_API_KEY` (environment variable or
a local `.env` file). Pick a folder and follow its instructions:

- **v1:** open `v1/parse_extract_utility_bills.ipynb`.
- **v2:** see [`v2/README.md`](v2/README.md), then run `python v2/process_utility_bills.py`.
