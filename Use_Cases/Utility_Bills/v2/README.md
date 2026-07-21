# Utility Bill Processing — ADE v2 (DPT-3)

Batch pipeline that extracts structured fields from **utility bills** (electric /
gas), built entirely on the LandingAI ADE **v2** async REST endpoints — **Parse
Jobs** and **Extract Jobs** — using the **DPT-3** model family. This is the v2
counterpart to the SDK-based `../v1` notebook.

## What it does

For every file in `../input_folder`, the pipeline:

1. Submits it to **Parse Jobs v2** (`POST /v2/parse/jobs`, `standard` tier, `dpt-3-pro-latest`).
2. Saves the full parse response as `results_folder/parse/<name>_parse.json` and the
   Markdown as `results_folder/parse/<name>_parse.md`.
3. Loads the extraction schema from the **shared `../utility_bill.json`** (the same
   schema the v1 notebook uses).
4. Submits each document's Markdown + schema to **Extract Jobs v2**
   (`POST /v2/extract/jobs`, `standard` tier).
5. Saves the full extract response as `results_folder/extract/<name>_extract.json`.
6. Writes `results_folder/csv_summaries/utility_bill_fields_summary.csv` — all
   extracted fields, one row per document (+ `job_id`, `document_name`, `processing_date`).
7. Writes `results_folder/csv_summaries/processing_metadata.csv` — parse + extract
   metadata, one row per document.

## Extracted fields

The shared schema (`../utility_bill.json`) groups fields into five objects:

- **provider_info** — `provider`, `phone_number`, `website`, `usage_bar_chart`
- **account_info** — `account_holder`, `account_number`, `service_address` (+ parsed parts)
- **billing_summary** — `due_date`, `bill_date`, `service_start_date`, `service_end_date`, `total_amount_due`
- **electric_charges** — `meter_number`, `usage_kwh`, `total_electric_charges`
- **gas_charges** — `meter_number`, `usage_therms`, `total_gas_charges`

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
python process_utility_bills.py               # all documents
python process_utility_bills.py --limit 1     # smoke test on one
python process_utility_bills.py --only electric1 electric_A
```

## Files

- `ade_v2_client.py` — thin REST client for the four v2 job endpoints + polling
  (shared, unchanged from the other v2 samples).
- `process_utility_bills.py` — the end-to-end pipeline (steps 1–7 above).
- `results_folder/` — generated output (`parse/`, `extract/`, `csv_summaries/`).

The extraction schema is **not** duplicated here — it lives at `../utility_bill.json`
and is shared with the v1 sample so both versions extract identical fields.

## Notes

- **Standard service tier** consumes half the credits of `priority`, with slower
  turnaround. The script submits all jobs first, then polls, so documents process
  in parallel server-side.
- Inputs are a mix of PDFs and images (JPG); the v2 Parse API handles both.
