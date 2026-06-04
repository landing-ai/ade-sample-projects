"""Build a ChromaDB index from cached parses in parsed/.

Small-to-big units: every table becomes one *header-aware sentence per row*
(e.g. "Coronavirus 229E. Serology: 10 (5); Total: 10 (5)"); every other leaf
element (text, figure, marginalia, ...) stays whole. Each unit stores a
`parent_*` pointer so retrieval can match the precise small unit, then expand to
the parent element for context + grounding (see query_engine.retrieve).

A pipe-delimited table embeds as a blur of all its cells and retrieves poorly;
one clean sentence per row retrieves precisely — the win is the unit shape, not a
bigger model.

Embedding: ChromaDB's default (sentence-transformers/all-MiniLM-L6-v2).
First run downloads the ~80MB model.

Usage:
    python build_index.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import chromadb
from tqdm import tqdm

from parse_helpers import iter_units

PARSED_DIR = Path("parsed")
CHROMA_DIR = "chroma"
COLLECTION_NAME = "medical_corpus"


def main() -> int:
    parses = sorted(PARSED_DIR.glob("*.json"))
    if not parses:
        sys.exit(f"No parsed responses in {PARSED_DIR}/ — run ingest.py first.")

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    # Rebuild the collection fresh — chunking is deterministic over the cache.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(name=COLLECTION_NAME)

    ids: list[str] = []
    docs: list[str] = []
    metas: list[dict] = []
    counts_by_type: dict[str, int] = {}

    for parse_path in parses:
        doc_id = parse_path.stem
        with open(parse_path) as f:
            parse = json.load(f)
        for u in iter_units(parse, doc_id):
            counts_by_type[u.unit_type] = counts_by_type.get(u.unit_type, 0) + 1
            ids.append(u.id)
            docs.append(u.text)
            metas.append({
                "doc_id": u.doc_id,
                "unit_type": u.unit_type,
                "parent_id": u.parent_id,
                "parent_type": u.parent_type,
                "parent_span_start": u.parent_span[0],
                "parent_span_end": u.parent_span[1],
                "page": u.page,
                "row": -1 if u.row is None else u.row,
            })

    if not ids:
        sys.exit("No chunks to index.")

    print(f"Indexing {len(ids)} chunks from {len(parses)} document(s)...")
    print(f"  by type: {counts_by_type}")

    BATCH = 100
    for i in tqdm(range(0, len(ids), BATCH), unit="batch"):
        collection.add(
            ids=ids[i:i + BATCH],
            documents=docs[i:i + BATCH],
            metadatas=metas[i:i + BATCH],
        )

    print(f"\nDone. {collection.count()} chunks in collection '{COLLECTION_NAME}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
