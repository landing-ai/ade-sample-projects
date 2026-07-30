# Human-in-the-Loop Review UI for ADE Extractions

A local review application for [LandingAI Agentic Document Extraction (ADE)](https://ade.landing.ai/).
Pick a folder of documents and a JSON Schema, run parse + extract over the batch, then
review each document with **the source line or table cell highlighted on the page**
beside every extracted value. Corrections are saved per file, along with a batch error
report showing which schema fields the model struggles with.

Built for rapid visual verification rather than data entry: a reviewer should be able to
confirm or correct a document without reaching for the mouse.

**ADE v2 only** (DPT-3): `client.v2.parse_jobs` and `client.v2.extract_jobs`, both at the
`standard` service tier. No v1 endpoints, no `dpt-2` models.

---

## Contents

- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Setup](#setup)
- [Running](#running)
- [Using the app](#using-the-app)
- [Output](#output)
- [Folder layout](#folder-layout)
- [Adding your own documents and schemas](#adding-your-own-documents-and-schemas)
- [Building with ADE AI agent skills](#building-with-ade-ai-agent-skills)
- [How this app was built](#how-this-app-was-built)
- [Code map](#code-map)
- [Limits and behaviour notes](#limits-and-behaviour-notes)

---

## How it works

```
documents/  ──▶  v2 Parse job  ──▶  markdown + structure (blocks, cells, lines)
                                          │
                 v2 Extract job  ──▶  extraction + extraction_metadata (ranges)
                                          │
                        range overlap join ▼
                   field path ──▶ page + normalized bounding box
                                          │
                          browser overlay  ▼
                    click a field, see exactly where it came from
```

The grounding chain is the interesting part. ADE's Extract API returns, for every field,
the character `ranges` in the parsed Markdown that the value came from. Parse returns a
`structure` tree where every block, table cell, and visual line carries both its own
Markdown `range` and a normalized bounding box. Overlapping those two gives you the
precise region on the page for each extracted value — narrowed to a single table cell or
a single line of text rather than a whole block.

---

## Requirements

- Python 3.12
- An ADE API key ([get one here](https://ade.landing.ai/settings/api-key))
- `landingai-ade >= 1.13.0` — earlier versions have no `client.v2` namespace

---

## Setup

```bash
cd "Applications/UI for Rapid Human View of Extracted Fields"

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then add your API key:

```bash
cp .env-sample .env
```

Edit `.env` and set your key:

```
VISION_AGENT_API_KEY=your_key_here
```

`.env` is gitignored. Never commit it.

Verify the key before spending any credits:

```bash
python check_key.py
```

This checks the key loads, the client builds, `client.v2` exists, and the key is
*accepted* — using a read-only `parse_jobs.list` call that parses nothing and costs
nothing. It prints only the key's length and first four characters, never the key.

---

## Running

Run it in a terminal you keep open, so you can see errors and stop it with `Ctrl+C`:

```bash
cd "Applications/UI for Rapid Human View of Extracted Fields"
uvicorn app:app --port 8000
```

Open <http://localhost:8000>.

> `uvicorn app:app` resolves `app.py` relative to the working directory, so the `cd` is
> required — from anywhere else it exits immediately and the browser shows a connection
> error. If a port is stuck: `kill $(lsof -t -iTCP:8000 -sTCP:LISTEN)`, or use a
> different `--port`.

---

## Using the app

1. **Pick a folder** from the dropdown — any subdirectory of `input_folders/`. Documents
   may sit in a `documents/` subfolder or directly in the folder. You can also paste an
   absolute path.
2. **Pick a schema** from `schemas/`.
3. **Parse+Extract** — runs both stages as async jobs at the `standard` tier. Documents
   that already have results on disk are reused and skipped; tick **Force re-run** to
   reprocess. The two progress bars track parse and extract completions. A document that
   fails is reported individually and does not stop the batch.
4. **Review** — click or arrow through the fields; the matching line or cell highlights
   on the page. Type in a field's box to override it.
5. **Submit Final for this File**, then **Submit Batch** when you're done.

### Keyboard

| Key | Action |
|---|---|
| `↑` / `↓` | previous / next field (highlight follows) |
| `Enter` | edit the selected field |
| `Esc` | leave the input |
| `[` / `]` | previous / next document |
| `PageUp` / `PageDown` | previous / next page |
| `Cmd/Ctrl+S` | Submit Final for this File |

### Display controls

All persist in `localStorage`:

- **Highlight theme** — three swatches in the document pane header: volt fill (green),
  ice fill (violet), and red outline (no fill, so dense text underneath stays readable).
- **Pane widths** — drag the divider between the panes.
- **Field text size** — `A−` / `A+` in the fields pane header.

### Clear & reset

The red **Clear & reset** button (lower right) deletes all generated results for the
**selected folder only**, and takes two clicks to confirm. Source documents are never
touched: the backend deletes only the five known result subdirectories, never the folder
itself or `documents/` — which matters for folders that keep their PDFs at the root.

---

## Output

`HIL_results/<name>.hil.json` per document:

| Key | Contents |
|---|---|
| `final` | schema-shaped object of final values, directly consumable downstream |
| `overrides` | every human correction with `ade_value`, `final_value`, `error_class` |
| `fields` | flat audit trail with `is_override` and the highlight regions per field |
| `parse_job_id` / `extract_job_id` / `doc_id` | traceability back to the ADE jobs |

`batch_report.json` and `batch_report.csv`:

- **Summary** — documents, fields, override rate, counts by error class
- **Per field** — override counts and rates, so you can see which schema fields ADE
  struggles with across the batch
- **Every override** — with before and after values

Error classes:

| Class | Meaning |
|---|---|
| `missing_filled` | ADE returned nothing, reviewer supplied a value |
| `cleared` | ADE had a value, reviewer deliberately emptied it |
| `format_only` | equal after normalizing whitespace, case, punctuation, currency, numbers, and date formats |
| `wrong_value` | differs beyond normalization |

`format_only` exists so cosmetic edits don't inflate the apparent error rate.
Normalization is deliberately conservative — anything that doesn't clearly reduce to the
same value is reported as `wrong_value` rather than explained away.

---

## Folder layout

```
<input folder>/
    documents/          source PDFs and images   (you provide; may also sit at the root)
    parse_results/      <stem>.parse.json + <stem>.md
    extract_results/    <stem>.extract.json
    regions/            <stem>.regions.json      field path -> highlight boxes
    page_images/        rendered page PNG cache
    HIL_results/        <stem>.hil.json + batch_report.{json,csv}
```

Everything except `documents/` is generated and **gitignored** — it's reproducible from
the source documents plus an API key, it can run to several MB per folder, and extraction
output contains whatever was in the documents.

---

## Adding your own documents and schemas

Nothing in the app is specific to any document type. To add a new case:

```
input_folders/my_documents/documents/*.pdf
schemas/my-schema.json
```

The schema is a plain JSON Schema. Objects nest, arrays are enumerated from whatever ADE
extracts, and every leaf becomes an editable row in the review panel. Field order in the
panel follows schema order, so put the fields a reviewer checks first at the top.

To generate a schema from sample documents, ADE has a Build Extract Schema API — see
[the docs](https://docs.landing.ai/).

---

## Building with ADE AI agent skills

This app was built with the ADE agent skills, which teach AI coding agents how to use ADE
correctly — the v2 API surface, response shapes, grounding semantics, and pipeline
patterns. They are worth installing before you extend this project, because ADE's v1 and
v2 APIs differ substantially and an agent working from memory tends to produce v1 code.

Reference: **<https://docs.landing.ai/ade/build-with-ai-agents>**

### Claude Code plugin

```bash
/plugin marketplace add landing-ai/ade-document-processing-skills
/plugin install ade-document-processing@ade-document-processing-skills
/reload-plugins
```

This installs two skills:

| Skill | Covers |
|---|---|
| `document-extraction` | single ADE operations: Parse, Extract, sync vs async jobs, service tiers, block structure, Markdown ranges, bounding boxes, v1↔v2 migration |
| `document-workflows` | end-to-end pipelines: batch and async processing, classify-then-extract, RAG ingestion, database loading, bounding-box visualization, Streamlit UIs |

Skills source: <https://github.com/landing-ai/ade-document-processing-skills>

### Documentation MCP server

Connects an agent to the ADE docs *and* the skills, with no local install:

**MCP server URL:** `https://docs.landing.ai/mcp`

```bash
# Claude Code
claude mcp add --transport http ade-docs https://docs.landing.ai/mcp
```

- **Claude.ai** — Settings → Connectors → add as a custom connector
- **Cursor / VS Code** — use *Connect to Cursor* / *Connect to VS Code* in the contextual
  menu at the top of any docs page

### Other tools

Any agent that reads instruction files can use the skills — clone the repository above
and copy the skill files into whatever directory your tool expects. For plain
documentation context, ADE publishes an index at
[llms.txt](https://docs.landing.ai/llms.txt) and a combined file at
[llms-full.txt](https://docs.landing.ai/llms-full.txt), and any docs page can be read as
Markdown by appending `.md` to its URL.

---

## How this app was built

This project was built end to end with an AI coding agent, and the paper trail is kept in
[`build-process/`](build-process/) as a worked example of the workflow:

| File | What it shows |
|---|---|
| [`instructions.md`](build-process/instructions.md) | the original one-page brief — what was asked for, before any clarification |
| [`BUILD_SPEC.md`](build-process/BUILD_SPEC.md) | the consolidated specification produced by interviewing the requester about everything the brief left open, then implemented against |
| [`Feedback on the application.md`](build-process/Feedback%20on%20the%20application.md) | review notes after using the running app, which drove a second round of changes |

The sequence — brief → interview → written spec → build → use it → feedback → revise — is
the useful part. Two things worth calling out:

- **The spec was written before any code, and revised when reality disagreed with it.**
  One example is recorded inline in `BUILD_SPEC.md` §6.2: the spec originally called for
  the server-side `client.v2.ground()` endpoint to map fields to page regions, and the
  implementation note explains why the local join was used instead.
- **Getting the ADE specifics right came from the skills, not from memory.** ADE's v1 and
  v2 APIs differ enough that an agent working from recall tends to emit v1 code. See
  [Building with ADE AI agent skills](#building-with-ade-ai-agent-skills).

---

## Code map

| File | Role |
|---|---|
| `app.py` | FastAPI routes, page rendering, reset endpoint |
| `ade_pipeline.py` | ADE v2 parse + extract job orchestration, run state, skip logic |
| `grounding.py` | field ranges → line / table-cell bounding boxes |
| `fields.py` | JSON Schema → ordered flat leaf fields, path get/set |
| `hil_output.py` | final per-file output, error classification, batch report |
| `paths.py` | folder layout helpers |
| `check_key.py` | no-cost API key verification |
| `static/` | single-page frontend — no build step, no framework |
| `build-process/` | how this app was specified and built — see [below](#how-this-app-was-built) |

---

## Limits and behaviour notes

- **PDFs and images only.** ADE v2 Parse does not accept Office formats; those need the
  v1 API, which this app deliberately avoids.
- **Array rows cannot be added or removed**, only their values edited. Every element ADE
  extracted is shown, grouped under a numbered heading (`Containers 3 of 6`).
- **Retyping an identical value is not an override.** Only genuine changes are recorded,
  so the batch report never reports corrections that didn't happen. Changed values show
  blue and bold.
- **ADE's extraction warnings are not surfaced in the UI.** They remain in the saved
  `extract_results/*.extract.json`. Local integrity warnings — parse/extract `doc_id`
  mismatch, failed pages — *are* shown, since those mean highlights may be wrong.
- **Highlight precision depends on the document.** Values inside a large table cell can
  only be located to that cell: real ADE `table_cell` nodes carry no per-line geometry,
  so the cell is the finest granularity available for tables. Text blocks resolve to
  individual lines.
- **Page indices.** ADE `grounding.page` is 1-indexed; PyMuPDF is 0-indexed. The
  conversion happens in exactly one place, `api_page_image` in `app.py`.
- **Single user, no auth.** Run state lives in the server process. This is a local demo
  and review tool, not a deployed service.
