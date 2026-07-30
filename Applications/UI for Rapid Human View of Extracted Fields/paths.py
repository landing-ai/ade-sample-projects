"""Folder layout helpers shared by the pipeline and the web app.

Every input folder follows the same shape:

    <folder>/
        documents/          source PDFs and images
        parse_results/      <stem>.parse.json + <stem>.md
        extract_results/    <stem>.extract.json
        regions/            <stem>.regions.json  (field path -> highlight boxes)
        page_images/        <stem>_p<N>.png      (rendered page cache)
        HIL_results/        <stem>.hil.json + batch_report.{json,csv}
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent
INPUT_ROOT = APP_ROOT / "input_folders"
SCHEMA_ROOT = APP_ROOT / "schemas"

# v2 Parse takes PDFs and images only. Office formats would need the v1 API,
# which this app deliberately does not use.
DOC_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp"}


@dataclass(frozen=True)
class FolderPaths:
    root: Path

    @property
    def documents(self) -> Path:
        """Where the source documents live.

        Canonically a `documents/` subfolder. If that is absent but the folder
        itself holds documents, the folder root is used instead -- some folders
        are dropped in with the PDFs sitting directly inside.
        """
        nested = self.root / "documents"
        if nested.is_dir():
            return nested
        if self.root.is_dir() and _has_documents(self.root):
            return self.root
        return nested

    @property
    def parse_results(self) -> Path:
        return self.root / "parse_results"

    @property
    def extract_results(self) -> Path:
        return self.root / "extract_results"

    @property
    def regions(self) -> Path:
        return self.root / "regions"

    @property
    def page_images(self) -> Path:
        return self.root / "page_images"

    @property
    def hil_results(self) -> Path:
        return self.root / "HIL_results"

    def ensure(self) -> None:
        for d in (
            self.documents,  # no-op when the root itself holds the documents
            self.parse_results,
            self.extract_results,
            self.regions,
            self.page_images,
            self.hil_results,
        ):
            d.mkdir(parents=True, exist_ok=True)

    def parse_json(self, stem: str) -> Path:
        return self.parse_results / f"{stem}.parse.json"

    def markdown(self, stem: str) -> Path:
        return self.parse_results / f"{stem}.md"

    def extract_json(self, stem: str) -> Path:
        return self.extract_results / f"{stem}.extract.json"

    def regions_json(self, stem: str) -> Path:
        return self.regions / f"{stem}.regions.json"

    def hil_json(self, stem: str) -> Path:
        return self.hil_results / f"{stem}.hil.json"

    def documents_list(self) -> list[Path]:
        if not self.documents.is_dir():
            return []
        return sorted(
            p
            for p in self.documents.iterdir()
            if p.is_file() and p.suffix.lower() in DOC_SUFFIXES and not p.name.startswith(".")
        )


def _has_documents(directory: Path) -> bool:
    """True when a directory holds at least one parseable file directly."""
    try:
        return any(
            p.is_file() and p.suffix.lower() in DOC_SUFFIXES and not p.name.startswith(".")
            for p in directory.iterdir()
        )
    except OSError:
        return False


def resolve_folder(folder: str) -> FolderPaths:
    """Accept either a name under input_folders/ or an absolute path.

    Browsers cannot hand back a real directory path, so the UI offers a
    dropdown of names discovered under input_folders/ plus a free-text path.
    """
    candidate = Path(folder).expanduser()
    if not candidate.is_absolute():
        candidate = INPUT_ROOT / folder
    return FolderPaths(candidate.resolve())


def list_input_folders() -> list[str]:
    """Subdirectories of input_folders/ that hold documents.

    Accepts either layout: a `documents/` subfolder, or documents sitting
    directly in the folder.
    """
    if not INPUT_ROOT.is_dir():
        return []
    return sorted(
        p.name
        for p in INPUT_ROOT.iterdir()
        if p.is_dir() and ((p / "documents").is_dir() or _has_documents(p))
    )


def list_schemas() -> list[str]:
    if not SCHEMA_ROOT.is_dir():
        return []
    return sorted(p.name for p in SCHEMA_ROOT.glob("*.json"))


def resolve_schema(schema: str) -> Path:
    candidate = Path(schema).expanduser()
    if not candidate.is_absolute():
        candidate = SCHEMA_ROOT / schema
    return candidate.resolve()
