# Prompt — Parse Jobs → Extract Jobs → CSV summaries (v2, async)

An async pipeline on the **v2 Jobs APIs** with the DPT-3 model family: parse a
folder of documents, extract against a fixed schema, and produce three CSV
summaries (top-level fields, line items, and processing metadata).

This is the prompt used to generate the [`Use_Cases/Invoices/v2`](../Use_Cases/Invoices/v2)
sample project. Put your files in `input_folder` and your schema in `schema/`.

---

Use the `ade-docs` MCP server for details on how to use the v2 APIs for Parse, Parse Jobs, Extract and Extract Jobs with the DPT-3 model family. Use only v2 endpoints for Parse and Extract.

Create a script which does the following:

1. Send all files in the `input_folder` to Parse Jobs v2 with `standard` service_tier.
2. Save the full JSON response as `.json` and the Markdown output as `.md` in `results_folder` inside a folder named `parse`.
3. Use the schema named `invoice_demo_schema.json` in the `schema` folder.
4. Send the Markdown for each parsed document and the schema to the Extract Jobs API with `standard` service_tier.
5. Save the full Extract JSON response as `.json` in `results_folder` inside a folder named `extract`.
6. Produce a summary CSV file in `results_folder` inside `csv_summaries` containing all the extracted fields other than the `line_items`, plus the `job_id`, document name and processing date.
7. Produce a summary CSV file in `results_folder` inside `csv_summaries` containing all the `line_item` details, plus the `job_id` as the primary key, document name and processing date.
8. Produce a summary CSV file in `results_folder` inside `csv_summaries` containing all the items in the parse metadata and the extract metadata. One row per document.

---

**Notes**
- Rename `invoice_demo_schema.json` (step 3) to your own schema, or ask the agent
  to build one first via the Build Schema API.
- Splitting fields (step 6) from line items (step 7) keeps each CSV a clean table;
  `job_id` ties the line-item rows back to their parent document.
- The async **Jobs** APIs are the right choice for large or long documents; for
  small batches the synchronous Parse/Extract APIs are simpler
  (see [`batchToCsv_with_parse_buildSchema_extract.md`](batchToCsv_with_parse_buildSchema_extract.md)).
