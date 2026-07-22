"""Build a ChromaDB index from cached parses in parsed/.

Block-level indexing: one chunk per top-level structural element (text, table,
figure, marginalia, logo, card, scan_code, attestation). We retrieve whole
blocks, then ground the answer's verbatim quote down to the exact line or cell
(see query_engine + parse_helpers). Retrieve the block, highlight the line.

Reads the DPT-3 (dpt-3-pro-20260710+) parse response: `structure` is a tree of
elements, each with an `id` and a `span` into `markdown`. `iter_chunks` walks it
and emits one chunk per leaf element. Tables are emitted whole — their
`table_cell` children are not indexed separately, but stay queryable at grounding
time via the parallel `grounding` tree (flattened by parse_helpers.grounding_map).

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

from parse_helpers import iter_chunks

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
        for chunk in iter_chunks(parse, doc_id):
            counts_by_type[chunk.element_type] = counts_by_type.get(chunk.element_type, 0) + 1
            ids.append(f"{chunk.doc_id}::{chunk.element_id}")
            docs.append(chunk.text)
            metas.append({
                "doc_id": chunk.doc_id,
                "element_id": chunk.element_id,
                "element_type": chunk.element_type,
                "page": chunk.page,
                "span_start": chunk.span[0],
                "span_end": chunk.span[1],
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
