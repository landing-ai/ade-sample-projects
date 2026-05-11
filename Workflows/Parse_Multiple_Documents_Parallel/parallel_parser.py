#!/usr/bin/env python3
"""
Parallel Document Parser - Batch parsing of documents using LandingAI ADE
with ThreadPoolExecutor (sync parallelism, no asyncio).

Self-contained workflow: drop documents into ./input_folder, results
land in ./results_folder.

Output structure:
    results_folder/
    ├── json/                  # Full parse JSON response per document
    ├── markdown/              # Per-document markdown
    ├── combined_corpus.md     # All documents concatenated with headers
    └── all_chunks.csv         # All chunks across all documents (one row per chunk)

Run parallel_extractor.py afterward to apply a structured-extraction schema
to the saved markdown without re-parsing.
"""

import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import landingai_ade
import pandas as pd
from dotenv import load_dotenv
from landingai_ade import LandingAIADE
from tqdm import tqdm


SCRIPT_DIR = Path(__file__).parent
INPUT_FOLDER = SCRIPT_DIR / "input_folder"
OUTPUT_FOLDER = SCRIPT_DIR / "results_folder"
MAX_WORKERS = 6
SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


def get_api_key() -> str:
    key = os.environ.get("VISION_AGENT_API_KEY")
    if not key:
        raise ValueError(
            "API key not found. Set VISION_AGENT_API_KEY in your environment or .env file."
        )
    return key


def setup_output_dirs(base: Path) -> Dict[str, Path]:
    dirs = {"json": base / "json", "markdown": base / "markdown"}
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return dirs


def collect_input_files(input_dir: Path) -> List[Path]:
    return sorted(
        p for p in input_dir.glob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def clean_chunk_text(text: str) -> str:
    return re.sub(r"<a id='[^']*'>\s*</a>", "", text).strip()


def extract_chunks_data(
    parse_result: Any,
    document_name: str,
    processed_at: str,
    ade_version: str,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    chunks = getattr(parse_result, "chunks", None) or []
    model_version = getattr(getattr(parse_result, "metadata", None), "version", "unknown")

    for idx, ch in enumerate(chunks):
        grounding = getattr(ch, "grounding", None)
        box = getattr(grounding, "box", None) if grounding else None
        page = getattr(grounding, "page", None) if grounding else None
        raw = getattr(ch, "markdown", "") or ""
        text = clean_chunk_text(raw)

        rows.append({
            "document_name": document_name,
            "chunk_id": getattr(ch, "id", None),
            "chunk_sequence_number": idx,
            "chunk_type": getattr(ch, "type", None),
            "chunk_content": text,
            "chunk_text_length": len(text),
            "chunk_word_count": len(text.split()) if text else 0,
            "page": page,
            "box_l": getattr(box, "left", None) if box else None,
            "box_t": getattr(box, "top", None) if box else None,
            "box_r": getattr(box, "right", None) if box else None,
            "box_b": getattr(box, "bottom", None) if box else None,
            "processed_at": processed_at,
            "ade_version": ade_version,
            "model_version": model_version,
        })
    return rows


def process_document(
    file_path: Path,
    client: LandingAIADE,
    output_dirs: Dict[str, Path],
    ade_version: str,
) -> Optional[Dict[str, Any]]:
    try:
        processed_at = datetime.now(timezone.utc).isoformat()
        parse_result = client.parse(document=file_path)

        stem = file_path.stem
        (output_dirs["json"] / f"{stem}.json").write_text(
            json.dumps(parse_result.model_dump(), indent=2, default=str),
            encoding="utf-8",
        )
        (output_dirs["markdown"] / f"{stem}.md").write_text(
            parse_result.markdown, encoding="utf-8"
        )

        chunks_data = extract_chunks_data(
            parse_result, file_path.name, processed_at, ade_version
        )
        return {
            "file_path": file_path,
            "markdown": parse_result.markdown,
            "chunks_data": chunks_data,
        }
    except Exception as e:
        print(f"FAILED {file_path.name}: {e}")
        return None


def combine_outputs(
    results: List[Dict[str, Any]],
    output_base: Path,
) -> None:
    """Write a single combined markdown corpus and a single combined chunks CSV."""
    results_sorted = sorted(results, key=lambda r: r["file_path"].name)

    combined_md_parts: List[str] = []
    all_chunks: List[Dict[str, Any]] = []
    for r in results_sorted:
        name = r["file_path"].name
        combined_md_parts.append(f"\n\n---\n\n# {name}\n\n{r['markdown']}")
        all_chunks.extend(r["chunks_data"])

    (output_base / "combined_corpus.md").write_text(
        "".join(combined_md_parts).lstrip(), encoding="utf-8"
    )

    df = pd.DataFrame(all_chunks)
    df.to_csv(output_base / "all_chunks.csv", index=False)
    print(f"Combined corpus  : {output_base / 'combined_corpus.md'}")
    print(f"Combined chunks  : {output_base / 'all_chunks.csv'}  ({len(df)} rows)")


def main() -> None:
    load_dotenv()

    if not INPUT_FOLDER.exists():
        print(f"Input folder not found: {INPUT_FOLDER}")
        return

    output_dirs = setup_output_dirs(OUTPUT_FOLDER)
    files = collect_input_files(INPUT_FOLDER)
    if not files:
        print(f"No supported documents in {INPUT_FOLDER}")
        return

    api_key = get_api_key()
    client = LandingAIADE(apikey=api_key)
    ade_version = landingai_ade.__version__

    print(f"Input folder : {INPUT_FOLDER}")
    print(f"Output folder: {OUTPUT_FOLDER}")
    print(f"Documents    : {len(files)}")
    print(f"Workers      : {MAX_WORKERS}")
    print(f"ADE version  : {ade_version}\n")

    results: List[Dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(process_document, fp, client, output_dirs, ade_version): fp
            for fp in files
        }
        for fut in tqdm(as_completed(futures), total=len(futures), desc="Parsing"):
            res = fut.result()
            if res is not None:
                results.append(res)

    if not results:
        print("\nNo successful results to combine.")
        return

    print(f"\nSuccessful: {len(results)}/{len(files)}")
    combine_outputs(results, OUTPUT_FOLDER)


if __name__ == "__main__":
    main()
