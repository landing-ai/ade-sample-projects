# Invoice Processing — ADE v2 (DPT-3)

Batch invoice pipeline built entirely on the LandingAI ADE **v2** async REST APIs
(**Parse Jobs** and **Extract Jobs**) with the **DPT-3** model family. This is the
v2 counterpart to the SDK-based `../v1` sample.

## What it does

For every document in `../input_folder`, the pipeline:

1. Submits it to **Parse Jobs v2** (`POST /v2/parse/jobs`, `standard` tier, `dpt-3-pro-latest`).
2. Saves the full parse response as `results_folder/parse/<name>_parse.json` and the
   Markdown as `results_folder/parse/<name>_parse.md`.
3. Loads the extraction schema from `schema/invoice_demo_schema.json`.
4. Submits each document's Markdown + schema to **Extract Jobs v2**
   (`POST /v2/extract/jobs`, `standard` tier).
5. Saves the full extract response as `results_folder/extract/<name>_extract.json`.
6. Writes `results_folder/csv_summaries/invoice_fields_summary.csv` — all extracted
   fields except line items, one row per document (+ `job_id`, `document_name`,
   `processing_date`).
7. Writes `results_folder/csv_summaries/invoice_line_items.csv` — all line-item
   details, one row per item, keyed by `job_id` (+ `document_name`, `processing_date`).
8. Writes `results_folder/csv_summaries/processing_metadata.csv` — parse + extract
   metadata, one row per document.

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
export VISION_AGENT_API_KEY=your-key-here     # or use a .env file
pip install -r requirements.txt
python process_invoices.py
```

## Files

- `ade_v2_client.py` — thin REST client for the four v2 job endpoints + polling.
- `process_invoices.py` — the end-to-end pipeline (steps 1–8 above).
- `schema/invoice_demo_schema.json` — the extraction schema.
- `results_folder/` — generated output (`parse/`, `extract/`, `csv_summaries/`).

## Notes

- **Standard service tier** consumes half the credits of `priority`, with slower
  turnaround. The script submits all jobs first, then polls, so documents process
  in parallel server-side.
- The Parse v2 Markdown ends with a `<!-- doc_id=<parse_job_id> -->` comment; Extract
  reads it automatically and echoes it back as `metadata.doc_id`, linking each
  extraction to its originating parse job.
