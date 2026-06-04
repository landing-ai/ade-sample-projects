"""DPT-3 demo — single-purpose verifiable Q&A.

Run:
    cp .env.example .env   # fill in keys
    source venv/bin/activate
    streamlit run app.py
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

import parse_helpers as ph

load_dotenv(override=True)

VERIFICATIONS_LOG = Path("verifications.jsonl")
PARSED_DIR = Path("parsed")
PAGES_DIR = Path("pages")
LOGO_PATH = Path("static/landing_ai_logo.png")


def _logo_data_url() -> str:
    """Read the LandingAI horizontal wordmark and return it as a data: URL
    suitable for use in CSS background-image or HTML img src.
    Picks MIME from the file extension."""
    if not LOGO_PATH.exists():
        return ""
    import base64
    mime = {
        ".png": "image/png",
        ".svg": "image/svg+xml",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }.get(LOGO_PATH.suffix.lower(), "application/octet-stream")
    raw = LOGO_PATH.read_bytes()
    return f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")


LANDINGAI_LOGO_URL = _logo_data_url()

# Brand palette — LandingAI 2026 brand book
COLOR_FOREST = "#03221D"
COLOR_FOREST_MID = "#43574C"
COLOR_FOREST_LIGHT = "#C7DCCD"
COLOR_VOLT = "#DBFF9B"
COLOR_SURFACE = "#F6F6EF"
COLOR_SURFACE_2 = "#EDEEE8"
COLOR_BORDER = "#E0E2DA"
COLOR_MUTED = "#525252"
COLOR_HEADLINE = "#1E232C"
COLOR_SUBTLE = "#7A8680"

st.set_page_config(
    layout="wide",
    page_title="Verifiable, Hierarchical RAG · LandingAI",
    initial_sidebar_state="collapsed",
)


# ---- brand CSS ----

_FONT_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Instrument+Serif:ital@0;1'
    '&family=Urbanist:wght@500;600;700;800'
    '&family=Inter:wght@300;400;500;600;700'
    '&display=swap" rel="stylesheet">'
)

_CSS_TEMPLATE = """\
:root {
  --forest: __FOREST__;
  --forest-mid: __FOREST_MID__;
  --forest-light: __FOREST_LIGHT__;
  --volt: __VOLT__;
  --surface: __SURFACE__;
  --surface-2: __SURFACE_2__;
  --border: __BORDER__;
  --muted: __MUTED__;
  --headline: __HEADLINE__;
  --subtle: __SUBTLE__;
}
html, body, [class*="css"], .stApp {
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--muted);
  background: #fff;
}
.stApp p, .stMarkdown p { color: var(--muted); }
.block-container {
  padding-top: 2.5rem;
  padding-bottom: 4rem;
  max-width: 1280px;
}
.display {
  font-family: 'Instrument Serif', Georgia, serif;
  font-weight: 400;
  line-height: 1.05;
  color: var(--headline);
  letter-spacing: -0.01em;
}
.display em { font-style: italic; }
.hero-card {
  background: var(--forest-light);
  border-radius: 16px;
  padding: 36px 40px 32px 40px;
  margin: 0 0 28px 0;
  position: relative;   /* anchor for the brand wordmark in the corner */
}
/* LandingAI wordmark in the hero card's top-right — more noticeable than the
   page corner, and sits on the sage panel where the black mark reads cleanly. */
.hero-card::after {
  content: "";
  position: absolute;
  top: 30px;
  right: 36px;
  width: 150px;
  height: 30px;
  background-image: url("__LOGO_URL__");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: right center;
  pointer-events: none;
}
.hero-card .eyebrow {
  background: rgba(3, 34, 29, 0.08);
  color: var(--forest);
}
.hero-card .hero-sub {
  color: var(--forest-mid);
  margin-bottom: 0;
}
.display-hero {
  font-size: clamp(36px, 4vw, 56px);
  margin-bottom: 12px;
}
.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-family: 'Urbanist', system-ui, sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--forest-mid);
  background: rgba(67, 87, 76, 0.08);
  padding: 4px 10px;
  border-radius: 4px;
  margin-bottom: 16px;
}
h1, h2, h3, h4 {
  font-family: 'Urbanist', system-ui, sans-serif;
  letter-spacing: -0.005em;
  color: var(--headline);
}
h3 { font-weight: 700; font-size: 16px; margin-bottom: 4px; }
.hero-sub {
  font-size: 15.5px;
  color: var(--muted);
  max-width: 720px;
  line-height: 1.7;
  margin-bottom: 24px;
}
.label {
  font-family: 'Urbanist', sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--subtle);
  margin-bottom: 8px;
}
.quote {
  border-left: 3px solid var(--forest-light);
  background: var(--surface);
  padding: 12px 18px;
  margin: 14px 0;
  font-style: italic;
  color: var(--muted);
  font-size: 14px;
  line-height: 1.65;
  border-radius: 0 8px 8px 0;
}
/* Structural type badge — sits under the answer paragraph */
.struct-badge {
  display: inline-block;
  font-family: 'Urbanist', sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--forest);
  background: rgba(67, 87, 76, 0.10);
  padding: 4px 10px;
  border-radius: 4px;
  margin-top: 4px;
}
/* Source-markdown pane (center column) */
.md-pane {
  font-family: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
  font-size: 12.5px;
  line-height: 1.7;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 18px;
  white-space: pre-wrap;
  word-break: break-word;
  color: var(--headline);
  max-height: 620px;
  overflow-y: auto;
}
.md-pane mark {
  border-radius: 2px;
  padding: 0 2px;
}
/* Granularity zoom radio — slim horizontal pill row */
.zoom-row [role="radiogroup"] {
  flex-direction: row !important;
  gap: 12px;
}
.zoom-row [role="radiogroup"] label {
  padding: 4px 8px;
  border-bottom: none;
}
.zoom-row [role="radiogroup"] label > div:nth-child(2) p {
  text-transform: none !important;
  letter-spacing: 0 !important;
  font-size: 12px !important;
  font-weight: 500 !important;
}
/* Radio list (Sources) — tighter spacing, brand-aligned label/caption styles */
[role="radiogroup"] label {
  padding: 8px 4px;
  border-bottom: 1px solid var(--border);
}
[role="radiogroup"] label:last-child { border-bottom: none; }
[role="radiogroup"] label > div:nth-child(2) p {
  font-family: 'Urbanist', sans-serif;
  font-size: 13px !important;
  font-weight: 600;
  color: var(--headline) !important;
  margin-bottom: 2px;
}
[role="radiogroup"] label small {
  font-family: 'Inter', sans-serif;
  font-size: 12.5px !important;
  color: var(--muted) !important;
  line-height: 1.5;
}
.stButton > button[kind="secondary"] {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--headline);
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 500;
  padding: 6px 14px;
  border-radius: 999px;
  transition: all 0.15s;
}
.stButton > button[kind="secondary"]:hover {
  background: var(--forest-light);
  border-color: var(--forest-mid);
  color: var(--forest);
}
.stButton > button[kind="primary"] {
  background: var(--forest);
  border: 1px solid var(--forest);
  color: #fff;
  font-family: 'Urbanist', sans-serif;
  font-weight: 600;
  letter-spacing: 0.02em;
  border-radius: 8px;
  padding: 8px 22px;
}
.stButton > button[kind="primary"]:hover {
  background: var(--forest-mid);
  border-color: var(--forest-mid);
}
.stTextInput > div > div > input,
.stSelectbox > div > div {
  font-family: 'Inter', sans-serif;
  border-radius: 8px !important;
}
[data-testid="stMetric"] {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 18px;
}
[data-testid="stMetricLabel"] {
  font-family: 'Urbanist', sans-serif;
  font-size: 10px !important;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--subtle) !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Instrument Serif', Georgia, serif !important;
  color: var(--headline) !important;
  font-weight: 400 !important;
}
.legend {
  display: flex; gap: 16px; align-items: center;
  font-size: 12px; color: var(--subtle); margin-top: 6px;
}
.legend-swatch {
  display: inline-block; width: 16px; height: 10px; border-radius: 3px;
  vertical-align: middle; margin-right: 6px;
}
footer { visibility: hidden; }
.stDeployButton { display: none; }

/* The brand wordmark now lives in the hero card (.hero-card::after). Hide
   Streamlit's top-right toolbar (Deploy + ⋮ menu) so the page corner stays clean. */
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }

/* ---- rebuilt answer / proof layout ---- */
.answer-card {
  font-size: 16px; line-height: 1.7; color: var(--headline);
  background: var(--surface-2); border: 1px solid var(--border);
  border-left: 4px solid var(--forest); border-radius: 12px;
  padding: 15px 20px; max-width: 1000px; margin: 2px 0 12px 0;
}
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0 2px 0; }
.chip {
  font-family: 'Urbanist', system-ui, sans-serif; font-size: 12.5px;
  color: var(--forest); background: var(--forest-light);
  border: 1px solid var(--border); border-radius: 999px; padding: 4px 12px;
}
.chip b { font-weight: 700; }
.quote-callout {
  font-family: Georgia, 'Times New Roman', serif; font-style: italic;
  font-size: 15px; line-height: 1.6; color: var(--headline);
  background: #fffdf0; border: 1px solid #ece6c2; border-radius: 10px;
  padding: 12px 18px; max-width: 1000px; margin: 12px 0;
}
.quote-src {
  display: block; font-style: normal; font-family: 'Urbanist', sans-serif;
  font-size: 11px; letter-spacing: .05em; text-transform: uppercase;
  color: var(--muted); margin-top: 6px;
}
.sublabel {
  font-family: 'Urbanist', sans-serif; font-size: 11px; font-weight: 700;
  letter-spacing: .12em; text-transform: uppercase; color: var(--muted);
  margin-bottom: 6px;
}
"""


def inject_brand_css() -> None:
    css = (
        _CSS_TEMPLATE
        .replace("__FOREST__", COLOR_FOREST)
        .replace("__FOREST_MID__", COLOR_FOREST_MID)
        .replace("__FOREST_LIGHT__", COLOR_FOREST_LIGHT)
        .replace("__VOLT__", COLOR_VOLT)
        .replace("__SURFACE__", COLOR_SURFACE)
        .replace("__SURFACE_2__", COLOR_SURFACE_2)
        .replace("__BORDER__", COLOR_BORDER)
        .replace("__MUTED__", COLOR_MUTED)
        .replace("__HEADLINE__", COLOR_HEADLINE)
        .replace("__SUBTLE__", COLOR_SUBTLE)
        .replace("__LOGO_URL__", LANDINGAI_LOGO_URL)
    )
    st.html(f"{_FONT_LINKS}<style>{css}</style>")


# ---- cached loaders ----

@st.cache_data
def list_docs() -> list[str]:
    return sorted(p.stem for p in PARSED_DIR.glob("*.json"))


@st.cache_data
def load_parse(doc_id: str) -> dict:
    with open(PARSED_DIR / f"{doc_id}.json") as f:
        return json.load(f)


@st.cache_data
def load_page_image(doc_id: str, page: int) -> Image.Image:
    return Image.open(PAGES_DIR / doc_id / f"page_{page}.png")


def short_doc_name(doc_id: str) -> str:
    s = doc_id.replace("_", " ")
    return s if len(s) < 60 else s[:57] + "…"


# ---- HITL log ----

def log_verification(question: str, quote: str | None, source_doc: str | None,
                     source_element_id: str | None, judgment: str) -> None:
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "question": question,
        "quote": quote,
        "source_doc": source_doc,
        "source_element_id": source_element_id,
        "judgment": judgment,
    }
    with VERIFICATIONS_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")


# ---- sample questions ----

EXAMPLE_QUESTION = "what happens to the sinus cavity during a cold"

SAMPLE_QUERIES = [
    ("Marathon runners",
     "Did the studies find a benefit for marathon runners taking vitamin C?"),
    ("Table 1 — general community RR",
     "In the Vitamin C meta-analyses Table 1, what was the relative risk for incidence of colds during prophylaxis in the general community studies?"),
    ("Prevention vs. treatment",
     "Does vitamin C work for either preventing or shortening the common cold? Answer with evidence from both prophylaxis trials and therapeutic-onset trials."),
    ("CT scans: acute vs. recovery",
     "What do the coronal sinus CT scans look like during the acute and recovery phases of a cold?"),
    ("Echinacea",
     "Is echinacea effective for preventing the common cold?"),
]


# ---- brand palette for multi-quote rendering ----

# Each entry: ((outline RGBA), (fill RGBA), css_hex_for_html_mark)
# Index 0 = primary quote (volt yellow — the existing single-quote color).
# Subsequent indices cycle through brand-book accent colors (ice, sky, warm).
QUOTE_PALETTE = [
    ((220, 30, 30, 255),  (255, 230, 0, 90),   "#FFE600"),  # 0: volt yellow
    ((100, 50, 200, 255), (215, 202, 255, 130),"#D7CAFF"),  # 1: ice lavender
    ((30, 90, 200, 255),  (171, 194, 235, 130),"#ABC2EB"),  # 2: sky blue
    ((180, 110, 40, 255), (245, 216, 178, 140),"#F5D8B2"),  # 3: warm tint
]


def quote_color(index: int) -> tuple[tuple[int,int,int,int], tuple[int,int,int,int], str]:
    return QUOTE_PALETTE[index % len(QUOTE_PALETTE)]


# ---- structural badge helpers (Feature 3) ----

def humanize_element_type(t: str) -> str:
    """Brand-friendly humanized label for an element's structural type."""
    return {
        "text": "Body text",
        "marginalia": "Header / footer",
        "figure": "Figure",
        "table": "Table",
        "td": "Table cell",
        "th": "Header cell",
        "logo": "Logo",
        "card": "Card",
        "scan_code": "Scan code",
        "attestation": "Attestation",
    }.get(t, t.title())


def badge_for_grounding(
    matches: list[ph.GroundingMatch],
    parse: dict,
    *,
    page: int | None = None,
    fallback: str = "",
) -> str:
    """Build a structural badge for a set of grounding matches.

    Uses cluster_matches to pick the most specific element in the cluster
    (a td/th if present, else the outer element) and decorates with row/col
    for table cells when the structure node exposes them."""
    if not matches:
        return fallback
    clusters = ph.cluster_matches(matches)
    if not clusters:
        return fallback
    outer, inner = clusters[0]
    label_type = humanize_element_type(inner.element_type)
    extra = ""
    if inner.element_type in ("td", "th"):
        node = ph.find_element_node(parse, inner.element_id)
        if node and "row" in node and "col" in node:
            extra = f" · r{node['row']}c{node['col']}"
    page_part = f" · p.{inner.page if page is None else page}"
    return f"{label_type}{extra}{page_part}"


# ---- token cost helpers (Feature 5) ----

@st.cache_resource
def _tokenizer():
    """Cached tiktoken encoder. cl100k_base is a reasonable proxy for Claude
    tokenization deltas; we're only displaying ratios, not absolute billing."""
    import tiktoken
    return tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    if not text:
        return 0
    return len(_tokenizer().encode(text))


# ---- grounding for a "view" ----

def grounding_for_quote_text(
    quote_text: str, source_parse: dict
) -> tuple[list[ph.GroundingMatch] | None, list[list[int]] | None]:
    """Resolve any verbatim quote string to (matches, spans) on the source parse,
    or (None, None) on miss."""
    if not quote_text:
        return None, None
    md = source_parse["markdown"]
    spans = ph.find_quote_span(quote_text, md)
    if not spans:
        return None, None
    return ph.get_grounding(spans, source_parse), spans


def grounding_for_answer(answer, source_parse: dict):
    """Backward-compat wrapper that uses answer.exact_quote (the primary quote)."""
    return grounding_for_quote_text(answer.exact_quote, source_parse)


def grounding_for_chunk(chunk, parse: dict):
    """Treat the chunk's whole span as the query — returns its element grounding.
    Useful for showing 'where would this passage land if it were the source?'"""
    return ph.get_grounding([list(chunk.span)], parse)


def resolve_all_quotes(answer, source_parse: dict):
    """For each quote on answer.quotes (or the legacy single quote), resolve to
    (quote, matches, spans). Drops quotes that don't resolve."""
    out = []
    quotes = answer.quotes
    if not quotes and answer.exact_quote and answer.source_doc:
        # Synthesize a single-entry quote list from legacy fields
        from query_engine import Quote
        quotes = [Quote(
            text=answer.exact_quote,
            source_doc=answer.source_doc,
            source_element_id=str(answer.source_element_id or ""),
        )]
    for q in quotes:
        # Only resolve quotes whose source_doc matches the parse we have loaded.
        # For multi-doc answers each quote could come from a different doc; the
        # caller handles per-doc dispatch.
        matches, spans = grounding_for_quote_text(q.text, source_parse)
        if matches and spans:
            out.append((q, matches, spans))
    return out


# ---- main render ----

def render() -> None:
    inject_brand_css()

    # Brand wordmark is painted into the hero card's top-right corner by
    # `.hero-card::after` (see inject_brand_css); no HTML insertion needed here.

    # Hero — sage card per brand book "industry panel" pattern
    st.html(
        '<div class="hero-card">'
        '<div class="eyebrow">DPT-3 · Parse API v2</div>'
        '<h1 class="display display-hero">'
        'Verifiable, Hierarchical RAG on Scientific Literature'
        '</h1>'
        '<p class="hero-sub">'
        'Ask a question about the common cold or vitamin C. The app pulls passages '
        'from 8 research papers, has an LLM answer with a verbatim quote, then '
        'highlights the <strong style="color:var(--headline);">exact line — or table '
        'cell — on the source PDF</strong> that proves it. '
        'Verifying a claim takes one glance instead of re-reading the paragraph.'
        '</p>'
        '</div>'
    )

    # Query engine
    try:
        from query_engine import ask
    except Exception as e:
        st.error(f"Query engine unavailable: {e}")
        return

    # ---- input ----

    if "ask_input" not in st.session_state:
        st.session_state.ask_input = ""
    if "ask_run_pending" not in st.session_state:
        st.session_state.ask_run_pending = False
    if "ask_answer" not in st.session_state:
        st.session_state.ask_answer = None
        st.session_state.ask_error = None
    if "selected_view" not in st.session_state:
        # "answer" | "passage:<index>"
        st.session_state.selected_view = "answer"

    def _use_sample(q: str) -> None:
        st.session_state.ask_input = q
        st.session_state.ask_run_pending = True
        st.session_state.ask_answer = None
        st.session_state.ask_error = None
        st.session_state.selected_view = "answer"

    st.markdown('<div class="label">Try a sample</div>', unsafe_allow_html=True)
    chip_cols = st.columns(len(SAMPLE_QUERIES))
    for col, (label, full_q) in zip(chip_cols, SAMPLE_QUERIES):
        with col:
            st.button(
                label,
                key=f"chip_{label}",
                on_click=_use_sample,
                args=(full_q,),
                width="stretch",
            )

    question = st.text_input(
        "Question",
        placeholder=EXAMPLE_QUESTION,
        key="ask_input",
        label_visibility="collapsed",
    )

    col_btn, col_k = st.columns([1, 4])
    with col_btn:
        # Always enabled — empty input falls back to the placeholder example.
        run_button = st.button("Ask", type="primary", width="stretch")
    with col_k:
        k = st.slider("Retrieved passages", 2, 12, 6, key="ask_k", label_visibility="collapsed")
        st.caption(f"Retrieving top {k} passages")

    # If the user clicked Ask with an empty input, treat the placeholder as the
    # intended query so the example is one click away.
    effective_question = question.strip() or EXAMPLE_QUESTION

    should_run = run_button or st.session_state.ask_run_pending
    if should_run:
        st.session_state.ask_run_pending = False
        st.session_state.ask_answer = None
        st.session_state.ask_error = None
        st.session_state.selected_view = "answer"
        with st.spinner("Retrieving passages and asking the model…"):
            try:
                st.session_state.ask_answer = ask(effective_question, k=k)
            except Exception as e:
                st.session_state.ask_error = str(e)

    if st.session_state.ask_error:
        st.error(f"Q&A failed: {st.session_state.ask_error}")
        st.caption("Check that ANTHROPIC_API_KEY in .env is valid.")
        return

    answer = st.session_state.ask_answer
    if not answer:
        return

    # ============ Selected view ============
    # selected_view values:
    #   "answer"     → show all quotes on the answer (or the single quote)
    #   "quote:N"    → multi-quote case: show only quote N
    #   "passage:N"  → show retrieved chunk N (not an answer source)

    view = st.session_state.selected_view
    selected_chunk = None
    selected_quote_idx = None

    def _reset_view():
        st.session_state.selected_view = "answer"
        return "answer"

    if view.startswith("passage:"):
        try:
            idx = int(view.split(":", 1)[1])
            if 0 <= idx < len(answer.retrieved):
                selected_chunk = answer.retrieved[idx]
            else:
                view = _reset_view()
        except ValueError:
            view = _reset_view()
    elif view.startswith("quote:"):
        try:
            idx = int(view.split(":", 1)[1])
            if 0 <= idx < len(answer.quotes):
                selected_quote_idx = idx
            else:
                view = _reset_view()
        except ValueError:
            view = _reset_view()

    is_answer_view = (view == "answer")
    is_quote_view = view.startswith("quote:") and selected_quote_idx is not None
    is_passage_view = view.startswith("passage:") and selected_chunk is not None

    # ============ Resolve all answer quotes upfront ============
    # answer_quote_groups: parallel list of (quote, matches, spans, parse).
    # Drops quotes that don't resolve verbatim.
    answer_quote_groups: list[tuple] = []
    parse_cache: dict[str, dict] = {}
    for q in answer.quotes:
        try:
            p = parse_cache.setdefault(q.source_doc, load_parse(q.source_doc))
        except FileNotFoundError:
            continue
        m, s = grounding_for_quote_text(q.text, p)
        if m and s:
            answer_quote_groups.append((q, m, s, p))

    has_grounded_answer = len(answer_quote_groups) > 0

    # ============ What to render in the center + right panes ============
    # quote_render_set: list of (matches, spans, color_idx).
    # markdown_marks: same data shape, used by the markdown panel.
    quote_render_set: list[tuple[list[ph.GroundingMatch], list[list[int]], int]] = []
    active_parse: dict | None = None
    active_doc: str | None = None

    if is_passage_view:
        try:
            active_parse = load_parse(selected_chunk.doc_id)
            active_doc = selected_chunk.doc_id
            m = grounding_for_chunk(selected_chunk, active_parse)
            quote_render_set = [(m, [list(selected_chunk.span)], 0)]
        except FileNotFoundError:
            pass
    elif is_quote_view:
        q, m, s, p = answer_quote_groups[selected_quote_idx]
        active_parse = p
        active_doc = q.source_doc
        quote_render_set = [(m, s, selected_quote_idx)]
    elif is_answer_view and has_grounded_answer:
        # Group by source_doc; show the primary doc (the first quote's doc).
        primary_doc = answer_quote_groups[0][0].source_doc
        active_doc = primary_doc
        active_parse = parse_cache[primary_doc]
        for idx, (q, m, s, p) in enumerate(answer_quote_groups):
            if q.source_doc == primary_doc:
                quote_render_set.append((m, s, idx))

    # ============ Full-width answer header (above the 3-col split) ============
    st.divider()

    st.markdown('<div class="label">Answer</div>', unsafe_allow_html=True)
    st.markdown(
        f"<div class='answer-card'>{answer.answer}</div>",
        unsafe_allow_html=True,
    )
    if not has_grounded_answer:
        st.warning("The model declined to produce a verbatim quote.")

    if has_grounded_answer:
        # Structural badges
        badges = []
        for q, m, s, p in answer_quote_groups:
            badge = badge_for_grounding(m, p)
            if badge and badge not in badges:
                badges.append(badge)
        if badges:
            st.html("".join(f'<span class="struct-badge">{b}</span>' for b in badges))

        # Precision win + token cost — 4 metrics get full width
        primary_doc = answer_quote_groups[0][0].source_doc
        primary_parse = parse_cache[primary_doc]
        primary_matches: list[ph.GroundingMatch] = []
        primary_spans: list[list[int]] = []
        for q, m, s, p in answer_quote_groups:
            if q.source_doc == primary_doc:
                primary_matches.extend(m)
                primary_spans.extend(s)

        metric = ph.precision_metric(primary_matches, primary_parse)
        md_full = primary_parse["markdown"]
        precise_tokens = sum(count_tokens(md_full[sp[0]:sp[1]]) for sp in primary_spans)
        element_token_total = 0
        seen_elem_spans: set[tuple[int, int]] = set()
        for outer, _ in ph.cluster_matches(primary_matches):
            key = tuple(outer.span)
            if key in seen_elem_spans:
                continue
            seen_elem_spans.add(key)
            element_token_total += count_tokens(md_full[outer.span[0]:outer.span[1]])
        token_ratio = (element_token_total / precise_tokens) if precise_tokens else 0.0

        # Compact metric chips, then the verbatim proof quote
        chips = (
            '<div class="chips">'
            f'<span class="chip"><b>{metric["ratio"]:.0f}×</b> tighter highlight</span>'
            f'<span class="chip">{metric["chunk_pct"]:.1f}% &rarr; <b>{metric["precise_pct"]:.3f}%</b> of page</span>'
            f'<span class="chip"><b>{precise_tokens}</b> tokens to prove it'
            + (f' &middot; {token_ratio:.0f}&times; cheaper' if token_ratio > 1 else '')
            + '</span></div>'
        )
        st.markdown(chips, unsafe_allow_html=True)
        _pq = answer_quote_groups[0][0]
        st.markdown(
            f'<div class="quote-callout">&ldquo;{_html_escape(_pq.text.strip())}&rdquo;'
            f'<span class="quote-src">{short_doc_name(_pq.source_doc)}</span></div>',
            unsafe_allow_html=True,
        )

        # Why retrieval found this — the unit-shape contrast behind small-to-big.
        # Only shown when the answer grounds to a table (the most striking case).
        tbl = next((m for m in primary_matches if m.element_type == "table"), None)
        if tbl is not None:
            rows = ph.table_row_sentences(primary_parse, tbl.element_id)
            if rows:
                with st.expander("🔍 How the app found the right cell in this table"):
                    st.markdown(
                        "To answer a question about a table, the app first turns it into text it "
                        "can search. **How** it turns the table into text decides whether it finds "
                        "the answer:"
                    )
                    c_blob, c_rows = st.columns(2)
                    with c_blob:
                        st.markdown("**❌ The whole table as one block**")
                        st.caption(
                            "One value is buried among 100+ cells, so the table as a whole barely "
                            "looks like a match for your question."
                        )
                        st.code(md_full[tbl.span[0]:tbl.span[1]].strip(), language="markdown")
                    with c_rows:
                        st.markdown("**✅ Each row as its own sentence**")
                        st.caption(
                            "What this app does. The matching row now reads like plain language, so "
                            "it stands out as the best match — and points straight at the cell."
                        )
                        st.code("\n".join(rows), language="text")
                    st.caption(
                        "Same search both ways — only the *shape of the text* changed. That's what "
                        "let your question land on the exact cell instead of getting lost in the table."
                    )

        # Verification — gets plenty of room at full width
        st.markdown('<div class="label" style="margin-top:18px;">Verification</div>', unsafe_allow_html=True)
        hcol1, hcol2, _ = st.columns([1, 1, 8])
        with hcol1:
            if st.button("Accept", key="hitl_accept", width="stretch"):
                log_verification(answer.question, answer.exact_quote,
                                 answer.source_doc, answer.source_element_id, "accept")
                st.success("Logged.")
        with hcol2:
            if st.button("Reject", key="hitl_reject", width="stretch"):
                log_verification(answer.question, answer.exact_quote,
                                 answer.source_doc, answer.source_element_id, "reject")
                st.warning("Logged.")

    # ============ 3-column exploration row (Sources | Markdown | Image) ============
    st.divider()
    page_col, text_col, src_col = st.columns([7, 5, 4])

    with src_col:
        st.markdown('<div class="label">Sources</div>', unsafe_allow_html=True)
        st.caption("Pick a source to highlight it on the page →")

        labels: list[str] = []
        captions: list[str] = []
        view_keys: list[str] = []

        # Multi-quote case → add an "all quotes" pseudo-row + per-quote rows
        if len(answer_quote_groups) >= 2:
            labels.append(f"★  All {len(answer_quote_groups)} quotes · combined view")
            q_summary = " · ".join(short_doc_name(q.source_doc) for q, _, _, _ in answer_quote_groups[:3])
            captions.append(q_summary)
            view_keys.append("answer")
            for idx, (q, m, s, p) in enumerate(answer_quote_groups):
                badge = badge_for_grounding(m, p) or f"p.?"
                labels.append(f"★  Quote {idx + 1} of {len(answer_quote_groups)} · {short_doc_name(q.source_doc)} · {badge}")
                preview = q.text.strip().replace("\n", " ")
                captions.append(preview[:160] + ("…" if len(preview) > 160 else ""))
                view_keys.append(f"quote:{idx}")
        # Single-quote case → one ★ row, merged into the retrieved list below
        elif len(answer_quote_groups) == 1:
            q, m, s, p = answer_quote_groups[0]
            # Try to find it in the retrieved list; if it's there, attach the star
            # in-line. If not, prepend it.
            answer_in_retrieved = any(
                c.doc_id == q.source_doc and c.element_id == q.source_element_id
                for c in answer.retrieved
            )
            if not answer_in_retrieved:
                badge = badge_for_grounding(m, p) or "—"
                labels.append(f"★  Answer source · {short_doc_name(q.source_doc)} · {badge}")
                preview = q.text.strip().replace("\n", " ")
                captions.append(preview[:160] + ("…" if len(preview) > 160 else ""))
                view_keys.append("answer")

        # Retrieved chunks. Skip any chunk that's already represented as an
        # answer-source quote row above (single- OR multi-quote case).
        quote_ident_set = {
            (q.source_doc, str(q.source_element_id)) for q, _, _, _ in answer_quote_groups
        }
        for i, c in enumerate(answer.retrieved):
            chunk_ident = (c.doc_id, str(c.element_id))
            is_single_answer_src = (
                len(answer_quote_groups) == 1
                and chunk_ident in quote_ident_set
            )
            already_a_quote = (
                len(answer_quote_groups) >= 2
                and chunk_ident in quote_ident_set
            )
            if already_a_quote:
                # Already surfaced as "★ Quote N of M …"; don't duplicate.
                continue
            elem_badge = humanize_element_type(c.element_type)
            page_part = f" · p.{c.page}"
            dist_part = f" · dist {c.distance:.2f}"
            if is_single_answer_src:
                prefix = "★  Answer source · "
                view_keys.append("answer")
                preview = answer_quote_groups[0][0].text.strip().replace("\n", " ")
            else:
                prefix = f"{i + 1}.  "
                view_keys.append(f"passage:{i}")
                preview = c.text.strip().replace("\n", " ")
            labels.append(
                f"{prefix}{short_doc_name(c.doc_id)} · {elem_badge}{page_part}{dist_part}"
            )
            captions.append(preview[:160] + ("…" if len(preview) > 160 else ""))

        # No sources at all (unlikely) — skip the radio
        if not labels:
            st.info("No retrievable sources for this answer.")
        else:
            try:
                default_idx = view_keys.index(st.session_state.selected_view)
            except ValueError:
                default_idx = 0
            radio_key = f"src_radio_{hash(answer.question)}_{len(answer.retrieved)}_{len(answer.quotes)}"
            selected_label = st.radio(
                "Sources",
                labels,
                captions=captions,
                index=default_idx,
                label_visibility="collapsed",
                key=radio_key,
            )
            new_view = view_keys[labels.index(selected_label)]
            if new_view != st.session_state.selected_view:
                st.session_state.selected_view = new_view
                st.rerun()

    # ---- source markdown panel (Feature 1) ----
    with text_col:
        st.markdown('<div class="label">Source markdown</div>', unsafe_allow_html=True)
        if not active_parse or not quote_render_set:
            st.info("Source text appears here once an answer resolves.")
        else:
            st.html(render_markdown_panel_html(quote_render_set, active_parse))

    # ---- source page image — the hero (Features 2 + 4 colors) ----
    with page_col:
        st.markdown('<div class="label">Source page — the proof</div>', unsafe_allow_html=True)
        if not active_parse or not quote_render_set:
            st.info("No page to highlight yet — ask a question to see the source page here.")
            return

        # Page selector (when multiple pages have hits)
        all_match_pages = sorted({mm.page for matches, _, _ in quote_render_set for mm in matches})
        if not all_match_pages:
            st.info("No grounding for the selected view.")
            return
        if len(all_match_pages) > 1:
            page = st.selectbox(
                "Page",
                all_match_pages,
                key="ask_page",
                format_func=lambda p: f"page {p}",
                label_visibility="collapsed",
            )
        else:
            page = all_match_pages[0]

        # Granularity zoom (Feature 2)
        st.markdown('<div class="zoom-row">', unsafe_allow_html=True)
        zoom_label = st.radio(
            "Detail",
            ["Page", "Element", "Lines / cells"],
            index=2,
            horizontal=True,
            label_visibility="collapsed",
            key=f"zoom_level_{hash(answer.question)}",
        )
        st.markdown("</div>", unsafe_allow_html=True)
        zoom_level = {"Page": "page", "Element": "element", "Lines / cells": "precise"}[zoom_label]

        try:
            img = load_page_image(active_doc, page)
        except FileNotFoundError:
            st.error("Page image not found.")
            return
        pmeta = ph.get_page_meta(active_parse, page)
        if not pmeta:
            st.error("No page metadata.")
            return

        # Build the quote_groups arg for render_overlays
        overlay_groups = [
            (matches, (quote_color(color_idx)[0], quote_color(color_idx)[1]))
            for matches, _, color_idx in quote_render_set
        ]
        out_img = ph.render_overlays(
            img,
            overlay_groups,
            page,
            pmeta["width"],
            pmeta["height"],
            level=zoom_level,
        )
        st.image(out_img, caption=f"{short_doc_name(active_doc)} — page {page}", width="stretch")

        # Legend — show one swatch per color in play
        legend_parts = ['<div class="legend">']
        legend_parts.append(
            '<span><span class="legend-swatch" style="background:#bbb; outline:1px solid #888;"></span>element-level box</span>'
        )
        for matches, _, color_idx in quote_render_set:
            _, fill_rgba, hex_color = quote_color(color_idx)
            label_for_color = (
                f"quote {color_idx + 1}" if len(quote_render_set) > 1 else "precise (lines / cell)"
            )
            legend_parts.append(
                f'<span><span class="legend-swatch" style="background:{hex_color}; outline:1px solid {COLOR_FOREST};"></span>{label_for_color}</span>'
            )
        legend_parts.append("</div>")
        st.html("".join(legend_parts))


# ---- markdown panel HTML builder ----

def _html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_markdown_panel_html(
    quote_render_set: list[tuple[list[ph.GroundingMatch], list[list[int]], int]],
    parse: dict,
) -> str:
    """Render the element-text(s) that contain the quotes, with <mark>s around
    each quote span in the matching color. Groups quotes by their parent
    element so the same element isn't re-rendered twice."""
    md = parse["markdown"]
    # element_span (tuple) → list of (start_rel, end_rel, color_hex)
    by_element: dict[tuple[int, int], list[tuple[int, int, str]]] = {}
    element_order: list[tuple[int, int]] = []

    for matches, spans, color_idx in quote_render_set:
        clusters = ph.cluster_matches(matches)
        if not clusters:
            continue
        outer, _ = clusters[0]
        elem_span = tuple(outer.span)
        if elem_span not in by_element:
            by_element[elem_span] = []
            element_order.append(elem_span)
        _, _, color_hex = quote_color(color_idx)
        for sp in spans:
            start_rel = max(0, sp[0] - elem_span[0])
            end_rel = min(elem_span[1] - elem_span[0], sp[1] - elem_span[0])
            if 0 <= start_rel < end_rel:
                by_element[elem_span].append((start_rel, end_rel, color_hex))

    if not element_order:
        return '<div class="md-pane">(no source text available for this view)</div>'

    block_htmls = []
    for elem_span in element_order:
        elem_text = md[elem_span[0]:elem_span[1]]
        marks = sorted(by_element[elem_span])
        pieces = []
        cursor = 0
        for s, e, color in marks:
            if s < cursor:
                continue
            pieces.append(_html_escape(elem_text[cursor:s]))
            pieces.append(
                f'<mark style="background:{color};">{_html_escape(elem_text[s:e])}</mark>'
            )
            cursor = e
        pieces.append(_html_escape(elem_text[cursor:]))
        block_htmls.append("".join(pieces))

    separator = '\n\n<span style="color:var(--subtle);">— — —</span>\n\n'
    return '<div class="md-pane">' + separator.join(block_htmls) + "</div>"


render()
