#!/usr/bin/env python3
"""
Parallel Document Extractor - Apply a Pydantic schema to already-parsed
markdown files in parallel using LandingAI ADE's extract endpoint.

Reads from:
    results_folder/markdown/*.md   (produced by parallel_parser.py)

Writes:
    results_folder/extract/*.json  (full extract response per document)
    results_folder/all_extractions.csv  (one row per document)

Decoupled from parallel_parser.py so extractions can be re-run with a
different schema without re-parsing the source PDFs.
"""

import io
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from dotenv import load_dotenv
from landingai_ade import LandingAIADE
from landingai_ade.lib import pydantic_to_json_schema
from pydantic import BaseModel, Field
from tqdm import tqdm


class PaperSummary(BaseModel):
    """Structured summary for a research paper / clinical review."""
    title: str = Field(description="The paper's title, plain text.")
    authors: List[str] = Field(
        default_factory=list,
        description="List of author names in order. Empty list if not found.",
    )
    publication_year: Optional[int] = Field(
        default=None, description="4-digit publication year, or null if not found."
    )
    study_type: Optional[str] = Field(
        default=None,
        description="Type of study, e.g. 'systematic review', 'randomized controlled trial', "
                    "'observational study', 'meta-analysis', 'narrative review'.",
    )
    interventions_studied: List[str] = Field(
        default_factory=list,
        description="Treatments, drugs, or interventions evaluated. Empty list if none.",
    )
    sample_size: Optional[int] = Field(
        default=None,
        description="Total participants/patients across all groups, or null if not applicable.",
    )
    key_findings: List[str] = Field(
        default_factory=list,
        description="3-5 short bullet points capturing the paper's main results.",
    )
    conclusion: Optional[str] = Field(
        default=None,
        description="One-paragraph plain-text summary of the paper's conclusion.",
    )


SCRIPT_DIR = Path(__file__).parent
RESULTS_FOLDER = SCRIPT_DIR / "results_folder"
MARKDOWN_FOLDER = RESULTS_FOLDER / "markdown"
EXTRACT_FOLDER = RESULTS_FOLDER / "extract"
MAX_WORKERS = 6


def get_api_key() -> str:
    key = os.environ.get("VISION_AGENT_API_KEY")
    if not key:
        raise ValueError(
            "API key not found. Set VISION_AGENT_API_KEY in your environment or .env file."
        )
    return key


def collect_markdown_files(md_dir: Path) -> List[Path]:
    return sorted(p for p in md_dir.glob("*.md") if p.is_file())


def extract_one(
    md_path: Path,
    client: LandingAIADE,
    schema_json: Dict[str, Any],
    out_dir: Path,
) -> Optional[Dict[str, Any]]:
    try:
        markdown_text = md_path.read_text(encoding="utf-8")
        result = client.extract(
            schema=schema_json,
            markdown=io.BytesIO(markdown_text.encode("utf-8")),
        )
        (out_dir / f"{md_path.stem}.json").write_text(
            json.dumps(result.model_dump(), indent=2, default=str),
            encoding="utf-8",
        )
        return {
            "stem": md_path.stem,
            "extraction": result.extraction or {},
        }
    except Exception as e:
        print(f"FAILED {md_path.name}: {e}")
        return None


def combine_extractions(results: List[Dict[str, Any]], output_path: Path) -> None:
    rows: List[Dict[str, Any]] = []
    for r in sorted(results, key=lambda x: x["stem"]):
        row: Dict[str, Any] = {"document_name": f"{r['stem']}.pdf"}
        for key, value in r["extraction"].items():
            if isinstance(value, list):
                row[key] = " | ".join(str(v) for v in value)
            else:
                row[key] = value
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Combined extracts: {output_path}  ({len(df)} rows)")


def main() -> None:
    load_dotenv()

    if not MARKDOWN_FOLDER.exists():
        print(f"Markdown folder not found: {MARKDOWN_FOLDER}")
        print("Run parallel_parser.py first.")
        return

    files = collect_markdown_files(MARKDOWN_FOLDER)
    if not files:
        print(f"No markdown files in {MARKDOWN_FOLDER}")
        return

    EXTRACT_FOLDER.mkdir(parents=True, exist_ok=True)

    api_key = get_api_key()
    client = LandingAIADE(apikey=api_key)
    schema_json = pydantic_to_json_schema(PaperSummary)
    schema_path = RESULTS_FOLDER / "paper_summary_schema.json"
    schema_path.write_text(
        json.dumps(json.loads(schema_json), indent=2), encoding="utf-8"
    )

    print(f"Markdown folder: {MARKDOWN_FOLDER}")
    print(f"Extract folder : {EXTRACT_FOLDER}")
    print(f"Documents      : {len(files)}")
    print(f"Workers        : {MAX_WORKERS}")
    print(f"Schema         : PaperSummary -> {schema_path}\n")

    results: List[Dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(extract_one, fp, client, schema_json, EXTRACT_FOLDER): fp
            for fp in files
        }
        for fut in tqdm(as_completed(futures), total=len(futures), desc="Extracting"):
            res = fut.result()
            if res is not None:
                results.append(res)

    if not results:
        print("\nNo successful extractions.")
        return

    print(f"\nSuccessful: {len(results)}/{len(files)}")
    combine_extractions(results, RESULTS_FOLDER / "all_extractions.csv")


if __name__ == "__main__":
    main()
