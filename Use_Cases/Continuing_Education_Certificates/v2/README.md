# CME Certificate Processing — ADE v2 (DPT-3)

Batch pipeline that extracts structured fields from **Continuing Medical
Education (CME) certificates**, built entirely on the LandingAI ADE **v2** async
REST endpoints — **Parse Jobs** and **Extract Jobs** — using the **DPT-3** model
family. This is the v2 counterpart to the SDK-based `../v1` notebook.

## What it does

For every file in `../input_folder`, the pipeline:

1. Submits it to **Parse Jobs v2** (`POST /v2/parse/jobs`, `standard` tier, `dpt-3-pro-latest`).
2. Saves the full parse response as `results_folder/parse/<name>_parse.json` and the
   Markdown as `results_folder/parse/<name>_parse.md`.
3. Loads the extraction schema from `schema/cme_demo_schema.json`.
4. Submits each document's Markdown + schema to **Extract Jobs v2**
   (`POST /v2/extract/jobs`, `standard` tier).
5. Saves the full extract response as `results_folder/extract/<name>_extract.json`.
6. Writes `results_folder/csv_summaries/certificate_fields_summary.csv` — all
   extracted fields, one row per document (+ `job_id`, `document_name`, `processing_date`).
7. Writes `results_folder/csv_summaries/processing_metadata.csv` — parse + extract
   metadata, one row per document.

## Extracted fields

The schema (`schema/cme_demo_schema.json`) is a flat set of 8 fields, **identical
to the v1 sample's schema** so the two versions can be compared directly:

`recipient_name`, `issuing_org`, `activity_title`, `date_awarded`,
`credit_awarded`, `credit_numeric`, `ama_pra_cat1`, `ama_pra_cat2`

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
python process_certificates.py                # all documents
python process_certificates.py --limit 1      # smoke test on one
python process_certificates.py --only CME_Mendez_ex1 CME_Mendez_ex2
```

## Files

- `ade_v2_client.py` — thin REST client for the four v2 job endpoints + polling
  (shared, unchanged from the Invoices v2 sample).
- `process_certificates.py` — the end-to-end pipeline (steps 1–7 above).
- `schema/cme_demo_schema.json` — the extraction schema.
- `results_folder/` — generated output (`parse/`, `extract/`, `csv_summaries/`).

## Notes

- **Standard service tier** consumes half the credits of `priority`, with slower
  turnaround. The script submits all jobs first, then polls, so documents process
  in parallel server-side.
- Inputs are images (PNG); the v2 Parse API handles PDFs and images alike.
