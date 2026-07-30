# Build Spec — UI for Rapid Human View of Extracted Fields

Consolidated build specification. Supersedes `instructions.md` (kept as the original source of record).

## 1. Goal

A local human-in-the-loop review application. A reviewer picks a folder of documents and an extraction schema, runs ADE parse + extract over the batch, then works through the documents one at a time comparing each extracted value against the original page — with the exact source line or table cell highlighted — correcting anything wrong and saving a final reviewed output per file plus a batch error report.

The reviewer's job is **rapid visual verification**, not data entry. Every design decision favors scanning speed.

## 2. Non-negotiable constraints

- **ADE v2 only.** Use the DPT-3 stack exclusively: `client.v2.*`. Do not call `client.parse()`, `client.extract()`, `client.section()`, or `client.split()`. Do not use `dpt-2-*` models.
- Consult the **`ade-document-processing` plugin skills** (`document-extraction`, `document-workflows`) for ADE API detail rather than working from memory. Note two places the skill is behind the shipped SDK: `client.v2.parse()` does accept a `password` parameter, and `client.v2` also exposes `ground`, `ground_jobs`, and `files.upload`, which the skill's API table omits.
- Parsing and extraction go through the **async jobs APIs at `standard` service tier** (half credits).
- **Schema-agnostic.** Nothing may hardcode bill-of-lading fields. The app must work with any JSON Schema dropped into `schemas/`. Bill of lading is the test case, not the contract.

## 3. Decisions already settled

These were confirmed during spec review. Do not revisit them.

| Area | Decision |
|---|---|
| Stack | FastAPI backend + a single self-contained HTML/CSS/JS frontend. No React, no build step. |
| Nested & array fields | Flatten to leaf paths; reviewer edits values only. **No** adding or removing array rows. |
| Re-run behavior | Reuse and skip any document that already has both parse and extract results on disk. A separate **Force re-run** control bypasses the skip. |
| Review model | Override-only. Untouched fields are implicitly accepted as ADE-extracted. Submit is always enabled. No per-field verify step. |
| Field presentation | All fields render **uniformly in schema order**. No flagging, badging, or reordering of null or ungrounded fields. |
| Batch scope | Submit Batch writes output for **every** file using current state, recording which files the reviewer never opened. |
| Error report | Per-field override counts and rates, each override auto-classified, with before/after values. Emitted as both CSV and JSON. |

## 4. Project layout

```
UI for Rapid Human View of Extracted Fields/
├── build-process/
│   ├── BUILD_SPEC.md             # this file
│   ├── instructions.md           # original brief
│   └── Feedback on the application.md
├── requirements.txt              # new
├── .env                          # new, gitignored: VISION_AGENT_API_KEY=...
├── app.py                        # new: FastAPI app + routes
├── ade_pipeline.py               # new: parse/extract job orchestration
├── grounding.py                  # new: field range -> line/cell box resolution
├── hil_output.py                 # new: final JSON + batch report writers
├── static/
│   ├── index.html                # new: single-page UI
│   ├── app.js                    # new
│   └── app.css                   # new
├── schemas/
│   └── bill-of-lading-schema.json
└── input_folders/
    └── bill_of_lading/
        ├── documents/            # source PDFs (3 demo bills of lading present)
        ├── parse_results/        # created by app
        ├── extract_results/      # created by app
        ├── page_images/          # created by app: rendered page PNG cache
        └── HIL_results/          # created by app: final reviewed output + reports
```

Run with `uvicorn app:app --reload --port 8000`, then open `http://localhost:8000`.

### Environment

The repo root `.venv` (Python 3.12) already has `landingai-ade` 1.15.0, `uvicorn` 0.52.0, `PyMuPDF` 1.28.0, `python-dotenv`, and `pandas`. **`fastapi` is not installed** and must be added. Ship a `requirements.txt` pinning at minimum:

```
landingai-ade>=1.13.0
fastapi
uvicorn[standard]
PyMuPDF
python-dotenv
```

API key comes from `VISION_AGENT_API_KEY` via a `.env` in this directory, loaded with `load_dotenv()` before constructing the client. Never log or echo the key. Add `.env` to gitignore if not already covered.

## 5. ADE pipeline

### 5.1 Parse

One job per document, `standard` tier, concurrency-limited with a `ThreadPoolExecutor` (4 workers is a sane default):

```python
job = client.v2.parse_jobs.create(
    document=doc_path,
    model="dpt-3-pro-latest",
    service_tier="standard",
)
done = client.v2.parse_jobs.wait(job.job_id, timeout=900, raise_on_failure=True)
parse = done.result          # V2ParseResponse
```

Persist for each document `<stem>`:
- `parse_results/<stem>.parse.json` — the full response, so the UI never needs to re-parse
- `parse_results/<stem>.md` — `parse.markdown` verbatim

**Keep the trailing `<!-- doc_id=... -->` line in the markdown.** v2 Extract reads it to link the extraction back to its parse job.

### 5.2 Extract

```python
job = client.v2.extract_jobs.create(
    markdown=markdown,                      # the saved .md, doc_id line intact
    schema=json.load(open(schema_path)),    # dict straight from schemas/*.json
    service_tier="standard",
)
done = client.v2.extract_jobs.wait(job.job_id, timeout=900, raise_on_failure=True)
extract = done.result        # V2ExtractResult
```

Persist `extract_results/<stem>.extract.json` (full response, including `extraction`, `extraction_metadata`, and `markdown`).

Do **not** pre-convert the schema. v2 takes a dict, a JSON string, or a Pydantic class directly — there is no `pydantic_to_json_schema()` step.

### 5.3 Skip logic

Before creating a parse job, skip the document if `parse_results/<stem>.parse.json` **and** `extract_results/<stem>.extract.json` both exist and are valid JSON — unless **Force re-run** is set. Count skipped files as complete in the progress bars so the bars always reach 100%.

### 5.4 Partial results and failures

- HTTP 206 on parse: some pages failed. `parse.metadata.failed_pages` is **1-indexed**. Keep the result, surface the failed page numbers in the UI, and render those pages without highlights.
- HTTP 206 on extract: check `extract.schema_violation_error` and `extract.warnings`. Keep the data — it is still billed and still usable.
- `JobFailedError` / `JobWaitTimeoutError`: record the document as failed with its message, keep processing the rest of the batch, and list failures in the top panel. One bad document must never abort a run.

## 6. Grounding: field value → highlighted line or cell

This is the core technical work. Get it right before building UI polish.

### 6.1 What the APIs give you

- `extract.extraction_metadata` mirrors `extraction`, every leaf replaced by `{"value": ..., "ranges": [{"start": n, "end": n}, ...]}`. Ranges are Unicode **code point** offsets into the markdown that was submitted. A value found in several places has several ranges. A synthesized value has `value` and `ranges` of `null`.
- `parse.structure` is a `document` node → page children → block children, with table cells nested as `table_cell` children of their `table` block.
- Every node carries `grounding.page` (**1-indexed**), `grounding.range` (`{start, end}`, start inclusive / end exclusive), and `grounding.box` (`xmin`, `ymin`, `xmax`, `ymax`, each normalized 0–1).
- Leaf blocks also carry `atomic_grounding`: a list of `{page, range, box}`, **one entry per visual line** for `text` and `marginalia` blocks.

### 6.2 Resolution algorithm

1. **Verify pairing.** Confirm `extract.metadata.doc_id == parse.metadata.job_id`. The ranges are only meaningful against the markdown that produced them; a mismatch means stale files on disk and must be treated as a cache miss, not silently highlighted.
2. **Field → block.** Overlap each field's `ranges` against every block's `grounding.range`.

   > **Implementation note (revised during the build).** The spec originally said to use `client.v2.ground()` for this. The shipped code does the join locally instead. Reason: `ground` returns `grounding` typed only as `Dict[str, object]`, so its concrete shape cannot be pinned down without live API access; the join itself is a few interval comparisons; and step 3's block→line/cell refinement has to run locally against the structure tree either way. Doing it locally keeps the resolution deterministic, unit-testable offline, and free of an extra billed call per document. `client.v2.ground` remains a valid alternative once its response shape can be verified against the live API.
3. **Block → line or cell.** For each matched block, narrow to the precise region the reviewer needs:
   - `table` block → intersect the field's ranges against each `table_cell` child's `grounding.range`; keep the cells that overlap.
   - `text` / `marginalia` block → intersect against each `atomic_grounding` entry; keep the overlapping **lines**.
   - Any other block type, or a block with no children and no `atomic_grounding` → fall back to the block's own `grounding.box`.
4. **Emit regions.** Produce, per field path, a list of `{page, xmin, ymin, xmax, ymax}`. A field legitimately maps to several regions across several pages.
5. **No ranges → no regions.** If a field's `ranges` is null or empty, it maps to an empty region list. Clicking it highlights nothing and the viewer stays where it is. Per the settled decision this is **not** visually flagged.

Precompute the full path → regions map once per document when it is first opened and cache it, so click-to-highlight is instant and never waits on the network.

### 6.3 Rendering the document

Render pages with PyMuPDF at roughly 2× (`pymupdf.Matrix(2, 2)`) for crispness, cache as `page_images/<stem>_p<N>.png`, and serve them. Overlay boxes as absolutely-positioned elements over the image in the browser.

**PyMuPDF page indices are 0-based; ADE `grounding.page` is 1-based. Use `page - 1` when rendering.** This off-by-one is the single most likely bug in the whole app: it silently produces a plausible-looking highlight on the wrong page.

Convert a normalized box to pixels against the rendered image's own dimensions:

```
left = xmin * image_width      top    = ymin * image_height
right = xmax * image_width     bottom = ymax * image_height
```

After implementing highlighting, **visually verify at least one highlight against a real document page** before declaring it working — confirm the highlighted region actually contains the value shown in the right panel.

## 7. Field flattening

Walk the **schema** (not the extraction) so that fields absent from the extraction still appear, and so panel order is schema order.

- Nested object → dotted path: `shipper.name`, `port_of_loading.city`
- Array of objects → indexed path per element present in the extraction: `containers[0].container_number`, `freight_charges[2].amount`
- Array elements are enumerated from the extracted data, since the count is data-dependent. If ADE returned three containers, show three groups of container leaves.
- Only **leaf** scalars get an override input. Container objects and arrays are structural.
- Display label: the schema's `description` is often long — use the last path segment humanized (`container_number` → "Container number") as the label, with the full dotted path shown smaller beside or beneath it, and the schema `description` available on hover.

## 8. UI

Three regions: fixed top bar, split main panel, fixed bottom bar. The main panel is the only scrolling area.

### 8.1 Top panel

- **Folder** select — populated by scanning `input_folders/` for subdirectories that contain a `documents/` folder. Also accept a typed absolute path, since the brief's example is a full path and browsers cannot pick real directory paths.
- **Schema** select — populated from `schemas/*.json`.
- **Parse+Extract** button — kicks off the run described in §5.
- **Force re-run** checkbox — bypasses skip logic.
- **Two progress bars** — "Parsed *n*/*total*" and "Extracted *n*/*total*", where total is the document count in `documents/`. Frontend polls `GET /api/progress` about once a second. Skipped files count as done.
- A compact failure list if any document errored.

### 8.2 Main panel — left: document

- Rendered page image with highlight overlay.
- Page navigation (prev/next plus a page indicator) for multi-page documents.
- Selecting a field **auto-jumps to the page of its first region** and highlights every region for that field on that page. If the field spans pages, indicate that other pages also contain regions.
- Highlight theme picker with the three variants in §9.

### 8.3 Main panel — right: fields

- Every leaf field in schema order: label, full path, the ADE-extracted value, and an override input.
- Clicking a field row selects it and drives the left-hand highlight.
- The override input starts empty with the ADE value as placeholder — a field is only an override once the reviewer actually types something. An explicitly cleared field (reviewer blanks a value that ADE populated) counts as an override of type `cleared`, so distinguish "never touched" from "deliberately emptied" in the frontend state.
- The selected row must be visibly distinct and must auto-scroll into view during keyboard navigation.

### 8.4 Bottom panel

- **Submit Final for this File** — writes `HIL_results/<stem>.hil.json` (§10.1).
- **Submit Batch** — writes HIL JSON for every document in the folder using current state, then the batch report (§10.2).
- File position indicator ("Document 2 of 3") and prev/next document controls.

## 9. Visual design

Minimalist, high-contrast, built for scanning. LandingAI brand tokens (these are now inlined at the top of `static/app.css`):

```
--forest:       #03221D     --volt:    #DBFF9B     --surface:   #F6F6EF
--forest-mid:   #43574C     --ice:     #D7CAFF     --surface-2: #EDEEE8
--forest-light: #C7DCCD     --sky:     #ABC2EB     --border:    #E0E2DA
--text:         #0A0A08     --mist:    #E7E7D9     --muted:     #4A5450
--radius: 10px   --radius-lg: 16px
```

Fonts: `Urbanist` for headings, `Inter` for body/UI, `SF Mono`/`Fira Code` for values and paths. Monospace for extracted values makes character-level mismatches (`0`/`O`, `1`/`l`) far easier to catch — use it for both the ADE value and the override input.

### Three highlight themes

Vary **both** color and formatting so the choice suits different eyes and different document backgrounds:

1. **Volt fill** — `#DBFF9B` at ~35% alpha with a 1.5px `#43574C` border. Highest contrast on white scans.
2. **Ice fill** — `#D7CAFF` at ~40% alpha with a 1.5px `#4A3882` border. Softer, better on dense or noisy pages.
3. **Outline only** — no fill, 2px solid `#43574C` border. For reviewers who find any fill obscures the underlying text.

Persist the choice in `localStorage`.

## 10. Output

### 10.1 Per-file final output

`HIL_results/<stem>.hil.json`:

```json
{
  "document": "demo_bill_of_lading_1.pdf",
  "schema": "bill-of-lading-schema.json",
  "reviewed_at": "2026-07-29T14:03:11Z",
  "opened_by_reviewer": true,
  "parse_job_id": "...",
  "extract_job_id": "...",
  "doc_id": "...",
  "final": { "...": "schema-shaped object of final values" },
  "override_count": 2,
  "overrides": [
    {
      "path": "shipper.name",
      "ade_value": "ACME CORP",
      "final_value": "ACME Corporation",
      "error_class": "wrong_value"
    }
  ],
  "fields": [
    {
      "path": "bill_of_lading_number",
      "ade_value": "BL-99213",
      "final_value": "BL-99213",
      "is_override": false,
      "page": 1,
      "regions": [{"page": 1, "xmin": 0.62, "ymin": 0.08, "xmax": 0.81, "ymax": 0.11}]
    }
  ]
}
```

`final` is schema-shaped and directly consumable downstream. `fields` is the flat audit trail. `is_override` and the `overrides` list both make human corrections unmistakable, satisfying the brief's requirement that overrides be clearly marked.

### 10.2 Batch report

Written to `HIL_results/` on Submit Batch, as both `batch_report.json` and `batch_report.csv`.

Contents:
- **Run summary** — folder, schema, timestamp, document count, how many were opened by the reviewer vs never opened, total fields, total overrides, overall override rate.
- **Per-field rows** — field path, times present, times overridden, override rate, and a count breakdown by error class. This is the diagnostic that shows which schema fields ADE struggles with.
- **Per-override rows** — document, path, ADE value, final value, error class. Full before/after detail.

Error classification, applied automatically:

| Class | Condition |
|---|---|
| `missing_filled` | ADE value null or empty, reviewer supplied a value |
| `cleared` | ADE had a value, reviewer deliberately emptied it |
| `format_only` | Values equal after normalization — trim, collapse whitespace, casefold, strip punctuation and currency symbols, parse equivalent dates |
| `wrong_value` | Differs beyond normalization |

`format_only` matters: it separates genuine extraction errors from cosmetic ones, so the report does not overstate ADE's error rate. Implement normalization conservatively — when in doubt, classify as `wrong_value` rather than explaining away a real miss.

Files never opened by the reviewer still get a `.hil.json` with `opened_by_reviewer: false` and zero overrides, and are counted separately in the summary so a partially finished batch is never mistaken for a fully reviewed one.

## 11. Backend routes

| Route | Purpose |
|---|---|
| `GET /` | serve `static/index.html` |
| `GET /api/folders` | input folders available |
| `GET /api/schemas` | schemas available |
| `POST /api/run` | `{folder, schema, force}` → start background parse+extract |
| `GET /api/progress` | `{total, parsed, extracted, skipped, failures[]}` |
| `GET /api/files` | documents in folder + per-file review status |
| `GET /api/doc` | flattened fields, values, path→regions map, page count |
| `GET /api/page-image` | rendered page PNG |
| `POST /api/submit-file` | write one `.hil.json` |
| `POST /api/submit-batch` | write all `.hil.json` + batch report |

Run state lives in a module-level dict in the backend process. Single-user local app — no database, no auth, no session handling.

## 12. Keyboard

Rapid review depends on never reaching for the mouse.

| Key | Action |
|---|---|
| `↑` / `↓` | previous / next field (highlight follows immediately) |
| `Enter` | focus the selected field's override input |
| `Esc` | leave the input, return focus to the field list |
| `Tab` | next field's input (native order must follow visual order) |
| `[` / `]` | previous / next document |
| `PageUp` / `PageDown` | previous / next document page |
| `Cmd/Ctrl+S` | Submit Final for this File |

Arrow keys must not scroll the page while the field list has focus.

## 13. Out of scope

No auth or multi-user support. No editing the schema in-app. No adding or removing array rows. No re-extracting a single field. No cloud deployment — this runs locally against local folders.

## 14. Acceptance checklist

1. Selecting `input_folders/bill_of_lading` + `bill-of-lading-schema.json` and pressing Parse+Extract processes all three demo PDFs, both progress bars reach 3/3, and `parse_results/`, `extract_results/`, and `page_images/` populate.
2. Pressing Parse+Extract again completes near-instantly with all three skipped; **Force re-run** reprocesses them.
3. Every leaf in the schema appears in the right panel in schema order, including nested paths (`shipper.name`) and indexed array paths (`containers[0].container_number`).
4. Clicking a field highlights the correct line or table cell on the correct page — **visually confirmed against the rendered page**, not just asserted.
5. `↑`/`↓` move the selection, the highlight tracks it, and the selected row scrolls into view.
6. All three highlight themes render and the choice survives a page reload.
7. Overriding two fields and pressing Submit Final writes `HIL_results/<stem>.hil.json` with `override_count: 2`, correct `final` values, and correct `error_class` on each override.
8. Submit Batch writes a `.hil.json` for all three documents plus `batch_report.json` and `batch_report.csv`, with untouched files marked `opened_by_reviewer: false`.
9. A field whose `extraction_metadata.ranges` is null is still listed and still editable; clicking it simply produces no highlight.
10. `grep -rn "client\.parse(\|client\.extract(\|dpt-2" *.py` returns nothing — the app is v2-only.
