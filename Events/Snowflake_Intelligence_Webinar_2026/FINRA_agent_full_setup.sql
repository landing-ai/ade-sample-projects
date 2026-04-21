
--------------------------------------------------------------------------------
-- FDA MEDICAL DEVICE DOCUMENT INTELLIGENCE AGENT
--
-- This script builds a complete Cortex Agent that answers questions about FINRA 
-- Arbitration Awards documents using LandingAI's Agentic Document
-- Extraction (ADE), Cortex Search, and Cortex Analyst. Documents sourced from 
-- https://www.finra.org/arbitraAtion-mediation/arbitration-awards-online
--
-- WHAT GETS CREATED:
--   • Database, schema, stages (with server-side encryption for presigned URLs)
--   • Warehouse for ADE processing
--   • Document parsing and extraction pipeline (via ADE API)
--   • Structured tables for extracted device metadata
--   • Cortex Search service over parsed document chunks
--   • Semantic view for natural language queries (Cortex Analyst)
--   • Stored procedure for generating presigned URLs
--   • Cortex Agent with multi-tool orchestration
--
-- PREREQUISITES:
--   • LandingAI Agentic Document Extraction app installed in your account
--   • ACCOUNTADMIN role (or equivalent CREATE/GRANT privileges)
--   • FDA medical device PDFs uploaded to stage after creation
--
-- IMPORTANT NOTES:
--   • Stage uses SNOWFLAKE_SSE encryption (required for presigned URLs)
--   • Script is idempotent - safe to re-run
--   • Sanity checks throughout help verify each step
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
-- SECTION 1: INITIAL SETUP - CORE INFRASTRUCTURE
-- This section creates the foundational Snowflake objects required for the
-- document intelligence pipeline (database, schema, stages, warehouse).
-- REQUIRED FOR SETUP
--------------------------------------------------------------------------------

-- Use a role with sufficient privileges to create and grant objects.
-- ACCOUNTADMIN is recommended for initial bootstrap.
USE ROLE ACCOUNTADMIN;

-- Create the main database and schema for the FDA medical device application
CREATE DATABASE IF NOT EXISTS ADE_APPS_DB;
CREATE SCHEMA IF NOT EXISTS ADE_APPS_DB.FINRA;

-- Create a stage to store PDF documents with directory listing enabled
-- This is where you'll upload your FDA medical device documents
-- IMPORTANT: Use SNOWFLAKE_SSE encryption for presigned URLs to work correctly
-- (files will be corrupted if client-side encryption is used)
CREATE STAGE IF NOT EXISTS ADE_APPS_DB.FINRA.DOCS
    DIRECTORY = (ENABLE = TRUE)
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- NOTE: If you have an existing stage without server-side encryption, you must:
-- 1. CREATE STAGE ADE_APPS_DB.FINRA.DOCS_NEW DIRECTORY = (ENABLE = TRUE) ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
-- 2. COPY FILES INTO @ADE_APPS_DB.FINRA.DOCS_NEW FROM @ADE_APPS_DB.FINRA.DOCS PATTERN = '.*';
-- 3. DROP STAGE ADE_APPS_DB.FINRA.DOCS;
-- 4. ALTER STAGE ADE_APPS_DB.FINRA.DOCS_NEW RENAME TO ADE_APPS_DB.FINRA.DOCS;
-- 5. Re-grant permissions: GRANT READ, WRITE ON STAGE ADE_APPS_DB.FINRA.DOCS TO APPLICATION "ADE";

-- Create a dedicated warehouse for ADE processing workloads
CREATE WAREHOUSE IF NOT EXISTS WH_LANDINGAI_ADE
    WITH WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE;

-- Set working context to the newly created database and schema
USE DATABASE ADE_APPS_DB;
USE SCHEMA ADE_APPS_DB.FINRA;

-- Create a stage for storing semantic models (used by Cortex Analyst)
CREATE STAGE IF NOT EXISTS ADE_APPS_DB.FINRA.SEMANTIC_MODELS;

-- Enable Cortex features across all regions to allow cross-region AI functionality
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';

-- Switch context to the ADE application to grant it necessary permissions
USE "ADE";

-- Grant the LandingAI ADE application access to the database, schema, and stage
-- This allows the app to read documents and write parse/extract results
GRANT USAGE ON DATABASE ADE_APPS_DB TO APPLICATION "ADE";
GRANT USAGE ON SCHEMA ADE_APPS_DB.FINRA TO APPLICATION "ADE";
GRANT READ, WRITE ON STAGE ADE_APPS_DB.FINRA.DOCS TO APPLICATION "ADE";

--------------------------------------------------------------------------------
-- SANITY CHECK: Verify files are staged correctly
-- IMPORTANT: Before proceeding, upload your PDF files to the /award subfolder
-- in the ADE_APPS_DB.FINRA.DOCS stage (best done via Snowflake UI)
--------------------------------------------------------------------------------

-- List all files in the stage to confirm they're uploaded correctly
LS @ADE_APPS_DB.FINRA.DOCS;


--------------------------------------------------------------------------------
-- SECTION 2: DOCUMENT PARSING AND EXTRACTION
-- This section processes PDF documents using the ADE API to:
-- 1. Parse documents into structured chunks (text, tables, figures)
-- 2. Extract specific fields based on a JSON schema
--
-- ALTERNATIVE APPROACH: You can also use the ADE UI or follow the docs at:
-- https://docs.landing.ai/ade/ade-sf-parse-cloud
-- https://docs.landing.ai/ade/ade-sf-extract-cloud
--
-- REQUIRED FOR SETUP (This is the automated batch processing approach)
--------------------------------------------------------------------------------

-- Parse and extract all PDFs on the stage that match the filter criteria
-- This loop processes multiple documents automatically
DECLARE
    -- Cursor to select files from the stage based on size and naming pattern
    file_cursor CURSOR FOR
        SELECT RELATIVE_PATH
        FROM DIRECTORY(@ADE_APPS_DB.FINRA.DOCS)
        LIMIT 200;  -- Adjust this limit based on how many files you want to process
    current_file_path STRING;
    full_stage_path STRING;

    parse_ret OBJECT;      -- Holds the parse API response
    extract_ret OBJECT;    -- Holds the extract API response

BEGIN
    -- Loop through each file matching the cursor criteria
    FOR file_record IN file_cursor DO
        current_file_path := file_record.RELATIVE_PATH;

        full_stage_path := '@"ADE_APPS_DB"."FINRA"."DOCS"/' || :current_file_path;

        -- STEP 1: Parse the document into structured chunks (text, tables, figures)
        -- The parse API breaks down the PDF into semantic chunks with grounding info
        CALL api.parse(
            file_path => :full_stage_path,
            model => 'dpt-2-latest',  -- Latest document parsing transformer model
            output_table => 'finra_awards_parse'  -- Output table (auto-created in ADE.DB schema)
        ) INTO :parse_ret;

        -- STEP 2: Extract specific fields using the parse result and a JSON schema
        -- This extracts structured data (case number, dates, financial awards) from the chunks

        CALL api.extract(
            parse_result => :parse_ret,
            output_table => 'finra_awards_extract',  -- Output table (auto-created in ADE.DB schema)
            model => 'extract-latest',
            schema => '{
              "title": "FINRA Award / Expungement Award - Consolidated Extraction Schema",
  "description": "Unified schema for FINRA arbitration award documents, including expungement awards. Supports both single-arbitrator and panel formats, variable fee breakdowns, and expungement-specific findings.",
  "type": "object",
  "required": [
    "case"
  ],
  "properties": {
    "document": {
      "type": "object",
      "description": "Document metadata.",
      "additionalProperties": false,
      "properties": {
        "document_type": {
          "type": "string",
          "description": "High-level document label (e.g., Arbitration Award, Expungement Award).",
          "nullable": true
        },
        "awarding_body": {
          "type": "string",
          "description": "Issuing organization (often FINRA Dispute Resolution Services).",
          "nullable": true
        }
      }
    },
    "case": {
      "type": "object",
      "description": "Case identifiers and dispute context.",
      "additionalProperties": false,
      "required": [
        "case_number"
      ],
      "properties": {
        "case_number": {
          "type": "string",
          "description": "FINRA case or arbitration number.",
          "nullable": true
        },
        "hearing_site_state": {
          "type": "string",
          "description": "State of the hearing location/site.",
          "nullable": true
        },
        "hearing_site_city": {
          "type": "string",
          "description": "City of the hearing location/site.",
          "nullable": true
        },
       "nature_of_dispute": {
          "type": "string",
          "description": "Nature of dispute / dispute type.",
          "nullable": true
        }
      }
    },
    "parties": {
      "type": "object",
      "description": "Parties and representation.",
      "additionalProperties": false,
      "properties": {
        "claimants": {
          "type": "array",
          "description": "List of claimants.",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
              "name": {
                "type": "string",
                "description": "Claimant name.",
                "nullable": true
              }
            }
          }
        },
        "respondents": {
          "type": "array",
          "description": "List of respondents.",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
              "name": {
                "type": "string",
                "description": "Respondent name.",
                "nullable": true
              }
            }
          }
        },
        "representation": {
          "type": "object",
          "description": "Counsel / representation by side.",
          "additionalProperties": false,
          "properties": {
            "claimant_representation": {
              "type": "string",
              "description": "Claimant counsel or pro se details.",
              "nullable": true
            },
            "respondent_representation": {
              "type": "string",
              "description": "Respondent counsel or pro se details.",
              "nullable": true
            }
          }
        }
      }
    },
    "timeline": {
      "type": "object",
      "description": "Key filing and hearing dates.",
      "additionalProperties": false,
      "properties": {
        "statement_of_claim_filed_date": {
          "type": "string",
          "format": "date",
          "description": "Statement of Claim filed date.",
          "nullable": true
        },
        "claimant_submission_agreement_signed_date": {
          "type": "string",
          "format": "date",
          "description": "Claimant submission agreement signed date.",
          "nullable": true
        },
        "statement_of_answer_filed_date": {
          "type": "string",
          "format": "date",
          "description": "Statement of Answer filed date.",
          "nullable": true
        },
        "respondent_submission_agreement_signed_date": {
          "type": "string",
          "format": "date",
          "description": "Respondent submission agreement signed date.",
          "nullable": true
        },
        "hearing_date": {
          "type": "string",
          "format": "date",
          "description": "Hearing date (often present in expungement awards).",
          "nullable": true
        }
      }
    },
    "case_summary": {
      "type": "object",
      "description": "Narrative case summary.",
      "additionalProperties": false,
      "properties": {
        "claimant_assertions": {
          "type": "string",
          "description": "Claims/allegations/causes of action asserted by claimant.",
          "nullable": true
        },
        "respondent_response": {
          "type": "string",
          "description": "Denials/defenses/response by respondent.",
          "nullable": true
        }
      }
    },
    "relief_requested": {
      "type": "object",
      "description": "Relief requested by parties.",
      "additionalProperties": false,
      "properties": {
        "claimant_requested_relief": {
          "type": "string",
          "description": "Relief sought by claimants.",
          "nullable": true
        },
        "respondent_requested_relief": {
          "type": "string",
          "description": "Relief sought by respondents.",
          "nullable": true
        },
        "claimant_damages_dismissed": {
          "type": "boolean",
          "description": "Whether claimant damages were dismissed (if explicitly stated).",
          "nullable": true
        },
        "respondent_cost_assessment_request": {
          "type": "boolean",
          "description": "Whether respondent requested costs/fees be assessed to claimant.",
          "nullable": true
        }
      }
    },
    "decision": {
      "type": "object",
      "description": "Award decision details.",
      "additionalProperties": false,
      "properties": {
        "disposition": {
          "type": "object",
          "description": "Outcome/disposition signals.",
          "additionalProperties": false,
          "properties": {
            "claimant_claims_denied_in_entirety": {
              "type": "boolean",
              "description": "True if all claimant claims were denied in entirety.",
              "nullable": true
            },
            "claimant_injunction_denied": {
              "type": "boolean",
              "description": "True if injunction request was denied.",
              "nullable": true
            },
            "other_relief_denied": {
              "type": "boolean",
              "description": "True if other relief was denied.",
              "nullable": true
            },
            "other_claims_denied_text": {
              "type": "string",
              "description": "Narrative denial language when provided instead of checkboxes/booleans.",
              "nullable": true
            }
          }
        },
        "monetary_awards": {
          "type": "object",
          "description": "Monetary awards (damages/fees/costs/reimbursements).",
          "additionalProperties": false,
          "properties": {
            "compensatory_damages": {
              "type": "number",
              "description": "Damages awarded to compensate claimant for losses caused by respondent misconduct.",
              "nullable": true
            },
            "punitive_damages": {
              "type": "number",
              "description": "Punitive or exemplary damages awarded, if any.",
              "nullable": true
            },
            "attorneys_fees_to_respondents": {
              "type": "number",
              "description": "Attorneys fees awarded to respondents.",
              "nullable": true
            },
            "costs_to_respondents": {
              "type": "number",
              "description": "Costs awarded to respondents.",
              "nullable": true
            },
            "reimbursement_to_claimant": {
              "type": "number",
              "description": "Procedural or administrative costs reimbursed to claimant (not compensatory damages).",
              "nullable": true
            },
            "filing_fee_retained_by_finra": {
              "type": "number",
              "description": "Filing fee retained by FINRA (if stated).",
              "nullable": true
            }
          }
        },
        "expungement": {
          "type": "object",
          "description": "Expungement-specific findings and conditions.",
          "additionalProperties": false,
          "properties": {
            "expungement_recommendation": {
              "type": "string",
              "description": "Expungement recommendation text.",
              "nullable": true
            },
            "occurrence_number": {
              "type": "string",
              "description": "Occurrence/disclosure number referenced for expungement.",
              "nullable": true
            },
            "affirmative_finding_of_fact": {
              "type": "string",
              "description": "Affirmative finding of fact supporting expungement.",
              "nullable": true
            },
            "reasons_for_finding": {
              "type": "string",
              "description": "Reasons supporting the affirmative finding.",
              "nullable": true
            },
            "expungement_condition": {
              "type": "string",
              "description": "Any expungement conditions (e.g., court confirmation language).",
              "nullable": true
            }
          }
        }
      }
    },
    "fees": {
      "type": "object",
      "description": "Fees and assessments, including hearing session fee split.",
      "additionalProperties": false,
      "properties": {
        "filing_fee": {
          "type": "number",
          "description": "Filing fee assessed (if stated).",
          "nullable": true
        },
        "initial_claim_filing_fee": {
          "type": "number",
          "description": "Initial claim filing fee (if stated).",
          "nullable": true
        },
        "member_surcharge": {
          "type": "number",
          "description": "FINRA member surcharge (if stated).",
          "nullable": true
        },
        "member_process_fee": {
          "type": "number",
          "description": "FINRA member process fee (if stated).",
          "nullable": true
        },
        "member_surcharge_fee_paid_by_respondent": {
          "type": "number",
          "description": "Member surcharge fee paid by respondent (if stated).",
          "nullable": true
        },
        "total_hearing_session_fees": {
          "type": "number",
          "description": "Total hearing session fees assessed (if stated).",
          "nullable": true
        },
        "hearing_session_fees": {
          "type": "object",
          "description": "Breakdown of hearing session fees paid by each side (when stated).",
          "additionalProperties": false,
          "properties": {
            "paid_by_claimants": {
              "type": "number",
              "description": "Hearing session fees paid by claimants.",
              "nullable": true
            },
            "paid_by_respondents": {
              "type": "number",
              "description": "Hearing session fees paid by respondents.",
              "nullable": true
            },
            "paid_by_finra_or_other": {
              "type": "number",
              "description": "Hearing session fees paid/waived by FINRA or another party (if stated).",
              "nullable": true
            },
            "allocation_basis": {
              "type": "string",
              "description": "Narrative basis for allocation (e.g., split equally, joint and several).",
              "nullable": true
            }
          }
        }
      }
    },
    "arbitrators": {
      "type": "array",
      "description": "Arbitrator(s) or panel members.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "name": {
            "type": "string",
            "description": "Arbitrator name.",
            "nullable": true
          },
          "role": {
            "type": "string",
            "description": "Arbitrator role (e.g., Sole Public Arbitrator, Chairperson, Panelist).",
            "nullable": true
          },
          "signature_date": {
            "type": "string",
            "format": "date",
            "description": "Date the arbitrator signed the award (if present).",
            "nullable": true
          }
        }
      }
    },
    "service": {
      "type": "object",
      "description": "Service details.",
      "additionalProperties": false,
      "properties": {
        "date_of_service": {
          "type": "string",
          "format": "date",
          "description": "Date of service of the award.",
          "nullable": true
        }
      }
    }
  }
            }'
            
        ) INTO :extract_ret;
        
    END FOR;

END;

--------------------------------------------------------------------------------
-- SANITY CHECK: Inspect raw parse and extract results
-- These tables are created by the ADE API in the ADE.DB schema
--------------------------------------------------------------------------------


-- View all parsed chunks (text, tables, figures with grounding information)
SELECT * FROM ADE.DB.FINRA_AWARDS_PARSE
    LIMIT 10;

-- View all extracted fields (structured data based on the JSON schema)
SELECT * FROM ADE.DB.FINRA_AWARDS_EXTRACT
    LIMIT 10;
    
--------------------------------------------------------------------------------
-- SECTION 3: COPY RESULTS TO APPLICATION SCHEMA
-- Move the parse and extract results from the ADE.DB schema to your
-- application schema (ADE_APPS_DB.FINRA) for downstream processing
-- REQUIRED FOR SETUP
--------------------------------------------------------------------------------

-- Copy parsed chunks to the application schema with deduplication
CREATE OR REPLACE TABLE ADE_APPS_DB.FINRA.FINRA_AWARDS_PARSE AS
SELECT DISTINCT *
FROM ADE.DB.FINRA_AWARDS_PARSE;

-- Copy extracted fields to the application schema with deduplication
CREATE OR REPLACE TABLE ADE_APPS_DB.FINRA.FINRA_AWARDS_EXTRACT AS
SELECT DISTINCT *
FROM ADE.DB.FINRA_AWARDS_EXTRACT;

--------------------------------------------------------------------------------
-- SANITY CHECK: Verify tables were copied correctly
--------------------------------------------------------------------------------

-- Inspect the copied parse table
SELECT * FROM ADE_APPS_DB.FINRA.FINRA_AWARDS_PARSE
    LIMIT 10;

-- Inspect the copied extract table
SELECT * FROM ADE_APPS_DB.FINRA.FINRA_AWARDS_EXTRACT
    LIMIT 10;

--------------------------------------------------------------------------------
-- SECTION 4: CREATE STRUCTURED TABLES FOR ANALYSIS
-- Transform the extracted JSON data into a clean, typed table structure
-- REQUIRED FOR SETUP
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE ADE_APPS_DB.FINRA.FINRA_AWARD_EXTRACTED AS
SELECT

  /* Primary key */
  DOC_ID,

  /* Service Date */
  TRY_TO_DATE(EXTRACTION:service:date_of_service::STRING)                     AS DATE_OF_SERVICE,
  
  /* Document */
  EXTRACTION:document:document_type::STRING                                   AS DOCUMENT_TYPE,
  EXTRACTION:document:awarding_body::STRING                                   AS AWARDING_BODY,

  /* Case */
  EXTRACTION:case:case_number::STRING                                         AS CASE_NUMBER,
  EXTRACTION:case:hearing_site_city::STRING                                   AS HEARING_SITE_CITY,
  EXTRACTION:case:hearing_site_state::STRING                                  AS HEARING_SITE_STATE,
  EXTRACTION:case:nature_of_dispute::STRING                                   AS NATURE_OF_DISPUTE,

  /* Case summary */
  EXTRACTION:case_summary:claimant_assertions::STRING                         AS CLAIMANT_ASSERTIONS,
  EXTRACTION:case_summary:respondent_response::STRING                         AS RESPONDENT_RESPONSE,

  /* Relief requested */
  EXTRACTION:relief_requested:claimant_requested_relief::STRING               AS CLAIMANT_REQUESTED_RELIEF,
  EXTRACTION:relief_requested:respondent_requested_relief::STRING             AS RESPONDENT_REQUESTED_RELIEF,
  EXTRACTION:relief_requested:claimant_damages_dismissed::BOOLEAN             AS CLAIMANT_DAMAGES_DISMISSED,
  EXTRACTION:relief_requested:respondent_cost_assessment_request::BOOLEAN     AS RESPONDENT_COST_ASSESSMENT_REQUEST,

  /* Timeline */
  TRY_TO_DATE(EXTRACTION:timeline:statement_of_claim_filed_date::STRING)      AS STATEMENT_OF_CLAIM_FILED_DATE,
  TRY_TO_DATE(EXTRACTION:timeline:claimant_submission_agreement_signed_date::STRING) AS CLAIMANT_SUBMISSION_AGREEMENT_SIGNED_DATE,
  TRY_TO_DATE(EXTRACTION:timeline:statement_of_answer_filed_date::STRING)     AS STATEMENT_OF_ANSWER_FILED_DATE,
  TRY_TO_DATE(EXTRACTION:timeline:respondent_submission_agreement_signed_date::STRING) AS RESPONDENT_SUBMISSION_AGREEMENT_SIGNED_DATE,
  TRY_TO_DATE(EXTRACTION:timeline:hearing_date::STRING)                       AS HEARING_DATE,

  /* Decision -> Disposition */
  EXTRACTION:decision:disposition:claimant_claims_denied_in_entirety::BOOLEAN AS CLAIMANT_CLAIMS_DENIED_IN_ENTIRETY,
  EXTRACTION:decision:disposition:claimant_injunction_denied::BOOLEAN         AS CLAIMANT_INJUNCTION_DENIED,
  EXTRACTION:decision:disposition:other_relief_denied::BOOLEAN                AS OTHER_RELIEF_DENIED,
  EXTRACTION:decision:disposition:other_claims_denied_text::STRING            AS OTHER_CLAIMS_DENIED_TEXT,

  /* Decision -> Monetary awards */
  EXTRACTION:decision:monetary_awards:compensatory_damages::FLOAT             AS COMPENSATORY_DAMAGES,
  EXTRACTION:decision:monetary_awards:punitive_damages::FLOAT                 AS PUNITIVE_DAMAGES,
  EXTRACTION:decision:monetary_awards:attorneys_fees_to_respondents::FLOAT    AS ATTORNEYS_FEES_TO_RESPONDENTS,
  EXTRACTION:decision:monetary_awards:costs_to_respondents::FLOAT             AS COSTS_TO_RESPONDENTS,
  EXTRACTION:decision:monetary_awards:reimbursement_to_claimant::FLOAT        AS REIMBURSEMENT_TO_CLAIMANT,
  EXTRACTION:decision:monetary_awards:filing_fee_retained_by_finra::FLOAT     AS FILING_FEE_RETAINED_BY_FINRA,

  /* Decision -> Expungement */
  EXTRACTION:decision:expungement:occurrence_number::STRING                   AS EXPUNGEMENT_OCCURRENCE_NUMBER,
  EXTRACTION:decision:expungement:expungement_recommendation::STRING          AS EXPUNGEMENT_RECOMMENDATION,
  EXTRACTION:decision:expungement:affirmative_finding_of_fact::STRING         AS AFFIRMATIVE_FINDING_OF_FACT,
  EXTRACTION:decision:expungement:reasons_for_finding::STRING                 AS REASONS_FOR_FINDING,
  EXTRACTION:decision:expungement:expungement_condition::STRING               AS EXPUNGEMENT_CONDITION,

  /* Fees */
  EXTRACTION:fees:filing_fee::FLOAT                                           AS FILING_FEE,
  EXTRACTION:fees:initial_claim_filing_fee::FLOAT                             AS INITIAL_CLAIM_FILING_FEE,
  EXTRACTION:fees:member_surcharge::FLOAT                                     AS MEMBER_SURCHARGE,
  EXTRACTION:fees:member_process_fee::FLOAT                                   AS MEMBER_PROCESS_FEE,
  EXTRACTION:fees:member_surcharge_fee_paid_by_respondent::FLOAT              AS MEMBER_SURCHARGE_FEE_PAID_BY_RESPONDENT,
  EXTRACTION:fees:total_hearing_session_fees::FLOAT                           AS TOTAL_HEARING_SESSION_FEES,
  EXTRACTION:fees:hearing_session_fees:paid_by_claimants::FLOAT               AS HEARING_SESSION_FEES_PAID_BY_CLAIMANTS,
  EXTRACTION:fees:hearing_session_fees:paid_by_respondents::FLOAT             AS HEARING_SESSION_FEES_PAID_BY_RESPONDENTS,
  EXTRACTION:fees:hearing_session_fees:paid_by_finra_or_other::FLOAT          AS HEARING_SESSION_FEES_PAID_BY_FINRA_OR_OTHER,
  EXTRACTION:fees:hearing_session_fees:allocation_basis::STRING               AS HEARING_SESSION_FEES_ALLOCATION_BASIS,

FROM ADE_APPS_DB.FINRA.FINRA_AWARDS_EXTRACT;

ALTER TABLE ADE_APPS_DB.FINRA.FINRA_AWARD_EXTRACTED
  ADD
    SERVICE_YEAR INTEGER,
    SERVICE_QUARTER INTEGER,
    SERVICE_YEAR_QUARTER STRING;


UPDATE ADE_APPS_DB.FINRA.FINRA_AWARD_EXTRACTED
SET
  SERVICE_YEAR = YEAR(DATE_OF_SERVICE),
  SERVICE_QUARTER = QUARTER(DATE_OF_SERVICE),
  SERVICE_YEAR_QUARTER =
    TO_VARCHAR(YEAR(DATE_OF_SERVICE)) || '-Q' || TO_VARCHAR(QUARTER(DATE_OF_SERVICE));


CREATE OR REPLACE TABLE ADE_APPS_DB.FINRA.FINRA_AWARD_ARBITRATORS AS
SELECT
  t.DOC_ID                                                     AS DOC_ID,
  f.index::INT                                                 AS ARBITRATOR_INDEX,
  f.value:name::STRING                                         AS ARBITRATOR_NAME,
  f.value:role::STRING                                         AS ARBITRATOR_ROLE,
  TRY_TO_DATE(f.value:signature_date::STRING)                  AS ARBITRATOR_SIGNATURE_DATE
FROM ADE_APPS_DB.FINRA.FINRA_AWARDS_EXTRACT t,
LATERAL FLATTEN(input => t.EXTRACTION:arbitrators) f;


CREATE OR REPLACE TABLE ADE_APPS_DB.FINRA.FINRA_AWARD_CLAIMANTS AS
SELECT
  t.DOC_ID                                                    AS DOC_ID,
  f.index::INT                                                AS CLAIMANT_INDEX,
  f.value:name::STRING                                        AS CLAIMANT_NAME
FROM ADE_APPS_DB.FINRA.FINRA_AWARDS_EXTRACT t,
LATERAL FLATTEN(input => t.EXTRACTION:parties:claimants) f;


CREATE OR REPLACE TABLE ADE_APPS_DB.FINRA.FINRA_AWARD_RESPONDENTS AS
SELECT
  t.DOC_ID                                                    AS DOC_ID,
  f.index::INT                                                AS RESPONDENT_INDEX,
  f.value:name::STRING                                        AS RESPONDENT_NAME
FROM ADE_APPS_DB.FINRA.FINRA_AWARDS_EXTRACT t,
LATERAL FLATTEN(input => t.EXTRACTION:parties:respondents) f;


--------------------------------------------------------------------------------
-- SANITY CHECK: Verify structured data looks correct
--------------------------------------------------------------------------------

-- Inspect the flattened, typed table
SELECT * FROM ADE_APPS_DB.FINRA.FINRA_AWARD_EXTRACTED
 LIMIT 20;

SELECT * FROM ADE_APPS_DB.FINRA.FINRA_AWARD_ARBITRATORS
 LIMIT 10; 

 SELECT * FROM ADE_APPS_DB.FINRA.FINRA_AWARD_CLAIMANTS
 LIMIT 10; 
 
 SELECT * FROM ADE_APPS_DB.FINRA.FINRA_AWARD_RESPONDENTS 
 LIMIT 10;
 

--------------------------------------------------------------------------------
-- SECTION 5: PREPARE CHUNKS TABLE FOR CORTEX SEARCH
-- Flatten the parsed chunks and enrich with file metadata and stage URLs
-- This table will be used as the source for the Cortex Search service
-- REQUIRED FOR SETUP
--------------------------------------------------------------------------------

-- Create a denormalized chunks table with one row per chunk
-- Includes grounding info (page, bounding box) and presigned URL helpers
CREATE OR REPLACE TABLE ADE_APPS_DB.FINRA.FINRA_AWARDS_CHUNKS AS
WITH FILE_MAP AS (
    SELECT
        RELATIVE_PATH,
        REGEXP_SUBSTR(RELATIVE_PATH, '[^/]+$') AS BASENAME
    FROM DIRECTORY(@ADE_APPS_DB.FINRA.DOCS)
),
PARSE_WITH_PATH AS (
    SELECT
        p.DOC_ID,
        p.SOURCE_URL,
        p.FILENAME,
        p.PAGE_COUNT,
        p.PARSED_AT,
        p.CHUNKS,
        m.RELATIVE_PATH
    FROM ADE_APPS_DB.FINRA.FINRA_AWARDS_PARSE p
    JOIN FILE_MAP m
      ON m.BASENAME = p.FILENAME
)
SELECT
    p.DOC_ID,
    p.FILENAME,
    p.SOURCE_URL,
    p.PAGE_COUNT,
    p.PARSED_AT,
    p.RELATIVE_PATH,

    c.INDEX::INTEGER AS CHUNK_INDEX,
    c.VALUE          AS CHUNK_INFO,

    -- chunk fields (per ade json response)
    c.VALUE:id::STRING       AS CHUNK_ID,
    c.VALUE:type::STRING     AS CHUNK_TYPE,
    c.VALUE:markdown::STRING AS CHUNK_MARKDOWN,

    -- grounding fields (grounding is an object with page + box)
    c.VALUE:grounding:page::INTEGER AS PAGE_NUMBER,
    c.VALUE:grounding:box::VARIANT  AS CHUNK_BOX,

    -- stage helpers
    '@ADE_APPS_DB.FINRA.DOCS' AS STAGE_NAME,
    '@ADE_APPS_DB.FINRA.DOCS/' || p.RELATIVE_PATH AS FULL_PATH,
    BUILD_SCOPED_FILE_URL('@ADE_APPS_DB.FINRA.DOCS', p.RELATIVE_PATH) AS FILE_URL

FROM PARSE_WITH_PATH p,
LATERAL FLATTEN(INPUT => p.CHUNKS) c
;

--------------------------------------------------------------------------------
-- SANITY CHECK: Verify chunks table structure
--------------------------------------------------------------------------------

-- Inspect the chunks table (should have one row per chunk with metadata)
SELECT * FROM ADE_APPS_DB.FINRA.FINRA_AWARDS_CHUNKS
    LIMIT 20;


--------------------------------------------------------------------------------
-- SECTION 6: CREATE CORTEX SEARCH SERVICE
-- Set up a Cortex Search service to enable semantic search over document chunks
-- This allows the agent to find relevant passages to answer user questions
-- REQUIRED FOR SETUP
--------------------------------------------------------------------------------

-- Enable change tracking so Cortex Search can incrementally update the index
ALTER TABLE ADE_APPS_DB.FINRA.FINRA_AWARDS_CHUNKS
SET CHANGE_TRACKING = TRUE;

-- Create the Cortex Search service
-- This indexes the CHUNK_MARKDOWN field and makes other fields available as attributes
-- You can also create this via the UI: AI & ML -> Cortex Search
CREATE OR REPLACE CORTEX SEARCH SERVICE ADE_APPS_DB.FINRA.FINRA_AWARD_SEARCH
    ON CHUNK_MARKDOWN
    ATTRIBUTES RELATIVE_PATH, FULL_PATH, FILE_URL, FILENAME, DOC_ID, PAGE_NUMBER, CHUNK_ID, CHUNK_TYPE
    WAREHOUSE = 'WH_LANDINGAI_ADE'
    TARGET_LAG = '1 DAY'
AS
(
    SELECT
        CHUNK_MARKDOWN,
        RELATIVE_PATH,
        FULL_PATH,
        FILE_URL,
        FILENAME,
        DOC_ID,
        PAGE_NUMBER,
        CHUNK_INDEX,
        CHUNK_INFO,
        CHUNK_ID,
        CHUNK_TYPE,
        CHUNK_BOX,
        STAGE_NAME
    FROM ADE_APPS_DB.FINRA.FINRA_AWARDS_CHUNKS
);

--------------------------------------------------------------------------------
-- SANITY CHECK: Test the Cortex Search service
-- Verify that the search service is working and returning relevant results
--------------------------------------------------------------------------------

-- Test query: Search for chunks related to "compensatory damages awarded"
-- This should return the top 10 most relevant chunks with their metadata
WITH RESP AS (
  SELECT PARSE_JSON(
    SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'ADE_APPS_DB.FINRA.FINRA_AWARD_SEARCH',
      '{
        "query": "compensatory damages awarded",
        "columns": [
          "CHUNK_MARKDOWN",
          "RELATIVE_PATH",
          "PAGE_NUMBER",
          "CHUNK_INDEX",
          "CHUNK_ID",
          "FILE_URL"
        ],
        "limit": 10
      }'
    )
  ) AS J
)
SELECT
  R.VALUE:CHUNK_MARKDOWN::STRING AS CHUNK_TEXT,
  R.VALUE:RELATIVE_PATH::STRING  AS RELATIVE_PATH,
  R.VALUE:PAGE_NUMBER::INTEGER   AS PAGE_NUMBER,
  R.VALUE:CHUNK_INDEX::INTEGER   AS CHUNK_INDEX,
  R.VALUE:CHUNK_ID::STRING       AS CHUNK_ID,
  R.VALUE:FILE_URL::STRING       AS FILE_URL
FROM RESP,
LATERAL FLATTEN(INPUT => J['results']) R;

--------------------------------------------------------------------------------
-- SECTION 7: CREATE SEMANTIC VIEW FOR CORTEX ANALYST
-- Define a semantic layer that maps business-friendly terms to database columns
-- This allows Cortex Analyst to translate natural language questions into SQL
-- You can also create/edit this via the UI: AI & ML -> Cortex Analyst
-- REQUIRED FOR SETUP
--------------------------------------------------------------------------------

-- Create a semantic view with business-friendly column descriptions and synonyms
-- This enables natural language queries like "What were the total filing fees in 2025?"

CREATE OR REPLACE SEMANTIC VIEW ADE_APPS_DB.FINRA.SV_FINRA_AWARD
  TABLES (
    award AS ADE_APPS_DB.FINRA.FINRA_AWARD_EXTRACTED
      PRIMARY KEY (DOC_ID)
  )

  FACTS (
    award.filing_fee                              AS FILING_FEE,
    award.initial_claim_filing_fee                AS INITIAL_CLAIM_FILING_FEE,
    award.member_surcharge                        AS MEMBER_SURCHARGE,
    award.member_process_fee                      AS MEMBER_PROCESS_FEE,
    award.member_surcharge_fee_paid_by_respondent AS MEMBER_SURCHARGE_FEE_PAID_BY_RESPONDENT,
    award.total_hearing_session_fees              AS TOTAL_HEARING_SESSION_FEES,
    award.hearing_session_fees_paid_by_claimants  AS HEARING_SESSION_FEES_PAID_BY_CLAIMANTS,
    award.hearing_session_fees_paid_by_respondents AS HEARING_SESSION_FEES_PAID_BY_RESPONDENTS,
    award.hearing_session_fees_paid_by_finra_or_other AS HEARING_SESSION_FEES_PAID_BY_FINRA_OR_OTHER,
    award.compensatory_damages                    AS COMPENSATORY_DAMAGES,
    award.punitive_damages                        AS PUNITIVE_DAMAGES,
    award.attorneys_fees_to_respondents           AS ATTORNEYS_FEES_TO_RESPONDENTS,
    award.costs_to_respondents                    AS COSTS_TO_RESPONDENTS,
    award.reimbursement_to_claimant               AS REIMBURSEMENT_TO_CLAIMANT,
    award.filing_fee_retained_by_finra            AS FILING_FEE_RETAINED_BY_FINRA
  )

  DIMENSIONS (
    award.doc_id                            AS DOC_ID
      WITH SYNONYMS = ('document id','doc id'),
    award.case_number                       AS CASE_NUMBER
      WITH SYNONYMS = ('case','case no','case number'),
    award.document_type                     AS DOCUMENT_TYPE,
    award.awarding_body                     AS AWARDING_BODY,
    award.hearing_site_city                 AS HEARING_SITE_CITY,
    award.hearing_site_state                AS HEARING_SITE_STATE
      WITH SYNONYMS = ('state'),
    award.nature_of_dispute                 AS NATURE_OF_DISPUTE,
    award.statement_of_claim_filed_date     AS STATEMENT_OF_CLAIM_FILED_DATE,
    award.statement_of_answer_filed_date    AS STATEMENT_OF_ANSWER_FILED_DATE,
    award.hearing_date                      AS HEARING_DATE,
    award.date_of_service                   AS DATE_OF_SERVICE,
    award.other_relief_denied               AS OTHER_RELIEF_DENIED,
    award.claimant_claims_denied_in_entirety AS CLAIMANT_CLAIMS_DENIED_IN_ENTIRETY,
    award.expungement_occurrence_number     AS EXPUNGEMENT_OCCURRENCE_NUMBER
  )

  METRICS (
    award.award_count                       AS COUNT(*)
      WITH SYNONYMS = ('awards','cases'),
    award.total_hearing_session_fees_sum    AS SUM(award.total_hearing_session_fees),
    award.compensatory_damages_sum          AS SUM(award.compensatory_damages),
    award.reimbursement_to_claimant_sum     AS SUM(award.reimbursement_to_claimant),
    award.avg_total_hearing_session_fees    AS AVG(award.total_hearing_session_fees)
  )

  COMMENT = 'FINRA awards: 1 row per award (main facts + dimensions).';


CREATE OR REPLACE SEMANTIC VIEW ADE_APPS_DB.FINRA.SV_FINRA_AWARD_ARBITRATORS
  TABLES (
    arb AS ADE_APPS_DB.FINRA.FINRA_AWARD_ARBITRATORS
      PRIMARY KEY (DOC_ID, ARBITRATOR_INDEX)
      COMMENT = '1 row per arbitrator per award'
  )

  DIMENSIONS (
    arb.doc_id                    AS DOC_ID
      WITH SYNONYMS = ('document id','doc id'),
    arb.arbitrator_index          AS ARBITRATOR_INDEX,
    arb.arbitrator_name           AS ARBITRATOR_NAME
      WITH SYNONYMS = ('arbitrator','panelist'),
    arb.arbitrator_role           AS ARBITRATOR_ROLE
      WITH SYNONYMS = ('role','chair','presiding chair'),
    arb.arbitrator_signature_date AS ARBITRATOR_SIGNATURE_DATE
      WITH SYNONYMS = ('signature date','signed date')
  )

  METRICS (
    arb.arbitrator_row_count      AS COUNT(*),
    arb.distinct_award_count      AS COUNT(DISTINCT arb.doc_id)
  )

  COMMENT = 'FINRA arbitrators semantic view.';



CREATE OR REPLACE SEMANTIC VIEW ADE_APPS_DB.FINRA.SV_FINRA_AWARD_CLAIMANTS
  TABLES (
    c AS ADE_APPS_DB.FINRA.FINRA_AWARD_CLAIMANTS
      PRIMARY KEY (DOC_ID, CLAIMANT_INDEX)
      COMMENT = '1 row per claimant per FINRA award'
  )

  DIMENSIONS (
    c.doc_id            AS DOC_ID
      WITH SYNONYMS = ('document id','doc id'),
    c.claimant_index    AS CLAIMANT_INDEX,
    c.claimant_name     AS CLAIMANT_NAME
      WITH SYNONYMS = ('claimant','customer')
  )

  METRICS (
    c.claimant_row_count  AS COUNT(*),
    c.distinct_award_count AS COUNT(DISTINCT c.doc_id)
  )

  COMMENT = 'FINRA claimants semantic view.';


  CREATE OR REPLACE SEMANTIC VIEW ADE_APPS_DB.FINRA.SV_FINRA_AWARD_RESPONDENTS
  TABLES (
    r AS ADE_APPS_DB.FINRA.FINRA_AWARD_RESPONDENTS
      PRIMARY KEY (DOC_ID, RESPONDENT_INDEX)
      COMMENT = '1 row per respondent per FINRA award'
  )

  DIMENSIONS (
    r.doc_id              AS DOC_ID
      WITH SYNONYMS = ('document id','doc id'),
    r.respondent_index    AS RESPONDENT_INDEX,
    r.respondent_name     AS RESPONDENT_NAME
      WITH SYNONYMS = ('respondent','firm','member')
  )

  METRICS (
    r.respondent_row_count AS COUNT(*),
    r.distinct_award_count AS COUNT(DISTINCT r.doc_id)
  )

  COMMENT = 'FINRA respondents semantic view.';



--------------------------------------------------------------------------------
-- SANITY CHECK: Test the Semantic Views
-- validate it from three angles:
-- 1 Semantic correctness (does Snowflake “see” the dimensions/facts/metrics?)
-- 2 Aggregation safety (no double counting)
-- 3 Cortex Analyst readiness (natural-language style questions)
--------------------------------------------------------------------------------

-- Count of awards
SELECT AGG(award_count) AS award_count
FROM ADE_APPS_DB.FINRA.SV_FINRA_AWARD;

-- List a few basic dimensions
SELECT
  CASE_NUMBER,
  DOCUMENT_TYPE,
  AWARDING_BODY,
  HEARING_SITE_STATE,
  DATE_OF_SERVICE
FROM ADE_APPS_DB.FINRA.SV_FINRA_AWARD
ORDER BY DATE_OF_SERVICE DESC
LIMIT 10;

-- Total hearing session fees by state
SELECT *
FROM SEMANTIC_VIEW(
  ADE_APPS_DB.FINRA.SV_FINRA_AWARD
  DIMENSIONS award.hearing_site_state
  METRICS award.total_hearing_session_fees_sum
)
ORDER BY total_hearing_session_fees_sum DESC;

-- Boolean dimensions behaving correctly
-- How often are claims denied in entirety?
SELECT *
FROM SEMANTIC_VIEW(
  ADE_APPS_DB.FINRA.SV_FINRA_AWARD
  DIMENSIONS award.claimant_claims_denied_in_entirety
  METRICS award.award_count
)
ORDER BY claimant_claims_denied_in_entirety;

-- Respondents table
SELECT *
FROM SEMANTIC_VIEW(
  ADE_APPS_DB.FINRA.SV_FINRA_AWARD_RESPONDENTS
  DIMENSIONS r.respondent_name
  METRICS r.respondent_row_count
)
ORDER BY respondent_row_count DESC;



--------------------------------------------------------------------------------
-- SECTION 7B: UNIFIED SEMANTIC VIEW FOR CORTEX ANALYST
-- Define a semantic layer that maps business-friendly terms to database columns
-- This allows Cortex Analyst to translate natural language questions into SQL
-- You can also create/edit this via the UI: AI & ML -> Cortex Analyst
-- REQUIRED FOR SETUP
--------------------------------------------------------------------------------

CREATE OR REPLACE SEMANTIC VIEW ADE_APPS_DB.FINRA.SV_FINRA_AWARD_FULL
  TABLES (
    award AS ADE_APPS_DB.FINRA.FINRA_AWARD_EXTRACTED
      PRIMARY KEY (DOC_ID)
      COMMENT = '1 row per FINRA award (facts + most dimensions)',

    arb AS ADE_APPS_DB.FINRA.FINRA_AWARD_ARBITRATORS
      PRIMARY KEY (DOC_ID, ARBITRATOR_INDEX)
      COMMENT = 'Arbitrators per award',

    c AS ADE_APPS_DB.FINRA.FINRA_AWARD_CLAIMANTS
      PRIMARY KEY (DOC_ID, CLAIMANT_INDEX)
      COMMENT = 'Claimants per award',

    r AS ADE_APPS_DB.FINRA.FINRA_AWARD_RESPONDENTS
      PRIMARY KEY (DOC_ID, RESPONDENT_INDEX)
      COMMENT = 'Respondents per award'
  )

  RELATIONSHIPS (
    arb (DOC_ID) REFERENCES award,
    c   (DOC_ID) REFERENCES award,
    r   (DOC_ID) REFERENCES award
  )

  /* Keep monetary / quantitative facts on the award table only */
  FACTS (
    award.filing_fee                              AS FILING_FEE,
    award.initial_claim_filing_fee                AS INITIAL_CLAIM_FILING_FEE,
    award.member_surcharge                        AS MEMBER_SURCHARGE,
    award.member_process_fee                      AS MEMBER_PROCESS_FEE,
    award.member_surcharge_fee_paid_by_respondent AS MEMBER_SURCHARGE_FEE_PAID_BY_RESPONDENT,
    award.total_hearing_session_fees              AS TOTAL_HEARING_SESSION_FEES,
    award.hearing_session_fees_paid_by_claimants  AS HEARING_SESSION_FEES_PAID_BY_CLAIMANTS,
    award.hearing_session_fees_paid_by_respondents AS HEARING_SESSION_FEES_PAID_BY_RESPONDENTS,
    award.hearing_session_fees_paid_by_finra_or_other AS HEARING_SESSION_FEES_PAID_BY_FINRA_OR_OTHER,
    award.compensatory_damages                    AS COMPENSATORY_DAMAGES,
    award.punitive_damages                        AS PUNITIVE_DAMAGES,
    award.attorneys_fees_to_respondents           AS ATTORNEYS_FEES_TO_RESPONDENTS,
    award.costs_to_respondents                    AS COSTS_TO_RESPONDENTS,
    award.reimbursement_to_claimant               AS REIMBURSEMENT_TO_CLAIMANT,
    award.filing_fee_retained_by_finra            AS FILING_FEE_RETAINED_BY_FINRA
  )

  DIMENSIONS (
    /* Award-level identifiers */
    award.doc_id                                  AS DOC_ID WITH SYNONYMS = ('document id','doc id'),
    award.case_number                             AS CASE_NUMBER WITH SYNONYMS = ('case','case no','case number'),

    /* Award-level descriptors */
    award.document_type                           AS DOCUMENT_TYPE,
    award.awarding_body                           AS AWARDING_BODY,
    award.hearing_site_city                       AS HEARING_SITE_CITY,
    award.hearing_site_state                      AS HEARING_SITE_STATE WITH SYNONYMS = ('state'),
    award.nature_of_dispute                       AS NATURE_OF_DISPUTE,

    /* Dates */
    award.statement_of_claim_filed_date           AS STATEMENT_OF_CLAIM_FILED_DATE,
    award.statement_of_answer_filed_date          AS STATEMENT_OF_ANSWER_FILED_DATE,
    award.hearing_date                            AS HEARING_DATE,
    award.date_of_service                         AS DATE_OF_SERVICE,

    award.service_year         AS SERVICE_YEAR WITH SYNONYMS = ('year','service year'),
    award.service_quarter      AS SERVICE_QUARTER WITH SYNONYMS = ('quarter','service quarter'),
    award.service_year_quarter AS SERVICE_YEAR_QUARTER WITH SYNONYMS = ('year quarter','year-quarter','service year quarter'),

    /* Decision flags / expungement */
    award.other_relief_denied                     AS OTHER_RELIEF_DENIED,
    award.claimant_claims_denied_in_entirety      AS CLAIMANT_CLAIMS_DENIED_IN_ENTIRETY,
    award.expungement_occurrence_number           AS EXPUNGEMENT_OCCURRENCE_NUMBER,

    /* Arbitrators */
    arb.arbitrator_name                           AS ARBITRATOR_NAME WITH SYNONYMS = ('arbitrator','panelist'),
    arb.arbitrator_role                           AS ARBITRATOR_ROLE WITH SYNONYMS = ('chair','presiding chair'),
    arb.arbitrator_signature_date                 AS ARBITRATOR_SIGNATURE_DATE,

    /* Parties */
    c.claimant_name                               AS CLAIMANT_NAME WITH SYNONYMS = ('claimant','customer'),
    r.respondent_name                             AS RESPONDENT_NAME WITH SYNONYMS = ('respondent','firm','member')
  )

  /* Metrics should reference award facts to avoid double counting */
  METRICS (
    /* Award-scoped metrics (safe with award-level dimensions) */
    award.award_count                             AS COUNT(*) WITH SYNONYMS = ('awards','cases'),
    award.total_hearing_session_fees_sum          AS SUM(award.total_hearing_session_fees),
    award.compensatory_damages_sum                AS SUM(award.compensatory_damages),
    award.reimbursement_to_claimant_sum           AS SUM(award.reimbursement_to_claimant),
    award.avg_total_hearing_session_fees          AS AVG(award.total_hearing_session_fees),

    /* Respondent-scoped metrics */
    r.respondent_award_count                      AS COUNT(DISTINCT r.doc_id),
    r.respondent_total_hearing_session_fees_sum   AS SUM(award.total_hearing_session_fees),

    /* Claimant-scoped metrics */
    c.claimant_award_count                         AS COUNT(DISTINCT c.doc_id),
    c.claimant_total_hearing_session_fees_sum      AS SUM(award.total_hearing_session_fees),

    /* Arbitrator-scoped metrics */
    arb.arbitrator_award_count                     AS COUNT(DISTINCT arb.doc_id),
    arb.arbitrator_total_hearing_session_fees_sum  AS SUM(award.total_hearing_session_fees)
  )

  COMMENT = 'Unified FINRA model: awards + arbitrators + claimants + respondents joined by DOC_ID.';


--------------------------------------------------------------------------------
-- SANITY CHECK: Test the Unified Semantic View
--------------------------------------------------------------------------------


--Fees by respondent (proves relationship works)
SELECT *
FROM SEMANTIC_VIEW(
  ADE_APPS_DB.FINRA.SV_FINRA_AWARD_FULL
  DIMENSIONS r.respondent_name
  METRICS r.respondent_total_hearing_session_fees_sum
)
ORDER BY respondent_total_hearing_session_fees_sum DESC;

SELECT *
FROM SEMANTIC_VIEW(
  ADE_APPS_DB.FINRA.SV_FINRA_AWARD_FULL
  DIMENSIONS c.claimant_name
  METRICS c.claimant_award_count
)
ORDER BY claimant_award_count DESC;


-- Arbitrators in California (role + state)
SELECT *
FROM (
  SELECT *
  FROM SEMANTIC_VIEW(
    ADE_APPS_DB.FINRA.SV_FINRA_AWARD_FULL
    DIMENSIONS award.hearing_site_state, arb.arbitrator_name
    METRICS arb.arbitrator_award_count
  )
)
WHERE hearing_site_state = 'California'
ORDER BY arbitrator_award_count DESC;

SELECT *
FROM SEMANTIC_VIEW(
  ADE_APPS_DB.FINRA.SV_FINRA_AWARD_FULL
  DIMENSIONS award.service_year, award.service_quarter
  METRICS award.award_count
)
ORDER BY service_year, service_quarter;



--------------------------------------------------------------------------------
-- SECTION 8: CREATE PRESIGNED URL STORED PROCEDURE
-- This stored procedure generates temporary browser-accessible URLs for files
-- in the stage, allowing the agent to provide document download links to users
-- REQUIRED FOR SETUP
--------------------------------------------------------------------------------

USE DATABASE ADE_APPS_DB;
USE SCHEMA ADE_APPS_DB.FINRA;

-- Create a stored procedure that generates presigned URLs with configurable expiration
CREATE OR REPLACE PROCEDURE ADE_APPS_DB.FINRA.GET_FILE_PRESIGNED_URL_SP(
    RELATIVE_FILE_PATH STRING,
    EXPIRATION_MINS INTEGER DEFAULT 60
)
RETURNS STRING
LANGUAGE SQL
COMMENT = 'Generates a presigned url for a file in @ADE_APPS_DB.FINRA.DOCS. Input is the relative file path (e.g., award/25-01597.pdf).'
EXECUTE AS CALLER
AS
$$
DECLARE
    presigned_url STRING;
    sql_stmt STRING;
    expiration_seconds INTEGER;
    stage_name STRING DEFAULT '@ADE_APPS_DB.FINRA.DOCS';
BEGIN
    expiration_seconds := EXPIRATION_MINS * 60;

    sql_stmt := 'SELECT GET_PRESIGNED_URL('
                || stage_name
                || ', '''
                || RELATIVE_FILE_PATH
                || ''', '
                || expiration_seconds
                || ') AS url';

    EXECUTE IMMEDIATE :sql_stmt;

    SELECT "URL"
      INTO :presigned_url
      FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));

    RETURN :presigned_url;
END;
$$;

--------------------------------------------------------------------------------
-- SECTION 9: CREATE THE CORTEX AGENT
-- Define the agent with its profile, instructions, tools, and tool resources
-- The agent orchestrates queries across structured data (Cortex Analyst),
-- document search (Cortex Search), and dynamic URLs
-- You can also create/edit this via the UI: AI & ML -> Agents
-- REQUIRED FOR SETUP
--------------------------------------------------------------------------------

-- Create the agent with comprehensive configuration


CREATE OR REPLACE AGENT SNOWFLAKE_INTELLIGENCE.AGENTS.LANDINGAI_ADE_FINRA_AWARDS
  PROFILE = '{"display_name":"FINRA Arbitration Awards Agent","avatar":"gavel.png","color":"#2563EB"}'
  COMMENT = $$Use this Agent to interact with FINRA Arbitration Awards. FINRA's Dispute Resolution Services (DRS) helps investors and firms resolve securities-related disputes through arbitration and mediation. Documents sourced from https://www.finra.org/arbitration-mediation/arbitration-awards-online.$$
  FROM SPECIFICATION
$$
{
  "models": {
    "orchestration": "auto"
  },

  "orchestration": {
    "budget": {
      "seconds": 30,
      "tokens": 16000
    }
  },

  "instructions": {
    "system": "You are an expert assistant for FINRA Arbitration Awards. Ground claims in the available Snowflake data: structured results via Analyst and document text via Search. Do not speculate beyond available sources. If an answer is not supported by the data, say so.",

    "response": "Be concise. Use tables where helpful. For numerical answers, base them on Analyst results. For claims about what an award says (findings, rationale, expungement language, exact phrasing), retrieve supporting excerpts using finra_award_search and cite the RELATIVE_PATH (and any chunk identifiers returned). For purely aggregated numeric answers from Analyst, cite the semantic view name once. Cite each source only once per answer.",

    "orchestration": "Use finra_award_lookup (Cortex Analyst) for questions about fees, damages, parties, arbitrators, claim outcomes, locations, or time. IMPORTANT GRANULARITY RULE: Use award.* metrics for award-level questions. For \"by respondent/claimant/arbitrator\" questions, use r.*, c.*, arb.* metrics respectively. Use SERVICE_YEAR, SERVICE_QUARTER, or SERVICE_YEAR_QUARTER when the user asks for time slicing. Use finra_award_search (Cortex Search) when the user asks what an award states, asks for supporting evidence, quotes, or document language. Only when the user explicitly asks to open, view, or download a document, call Dynamic_Doc_URL_Tool to generate a temporary, browser-accessible URL. Do not return Snowflake internal /api/files URLs.",

    "sample_questions": [
    {
        "question": "What are the 10 largest compensatory damage amounts awarded in 2025 for unique claims? For each one, provide the names of the respondent(s), the case number, and a brief summary of the claim.",
        "answer": ""
      },
      {
        "question": "How many times was UBS involved as a respondent in 2025? What percent of the cases resulted in damages assessed against UBS and what is the sum of those damages?",
        "answer": ""
      },
            {
        "question": "What is the average time in days from the filing of a claim to its resolution by arbitration? Also provide 25th, 50th and 75th percentiles.",
        "answer": ""
      },
                  {
        "question": "Which arbitration cases involve disputes between employees and employers, former or present? Provide the case number and a summary of each including whether the employee or the employer prevailed in the case.",
        "answer": ""
      },
      {
        "question": "What are the total hearing session fees paid by all claimants and all respondents in 2025?",
        "answer": ""
      },
     {
        "question": "In what percent of cases are respondents ordered to pay attorneys fees for claimants as part of the judgment? Which respondents paid the most in such attorney's fees in 2025?",
        "answer": ""
      },
      {
        "question": "Which claims deal with conflict of interests? Provide a table showing the case number, claimant, claimant's attorneys, state where adjudicated and a brief description of the claim.",
        "answer": ""
      },
      {
        "question": "Open the file for case 25-00053.",
        "answer": "I need to construct the relative file path for this case."
      }
    ]
  },

  "tools": [
    {
      "tool_spec": {
        "type": "cortex_analyst_text_to_sql",
        "name": "finra_award_lookup",
        "description": "Semantic view over FINRA Arbitration Award extracted fields (case number, parties, dates, decisions, damages, fees, etc.)."
      }
    },
    {
      "tool_spec": {
        "type": "cortex_search",
        "name": "finra_award_search",
        "description": "Looks up FINRA arbitration award documents (chunk-level search)."
      }
    },
    {
      "tool_spec": {
        "type": "generic",
        "name": "Dynamic_Doc_URL_Tool",
        "description": "Generates a temporary URL for a document in the stage given its relative file path (e.g., award/25-01597.pdf).",
        "input_schema": {
          "type": "object",
          "properties": {
            "expiration_mins": {
              "type": "number",
              "description": "Expiration in minutes."
            },
            "relative_file_path": {
              "type": "string",
              "description": "Relative file path inside the stage (e.g., award/25-01597.pdf)."
            }
          },
          "required": ["expiration_mins", "relative_file_path"]
        }
      }
    }
  ],

  "tool_resources": {
    "finra_award_lookup": {
      "execution_environment": {
        "type": "warehouse",
        "warehouse": "ADE_DEMOS_WH",
        "query_timeout": 300
      },
      "semantic_view": "ADE_APPS_DB.FINRA.SV_FINRA_AWARD_FULL"
    },

    "finra_award_search": {
      "name": "ADE_APPS_DB.FINRA.FINRA_AWARD_SEARCH",
      "max_results": 8,
      "id_column": "RELATIVE_PATH",
      "title_column": "RELATIVE_PATH"
    },

    "Dynamic_Doc_URL_Tool": {
      "execution_environment": {
        "type": "warehouse",
        "warehouse": "ADE_DEMOS_WH",
        "query_timeout": 274
      },
      "identifier": "ADE_APPS_DB.FINRA.GET_FILE_PRESIGNED_URL_SP",
      "type": "procedure"
    }
  }
}

$$;


--------------------------------------------------------------------------------
-- SANITY CHECKS: Test all components end-to-end
-- Run these queries to verify the entire pipeline is working correctly
--------------------------------------------------------------------------------

DESCRIBE AGENT SNOWFLAKE_INTELLIGENCE.AGENTS.LANDINGAI_ADE_FINRA_AWARDS;

-- Semantic view basic health
SELECT *
FROM SEMANTIC_VIEW(
  ADE_APPS_DB.FINRA.SV_FINRA_AWARD_FULL
  DIMENSIONS award.hearing_site_state
  METRICS award.award_count
)
ORDER BY award_count DESC;


-- These confirm your entity-scoped metrics exist and behave.
SELECT *
FROM SEMANTIC_VIEW(
  ADE_APPS_DB.FINRA.SV_FINRA_AWARD_FULL
  DIMENSIONS r.respondent_name
  METRICS r.respondent_award_count
)
ORDER BY respondent_award_count DESC
LIMIT 25;

-- “Denied in entirety” rate check
SELECT *
FROM SEMANTIC_VIEW(
  ADE_APPS_DB.FINRA.SV_FINRA_AWARD_FULL
  DIMENSIONS award.claimant_claims_denied_in_entirety
  METRICS award.award_count
)
ORDER BY claimant_claims_denied_in_entirety;


-- Verify Cortex Search is working end-to-end
-- This should return relevant chunks about compensatory damages
WITH RESP AS (
  SELECT PARSE_JSON(
    SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'ADE_APPS_DB.FINRA.FINRA_AWARD_SEARCH',
      '{
        "query": "compensatory damages awarded",
        "columns": ["CHUNK_MARKDOWN","RELATIVE_PATH","PAGE_NUMBER"],
        "limit": 5
      }'
    )
  ) AS J
)
SELECT
  R.VALUE:CHUNK_MARKDOWN::STRING AS TEXT,
  R.VALUE:RELATIVE_PATH::STRING  AS FILE,
  R.VALUE:PAGE_NUMBER::INTEGER   AS PAGE
FROM RESP,
LATERAL FLATTEN(INPUT => J['results']) R;


-- Test 2: Verify the presigned URL stored procedure works
-- This should return a temporary URL that you can open in a browser
CALL ADE_APPS_DB.FINRA.GET_FILE_PRESIGNED_URL_SP('award/25-01597.pdf', 60);

--------------------------------------------------------------------------------
-- FINAL NOTES: PERMISSIONS AND USAGE
--------------------------------------------------------------------------------

-- Since we used ACCOUNTADMIN, make sure to grant necessary permissions to roles
-- that will interact with the agent, including:
--   - USAGE on the database, schema, and warehouse
--   - READ on tables and stages
--   - USAGE on Cortex Search services and Agents

-- To interact with the agent:
-- Navigate to ai.snowflake.com, find your agent, and start asking questions!
-- The agent can answer questions about arbitration awards, search documents, 
-- and generate download links for FINRA documents.