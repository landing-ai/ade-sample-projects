Invoice Sample Project Instructions

Use the ade-docs MCP server for details on how to use the v2 APIs for Parse, Parse Jobs, Extract and Extract Jobs with the DPT-3 model family. Use only v2 endpoints for Parse and Extract.

Create a script which does the following:
1. Send all files in the input_folder to Parse Jobs v2 with standard service_tier.
2. Save the full JSON response as .json and the Markdown output as .md in results_folder inside a folder named parse. 
3. Use the schema named invoice_demo_schema.json in the schema folder
4. Send the Markdown for each parsed document and the schmema to the Extract Jobs API with standard service_tier.
5. Save the full Extract JSON response as .json in results_folder inside a folder named extract
6. Produce a summary csv file in results_folder inside csv_summaries containing all the extracted fileds other than the line_items, plus the job_id, document name and processing date.
7. Produce a summary csv file in results_folder inside csv_summaries containing all the line_item details, plus the job_id as the primary key, document name and processing date.
8. Produce a summary csv file in results_folder inside csv_summaries containing all the items in the parse metadata and the extract metadata. One row per document.
