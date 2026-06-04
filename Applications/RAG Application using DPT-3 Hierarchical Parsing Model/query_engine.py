"""Retrieval + Claude-powered verifiable Q&A.

Retrieves the top-k chunks from ChromaDB (filtering out marginalia) and asks
Claude to produce {answer, exact_quote, source_doc, source_element_id} via
forced tool-use, so the output schema is guaranteed.

Usage:
    from query_engine import ask
    a = ask("Does vitamin C help marathon runners?")
    print(a.answer, a.exact_quote)
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import anthropic
import chromadb
from dotenv import load_dotenv

load_dotenv(override=True)

CHROMA_DIR = "chroma"
COLLECTION_NAME = "medical_corpus"
PARSED_DIR = "parsed"
DEFAULT_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
DEFAULT_K = 6

SYSTEM_PROMPT = """You are a careful medical research assistant. The user is \
researching the common cold and vitamin C. You will be given the most relevant \
passages from a corpus of journal articles.

Your job:
1. Answer the question concisely based ONLY on the passages provided.
2. Quote verbatim from the passages the exact text that supports your answer.

CRITICAL: Every quote you produce MUST appear character-for-character in one \
of the source passages. The system will use string search to find that quote on \
the source PDF and highlight it. If your quote does not match a source passage \
verbatim, the highlight will fail. Do not paraphrase, do not normalize whitespace \
or punctuation, do not change capitalization.

Prefer the shortest faithful quote that proves your answer — a single sentence or \
sentence fragment is ideal. For numeric values inside tables, quote just the value \
itself (e.g. "0.98 (0.95, 1.00)").

MULTI-QUOTE: If the answer combines facts from non-adjacent passages (e.g. comparing \
prevention vs treatment, adults vs children, two separate studies), use the `quotes` \
array to list each supporting fragment as a separate entry. Each entry needs its own \
text, source_doc, and source_element_id. The first entry must duplicate exact_quote/\
source_doc/source_element_id. Use multi-quote only when the answer GENUINELY needs \
multiple non-adjacent sources — don't pad with extras when a single quote suffices.

If the passages don't support a confident answer, say so and set exact_quote to null."""

ANSWER_TOOL = {
    "name": "answer_with_grounded_quote",
    "description": "Answer the question with one or more verbatim quotes from the source passages.",
    "input_schema": {
        "type": "object",
        "properties": {
            "answer": {
                "type": "string",
                "description": "Concise answer (1-3 sentences) based on the passages.",
            },
            "exact_quote": {
                "type": ["string", "null"],
                "description": (
                    "Verbatim text from one source passage that supports the answer. "
                    "Must match character-for-character. Null if no passage supports a "
                    "confident answer. If quotes is provided, this MUST equal quotes[0].text."
                ),
            },
            "source_doc": {
                "type": ["string", "null"],
                "description": "doc_id of the passage you quoted, or null.",
            },
            "source_element_id": {
                "type": ["string", "null"],
                "description": "element_id of the passage you quoted, or null.",
            },
            "quotes": {
                "type": ["array", "null"],
                "description": (
                    "OPTIONAL. Use this only when the answer combines facts from "
                    "non-adjacent passages. Each entry is one verbatim supporting "
                    "fragment. The first entry MUST duplicate exact_quote / "
                    "source_doc / source_element_id."
                ),
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Verbatim fragment."},
                        "source_doc": {"type": "string"},
                        "source_element_id": {"type": "string"},
                    },
                    "required": ["text", "source_doc", "source_element_id"],
                },
            },
        },
        "required": ["answer", "exact_quote", "source_doc", "source_element_id"],
    },
}


@dataclass
class RetrievedChunk:
    doc_id: str
    element_id: str
    element_type: str
    page: int
    span: list[int]
    text: str
    distance: float


@dataclass
class Quote:
    """One verbatim supporting fragment for an answer.

    Multiple Quotes per Answer enable non-contiguous grounding — e.g. comparing
    findings from two non-adjacent paragraphs or two different documents.
    """
    text: str
    source_doc: str
    source_element_id: str


@dataclass
class Answer:
    question: str
    answer: str
    exact_quote: str | None
    source_doc: str | None
    source_element_id: str | None
    retrieved: list[RetrievedChunk] = field(default_factory=list)
    model: str = ""
    # Always populated when there's any grounded quote at all (length 1 for
    # single-quote answers, length 2+ for multi-quote / non-contiguous evidence).
    # Empty list when the model declined to quote.
    quotes: list[Quote] = field(default_factory=list)


def _get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(COLLECTION_NAME)


@lru_cache(maxsize=64)
def _doc_markdown(doc_id: str) -> str:
    with open(f"{PARSED_DIR}/{doc_id}.json") as f:
        return json.load(f)["markdown"]


def retrieve(question: str, k: int = DEFAULT_K, exclude_marginalia: bool = True) -> list[RetrievedChunk]:
    """Small-to-big retrieval. Match fine-grained units (table rows / elements),
    then merge to their parent element so the LLM gets full context and grounding
    still resolves to the precise line/cell.

    A parent's rank = its best (closest) unit. So a table whose *Coronavirus 229E*
    row is the top hit surfaces at rank 1, even though the whole-table embedding
    would have ranked 5th."""
    coll = _get_collection()
    # Pull a wide pool of small units, then collapse to distinct parent elements.
    n_candidates = max(k * 8, 48)
    where = {"parent_type": {"$ne": "marginalia"}} if exclude_marginalia else None
    result = coll.query(query_texts=[question], n_results=n_candidates, where=where)
    if not result["ids"] or not result["ids"][0]:
        return []

    best: dict[tuple[str, str], tuple[float, dict]] = {}
    for i in range(len(result["ids"][0])):
        meta = result["metadatas"][0][i]
        dist = result["distances"][0][i]
        key = (meta["doc_id"], meta["parent_id"])
        if key not in best or dist < best[key][0]:
            best[key] = (dist, meta)

    parents = sorted(best.values(), key=lambda dm: dm[0])[:k]
    out: list[RetrievedChunk] = []
    for dist, meta in parents:
        s, e = meta["parent_span_start"], meta["parent_span_end"]
        text = _doc_markdown(meta["doc_id"])[s:e].strip()
        out.append(RetrievedChunk(
            doc_id=meta["doc_id"],
            element_id=meta["parent_id"],
            element_type=meta["parent_type"],
            page=meta["page"],
            span=[s, e],
            text=text,
            distance=dist,
        ))
    return out


def _format_passages(chunks: list[RetrievedChunk]) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        header = (
            f"--- Passage {i} "
            f"(doc={c.doc_id}, element_id={c.element_id}, "
            f"type={c.element_type}, page={c.page}) ---"
        )
        parts.append(header)
        parts.append(c.text)
        parts.append("")
    return "\n".join(parts)


def ask(
    question: str,
    *,
    k: int = DEFAULT_K,
    model: str = DEFAULT_MODEL,
    exclude_marginalia: bool = True,
) -> Answer:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Add it to .env or export it."
        )

    chunks = retrieve(question, k=k, exclude_marginalia=exclude_marginalia)
    if not chunks:
        return Answer(
            question=question,
            answer="No relevant passages found in the corpus.",
            exact_quote=None,
            source_doc=None,
            source_element_id=None,
            retrieved=[],
            model=model,
        )

    client = anthropic.Anthropic()
    user_content = (
        f"Question: {question}\n\n"
        f"Relevant passages:\n{_format_passages(chunks)}\n"
        f"Use the answer_with_grounded_quote tool to respond."
    )

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=[ANSWER_TOOL],
        tool_choice={"type": "tool", "name": "answer_with_grounded_quote"},
        messages=[{"role": "user", "content": user_content}],
    )

    tool_input: dict = {}
    for block in response.content:
        if block.type == "tool_use" and block.name == "answer_with_grounded_quote":
            tool_input = block.input
            break

    primary_quote = tool_input.get("exact_quote")
    primary_doc = tool_input.get("source_doc")
    primary_eid = tool_input.get("source_element_id")

    # Normalize quotes list: empty when no quote at all, length 1 for single-quote,
    # length 2+ when the model used the multi-quote field.
    quotes: list[Quote] = []
    raw_quotes = tool_input.get("quotes")
    if raw_quotes:
        for q in raw_quotes:
            if not isinstance(q, dict):
                continue
            text = q.get("text")
            doc = q.get("source_doc")
            eid = q.get("source_element_id")
            if text and doc and eid:
                quotes.append(Quote(text=text, source_doc=doc, source_element_id=str(eid)))
    elif primary_quote and primary_doc and primary_eid:
        quotes.append(Quote(
            text=primary_quote,
            source_doc=primary_doc,
            source_element_id=str(primary_eid),
        ))

    return Answer(
        question=question,
        answer=tool_input.get("answer", ""),
        exact_quote=primary_quote,
        source_doc=primary_doc,
        source_element_id=primary_eid,
        retrieved=chunks,
        model=model,
        quotes=quotes,
    )
