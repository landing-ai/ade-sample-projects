
"""
doc_utils.py
------------
Utilities for document-level metadata and page counting used in the ADE → Snowflake pipeline.

Key Functions:
- `get_doc_pages(doc)`: Safely extract the number of pages in a parsed document.
    - Falls back to 1 if page count is unavailable or malformed.
    - Ensures accurate metrics reporting during pipeline runs.

Intended for use in:
- Metrics aggregation (e.g., pages per document)
- Logging and diagnostics
- Runtime safeguards for edge cases (e.g., image-only or malformed docs)

Example:
    from doc_utils import get_doc_pages
    pages = get_doc_pages(parsed_doc)
"""

from typing import Any, Optional


def _coerce_int(x: Any) -> Optional[int]:
    """
    Convert a value to an int if possible, else return None.
    Useful for fields that may be None, strings, or invalid types.
    """
    try:
        return None if x is None else int(x)
    except Exception:
        return None


def get_doc_pages(doc: Any) -> int:
    """
    Return the number of pages in a parsed document.

    Prefers the authoritative `metadata.page_count` from the DPT-3
    `V2ParseResponse`. Falls back to scanning per-element grounding in the
    structure tree (page numbers are 0-indexed, so max + 1 = total count).
    """
    page_count = _coerce_int(getattr(getattr(doc, "metadata", None), "page_count", None))
    if page_count:
        return page_count

    # Fallback: count the page nodes directly under the structure tree.
    structure = getattr(doc, "structure", None)
    pages = getattr(structure, "children", None) or []
    return len(pages) if pages else 1
