# Prompt — Parse → Build Schema → Extract → combined CSV (Python SDK)

A batch pipeline that parses a folder of documents, builds an extraction schema
automatically, extracts structured fields, and flattens everything into a single
CSV (one row per document, one column per field).

Copy the prompt below into your agent. Drop your files in `input_folder` first.

---

Can you use the ADE document processing skills to build me a script that performs the following steps:

1. Takes all the files in `input_folder` and sends them to the Parse API using multiple parallel threads.
2. Saves all of the JSON and Markdown output from parse in a folder named `parse_output`.
3. Creates an extraction schema by calling the Build Schema API and saves the schema to a folder named `schemas`. Avoid nested levels in the schema to make it easier to convert the output to a CSV later in step 6.
4. Sends all the parsed files to the Extract API with the schema built in step 3.
5. Saves all the JSON output from Extract in a folder named `extract_output`.
6. Prepares a CSV file where each document is a row and each extracted field is a column. Save this as `extraction_results_combined.csv`.

I prefer to use the Python SDK.

---

**Notes**
- Reads the API key from `VISION_AGENT_API_KEY` (keep it in a git-ignored `.env`).
- Asking for a flat (non-nested) schema in step 3 is what makes the step-6 CSV clean.
- Swap "Parse API / Extract API" for "Parse Jobs / Extract Jobs" if you want the
  async APIs for large batches (see [`invoice_with_parseJobs_extractJobs.md`](invoice_with_parseJobs_extractJobs.md)).
