# Document Extraction Accuracy Pipeline
### Data Science Dojo 2026 — LandingAI ADE Tutorial

Build an end-to-end pipeline that extracts structured data from PDFs, evaluates accuracy against a golden set, and iteratively refines the extraction schema until all fields reach ≥ 95% accuracy — driven by Claude Code agents.

---

## What You'll Learn

- How to use LandingAI's **Agentic Document Extraction (ADE)** REST APIs:
  - **Parse API** — convert PDFs to structured markdown
  - **Build Schema API** — generate and refine extraction schemas from natural language prompts
  - **Extract API** — pull structured fields from parsed markdown
- How to evaluate extraction accuracy against a golden evaluation set
- How to iteratively improve schema quality using the **schema refinement loop**
- Patterns for parallel API calls, schema versioning, and human-in-the-loop workflows

---

## The Pipeline

```
── Setup (run once) ──────────────────────────────────────────────────────
  1. Parse all PDFs        →  python scripts/parse.py
  2. Build initial schema  →  Claude drafts a prompt
                              YOU REVIEW AND APPROVE
                              python scripts/build_schema.py --prompt "..."

── Iteration loop ────────────────────────────────────────────────────────
  3. Extract               →  python scripts/extract.py --force
  4. Evaluate              →  python scripts/evaluate.py
  5a. All fields ≥ 95%?   →  Done ✓
  5b. 3 iters no progress? →  Escalate to user
  5c. Otherwise           →  Claude analyzes errors, drafts a revision prompt
                              YOU REVIEW AND APPROVE
                              python scripts/build_schema.py --schema schemas/current.json --prompt "..."
                              → Go to step 3
```

The core teaching moment is **step 5c**: you see exactly what failed, why, and what schema change fixes it — before any API call is made.

---

## Project Structure

```
data/
  pdfs/                     ← Source PDFs (6 CBC lab reports)
  customer-supplied/        ← Raw golden answers from client
  golden_eval/
    golden.csv              ← Prepared evaluation set (34 fields × 6 documents)
  pipeline_outputs/
    parsed/                 ← Parse API outputs (*_markdown.md, *_parse_response.json)
    extracted/              ← Extract API outputs (*_extracted.json, *_extract_response.json)
reference/
  landingai-ade-api-spec.md          ← Parse + Extract API reference
  landingai-build-schema-spec.md     ← Build Schema API reference
  landingai-extract-schema-spec.md   ← JSON schema format reference
schemas/
  current.json              ← Active extraction schema
  history/                  ← Timestamped backups of every prior schema
scripts/
  parse.py                  ← Batch-parse PDFs in parallel
  build_schema.py           ← Generate or refine the extraction schema
  extract.py                ← Batch-extract fields from parsed markdown
  evaluate.py               ← Score results against the golden set
reports/
  iteration_log.md          ← Running log of all iterations
  iteration_N_YYYYMMDD.md   ← Per-iteration human-readable reports
  eval_YYYYMMDD_HHMMSS.json ← Raw accuracy data
```

---

## Setup

**1. Clone the repo and navigate to this project**
```bash
git clone https://github.com/landing-ai/ade-sample-projects.git
cd ade-sample-projects/Events/Data_Science_Dojo_2026
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install requests python-dotenv
```

**3. Add your LandingAI API key**

Create a `.env` file at the project root:
```
VISION_AGENT_API_KEY=your_key_here
```

Get your API key at [va.landing.ai](https://va.landing.ai).

---

## Running the Pipeline

### Option A — With Claude Code (recommended)

Open this project in Claude Code and type:
```
Run the pipeline
```

Claude's agents will drive the full loop, pause for your approval at each schema build step, and generate reports after each iteration.

### Option B — Manually

```bash
# Step 1: Parse PDFs
python scripts/parse.py

# Step 2: Build initial schema (craft your own prompt)
python scripts/build_schema.py --prompt "Extract patient_name, age, gender, test_date, and all CBC panel values..."

# Step 3: Extract
python scripts/extract.py --force

# Step 4: Evaluate
python scripts/evaluate.py

# Step 5: Refine (repeat until all fields pass)
python scripts/build_schema.py \
    --schema schemas/current.json \
    --prompt "Fix the age field — it is returning '21 Years' instead of just '21'..."

python scripts/extract.py --force
python scripts/evaluate.py
```

---

## The Golden Evaluation Set

`data/golden_eval/golden.csv` contains manually verified answers for all 6 CBC lab reports across 34 fields — patient demographics and every CBC panel value with its unit.

Accuracy thresholds:
- **Numeric fields**: match within ±0.5% relative tolerance (floor ±0.01 absolute)
- **String fields**: case-insensitive exact match
- **Pass threshold**: ≥ 95% per field

---

## Scripts at a Glance

| Script | Key patterns |
|---|---|
| `parse.py` | `ThreadPoolExecutor` for parallel API calls, `time.perf_counter()` for timing |
| `build_schema.py` | Multipart form upload, automatic schema versioning to `schemas/history/` |
| `extract.py` | Parallel extraction, `--force` flag archives prior outputs before re-running |
| `evaluate.py` | Numeric tolerance matching, per-field accuracy table, JSON report, exits with code 1 if any field below threshold |

All scripts use the `requests` library directly — no LandingAI Python SDK required. The Build Schema API is not yet available in the SDK.

---

## Resetting to Clean State

```bash
git clean -fdx --exclude=venv
```

Removes all generated outputs (`pipeline_outputs/`, `schemas/`, `reports/`) while leaving source files and the virtual environment intact.

> **Note:** `.env` is also removed by this command. Recreate it before running again.
