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

SAMPLE_QUERIES = [
    ("Marathon runners",
     "Did the studies find a benefit for marathon runners taking vitamin C?"),
    ("Table 1 — general community RR",
     "In the Vitamin C meta-analyses Table 1, what was the relative risk for incidence of colds during prophylaxis in the general community studies?"),
    ("High-dose in children",
     "What is the main finding regarding high-dose vitamin C therapy in children?"),
    ("Echinacea",
     "Is echinacea effective for preventing the common cold?"),
]


# ---- grounding for a "view" (answer or a retrieved chunk) ----

def grounding_for_answer(answer, source_parse: dict):
    """Resolve the LLM's verbatim quote to grounding matches on the source doc.
    Returns (matches, spans) or (None, None) on miss."""
    md = source_parse["markdown"]
    spans = ph.find_quote_span(answer.exact_quote, md)
    if not spans:
        return None, None
    return ph.get_grounding(spans, source_parse), spans


def grounding_for_chunk(chunk, parse: dict):
    """Treat the chunk's whole span as the query — returns its element grounding.
    Useful for showing 'where would this passage land if it were the source?'"""
    return ph.get_grounding([list(chunk.span)], parse)


# ---- main render ----

def render() -> None:
    inject_brand_css()

    # Hero — sage card per brand book "industry panel" pattern
    st.html(
        '<div class="hero-card">'
        '<div class="eyebrow">DPT-3 · Parse API v3</div>'
        '<h1 class="display display-hero">'
        'Verifiable, Hierarchical RAG on Medical Literature'
        '</h1>'
        '<p class="hero-sub">'
        '8 cold and vitamin-C papers. Every answer cites the exact line or table cell that proves it.'
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
        placeholder="Ask about vitamin C, echinacea, marathon runners, dosing, mechanisms…",
        key="ask_input",
        label_visibility="collapsed",
    )

    col_btn, col_k = st.columns([1, 4])
    with col_btn:
        run_button = st.button(
            "Ask", type="primary",
            disabled=not question.strip(),
            width="stretch",
        )
    with col_k:
        k = st.slider("Retrieved passages", 2, 12, 6, key="ask_k", label_visibility="collapsed")
        st.caption(f"Retrieving top {k} passages")

    should_run = (run_button or st.session_state.ask_run_pending) and question.strip()
    if should_run:
        st.session_state.ask_run_pending = False
        st.session_state.ask_answer = None
        st.session_state.ask_error = None
        st.session_state.selected_view = "answer"
        with st.spinner("Retrieving passages and asking the model…"):
            try:
                st.session_state.ask_answer = ask(question, k=k)
            except Exception as e:
                st.session_state.ask_error = str(e)

    if st.session_state.ask_error:
        st.error(f"Q&A failed: {st.session_state.ask_error}")
        st.caption("Check that ANTHROPIC_API_KEY in .env is valid.")
        return

    answer = st.session_state.ask_answer
    if not answer:
        return

    # ---- determine the "selected view" — answer or one of the retrieved chunks ----

    view = st.session_state.selected_view
    selected_chunk = None
    if view.startswith("passage:"):
        try:
            idx = int(view.split(":", 1)[1])
            if 0 <= idx < len(answer.retrieved):
                selected_chunk = answer.retrieved[idx]
            else:
                st.session_state.selected_view = "answer"
                view = "answer"
        except ValueError:
            st.session_state.selected_view = "answer"
            view = "answer"

    # Build matches + parse + meta for the currently-selected view
    matches = None
    spans = None
    active_parse = None
    active_doc = None
    is_answer_view = (view == "answer")

    if is_answer_view:
        if answer.exact_quote and answer.source_doc:
            try:
                active_parse = load_parse(answer.source_doc)
                active_doc = answer.source_doc
                matches, spans = grounding_for_answer(answer, active_parse)
            except FileNotFoundError:
                pass
    else:
        try:
            active_parse = load_parse(selected_chunk.doc_id)
            active_doc = selected_chunk.doc_id
            matches = grounding_for_chunk(selected_chunk, active_parse)
        except FileNotFoundError:
            pass

    # ---- two-column layout: answer/sources on left, page image on right ----

    st.divider()
    left, right = st.columns([1, 1])

    with left:
        st.markdown('<div class="label">Answer</div>', unsafe_allow_html=True)
        st.markdown(
            f"<p style='font-size:15.5px; line-height:1.7; color:{COLOR_HEADLINE};'>{answer.answer}</p>",
            unsafe_allow_html=True,
        )
        if not answer.exact_quote:
            st.warning("The model declined to produce a verbatim quote.")

        # Precision metric — only meaningful for the answer view
        if is_answer_view and matches:
            metric = ph.precision_metric(matches, active_parse)
            st.markdown('<div class="label" style="margin-top:18px;">Precision win</div>', unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            m1.metric("Element-level", f"{metric['chunk_pct']:.2f}%")
            m2.metric("Line / cell", f"{metric['precise_pct']:.2f}%")
            m3.metric("More precise", f"{metric['ratio']:.1f}×")

        # HITL
        if answer.exact_quote and answer.source_doc:
            st.markdown('<div class="label" style="margin-top:18px;">Verification</div>', unsafe_allow_html=True)
            hcol1, hcol2, _ = st.columns([1, 1, 3])
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

        # Retrieved passages — radio list, the option label IS the click target.
        # The LLM's source is (almost) always one of the retrieved chunks, so we
        # merge them into a single row marked with a star instead of duplicating.
        st.markdown('<div class="label" style="margin-top:22px;">Sources</div>', unsafe_allow_html=True)
        st.caption("Pick a source to highlight it on the page →")

        labels: list[str] = []
        captions: list[str] = []
        view_keys: list[str] = []

        answer_source_matched = False
        for i, c in enumerate(answer.retrieved):
            is_answer_source = (
                answer.exact_quote is not None
                and answer.source_doc == c.doc_id
                and answer.source_element_id == c.element_id
            )
            if is_answer_source:
                prefix = "★  Answer source · "
                view_keys.append("answer")
                # Use the LLM's quote as the caption when this row IS the answer source.
                q_preview = answer.exact_quote.strip().replace("\n", " ")
                captions.append(q_preview[:160] + ("…" if len(q_preview) > 160 else ""))
                answer_source_matched = True
            else:
                prefix = f"{i + 1}.  "
                view_keys.append(f"passage:{i}")
                preview = c.text.strip().replace("\n", " ")
                captions.append(preview[:160] + ("…" if len(preview) > 160 else ""))

            labels.append(
                f"{prefix}{short_doc_name(c.doc_id)}"
                f" · {c.element_type} · p.{c.page} · dist {c.distance:.2f}"
            )

        # Edge case: LLM cited a doc/element not in the retrieved set. Surface it
        # explicitly so the user isn't confused by a missing star.
        if answer.exact_quote and answer.source_doc and not answer_source_matched:
            labels.insert(0, f"★  Answer source · {short_doc_name(answer.source_doc)}"
                             f" · element {answer.source_element_id}")
            q_preview = answer.exact_quote.strip().replace("\n", " ")
            captions.insert(0, q_preview[:160] + ("…" if len(q_preview) > 160 else ""))
            view_keys.insert(0, "answer")

        # Default selection = current session view, or 0 (answer).
        try:
            default_idx = view_keys.index(st.session_state.selected_view)
        except ValueError:
            default_idx = 0

        # Key includes the question + retrieved count so a new query resets the widget.
        radio_key = f"src_radio_{hash(answer.question)}_{len(answer.retrieved)}"

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

    with right:
        st.markdown('<div class="label">Source page</div>', unsafe_allow_html=True)
        if not active_parse or not matches:
            st.info("No page to highlight yet — ask a question to see the source page here.")
            return

        pages_with_hits = sorted({m.page for m in matches})
        if not pages_with_hits:
            st.info("No grounding for the selected view.")
            return

        page = (
            st.selectbox(
                "Page",
                pages_with_hits,
                key="ask_page",
                format_func=lambda p: f"page {p}",
                label_visibility="collapsed",
            )
            if len(pages_with_hits) > 1
            else pages_with_hits[0]
        )

        try:
            img = load_page_image(active_doc, page)
        except FileNotFoundError:
            st.error("Page image not found.")
            return
        pmeta = ph.get_page_meta(active_parse, page)
        if not pmeta:
            st.error("No page metadata.")
            return

        out = ph.render_dual_overlay(img, matches, page, pmeta["width"], pmeta["height"])
        st.image(out, caption=f"{short_doc_name(active_doc)} — page {page}", width="stretch")

        st.html(
            f'<div class="legend">'
            f'<span><span class="legend-swatch" style="background:#bbb; outline:1px solid #888;"></span>element-level box</span>'
            f'<span><span class="legend-swatch" style="background:rgba(255,230,0,0.5); outline:1px solid {COLOR_FOREST};"></span>precise (lines / cell)</span>'
            f'</div>'
        )


render()
