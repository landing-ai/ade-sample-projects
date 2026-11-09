# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Teaches

An end-to-end document extraction accuracy pipeline using LandingAI's Agentic Document
Extraction (ADE) REST APIs:

- **Parse API** — convert PDFs to structured markdown
- **Build Schema API** — generate and refine extraction schemas from natural language prompts
- **Extract API** — pull structured fields from markdown using a schema

The pipeline iteratively improves schema quality against a golden evaluation set until
all fields reach ≥ 95% accuracy. The key teaching moment is the **schema refinement loop**:
evaluation results → revision prompt (human-approved) → Build Schema API → repeat.

---

## The Loop

```
── Setup (run once) ──────────────────────────────────────────────────────
  1. Parse all PDFs        →  python scripts/parse.py
  2. Build initial schema  →  schema_builder drafts prompt
                              YOU REVIEW AND APPROVE
                              python scripts/build_schema.py --prompt "..."

── Iteration loop ────────────────────────────────────────────────────────
  3. Extract               →  python scripts/extract.py --force
  4. Evaluate              →  python scripts/evaluate.py
  5a. All fields ≥ 95%?   →  Done
  5b. 3 iters no progress? →  Escalate to user
  5c. Otherwise           →  schema_builder analyzes errors, drafts revision prompt
                              YOU REVIEW AND APPROVE
                              python scripts/build_schema.py --schema schemas/current.json --prompt "..."
                              → Go to step 3
```

---

## Pre-Written Scripts

All LandingAI API calls are in `scripts/`. Read these to understand the API patterns —
parallelism with `ThreadPoolExecutor`, timing with `time.perf_counter()`, REST via `requests`.

| Script | What it does |
|---|---|
| `parse.py` | Sends all PDFs to Parse API in parallel; saves `*_markdown.md` + full response |
| `build_schema.py` | Calls Build Schema API; versions previous schema to `schemas/history/` |
| `extract.py` | Sends all markdowns + current schema to Extract API in parallel |
| `evaluate.py` | Scores `*_extracted.json` against `data/golden_eval/golden.csv`; saves report |

**REST only** — all scripts use `requests`, not the `landingai-ade` Python library.
The Build Schema API is not yet available in the Python library.

---

## Agent Roster

| Agent | Role |
|---|---|
| `orchestrator` | Drives the loop; tracks iterations; decides when to stop |
| `schema_builder` | Analyzes eval results; drafts revision prompt; **always waits for your approval** before calling the API |
| `evaluation_agent` | Runs `evaluate.py`; interprets accuracy numbers and error patterns |
| `report_generator` | Writes human-readable markdown reports after each iteration |

---

## Directory Structure

```
data/
  pdfs/                               ← Source PDFs (READ ONLY — never modify)
  customer-supplied/                  ← Raw golden answers from client (READ ONLY)
  golden_eval/
    golden.csv                        ← Golden set with pdf_filename column (see Setup)
  pipeline_outputs/
    parsed/                           ← Parse API outputs (*_markdown.md, *_parse_response.json)
    extracted/                        ← Extract API outputs (*_extracted.json, *_extract_response.json)
reference/
  landingai-ade-api-spec.md           ← Parse + Extract API spec (READ ONLY)
  landingai-build-schema-spec.md      ← Build Schema API spec (READ ONLY)
  landingai-extract-schema-spec.md    ← JSON schema format spec (READ ONLY)
schemas/
  current.json                        ← Active schema (managed by build_schema.py)
  history/                            ← Versioned backups — never delete
scripts/
  parse.py
  build_schema.py
  extract.py
  evaluate.py
reports/
  iteration_log.md                    ← Running log maintained by orchestrator
  iteration_N_YYYYMMDD.md            ← Per-iteration reports from report_generator
  eval_YYYYMMDD_HHMMSS.json          ← Raw accuracy data from evaluate.py
```

---

## Setup Before First Run

**1. Prepare the golden eval set**

Copy your golden answers CSV to `data/golden_eval/golden.csv` and add a
`pdf_filename` column with the PDF filename for each row:

```csv
pdf_filename,patient_name,age,gender,...
demo_labs_cbc_1.pdf,Master Vidhan,5,Male,...
demo_labs_cbc_2.pdf,Kalpana Kishor Bhosle,52,Female,...
```

The column names (except `pdf_filename`) must exactly match the field names you
will ask Build Schema to extract — evaluate.py matches them by name.

**2. Set your API key**

Add to `.env` at the project root:
```
VISION_AGENT_API_KEY=v2_...
```

**3. Install dependencies**
```bash
pip install requests python-dotenv
```

---

## Key Constraints

- **Never modify** files in `data/pdfs/`, `data/customer_supplied/`, or `reference/`
- **Schema versioning is automatic** — `build_schema.py` backs up `schemas/current.json`
  to `schemas/history/` with a timestamp before every overwrite
- **Human approval required** — `schema_builder` always shows you the revision prompt
  before calling the API; this is the core teaching moment of the pipeline
- **Field name alignment** — the schema field names must match the golden CSV column names
  exactly; use the `--prompt` to specify exact names during initial build
- **Stop conditions** — all fields ≥ 95%, OR 3 consecutive iterations without improvement
- **parse.py always re-parses** — there is no skip-if-exists logic; re-running it will
  re-parse all PDFs and consume API credits unnecessarily. Run it once per project.

---

## Resetting to Clean State

To reset the pipeline to its starting point (e.g., between tutorial runs):

```bash
git clean -fdx --exclude=venv
```

This removes all generated outputs — `data/pipeline_outputs/`, `schemas/`, `reports/` —
while leaving source files, reference docs, and the virtual environment untouched.

**Important:** `.env` is also gitignored and will be deleted. Recreate it after reset:

```
VISION_AGENT_API_KEY=your_key_here
```
