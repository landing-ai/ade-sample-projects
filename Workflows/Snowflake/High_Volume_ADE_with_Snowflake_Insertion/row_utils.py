"""
row_utils.py
------------
Helper functions for safely extracting, formatting, and transforming parsed fields
into structured row values for database insertion in the ADE → Snowflake pipeline.

Includes:
- Safe dictionary access and conversion utilities
- Enum, string, float, and integer formatting
- Grounding metadata extraction (e.g., confidence, reference chunks)
- Layout coordinate utilities (e.g., left/top/bottom/right box positions)
- JSON serialization helpers for structured record storage

Used primarily by:
- `row_builder.py` to construct main, line item, and block-level records
- Markdown and metrics logic for enhanced traceability and diagnostics

Functions:
- `_dig`, `_add_meta`, `_to_int`, `_to_float`, `_enum_to_str`, `_asdict`, `_jsonify`
- `iter_parse_blocks` — walks a DPT-3 parse `structure` tree and yields one
  block dict per element (id, type, text, page, box l/t/r/b)
- `_strip_anchor` — removes the `<a id='...'></a>` prefix ADE embeds in markdown
- `pkg_version` — resolves version of a given installed Python package
- `_first` — returns the first item in a list or None

These utilities ensure robustness against missing fields, type mismatches,
and inconsistent schema returns in the document parsing workflow.
"""


import math
import re
import json
import dataclasses
import importlib
from typing import Any, Dict, Iterator, Optional, Tuple
from importlib.metadata import version as _pkg_version, PackageNotFoundError

# Matches the anchor tag ADE prepends to each block's markdown, e.g.
# "<a id='abc'></a>Some text" -> "Some text".
_ANCHOR_RE = re.compile(r"<a id='[^']*'>\s*</a>")

# --- Core utility functions ---

def pkg_version(dist_name: str, default: str = "unknown") -> str:
    try:
        return _pkg_version(dist_name)
    except PackageNotFoundError:
        try:
            mod = importlib.import_module(dist_name.replace("-", "_"))
            return getattr(mod, "__version__", default)
        except Exception:
            return default

def _enum_to_str(x: Any) -> Any:
    if x is None:
        return None
    try:
        return getattr(x, "name", None) or getattr(x, "value", None) or str(x)
    except Exception:
        return str(x)

def _to_int(x: Any) -> Optional[int]:
    try:
        if x is None: return None
        if isinstance(x, bool): return int(x)
        if isinstance(x, int): return x
        if isinstance(x, float) and math.isfinite(x): return int(round(x))
        if hasattr(x, "value"): return _to_int(getattr(x, "value"))
        if isinstance(x, str):
            s = x.strip()
            return int(s) if s and all(c in "+-0123456789" for c in s) else None
    except Exception:
        return None

def _to_float(x: Any) -> Optional[float]:
    try:
        if x is None: return None
        if isinstance(x, (int, float)) and math.isfinite(float(x)): return float(x)
        if hasattr(x, "value"): return _to_float(getattr(x, "value"))
        if isinstance(x, str): return float(x.strip())
        return float(x)
    except Exception:
        return None

def _asdict(obj: Any) -> Any:
    if obj is None:
        return None
    try:
        dump = getattr(obj, "model_dump", None) or getattr(obj, "dict", None)
        if callable(dump):
            return dump()
    except Exception:
        pass
    try:
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
    except Exception:
        pass
    try:
        if isinstance(obj, dict):
            return obj
        return dict(obj.__dict__)
    except Exception:
        return obj

def _dig(container: Any, *keys: str, default=None) -> Any:
    if container is None:
        return default
    cur = container
    for k in keys:
        if cur is None:
            return default
        if isinstance(cur, dict):
            cur = cur.get(k, default if k == keys[-1] else None)
            continue
        if hasattr(cur, k):
            try:
                cur = getattr(cur, k)
                continue
            except Exception:
                return default
        try:
            if hasattr(cur, "model_dump"):
                cur = cur.model_dump().get(k, default if k == keys[-1] else None)
                continue
        except Exception:
            pass
        return default
    return cur if cur is not None else default

def _first(it, default=None):
    try:
        for x in it:
            return x
        return default
    except Exception:
        return default

def _jsonify(x: Any) -> Any:
    v = _asdict(x)
    try:
        json.dumps(v)
        return v
    except Exception:
        return str(v)

def _strip_anchor(md: Optional[str]) -> Optional[str]:
    """Remove the ``<a id='...'></a>`` anchor ADE prepends to block markdown."""
    if md is None:
        return None
    return _ANCHOR_RE.sub("", md).strip()


def _ltbr_from_grounding(grounding: Any) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    Map a DPT-3 ``V2ParseNodeGrounding.box`` (xmin/ymin/xmax/ymax, normalized
    0-1) to the (left, top, right, bottom) convention used by our tables.
    """
    box = getattr(grounding, "box", None) if grounding is not None else None
    if box is None:
        return (None, None, None, None)
    return (
        _to_float(getattr(box, "xmin", None)),
        _to_float(getattr(box, "ymin", None)),
        _to_float(getattr(box, "xmax", None)),
        _to_float(getattr(box, "ymax", None)),
    )


def _text_from_range(md: str, grounding: Any) -> Optional[str]:
    """
    Slice a block's text out of the document-level markdown using its
    ``grounding.range`` (``start``/``end``). DPT-3 blocks do not duplicate
    text — they reference ranges into the top-level markdown, and the parse
    metadata reports ``range_units = unicode_codepoints`` so Python string
    slicing lines up exactly.
    """
    rng = getattr(grounding, "range", None) if grounding is not None else None
    if rng is None or not md:
        return None
    start = _to_int(getattr(rng, "start", None))
    end = _to_int(getattr(rng, "end", None))
    if start is None or end is None:
        return None
    return md[start:end]


def iter_parse_blocks(parse_result: Any) -> Iterator[Dict[str, Any]]:
    """
    Walk a DPT-3 ``V2ParseResponse.structure`` tree and yield one dict per
    block (the direct children of each page). Each dict has: ``id``, ``type``,
    ``text``, ``page``, ``box_l``, ``box_t``, ``box_r``, ``box_b``.

    Text comes from the block's own ``markdown`` when present, otherwise it is
    sliced from the document-level markdown via the block's ``grounding.range``.

    We emit page-level blocks (not every nested descendant such as individual
    table cells) to mirror the granularity of the flat chunk list from earlier
    ADE versions. To capture the full hierarchy instead, recurse into each
    element's ``children``.
    """
    md = getattr(parse_result, "markdown", None) or ""
    structure = getattr(parse_result, "structure", None)
    pages = getattr(structure, "children", None) or []
    for page_node in pages:
        page_idx = _to_int(getattr(page_node, "page", None))
        for el in (getattr(page_node, "children", None) or []):
            grounding = getattr(el, "grounding", None)
            el_page = _to_int(getattr(grounding, "page", None))
            l, t, r, b = _ltbr_from_grounding(grounding)
            text = getattr(el, "markdown", None) or _text_from_range(md, grounding)
            yield {
                "id": getattr(el, "id", None),
                "type": getattr(el, "type", None),
                "text": _strip_anchor(text),
                "page": el_page if el_page is not None else page_idx,
                "box_l": l,
                "box_t": t,
                "box_r": r,
                "box_b": b,
            }

def _add_meta(row: Dict[str, Any], meta: Any, section: str, field: str, out_prefix: str) -> None:
    """
    Record extraction evidence for one field into ``{out_prefix}_ref`` and
    ``{out_prefix}_conf``.

    DPT-3 ``extraction_metadata`` mirrors the schema nesting; each leaf field
    carries ``ranges`` (character ranges into the parse markdown that locate the
    evidence) and ``value``. There is no confidence score, so ``_conf`` stays
    null unless a legacy ``confidence``/``score`` key is present. Legacy
    ``chunk_references`` are still honored as a fallback.
    """
    if not meta:
        row[f"{out_prefix}_ref"] = None
        row[f"{out_prefix}_conf"] = None
        return

    node = _dig(meta, section, field, default=None)
    if not node:
        row[f"{out_prefix}_ref"] = None
        row[f"{out_prefix}_conf"] = None
        return

    # DPT-3 evidence: `ranges` (list of {start, end}). Fall back to legacy refs.
    refs = node.get("ranges") if isinstance(node, dict) else _dig(node, "ranges", default=None)
    if refs is None:
        refs = node.get("chunk_references") if isinstance(node, dict) else _dig(node, "chunk_references", default=None)
    if refs is None:
        refs = node.get("chunk_reference") if isinstance(node, dict) else _dig(node, "chunk_reference", default=None)
        if refs is not None and not isinstance(refs, list):
            refs = [refs]

    conf = node.get("confidence") if isinstance(node, dict) else _dig(node, "confidence", default=None)
    if conf is None:
        conf = node.get("score") if isinstance(node, dict) else _dig(node, "score", default=None)

    row[f"{out_prefix}_ref"] = _jsonify(refs) if refs else None
    row[f"{out_prefix}_conf"] = _to_float(conf)
