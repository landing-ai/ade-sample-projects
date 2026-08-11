-- ============================================================================
-- ADE on Snowflake — Native App (DPT-3) procedures: api.parse_v2 / api.extract_v2
-- ============================================================================
--
-- This is an ALTERNATIVE to the Python streaming pipeline in this folder.
--
--   * The Python pipeline (ade_sf_pipeline_main.py) runs ADE from OUTSIDE
--     Snowflake with the `landingai-ade` SDK, then streams rows in via
--     PUT + COPY INTO. Use it when you want full control of orchestration,
--     concurrency, and row shaping, or when you run ADE outside Snowflake.
--
--   * The ADE Snowflake NATIVE APP (this file) runs parsing and extraction
--     as stored procedures INSIDE Snowflake. No Python, no external egress
--     beyond the app's managed connection. Results land straight in tables.
--     This is the simplest path for teams that live in Snowsight, and it
--     works with Zero Data Retention (ZDR) organizations because results are
--     returned inline and stored only in your tables.
--
-- Prerequisites:
--   1. Install "Agentic Document Extraction - App" from the Snowflake
--      Marketplace and enter your API key in the app.
--   2. Connect the app's external access (Catalog > Apps > ADE App >
--      Configurations). If a previous version was installed, DELETE and
--      RE-CREATE the connection so the parse_v2/extract_v2 endpoints are
--      added — Disconnect/Reconnect keeps the old endpoint list. Verify with
--      the "Test connection" button on the app's Settings page.
--
-- Docs:
--   Overview:  https://docs.landing.ai/ade/ade-sf-overview
--   Parse:     https://docs.landing.ai/ade/ade-sf-parse-cloud
--   Extract:   https://docs.landing.ai/ade/ade-sf-extract-cloud
--   Own DB:    https://docs.landing.ai/ade/ade-sf-grant-access-to-output-tables
-- ============================================================================


-- ----------------------------------------------------------------------------
-- 1. PARSE with DPT-3  (api.parse_v2)
-- ----------------------------------------------------------------------------
-- Sends a document (Snowflake stage path or publicly accessible URL) to the
-- Parse v2 API as an async job and writes the result to db.parse_v2_output.

CALL api.parse_v2(
    file_path => 'https://ade.landing.ai/pdfs/invoice_1.pdf'
    -- , model   => 'dpt-3-pro'                 -- optional: pin a model version
    -- , options => '{"pages": [1, 3]}'         -- optional: passthrough options
);

-- Inspect the parse output. Note the v2 schema differs from v1:
--   * STRUCTURE (VARIANT) is a document -> page -> block tree with per-block
--     grounding — it replaces the flat CHUNKS/SPLITS of the v1 api.parse.
--   * MARKDOWN ends with a `<!-- doc_id=... -->` comment used for auto-linking.
--   * STATUS_CODE is 200 for full success, 206 when some pages failed
--     (see METADATA:failed_pages).
SELECT DOC_ID, FILENAME, PAGE_COUNT, MODEL_VERSION, STATUS_CODE
FROM db.parse_v2_output
ORDER BY PARSED_AT DESC;


-- ----------------------------------------------------------------------------
-- 2. EXTRACT with DPT-3  (api.extract_v2)
-- ----------------------------------------------------------------------------
-- Sends Markdown + a JSON schema to the Extract v2 API and writes structured
-- fields to db.extract_v2_output. The schema may be a JSON string, a stage
-- path, or a URL. (The Python pipeline in this folder uses the equivalent
-- InvoiceExtractionSchema — see invoice_schema.py.)
--
-- Automatic linking: because the Markdown from api.parse_v2 carries the
-- `<!-- doc_id=... -->` comment, extract rows join back to parse rows on
-- DOC_ID without you passing doc_id explicitly.

CALL api.extract_v2(
    markdown => (SELECT MARKDOWN FROM db.parse_v2_output WHERE DOC_ID = '<doc_id>'),
    schema   => 'https://ade.landing.ai/pdfs/InvoiceExtractionSchema.json'
    -- , options => '{"strict": true}'   -- fail (don't skip) fields the model can't honor
);

-- Review results. WARNINGS / SCHEMA_VIOLATION_ERROR are populated on partial
-- success; when either is set, STATUS_CODE is 206 (same signal the sync API
-- returns). This mirrors the SCHEMA_VIOLATION_ERROR column the Python pipeline
-- writes to INVOICES_MAIN.
SELECT DOC_ID, STATUS_CODE, SCHEMA_VIOLATION_ERROR, WARNINGS, EXTRACTION
FROM db.extract_v2_output
ORDER BY EXTRACTED_AT DESC;


-- ----------------------------------------------------------------------------
-- 3. CHAIN parse -> extract in one block (no manual doc_id)
-- ----------------------------------------------------------------------------
-- api.parse_v2 returns {message, output_table, doc_id, status_code}; pass that
-- object straight to api.extract_v2 via the parse_result overload.

DECLARE
    parse_result OBJECT;
BEGIN
    parse_result := (CALL api.parse_v2(
        file_path => 'https://ade.landing.ai/pdfs/invoice_1.pdf'
    ));
    RETURN (CALL api.extract_v2(
        parse_result => :parse_result,
        schema       => 'https://ade.landing.ai/pdfs/InvoiceExtractionSchema.json'
    ));
END;


-- ----------------------------------------------------------------------------
-- 4. (Optional) Write results to YOUR OWN database tables
-- ----------------------------------------------------------------------------
-- By default results go to the app's db.parse_v2_output / db.extract_v2_output.
-- To land them in customer-owned tables (recommended — ownership and data
-- survive an app uninstall), grant the app access, then pass output_table.

GRANT USAGE ON DATABASE YOUR_DB TO APPLICATION "APP_NAME";
GRANT USAGE ON SCHEMA YOUR_DB.YOUR_SCHEMA TO APPLICATION "APP_NAME";

-- To use a table you created (recommended): match the column set of the
-- matching default table (e.g. db.parse_v2_output).
GRANT SELECT, INSERT ON TABLE YOUR_DB.YOUR_SCHEMA.YOUR_TABLE TO APPLICATION "APP_NAME";

-- Or, to let the app create the table for you:
-- GRANT CREATE TABLE ON SCHEMA YOUR_DB.YOUR_SCHEMA TO APPLICATION "APP_NAME";

-- Then target it. (SELECT on the parse table is required for extract chaining.)
CALL api.parse_v2(
    file_path    => 'https://ade.landing.ai/pdfs/invoice_1.pdf',
    output_table => 'YOUR_DB.YOUR_SCHEMA.YOUR_TABLE'
);
-- A missing grant makes the procedure write nothing and return status_code 403
-- with a message naming the missing grant.
