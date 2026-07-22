# Food Label Extraction — LandingAI ADE

This use case extracts structured product information from **food label images**
using LandingAI's **Agentic Document Extraction (ADE)** — product identification
(name, brand, type, flavor), weight/serving info, and a large set of
certification and dietary-claim flags (organic, grass-fed, non-GMO, keto, kosher,
gluten-free, USDA-inspected, and more).

It ships **two independent implementations of the same task**, extracting the
**same fields**, so you can compare approaches side by side:

| | `v1/` | `v2/` |
|---|---|---|
| Model family | **DPT-2** | **DPT-3** |
| Interface | `landingai-ade` **Python SDK** | **v2 REST APIs** (direct calls) |
| APIs used | Parse + Extract (SDK) | **Parse Jobs** + **Extract Jobs** (async) |
| Form factor | Jupyter notebook + helpers | Standalone Python scripts |
| Schema | Pydantic (`food_label_schema.py`) | JSON Schema (`food_label_schema.json`) |
| Service tier | n/a | `standard` |

Both read the **same inputs** and extract the **same 27 fields** (the v2 JSON
schema was generated directly from the v1 Pydantic model), so results are
directly comparable.

## Folder layout

```
Food_Labels/
├── input_folder/                 # 6 food-label images (JPG), shared by both versions
├── README.md                     # this file
├── v1/                           # DPT-2, via the Python SDK
│   ├── food_labels_demo.ipynb    # walkthrough notebook
│   ├── food_label_schema.py      # Pydantic extraction schema
│   ├── food_label_utilities.py   # summary-table helper
│   └── results_folder/           # generated outputs (gitignored)
└── v2/                           # DPT-3, via the v2 REST APIs
    ├── README.md                 # detailed v2 walkthrough
    ├── process_food_labels.py    # end-to-end pipeline
    ├── ade_v2_client.py          # thin REST client for the v2 Jobs APIs
    ├── schema/
    │   └── food_label_schema.json # extraction schema (JSON rewrite of the v1 model)
    └── results_folder/           # generated outputs (parse / extract / csv_summaries)
```

## The two versions

### `v1/` — DPT-2 via the Python SDK
The original sample. It uses the `landingai-ade` SDK to parse each label and
extract fields against a Pydantic schema, driven from a Jupyter notebook. Open
`v1/food_labels_demo.ipynb` to run it.

### `v2/` — DPT-3 via the v2 REST APIs
A newer sample that calls the **v2 REST endpoints directly** — submitting each
image to **Parse Jobs**, polling for results, then running **Extract Jobs**
against a JSON Schema — using the **DPT-3** model family. It runs as a plain
Python script. See [`v2/README.md`](v2/README.md) for the full walkthrough.

## Cost comparison (high level)

Both versions were run over the same 6 food labels (**6 pages total**) extracting
the same 27 fields. Costs below are **credits as reported by each API**.

| Stage | v1 (DPT-2) | v2 (DPT-3) | Difference |
|---|--:|--:|--:|
| Parse | 18.0 | 4.5 | **−75%** |
| Extract | 6.0 | 5.7 | **−5%** |
| **Total** | **24.0** | **10.2** | **−58%** |
| **Credits per page** | **4.0** | **1.7** | **−58%** |

For this set of labels, **v2 (DPT-3) costs about 58% fewer credits than v1
(DPT-2)**. Nearly all of the savings come from the parse step: DPT-2 charged a
flat 3.0 credits per page, while DPT-3 Parse Jobs (standard tier) is
complexity-aware and much cheaper for these single-image labels.

> **Notes.** This is a credits-to-credits comparison on one small sample, not a
> dollar quote. `v2` runs on the `standard` service tier (the lowest-cost tier).
> The two versions use different model families and pricing, so treat the numbers
> as directional guidance for this dataset rather than a universal benchmark.

## Getting started

Each version authenticates with a `VISION_AGENT_API_KEY` (environment variable or
a local `.env` file). Pick a folder and follow its instructions:

- **v1:** open `v1/food_labels_demo.ipynb`.
- **v2:** see [`v2/README.md`](v2/README.md), then run `python v2/process_food_labels.py`.
