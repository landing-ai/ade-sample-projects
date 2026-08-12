-- ============================================================================
-- Snowflake setup for the High-Volume ADE (DPT-3) -> Snowflake demo
-- ----------------------------------------------------------------------------
-- Adjust the DATABASE / SCHEMA / WAREHOUSE / ROLE / USER names to match your
-- account and your .env. Run as a role that can create these objects.
-- ============================================================================

USE ROLE ACCOUNTADMIN;

CREATE DATABASE IF NOT EXISTS ADE_DEMO;
CREATE SCHEMA   IF NOT EXISTS ADE_DEMO.INVOICES;
USE SCHEMA ADE_DEMO.INVOICES;

-- ---------------------------------------------------------------- stages -----
-- Long-term archive of the original documents (never purged).
CREATE STAGE IF NOT EXISTS ADE_DEMO.INVOICES.RAW_DOCS
  DIRECTORY = (ENABLE = TRUE);

-- Short-lived ingest buffer; shards are PURGEd after each COPY.
CREATE STAGE IF NOT EXISTS ADE_DEMO.INVOICES.INGEST_TMP;

-- ------------------------------------------------------------ file formats ---
CREATE FILE FORMAT IF NOT EXISTS ADE_DEMO.INVOICES.CSV_STD
  TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1
  NULL_IF = ('', 'NULL') EMPTY_FIELD_AS_NULL = TRUE;

CREATE FILE FORMAT IF NOT EXISTS ADE_DEMO.INVOICES.JSON_STD
  TYPE = JSON STRIP_OUTER_ARRAY = FALSE;

-- ---------------------------------------------------------------- tables -----

-- Header fields, one row per invoice.
CREATE OR REPLACE TABLE ADE_DEMO.INVOICES.INVOICES_MAIN (
  RUN_ID                  STRING,
  INVOICE_UUID            VARCHAR NOT NULL,
  DOCUMENT_NAME           VARCHAR,
  SENT_AT                 TIMESTAMP_TZ,
  ADE_SDK_VERSION         VARCHAR,
  SCHEMA_VIOLATION_ERROR  VARCHAR,     -- non-null when DPT-3 extract returns HTTP 206
  INVOICE_DATE_RAW        VARCHAR,
  INVOICE_DATE            DATE,
  INVOICE_NUMBER          VARCHAR,
  ORDER_DATE              VARCHAR,
  PO_NUMBER               VARCHAR,
  STATUS                  VARCHAR,
  SOLD_TO_NAME            VARCHAR,
  SOLD_TO_ADDRESS         VARCHAR,
  CUSTOMER_EMAIL          VARCHAR,
  SUPPLIER_NAME           VARCHAR,
  SUPPLIER_ADDRESS        VARCHAR,
  SUPPLIER_EMAIL          VARCHAR,
  SUPPLIER_PHONE          VARCHAR,
  PAYMENT_TERMS           VARCHAR,
  SHIP_VIA                VARCHAR,
  SHIP_DATE               VARCHAR,
  TRACKING_NUMBER         VARCHAR,
  CURRENCY                VARCHAR,
  TOTAL_DUE_RAW           VARCHAR,
  TOTAL_DUE               NUMBER(18,4),
  SUBTOTAL                NUMBER(18,4),
  TAX                     NUMBER(18,4),
  SHIPPING                NUMBER(18,4),
  SUPPLIER_NAME_REF       STRING,      -- DPT-3 evidence: markdown ranges (JSON)
  TOTAL_DUE_REF           STRING,
  CONSTRAINT PK_INVOICES_MAIN PRIMARY KEY (INVOICE_UUID)
);

-- Line items, one+ rows per invoice.
CREATE OR REPLACE TABLE ADE_DEMO.INVOICES.INVOICE_LINE_ITEMS (
  RUN_ID                  STRING,
  INVOICE_UUID            VARCHAR NOT NULL,
  DOCUMENT_NAME           VARCHAR,
  SENT_AT                 TIMESTAMP_TZ,
  ADE_SDK_VERSION         VARCHAR,
  LINE_INDEX              NUMBER(9,0),
  LINE_NUMBER             VARCHAR,
  SKU                     VARCHAR,
  DESCRIPTION             VARCHAR,
  QUANTITY                FLOAT,
  UNIT_PRICE              NUMBER(18,4),
  AMOUNT                  NUMBER(18,4)
);

-- Parsed blocks (DPT-3 structure-tree elements) with grounding.
CREATE OR REPLACE TABLE ADE_DEMO.INVOICES.PARSED_BLOCKS (
  RUN_ID          STRING,
  INVOICE_UUID    VARCHAR NOT NULL,
  DOCUMENT_NAME   STRING,
  BLOCK_ID        STRING,
  BLOCK_TYPE      STRING,       -- text, table, figure, logo, marginalia, ...
  TEXT            STRING,
  PAGE            NUMBER,       -- 1-indexed (DPT-3)
  -- Normalized 0-1 box; DPT-3 xmin/ymin/xmax/ymax -> box_l/box_t/box_r/box_b.
  BOX_L           FLOAT,
  BOX_T           FLOAT,
  BOX_R           FLOAT,
  BOX_B           FLOAT,
  CONSTRAINT PK_PARSED_BLOCKS PRIMARY KEY (BLOCK_ID)
);

-- Full parsed markdown per document (VARIANT), for QA / RAG / re-processing.
CREATE OR REPLACE TABLE ADE_DEMO.INVOICES.MARKDOWN (
  RUN_ID                  STRING,
  INVOICE_UUID            VARCHAR NOT NULL,
  DOCUMENT_NAME           VARCHAR,
  SENT_AT                 TIMESTAMP_TZ,
  ADE_SDK_VERSION         VARCHAR,
  MARKDOWN                VARIANT,
  CONSTRAINT PK_MARKDOWN PRIMARY KEY (INVOICE_UUID)
);

-- --------------------------------------------------------- role + grants -----
CREATE ROLE IF NOT EXISTS ADE_DEMOS;
GRANT ROLE ADE_DEMOS TO USER MACHINE_USER;   -- change to your pipeline user

GRANT USAGE ON WAREHOUSE ADE_WH TO ROLE ADE_DEMOS;
GRANT USAGE ON DATABASE ADE_DEMO TO ROLE ADE_DEMOS;
GRANT USAGE ON SCHEMA ADE_DEMO.INVOICES TO ROLE ADE_DEMOS;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA ADE_DEMO.INVOICES TO ROLE ADE_DEMOS;
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA ADE_DEMO.INVOICES TO ROLE ADE_DEMOS;

GRANT READ, WRITE ON STAGE ADE_DEMO.INVOICES.RAW_DOCS   TO ROLE ADE_DEMOS;
GRANT READ, WRITE ON STAGE ADE_DEMO.INVOICES.INGEST_TMP TO ROLE ADE_DEMOS;

GRANT CREATE STAGE, CREATE FILE FORMAT ON SCHEMA ADE_DEMO.INVOICES TO ROLE ADE_DEMOS;
GRANT USAGE ON FILE FORMAT ADE_DEMO.INVOICES.CSV_STD  TO ROLE ADE_DEMOS;
GRANT USAGE ON FILE FORMAT ADE_DEMO.INVOICES.JSON_STD TO ROLE ADE_DEMOS;
