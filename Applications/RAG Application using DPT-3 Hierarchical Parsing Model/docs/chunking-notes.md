# Chunking strategy — design notes

Why this app indexes the way it does, and what the RAG literature says about the
alternatives. Condensed from a multi-source review (sources at the bottom).

## TL;DR

- **Element-based chunking is the right *default* retrieval-and-context unit.** One
  chunk per parsed element (paragraph, whole table) is cheap, robust, and—because it
  keeps a unit coherent—wins especially for tables.
- **A table is the exception:** a whole table embeds as a blurry average of all its
  cells, so we split it into **one header-aware sentence per row** (cells → row sentence)
  and merge back to the table for context. This is the big, measurable win in this corpus
  (a specific-fact query went from rank ~5 to rank 1).
- **Line-level structure's clearest value is *grounding*, not retrieval.** A visual line
  is a typographic artifact (sentences span lines; a line is often a fragment), so it's a
  poor *embedding* unit but an excellent *highlight* unit. We use DPT-3's per-line boxes
  to highlight the exact line/cell — something a plain-text extractor can't do.
- **Retrieval granularity ≠ grounding granularity.** Retrieve coherent units (element,
  sentence); ground to precise spans (line, cell). DPT-3 gives both; don't conflate them.

## The landscape (what the evidence supports)

| Strategy | Verdict |
|---|---|
| Fixed-size + overlap | Strong, cheap baseline; hard to beat decisively. |
| Recursive / character | Small, consistent edge; common default. |
| Sentence / semantic | Real but usually single-digit gains; corpus-dependent. |
| Sentence-window / small-to-big / auto-merging | Embed small, return the parent. Raises retrieval **precision**, but precision↑ does **not** reliably raise answer quality — so feed the LLM the merged parent. |
| Proposition-based | Coherent factoids can help precision; "beats passages" is **contested**; adds cost. |
| Late chunking | Embeds the whole doc then pools per-chunk to keep neighbor context; evidence is **vendor-origin** (suggestive, not settled). |
| Layout / structure-aware (element) | Cheap; **clearly helps tables** ("coherence beats chunk count"). This is our default. |

**No method is universally best.** Gains are usually small and corpus-specific;
structure-awareness matters most for tables and layout.

## Element-based vs. line-window (the option we evaluated for prose)

"Line-window" = use DPT-3's visual-line boundaries as units, embed each line with a small
window of neighbor lines, retrieve the small unit, merge back to the parent element.

| Axis | Element-based | Line-window |
|---|---|---|
| Recall / precision | Good recall; a fact in a long element can be diluted | Higher precision *if* the window is coherent; little gain on short paragraphs |
| Embedding behavior | Long elements dilute & can truncate (MiniLM cuts ~256 tok) | Smaller inputs dodge truncation/dilution — the main upside |
| Answer quality | Strong (full context) | Not automatically better; must merge parent back (→ ≈ element for the LLM) |
| Grounding | Coarse (whole element) | Precise (exact line) — where line-level genuinely shines |
| Index / compute / storage | Smallest (1 vec/element) | Larger (several vecs/element) |
| Latency | Lowest | Slightly higher (+merge) |
| Robustness | Simple | Fragile boundaries — a line is typographic, not semantic |

**Key nuance:** windowing repairs the "line is a fragment" problem — but once it does, a
line-window is essentially a **sentence-window**. The coherent small unit for prose is the
*sentence*; the natural unit for *grounding* is the *line*. No public benchmark directly
tests visual-line chunking, so line-window for retrieval is partly extrapolation.

## What this app does (and when to revisit)

- **Tables → row/cell units** (done): the well-supported structure-aware win.
- **Prose → element-level retrieval** (default): paragraphs here are short/single-topic
  and retrieve fine. Consider **sentence- or line-window only for long/multi-topic
  elements**, where dilution + the 256-token truncation actually bite.
- **Grounding → line/cell** via DPT-3 boxes: the verifiability showcase, on the firmest
  evidence.

## Sources
- Chroma, *Evaluating Chunking* — research.trychroma.com/evaluating-chunking
- ARAGOG eval — arxiv.org/html/2404.01037v1 *(small preprint, GPT-3.5 judge)*
- Late chunking — arxiv.org/abs/2409.04701 · jina.ai/news/late-chunking-in-long-context-embedding-models *(vendor-origin)*
- Dense X / propositions — arxiv.org/abs/2312.06648 *(contested)*
- Chunking benchmarks — arxiv.org/abs/2410.13070
- LlamaIndex auto-merging / sentence-window; Pinecone chunking strategies; Unstructured chunking best-practices; AWS layout-aware RAG; Voyage context-3
- MiniLM 256-token truncation — huggingface.co/sentence-transformers/all-MiniLM-L6-v2/discussions/54
