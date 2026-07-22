#!/usr/bin/env python3
"""
LandingAI ADE loan-management pipeline: Classify -> filter -> Parse -> Extract

This script uses the official LandingAI ADE Python SDK (`landingai-ade`) to run a
full document-understanding pipeline over a residential mortgage file:

  1. Classify each document into one of the categories defined in `classes.json`.
  2. Filter — keep only documents whose predicted class is "of interest"
     (see PARSE_CLASSES; default: income & employment documents).
  3. Parse the kept documents into Markdown + structured chunks.
  4. Extract structured field values from the parsed Markdown using the JSON
     schema in `extract_schema.json` (ADE Extract API).

Classifying up front lets you triage a large, mixed packet cheaply and spend the
more expensive Parse + Extract steps only on the documents you actually care about.

Setup:
    pip install -r requirements.txt

Docs: https://docs.landing.ai/ade/ade-python
"""

import io
import json
from pathlib import Path

from landingai_ade import LandingAIADE

try:
    # Optional: load VISION_AGENT_API_KEY (and friends) from a local .env file.
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


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

# --- Where to save output ------------------------------------------------
# Per-document parse/extract JSON plus a combined extractions.json land here.
OUTPUT_DIR = Path("./results_folder")

# --- Classification categories -------------------------------------------
# The category definitions live in an external JSON file ({class_name: description})
# so the class set can be edited without touching this script.
CLASSES_FILE = Path("classes.json")

# --- Extraction schema ---------------------------------------------------
# A JSON Schema describing the fields to pull from each parsed document. Passed
# straight to client.extract — no Pydantic model required.
SCHEMA_FILE = Path("extract_schema.json")

# --- Parse/extract filter ------------------------------------------------
# Only documents whose predicted class is in this set are parsed AND extracted.
# Every other document is still classified (so you see how it was routed) but
# skipped before the more expensive steps. Edit this set to change what's kept.
# Default: income & employment documents.
PARSE_CLASSES = {
    "pay_stub",
    "w2",
    "tax_return",
    "employment_verification",
}


def load_json(path: Path) -> dict:
    """Load and lightly validate a JSON config file."""
    if not path.exists():
        raise SystemExit(f"File not found: {path}")
    with path.open() as f:
        data = json.load(f)
    if not isinstance(data, dict) or not data:
        raise SystemExit(f"{path} must be a non-empty JSON object")
    return data


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
    response = client.parse(document=document, model=PARSE_MODEL)
    # response.markdown  -> full Markdown text
    # response.chunks    -> list of parsed content regions
    print(f"  parsed {len(response.chunks)} chunks")
    return response


def extract_fields(client: LandingAIADE, markdown: str, schema: dict):
    """Step 3 — extract structured fields from parsed Markdown using the schema."""
    response = client.extract(
        schema=schema,
        markdown=io.BytesIO(markdown.encode("utf-8")),
    )
    # response.extraction -> dict of extracted field values
    extraction = response.extraction or {}
    non_null = {k: v for k, v in extraction.items() if v not in (None, "", [])}
    print(f"  extracted {len(non_null)} field(s): {sorted(non_null)}")
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

def _dump(obj) -> str:
    """Serialize an SDK response (or plain object) to pretty JSON."""
    if hasattr(obj, "model_dump"):
        obj = obj.model_dump()
    return json.dumps(obj, indent=2, default=str)


def process_file(client: LandingAIADE, document: Path, classes: str, schema: dict) -> dict:
    """Classify a file, then parse + extract only if its class is of interest."""
    print(f"\n=== {document.name} ===")
    stem = document.stem

    print("Step 1: Classifying...")
    classification = classify_document(client, document, classes)

    found = predicted_classes(classification)
    of_interest = found & PARSE_CLASSES
    if not of_interest:
        print(f"Step 2: Skipping parse/extract — class {sorted(found) or '[none]'} not in filter.")
        return {"file": document, "skipped": True, "extraction": None}

    print(f"Step 2: Parsing (matched {sorted(of_interest)})...")
    parsed = parse_document(client, document)
    (OUTPUT_DIR / f"parse_{stem}.json").write_text(_dump(parsed), encoding="utf-8")

    print("Step 3: Extracting...")
    extracted = extract_fields(client, parsed.markdown, schema)
    (OUTPUT_DIR / f"extract_{stem}.json").write_text(_dump(extracted), encoding="utf-8")

    return {"file": document, "skipped": False, "extraction": extracted.extraction or {}}


def main():
    documents = collect_documents()
    if not documents:
        raise SystemExit("No files to process — check INPUT_DIR / DOCUMENT_PATHS.")

    classes = json.dumps(load_json(CLASSES_FILE))
    schema = load_json(SCHEMA_FILE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Found {len(documents)} file(s) to process.")
    print(f"Parse/extract filter (classes of interest): {sorted(PARSE_CLASSES)}")
    client = make_client()

    results = []
    for document in documents:
        try:
            results.append(process_file(client, document, classes, schema))
        except Exception as exc:
            # Keep going if one file fails; report at the end.
            print(f"  ERROR processing {document.name}: {exc}")

    extracted = [r for r in results if not r.get("skipped")]
    skipped = [r for r in results if r.get("skipped")]

    # Combined view: one entry per extracted document.
    combined = [
        {"document_name": r["file"].name, **(r["extraction"] or {})}
        for r in extracted
    ]
    (OUTPUT_DIR / "extractions.json").write_text(
        json.dumps(combined, indent=2, default=str), encoding="utf-8"
    )

    print(
        f"\nDone. Classified {len(results)}/{len(documents)} file(s); "
        f"extracted {len(extracted)}, skipped {len(skipped)} by filter."
    )
    print(f"Results written to {OUTPUT_DIR}/ (parse_*.json, extract_*.json, extractions.json).")


if __name__ == "__main__":
    main()
