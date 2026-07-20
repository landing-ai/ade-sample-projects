"""
Section API for building document hierarchy with LandingAI ADE

The Section endpoint takes parsed markdown (with reference anchors) and returns
a hierarchical table of contents. This turns a flat wall of text into a
structured, section-aware document — the backbone of high-quality RAG chunking.
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = 'https://api.va.landing.ai'


def parse_document(file_path: str, api_key: str) -> Optional[str]:
    """
    Parse a document into markdown that contains reference anchors
    (<a id='...'></a>). These anchors are what the Section endpoint uses to
    pin each table-of-contents entry back to a location in the document.

    Args:
        file_path: Path to the PDF (or image) to parse.
        api_key: Your API key.

    Returns:
        The parsed markdown string, or None on failure.
    """
    p = Path(file_path).expanduser().resolve()
    if not p.exists():
        print(f"❌ File not found: {p}")
        return None

    print(f"📄 File: {p.name}  |  📏 {p.stat().st_size / 1_048_576:.1f} MB")

    url = f'{BASE_URL}/v1/ade/parse'
    headers = {"Authorization": f"Bearer {api_key}"}

    with p.open("rb") as fh:
        files = {"document": fh}
        resp = requests.post(url, headers=headers, files=files, timeout=120)

    if resp.status_code == 200:
        data = resp.json()
        markdown = data.get("markdown", "")
        if markdown:
            print(f"✅ Parsed {len(markdown)} characters of markdown.")
            return markdown
        print("❌ Response missing markdown:", data)
        return None

    print(f"❌ Parse failed ({resp.status_code}): {resp.text}")
    return None


def section_markdown(
    markdown: str,
    api_key: str,
    guidelines: Optional[str] = None,
    model: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Send parsed markdown to the ADE Section endpoint and get back a
    hierarchical table of contents.

    Endpoint: POST /v1/ade/section

    Args:
        markdown: Parsed markdown that includes reference anchors.
        api_key: Your API key.
        guidelines: Optional natural-language instructions to control the
            hierarchy (e.g. "Group by topic", "Treat each numbered clause as
            its own section").
        model: Optional Section model version. Defaults to the latest.

    Returns:
        The Section response dict (table_of_contents, table_of_contents_md,
        metadata), or None on failure.
    """
    url = f'{BASE_URL}/v1/ade/section'
    headers = {"Authorization": f"Bearer {api_key}"}

    # The markdown is uploaded as a file part (multipart/form-data).
    files = {"markdown": ("markdown.md", markdown.encode("utf-8"), "text/markdown")}

    data: Dict[str, str] = {}
    if guidelines:
        data["guidelines"] = guidelines
    if model:
        data["model"] = model

    resp = requests.post(url, headers=headers, files=files, data=data, timeout=120)

    if resp.status_code == 200:
        result = resp.json()
        toc = result.get("table_of_contents", [])
        print(f"✅ Section complete — {len(toc)} table-of-contents entries.")

        metadata = result.get("metadata", {})
        if metadata:
            print("\n📊 Processing stats:")
            print(f"  • Time: {metadata.get('duration_ms', 0) / 1000:.1f}s")
            print(f"  • Credits: {metadata.get('credit_usage', 'N/A')}")

        return result

    print(f"❌ Section failed ({resp.status_code}): {resp.text}")
    return None


def save_results(result: Dict[str, Any], output_dir: str, stem: str) -> None:
    """
    Save the Section response to the output folder as both the raw JSON
    hierarchy and a human-readable markdown table of contents.

    Args:
        result: The Section response dict.
        output_dir: Directory to write outputs to.
        stem: Base filename (without extension) for the output files.
    """
    out = Path(output_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    json_path = out / f"{stem}_sections.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved hierarchy JSON to: {json_path}")

    toc_md = result.get("table_of_contents_md")
    if toc_md:
        md_path = out / f"{stem}_toc.md"
        with md_path.open("w", encoding="utf-8") as f:
            f.write(toc_md)
        print(f"💾 Saved table of contents to: {md_path}")


def process_document(
    file_path: str,
    api_key: str,
    output_dir: str = "output_folder",
    guidelines: Optional[str] = None,
    model: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Complete workflow: parse a document, section it, and save the results.

    Args:
        file_path: Path to the input document.
        api_key: Your API key.
        output_dir: Where to write the section outputs.
        guidelines: Optional natural-language sectioning instructions.
        model: Optional Section model version.

    Returns:
        Dict with the parsed markdown and the Section result, or None.
    """
    print("🚀 DOCUMENT SECTIONING WORKFLOW")
    print("=" * 50)

    # Step 1: Parse the document to markdown (with reference anchors).
    print("\n1️⃣ Parsing document...")
    markdown = parse_document(file_path, api_key)
    if not markdown:
        print("Failed to parse document")
        return None

    # Step 2: Build the hierarchy from the parsed markdown.
    print("\n2️⃣ Building section hierarchy...")
    result = section_markdown(markdown, api_key, guidelines=guidelines, model=model)
    if not result:
        print("Failed to section document")
        return None

    # Step 3: Save both the JSON hierarchy and the markdown TOC.
    print("\n3️⃣ Saving results...")
    save_results(result, output_dir, Path(file_path).stem)

    return {"markdown": markdown, "sections": result}


def preview_toc(result: Dict[str, Any], max_entries: int = 25) -> None:
    """
    Print the first few table-of-contents entries with indentation by level.

    Args:
        result: The Section response dict.
        max_entries: Maximum number of entries to display.
    """
    toc = result.get("table_of_contents", [])
    print(f"📑 Table of contents ({len(toc)} entries, showing up to {max_entries}):")
    print("--------------------- START OF TOC ---------------------")
    for entry in toc[:max_entries]:
        level = entry.get("level", 1)
        indent = "  " * max(level - 1, 0)
        number = entry.get("section_number", "")
        title = entry.get("title", "")
        prefix = f"{number} " if number else ""
        print(f"{indent}{prefix}{title}")
    if len(toc) > max_entries:
        print("... (more sections)")
    print("---------------------- END OF TOC ----------------------")


if __name__ == "__main__":
    API_KEY = os.getenv("VISION_AGENT_API_KEY")
    if not API_KEY:
        raise SystemExit("Set VISION_AGENT_API_KEY in your environment or .env file.")

    INPUT_FILE = "input_folder/ibm_annual_report.pdf"

    results = process_document(INPUT_FILE, API_KEY)
    if results:
        preview_toc(results["sections"])
