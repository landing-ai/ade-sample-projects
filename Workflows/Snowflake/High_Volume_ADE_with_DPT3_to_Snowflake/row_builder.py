"""
row_builder.py
--------------
Turn a DPT-3 parse result + extract result into flat, Snowflake-ready rows.

Produces four row sets per document:
  - main_row       : one row of header fields          -> INVOICES_MAIN
  - line_rows      : one row per line item             -> INVOICE_LINE_ITEMS
  - block_rows     : one row per parsed block          -> PARSED_BLOCKS
  - markdown_record: full markdown (VARIANT)           -> MARKDOWN

DPT-3 specifics handled here:
  - Extraction values live in ``extract_result.extraction`` (a plain dict).
  - Parsed content is a ``structure`` tree (page -> block); a block carries no
    text, so we slice it out of the document markdown via ``grounding.range``
    (``range_units == "unicode_codepoints"``).
  - Grounding boxes are normalized 0-1 ``xmin/ymin/xmax/ymax`` -> box_l/t/r/b.
  - Pages are 1-indexed.
  - Field evidence lives in ``extraction_metadata[...]['ranges']``.
"""

from __future__ import annotations

import os
import re
import uuid
import json
import math
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional, Tuple

_ANCHOR_RE = re.compile(r"<a id='[^']*'>\s*</a>")


# ---------------------------------------------------------------- helpers -----

def _to_int(x: Any) -> Optional[int]:
    try:
        if x is None:
            return None
        if isinstance(x, bool):
            return int(x)
        if isinstance(x, int):
            return x
        if isinstance(x, float) and math.isfinite(x):
            return int(round(x))
        s = str(x).strip()
        return int(s) if s and all(c in "+-0123456789" for c in s) else None
    except Exception:
        return None


def _to_float(x: Any) -> Optional[float]:
    try:
        if x is None:
            return None
        if isinstance(x, (int, float)) and math.isfinite(float(x)):
            return float(x)
        return float(str(x).strip())
    except Exception:
        return None


def _dig(container: Any, *keys: str, default: Any = None) -> Any:
    cur = container
    for k in keys:
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            cur = getattr(cur, k, None)
        if cur is None:
            return default
    return cur


def _strip_anchor(md: Optional[str]) -> Optional[str]:
    return _ANCHOR_RE.sub("", md).strip() if md else md


def _box_ltrb(grounding: Any) -> Tuple[Optional[float], ...]:
    box = getattr(grounding, "box", None)
    if box is None:
        return (None, None, None, None)
    return (
        _to_float(getattr(box, "xmin", None)),
        _to_float(getattr(box, "ymin", None)),
        _to_float(getattr(box, "xmax", None)),
        _to_float(getattr(box, "ymax", None)),
    )


def _text_from_range(md: str, grounding: Any) -> Optional[str]:
    rng = getattr(grounding, "range", None)
    if rng is None or not md:
        return None
    s, e = _to_int(getattr(rng, "start", None)), _to_int(getattr(rng, "end", None))
    return md[s:e] if (s is not None and e is not None) else None


def iter_blocks(parse_result: Any) -> Iterator[Dict[str, Any]]:
    """Yield one dict per block (direct children of each page in the
    ``structure`` tree). Table cells and other nested descendants are not
    emitted individually, mirroring block-level granularity."""
    md = getattr(parse_result, "markdown", None) or ""
    structure = getattr(parse_result, "structure", None)
    for page in (getattr(structure, "children", None) or []):
        page_idx = _to_int(getattr(page, "page", None))
        for el in (getattr(page, "children", None) or []):
            g = getattr(el, "grounding", None)
            el_page = _to_int(getattr(g, "page", None))
            l, t, r, b = _box_ltrb(g)
            text = getattr(el, "markdown", None) or _text_from_range(md, g)
            yield {
                "id": getattr(el, "id", None),
                "type": getattr(el, "type", None),
                "text": _strip_anchor(text),
                "page": el_page if el_page is not None else page_idx,
                "box_l": l, "box_t": t, "box_r": r, "box_b": b,
            }


def _evidence(meta: Any, *path: str) -> Optional[str]:
    """Return the DPT-3 ``ranges`` evidence for a field as a JSON string, or
    None. ``extraction_metadata`` mirrors the schema nesting; each leaf carries
    ``ranges`` (character ranges into the markdown) and ``value``."""
    node = _dig(meta, *path)
    if not node:
        return None
    ranges = node.get("ranges") if isinstance(node, dict) else getattr(node, "ranges", None)
    return json.dumps(ranges, default=str) if ranges else None


# ------------------------------------------------------------ main builder ----

def rows_from_doc(
    fp: str,
    parse_result: Any,
    extract_result: Any,
    run_id: str,
    sent_at: datetime,
    sdk_version: str,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any], str]:
    doc_name = os.path.basename(fp)
    doc_uuid = str(uuid.uuid4())

    markdown = getattr(parse_result, "markdown", None)
    f = getattr(extract_result, "extraction", None)
    m = getattr(extract_result, "extraction_metadata", None)
    schema_violation = getattr(extract_result, "schema_violation_error", None)

    base = {
        "run_id": run_id,
        "invoice_uuid": doc_uuid,
        "document_name": doc_name,
        "sent_at": sent_at,
        "ade_sdk_version": sdk_version,
    }

    markdown_record = {
        "RUN_ID": run_id, "INVOICE_UUID": doc_uuid, "DOCUMENT_NAME": doc_name,
        "SENT_AT": sent_at, "ADE_SDK_VERSION": sdk_version, "MARKDOWN": markdown,
    }

    block_rows: List[Dict[str, Any]] = []
    for blk in iter_blocks(parse_result):
        block_rows.append({
            **base,
            "block_id": str(blk["id"] or f"{doc_uuid}:{uuid.uuid4().hex[:12]}"),
            "block_type": blk["type"],
            "text": blk["text"],
            "page": _to_int(blk["page"]),
            "box_l": blk["box_l"], "box_t": blk["box_t"],
            "box_r": blk["box_r"], "box_b": blk["box_b"],
        })

    main_row: Dict[str, Any] = {
        **base,
        "schema_violation_error": schema_violation,
        # invoice_info
        "invoice_date_raw": _dig(f, "invoice_info", "invoice_date_raw"),
        "invoice_date": _dig(f, "invoice_info", "invoice_date"),
        "invoice_number": _dig(f, "invoice_info", "invoice_number"),
        "order_date": _dig(f, "invoice_info", "order_date"),
        "po_number": _dig(f, "invoice_info", "po_number"),
        "status": _dig(f, "invoice_info", "status"),
        # customer_info
        "sold_to_name": _dig(f, "customer_info", "sold_to_name"),
        "sold_to_address": _dig(f, "customer_info", "sold_to_address"),
        "customer_email": _dig(f, "customer_info", "customer_email"),
        # company_info
        "supplier_name": _dig(f, "company_info", "supplier_name"),
        "supplier_address": _dig(f, "company_info", "supplier_address"),
        "supplier_email": _dig(f, "company_info", "email"),
        "supplier_phone": _dig(f, "company_info", "phone"),
        # order_details
        "payment_terms": _dig(f, "order_details", "payment_terms"),
        "ship_via": _dig(f, "order_details", "ship_via"),
        "ship_date": _dig(f, "order_details", "ship_date"),
        "tracking_number": _dig(f, "order_details", "tracking_number"),
        # totals_summary
        "currency": _dig(f, "totals_summary", "currency"),
        "total_due_raw": _dig(f, "totals_summary", "total_due_raw"),
        "total_due": _dig(f, "totals_summary", "total_due"),
        "subtotal": _dig(f, "totals_summary", "subtotal"),
        "tax": _dig(f, "totals_summary", "tax"),
        "shipping": _dig(f, "totals_summary", "shipping"),
        # evidence (DPT-3 ranges) for a couple of key fields
        "supplier_name_ref": _evidence(m, "company_info", "supplier_name"),
        "total_due_ref": _evidence(m, "totals_summary", "total_due"),
    }

    line_rows: List[Dict[str, Any]] = []
    for idx, li in enumerate(_dig(f, "line_items", default=[]) or []):
        line_rows.append({
            **base,
            "line_index": idx,
            "line_number": _dig(li, "line_number"),
            "sku": _dig(li, "sku"),
            "description": _dig(li, "description"),
            "quantity": _dig(li, "quantity"),
            "unit_price": _dig(li, "unit_price"),
            "amount": _dig(li, "amount"),
        })

    return main_row, line_rows, block_rows, markdown_record, doc_uuid
