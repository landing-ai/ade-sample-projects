# Food Label Processing — ADE v2 (DPT-3)

Batch pipeline that extracts structured product information from **food label
images**, built entirely on the LandingAI ADE **v2** async REST endpoints —
**Parse Jobs** and **Extract Jobs** — using the **DPT-3** model family. This is
the v2 counterpart to the SDK-based `../v1` notebook.

## What it does

For every file in `../input_folder`, the pipeline:

1. Submits it to **Parse Jobs v2** (`POST /v2/parse/jobs`, `standard` tier, `dpt-3-pro-latest`).
2. Saves the full parse response as `results_folder/parse/<name>_parse.json` and the
   Markdown as `results_folder/parse/<name>_parse.md`.
3. Loads the extraction schema from `schema/food_label_schema.json`.
4. Submits each document's Markdown + schema to **Extract Jobs v2**
   (`POST /v2/extract/jobs`, `standard` tier).
5. Saves the full extract response as `results_folder/extract/<name>_extract.json`.
6. Writes `results_folder/csv_summaries/food_label_fields_summary.csv` — all
   extracted fields, one row per document (+ `job_id`, `document_name`, `processing_date`).
7. Writes `results_folder/csv_summaries/processing_metadata.csv` — parse + extract
   metadata, one row per document.

## Extracted fields

The schema (`schema/food_label_schema.json`) is a flat set of 27 fields — the same
fields as the v1 Pydantic schema (`../v1/food_label_schema.py`), re-expressed as
JSON Schema so both versions extract identical data. It covers product
identification (name, brand, type, flavor), weight/serving info, and a large set
of boolean certification/claim flags (grass-fed, organic, non-GMO, keto, kosher,
gluten-free, USDA-inspected, etc.).

## API surface (v2 only)

| Action | Endpoint |
| --- | --- |
| Create parse job | `POST /v2/parse/jobs` |
| Poll parse job | `GET /v2/parse/jobs/{job_id}` |
| Create extract job | `POST /v2/extract/jobs` |
| Poll extract job | `GET /v2/extract/jobs/{job_id}` |

Host: `https://api.ade.landing.ai` · Auth: `Authorization: Bearer $VISION_AGENT_API_KEY`

## Run

```bash
export VISION_AGENT_API_KEY=your-key-here     # or use the ../.env file
pip install -r requirements.txt
python process_food_labels.py                 # all documents
python process_food_labels.py --limit 1       # smoke test on one
python process_food_labels.py --only chomps goji
```

## Files

- `ade_v2_client.py` — thin REST client for the four v2 job endpoints + polling
  (shared, unchanged from the other v2 samples).
- `process_food_labels.py` — the end-to-end pipeline (steps 1–7 above).
- `schema/food_label_schema.json` — the extraction schema (JSON rewrite of the v1 Pydantic model).
- `results_folder/` — generated output (`parse/`, `extract/`, `csv_summaries/`).

## Notes

- **Standard service tier** consumes half the credits of `priority`, with slower
  turnaround. The script submits all jobs first, then polls, so documents process
  in parallel server-side.
- Inputs are label photos (JPG); the v2 Parse API handles images and PDFs alike.
