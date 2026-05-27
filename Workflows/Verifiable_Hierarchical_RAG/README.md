# Verifiable, Hierarchical RAG on Medical Literature

A Streamlit demo that turns 8 medical journal PDFs about the common cold and vitamin C into a verifiable Q&A app. Every answer is grounded in a verbatim quote that gets resolved back to the **exact line or table cell** on the source page — not the whole paragraph or table — using DPT-3's hierarchical structure tree and line-level grounding map.

## What this shows

The point of DPT-3's new Parse API is *progressive disclosure*: one response gives you three independently useful representations of a document.

- **`markdown`** — clean CommonMark for your LLM context (no anchor tags or chunk IDs in the body)
- **`structure`** — a logical tree (Document → Page → element → table cells / visual lines), each node with a half-open `span: [start, end)` into the markdown
- **`grounding`** — a flat map keyed by element ID, with each entry exposing both the element-level `box` (what v1-style chunk grounding would have given) and a `parts` array with one bounding box per visual line for text

This demo wires those three together into a single workflow:

1. Ask a medical question (sample chips or freeform).
2. ChromaDB retrieves the most relevant elements across the corpus (filtering out marginalia like page headers).
3. Claude (`claude-sonnet-4-6`) answers using tool-forced JSON output, and is *required* to include a verbatim quote.
4. The app finds that quote's span in the source markdown.
5. `get_grounding(spans, parse_response)` walks the structure tree to find every element overlapping the quote, then returns both element-level and precise (line/cell) boxes.
6. The page renders with a dual overlay: gray outline for the parent element (the v1 view), yellow fill for the precise lines or cell (the v2 win).

For a quote inside a table cell, the win is dramatic: highlighting the whole 49-cell table vs. a single cell yields ~**32× more precise** highlights. For prose, single-line-of-paragraph wins are ~3–8×.

## Quick start

### 1. Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Python 3.10+ recommended.

### 2. Configure

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

```
VISION_AGENT_API_KEY=pat_your_key_here   # https://va.landing.ai/settings/api-key
ANTHROPIC_API_KEY=sk-ant-your_key_here   # https://console.anthropic.com/settings/keys
```

### 3. Add documents

Drop PDFs in `input/`. This demo ships with 8 cold/vitamin-C papers from the public literature. Any PDFs work.

### 4. Parse + cache

```bash
python ingest.py
```

This:
- Sends each PDF to `https://api.va.staging.landing.ai/v2/ade/parse` (the DPT-3 endpoint)
- Caches the full JSON response (markdown + structure + grounding + metadata) to `parsed/<doc>.json`
- Pre-rasterizes each page to PNG at 144 dpi in `pages/<doc>/page_<n>.png` for fast Streamlit rendering
- Runs 4 PDFs in parallel; idempotent (skips work for any doc already cached)

Total cost for the 8-doc sample corpus: ~170 credits (a one-time spend; the cache is durable).

### 5. Build the retrieval index

```bash
python build_index.py
```

Walks every cached parse and emits one chunk per top-level element (text, table, figure, marginalia, logo, card, scan_code, attestation). Tables stay whole — their cells remain queryable via grounding, not as separate chunks. Embeds with ChromaDB's default Sentence Transformers (`all-MiniLM-L6-v2`), persists to `chroma/`.

### 6. Run the app

```bash
streamlit run app.py
```

Open the browser tab Streamlit shows you. Try a sample chip — `Table 1 — general community RR` is the headline showpiece for cell-level grounding.

## Architecture

```
input/                      ← your PDFs
   ↓ ingest.py (parallel)
parsed/<doc>.json           ← cached DPT-3 parse responses
   ↓ build_index.py
chroma/                     ← embedded chunks, persistent
   ↓ app.py
   ├─ ChromaDB retrieval (filters marginalia)
   ├─ Claude with tool-forced JSON ({answer, exact_quote, source_doc, element_id})
   ├─ parse_helpers.find_quote_span  → spans into source markdown
   ├─ parse_helpers.get_grounding    → element-level + precise boxes
   ├─ parse_helpers.cluster_matches  → de-dup nested matches (e.g. table + cell)
   └─ parse_helpers.render_dual_overlay → gray chunk box + yellow precise boxes
```

## File structure

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI: hero, sample chips, question input, dual overlay, HITL log |
| `ingest.py` | Parallel parse + cache + pre-rasterize |
| `build_index.py` | Walk cached parses, chunk, embed, store in ChromaDB |
| `query_engine.py` | Retrieval + Claude tool-forced JSON Q&A |
| `parse_helpers.py` | Spans, grounding, dual overlay, precision metric — the core RAG-with-grounding library |
| `.env.example` | API key template |
| `.streamlit/config.toml` | Brand theme (Forest primary) |

## Sample queries to try

| Query | What it demonstrates | Expected win |
|---|---|---|
| `Did the studies find a benefit for marathon runners taking vitamin C?` | Line-level grounding in a dense paragraph | ~3–5× |
| `In the Vitamin C meta-analyses Table 1, what was the relative risk for incidence of colds in the general community studies?` | Cell-level grounding inside a 49-cell table | **~32×** |
| `What is the main finding regarding high-dose vitamin C therapy in children?` | Line-level grounding in a discussion paragraph | ~5–8× |
| `Is echinacea effective for preventing the common cold?` | Cross-document retrieval | qualitative |

## Tech notes

### The DPT-3 response shape (v3 design / v2 endpoint on staging)

```json
{
  "structure": { "type": "document", "children": [ /* pages → elements */ ] },
  "grounding": { "<id>": { "page": 0, "span": [s,e], "box": [l,t,r,b], "parts": [...] } },
  "markdown": "...",
  "metadata": { "run_id": "...", "version": "...", "credit_usage": 4.8, /* ... */ }
}
```

- **Spans are half-open** `[start, end)` Unicode code-point offsets into the root markdown.
- **Text elements** expose one `parts` entry per visual line. **Tables and visuals** (figure/logo/card/scan_code/attestation) have `parts: []` — use the element-level `box`.
- **Table cells** (`td`/`th`) live as children of their parent table; each has its own grounding entry, so you get cell-level boxes even though the table itself doesn't have `parts`.
- **Page break marker** in the markdown: `<!-- page -->` between pages, absent for single-page documents.
- **HTTP**: 200 OK, 206 partial (some pages failed — surfaced in `metadata.failed_pages` and as `status: "failed"` page nodes), 422 validation, 429 rate limit.

### Spec-vs-reality quirk

The published spec describes visual elements (figures, logos, cards, scan codes, attestations) as rendering in `> [!FIGURE]` GitHub admonition blocks. The actual output uses **markdown image syntax** instead: `![alt]\n<any text inside the visual>`. Slice the markdown by element span rather than parse for admonition syntax — `parse_helpers.iter_chunks` does this correctly.

### Endpoint

Currently `https://api.va.staging.landing.ai/v2/ade/parse`. Will move to the production `/v3/ade/parse` path once that ships publicly. The response shape we depend on is the same.

### Auth

`Authorization: Basic <pat_xxx>` — the raw personal access token, no base64 wrapping. Staging keys are separate from production. The app uses `python-dotenv` with `override=True` so `.env` wins over any pre-existing shell `VISION_AGENT_API_KEY` (a common gotcha when developers have a production key in their shell profile).

### Known issues

- **Transient 502 from upstream `parse3-service`** for some pages on some documents. The app handles `206 Partial Content` cleanly: failed page nodes get a `status: "failed"` + `reason`, their children list is empty, and the rest of the doc is usable. Recovery: delete `parsed/<doc>.json` and re-run `ingest.py` — 502s are not sticky.
- The Anthropic SDK strictly validates the model ID. If you pin a model that doesn't exist for your workspace, you'll get a 404. Default is `claude-sonnet-4-6`; override with `ANTHROPIC_MODEL` in `.env`.

## Verification log

Every Accept / Reject click in the UI appends one line of JSON to `verifications.jsonl`:

```json
{"ts":"2026-05-26T17:42:11","question":"...","quote":"RR = 0.98 (0.95, 1.00)","source_doc":"Vitamin_C...","source_element_id":"47","judgment":"accept"}
```

Use this to build a labeled set of "grounded answers that were right" vs "grounded answers that were wrong" for model evaluation.

## License

This sample is published under the same license as [landing-ai/ade-sample-projects](https://github.com/landing-ai/ade-sample-projects).
