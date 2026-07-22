#!/usr/bin/env python3
"""
LandingAI ADE pipeline: Classify (API) -> filter -> Parse

This script uses the official LandingAI ADE Python SDK (`landingai-ade`) to:
  1. Classify a document into one of your defined categories, where the
     categories are loaded from an external `classes.json` file.
  2. Parse ONLY the documents whose predicted class is "of interest"
     (see PARSE_CLASSES below). Everything else is classified but skipped.

Running Classify before Parse lets you triage a large, mixed batch cheaply and
spend parse budget only on the document types you actually care about.

Setup:
    pip install landingai-ade python-dotenv

Docs: https://docs.landing.ai/ade/ade-python
"""

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
INPUT_DIR = Path("loan_demo_documents")
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

# --- Classification categories -------------------------------------------
# The category definitions are loaded from an external JSON file so the class
# set can be edited without touching this script. The file is a flat object of
# {class_name: description}, e.g.:
#   { "pay_stub": "Employee pay stub showing wages and deductions", ... }
CLASSES_FILE = Path("classes.json")

# --- Parse filter --------------------------------------------------------
# Only documents whose predicted class is in this set are parsed. Every other
# document is still classified (so you see how it was routed) but skipped
# before the more expensive parse step. Edit this set to change what's kept.
# Default: income & employment documents.
PARSE_CLASSES = {
    "pay_stub",
    "w2",
    "tax_return",
    "employment_verification",
}


def load_classes(path: Path) -> dict:
    """Load the {class_name: description} category map from a JSON file."""
    if not path.exists():
        raise SystemExit(f"Classes file not found: {path} — set CLASSES_FILE")
    with path.open() as f:
        classes = json.load(f)
    if not isinstance(classes, dict) or not classes:
        raise SystemExit(f"{path} must be a non-empty JSON object of class -> description")
    return classes


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

def classify_document(client: LandingAIADE, document: Path, classes: str):
    """Step 1 — classify the document into one of the defined classes."""
    response = client.classify(
        document=document,
        classes=classes,
        model=CLASSIFY_MODEL,
    )
    # response.classification -> list of results with:
    #   .class_, .page, .reason, .suggested_class
    for result in response.classification:
        print(f"  page {result.page}: {result.class_}  ({result.reason})")
    return response


def predicted_classes(classification_response) -> set:
    """Collect the set of class labels the classifier assigned across pages."""
    return {
        r.class_
        for r in classification_response.classification
        if getattr(r, "class_", None)
    }


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

def process_file(client: LandingAIADE, document: Path, classes: str) -> dict:
    """Classify a file, then parse it only if its class is of interest."""
    print(f"\n=== {document.name} ===")

    print("Step 1: Classifying...")
    classification = classify_document(client, document, classes)

    found = predicted_classes(classification)
    of_interest = found & PARSE_CLASSES

    if not of_interest:
        print(f"Step 2: Skipping parse — class {sorted(found) or '[none]'} not in filter.")
        return {
            "file": document,
            "classification": classification,
            "parsed": None,
            "skipped": True,
        }

    print(f"Step 2: Parsing (matched {sorted(of_interest)})...")
    parsed = parse_document(client, document)
    return {
        "file": document,
        "classification": classification,
        "parsed": parsed,
        "skipped": False,
    }


def main():
    documents = collect_documents()
    if not documents:
        raise SystemExit("No files to process — check INPUT_DIR / DOCUMENT_PATHS.")

    classes = json.dumps(load_classes(CLASSES_FILE))

    print(f"Found {len(documents)} file(s) to process.")
    print(f"Parse filter (classes of interest): {sorted(PARSE_CLASSES)}")
    client = make_client()

    results = []
    for document in documents:
        try:
            results.append(process_file(client, document, classes))
        except Exception as exc:
            # Keep going if one file fails; report at the end.
            print(f"  ERROR processing {document.name}: {exc}")

    parsed = [r for r in results if not r.get("skipped")]
    skipped = [r for r in results if r.get("skipped")]

    # TODO: do something with `parsed` — e.g. extract data, save the markdown,
    # feed chunks downstream, etc.
    print(
        f"\nDone. Classified {len(results)}/{len(documents)} file(s); "
        f"parsed {len(parsed)}, skipped {len(skipped)} by filter."
    )


if __name__ == "__main__":
    main()
