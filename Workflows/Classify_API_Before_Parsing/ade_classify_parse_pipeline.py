#!/usr/bin/env python3
"""
LandingAI ADE pipeline skeleton: Classify -> Parse

This script uses the official LandingAI ADE Python SDK (`landingai-ade`) to:
  1. Classify a document into one of your defined categories.
  2. Parse the document into Markdown + structured chunks.

Setup:
    pip install landingai-ade python-dotenv

Docs: https://docs.landing.ai/ade/ade-python
"""

import os
import json
from pathlib import Path

from landingai_ade import LandingAIADE


# ---------------------------------------------------------------------------
# 1. CONFIG — fill these in
# ---------------------------------------------------------------------------

# --- API key -------------------------------------------------------------
# Recommended: set the VISION_AGENT_API_KEY environment variable and leave
# API_KEY = None so the SDK picks it up automatically. Do NOT hard-code real
# keys in source control.
#   export VISION_AGENT_API_KEY=<your-api-key>
API_KEY = None  # or "your-api-key-here" to pass it explicitly below

# --- Input documents -----------------------------------------------------
# You can process multiple files. Choose EITHER option A or B.
#
# Option A: point at a folder and process every matching file inside it.
INPUT_DIR = Path("path/to/your/documents")
# File types to include when scanning INPUT_DIR:
FILE_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg", ".tiff")
# Set to True to also scan subfolders:
RECURSIVE = False
#
# Option B: OR list specific files explicitly (takes priority if non-empty).
DOCUMENT_PATHS = [
    # Path("path/to/first.pdf"),
    # Path("path/to/second.png"),
]

# --- Models --------------------------------------------------------------
CLASSIFY_MODEL = "classify-latest"
PARSE_MODEL = "dpt-2-latest"

# --- Where to save parse output (optional) -------------------------------
OUTPUT_DIR = "./ade_output"

# --- Classification categories ------------------------------------------
# TODO: describe your own classes. `classes` is passed as a JSON string.
CLASSES = json.dumps(
    {
        "invoice": "A billing document listing charges, totals, and payment terms",
        "contract": "A legal agreement between parties",
        "report": "A general informational or technical report",
        # add more classes as needed...
    }
)


# ---------------------------------------------------------------------------
# 2. CLIENT
# ---------------------------------------------------------------------------

def make_client() -> LandingAIADE:
    """Create the ADE client. Falls back to VISION_AGENT_API_KEY env var."""
    if API_KEY:
        return LandingAIADE(apikey=API_KEY)
    # apikey defaults to the VISION_AGENT_API_KEY environment variable
    return LandingAIADE()
    # For EU endpoints: return LandingAIADE(environment="eu")


# ---------------------------------------------------------------------------
# 3. PIPELINE STEPS
# ---------------------------------------------------------------------------

def classify_document(client: LandingAIADE, document: Path):
    """Step 1 — classify the document into one of the CLASSES."""
    response = client.classify(
        document=document,
        classes=CLASSES,
        model=CLASSIFY_MODEL,
    )
    # response.classification -> list of results with:
    #   .class_, .page, .reason, .suggested_class
    for result in response.classification:
        print(f"  page {result.page}: {result.class_}  ({result.reason})")
    return response


def parse_document(client: LandingAIADE, document: Path):
    """Step 2 — parse the document into Markdown + chunks."""
    response = client.parse(
        document=document,
        model=PARSE_MODEL,
        save_to=OUTPUT_DIR,  # optional: writes JSON response to this folder
    )
    # response.markdown  -> full Markdown text
    # response.chunks    -> list of parsed content regions
    # response.grounding -> chunk_id -> location data
    # response.metadata  -> processing details
    print(f"  parsed {len(response.chunks)} chunks")
    return response


# ---------------------------------------------------------------------------
# 4. FILE DISCOVERY
# ---------------------------------------------------------------------------

def collect_documents() -> list[Path]:
    """Return the list of files to process (Option B if set, else Option A)."""
    # Option B: explicit list wins if provided.
    if DOCUMENT_PATHS:
        return [Path(p) for p in DOCUMENT_PATHS]

    # Option A: scan a folder for matching file types.
    if not INPUT_DIR.exists():
        raise SystemExit(f"Input folder not found: {INPUT_DIR} — set INPUT_DIR")

    pattern = "**/*" if RECURSIVE else "*"
    files = [
        p
        for p in sorted(INPUT_DIR.glob(pattern))
        if p.is_file() and p.suffix.lower() in FILE_EXTENSIONS
    ]
    return files


# ---------------------------------------------------------------------------
# 5. MAIN
# ---------------------------------------------------------------------------

def process_file(client: LandingAIADE, document: Path) -> dict:
    """Run the full Classify -> Parse pipeline on a single file."""
    print(f"\n=== {document.name} ===")

    print("Step 1: Classifying...")
    classification = classify_document(client, document)

    print("Step 2: Parsing...")
    parsed = parse_document(client, document)

    return {"file": document, "classification": classification, "parsed": parsed}


def main():
    documents = collect_documents()
    if not documents:
        raise SystemExit("No files to process — check INPUT_DIR / DOCUMENT_PATHS.")

    print(f"Found {len(documents)} file(s) to process.")
    client = make_client()

    results = []
    for document in documents:
        try:
            results.append(process_file(client, document))
        except Exception as exc:
            # Keep going if one file fails; report at the end.
            print(f"  ERROR processing {document.name}: {exc}")

    # TODO: do something with `results` — e.g. route by class, extract data,
    # save the markdown, feed chunks downstream, etc.
    print(f"\nDone. Processed {len(results)}/{len(documents)} file(s) successfully.")


if __name__ == "__main__":
    main()
