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

import os
from dataclasses import dataclass, field
from pathlib import Path

import anthropic
import chromadb
from dotenv import load_dotenv

load_dotenv(override=True)

CHROMA_DIR = "chroma"
COLLECTION_NAME = "medical_corpus"
DEFAULT_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
DEFAULT_K = 6

SYSTEM_PROMPT = """You are a careful medical research assistant. The user is \
researching the common cold and vitamin C. You will be given the most relevant \
passages from a corpus of journal articles.

Your job:
1. Answer the question concisely based ONLY on the passages provided.
2. Quote verbatim from ONE passage the exact text that supports your answer.

CRITICAL: The exact_quote you produce MUST appear character-for-character in one \
of the source passages. The system will use string search to find that quote on \
the source PDF and highlight it. If your quote does not match a source passage \
verbatim, the highlight will fail. Do not paraphrase, do not normalize whitespace \
or punctuation, do not change capitalization.

Prefer the shortest faithful quote that proves your answer — a single sentence or \
sentence fragment is ideal. For numeric values inside tables, quote just the value \
itself (e.g. "0.98 (0.95, 1.00)").

If the passages don't support a confident answer, say so and set exact_quote to null."""

ANSWER_TOOL = {
    "name": "answer_with_grounded_quote",
    "description": "Answer the question with a verbatim quote from a source passage.",
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
                    "confident answer."
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
class Answer:
    question: str
    answer: str
    exact_quote: str | None
    source_doc: str | None
    source_element_id: str | None
    retrieved: list[RetrievedChunk] = field(default_factory=list)
    model: str = ""


def _get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(COLLECTION_NAME)


def retrieve(question: str, k: int = DEFAULT_K, exclude_marginalia: bool = True) -> list[RetrievedChunk]:
    coll = _get_collection()
    where = {"element_type": {"$ne": "marginalia"}} if exclude_marginalia else None
    result = coll.query(query_texts=[question], n_results=k, where=where)
    out: list[RetrievedChunk] = []
    if not result["ids"] or not result["ids"][0]:
        return out
    for i in range(len(result["ids"][0])):
        meta = result["metadatas"][0][i]
        out.append(RetrievedChunk(
            doc_id=meta["doc_id"],
            element_id=meta["element_id"],
            element_type=meta["element_type"],
            page=meta["page"],
            span=[meta["span_start"], meta["span_end"]],
            text=result["documents"][0][i],
            distance=result["distances"][0][i],
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

    return Answer(
        question=question,
        answer=tool_input.get("answer", ""),
        exact_quote=tool_input.get("exact_quote"),
        source_doc=tool_input.get("source_doc"),
        source_element_id=tool_input.get("source_element_id"),
        retrieved=chunks,
        model=model,
    )
