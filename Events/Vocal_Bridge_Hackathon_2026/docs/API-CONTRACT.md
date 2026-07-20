# DPT-3 v2 API contract — VERIFIED against live API (2026-07-11)

Probed with the sample policy (`sample-travel-policy.pdf`, 23 pages) via
`api.ade.landing.ai`. This is ground truth, not docs paraphrase. Full sample responses
cached in the session scratchpad (`probe-out/parse-full.json`, `extract-full.json`).

## Parse v2
`POST https://api.ade.landing.ai/v2/parse` · `Authorization: Bearer <VISION_AGENT_API_KEY>`
· `multipart/form-data`: `document` (file), `model=dpt-3-pro-latest`, `options` (JSON, optional,
e.g. `{"pages":[0,1]}`).

Response top-level keys: **`markdown`, `metadata`, `structure`, `grounding`**.

- `metadata`: `{ job_id, model_version, page_count, markdown_chars, failed_pages[], duration_ms, billing }`
- `structure`: `{ type:"document", children:[ page ] }`
  - **page**: `{ type:"page", page:0, span:[start,end], width:1700, height:2200, dpi:200, status:"ok", children:[block] }`
  - **block**: `{ type:"text"|"table"|"figure"|..., id:"2", span:[start,end], children?:[cell] }`
  - **table_cell**: `{ type:"table_cell", id, span:[start,end], row, col, colspan, rowspan }`
- `grounding`: parallel `{ type:"document", children:[ page ] }` — same page/block ids as `structure`
  - **block**: `{ type, id, span:[start,end], box:[l,t,r,b], parts:[ { span:[start,end], box:[l,t,r,b] } ] }`
  - **`parts` = the per-line boxes.** Each part is one visual line: its own `span` slice of the
    markdown + its own pixel `box`.

**`box` = `[left, top, right, bottom]` in PIXELS at the page's `dpi`, top-left origin.**
Normalize resolution-independently: `l/width, t/height, r/width, b/height` → 0..1 fractions →
CSS %. (Do NOT normalize by the rendered PNG size; use the page node's width/height.)

**`span` = `[start, end)` code-point offsets into the top-level `markdown`.** Page spans nest
block spans nest part spans. `Array.from(markdown)` before slicing — code-point offsets.

## Extract v2
`POST https://api.ade.landing.ai/v2/extract` · same auth · `multipart/form-data`:
`markdown` (file, text/markdown), `schema` (JSON string). `model` optional.

Response top-level keys: **`extraction`, `extraction_metadata`, `markdown`, `metadata`**.

- `extraction`: the values object matching the schema.
- `extraction_metadata.<field>`: **`{ spans:[[start,end], ...], value }`** — one entry per leaf
  (arrays/objects recurse; each atomic leaf carries its own spans).
- **VERIFIED: Extract's returned `markdown` === the `markdown` we sent (Parse's markdown), byte
  for byte.** So Extract `spans` and Parse `span`/`parts` index the *same* code-point space.

## The span bridge (verified)
```
field.spans (Extract)  ∩  part.span (Parse grounding)  →  part.box  →  normalized line rect
```
Verified: `plan_name.spans = [[0,41]]` → `markdown.slice(0,41)` = "World Travel Holdings
LeisureCare Classic"; the Parse part whose span covers [0,41] carries the pixel box. One lookup,
first-party grounding — this retires v1's Claude-invented `chunk_ids`.

## Notes for the adapter
- Some blocks have no `parts` (e.g. figures) — fall back to the block `box`.
- A field span may cross multiple parts/blocks → return all overlapping line boxes (multi-line
  highlight), grouped by page.
- `metadata.billing.total_credits` present — real cost per parse; cache fixtures in dev.
