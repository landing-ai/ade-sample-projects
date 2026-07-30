"""Resolve extracted field values back to the exact line or table cell they came from.

The chain, all in ADE v2 terms:

    extract.extraction_metadata[<path>].ranges   code point offsets into the markdown
        -> overlap against parse.structure block grounding.range
            -> narrow to the table_cell child, or the atomic_grounding visual line
                -> normalized box {xmin, ymin, xmax, ymax}, 0..1 of page width/height

Ranges are half-open: [start, end). Pages are 1-indexed throughout v2.

Note on `client.v2.ground`: the SDK exposes a server-side version of the
range-overlap join, but it returns a loosely typed `Dict[str, object]` whose
concrete shape cannot be pinned down without live API access. The join is a
handful of interval comparisons and the block -> line/cell refinement has to
happen locally against the structure tree regardless, so this module does the
whole resolution locally. That keeps it deterministic, unit-testable offline,
and free of an extra billed call per document.
"""

from __future__ import annotations

from typing import Any, Iterable

# Block types whose atomic_grounding gives one entry per visual line.
LINE_BLOCK_TYPES = {"text", "marginalia", "attestation"}


def _overlaps(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    """True when [a_start, a_end) and [b_start, b_end) share any position.

    Zero-length ranges are treated as a point so a collapsed range still
    matches the block that contains it.
    """
    if a_start == a_end:
        return b_start <= a_start < b_end or (b_start == b_end and b_start == a_start)
    if b_start == b_end:
        return a_start <= b_start < a_end
    return a_start < b_end and b_start < a_end


def _range_from(rng: Any) -> tuple[int, int] | None:
    if isinstance(rng, dict):
        start, end = rng.get("start"), rng.get("end")
        if isinstance(start, int) and isinstance(end, int):
            return start, end
    if isinstance(rng, list) and len(rng) == 2 and all(isinstance(v, int) for v in rng):
        return rng[0], rng[1]
    return None


def _as_range(node: Any) -> tuple[int, int] | None:
    """Pull (start, end) from a node, tolerating every v2 range shape.

    Blocks and pages nest it as `grounding.range`. atomic_grounding entries are
    themselves grounding objects, carrying `range` at the top level. Some
    responses also use a positional `span: [start, end]`.
    """
    if not isinstance(node, dict):
        return None
    grounding = node.get("grounding")
    if isinstance(grounding, dict):
        found = _range_from(grounding.get("range"))
        if found:
            return found
    found = _range_from(node.get("range"))
    if found:
        return found
    return _range_from(node.get("span"))


def _box_from(box: Any, page_width: float | None, page_height: float | None) -> dict | None:
    """Normalize a box in either shape.

    A dict box (`{xmin, ymin, xmax, ymax}`) is already normalized 0..1. A
    positional list box is pixel coordinates and needs the page dimensions.
    """
    if isinstance(box, dict):
        vals = {k: box.get(k) for k in ("xmin", "ymin", "xmax", "ymax")}
        if all(isinstance(v, (int, float)) for v in vals.values()):
            return {k: float(v) for k, v in vals.items()}
    if isinstance(box, list) and len(box) == 4 and all(isinstance(v, (int, float)) for v in box):
        if page_width and page_height:
            return {
                "xmin": box[0] / float(page_width),
                "ymin": box[1] / float(page_height),
                "xmax": box[2] / float(page_width),
                "ymax": box[3] / float(page_height),
            }
    return None


def _as_box(node: Any, page_width: float | None = None, page_height: float | None = None) -> dict | None:
    """Normalized box from a node, whether nested under `grounding` or top-level."""
    if not isinstance(node, dict):
        return None
    grounding = node.get("grounding")
    if isinstance(grounding, dict):
        found = _box_from(grounding.get("box"), page_width, page_height)
        if found:
            return found
    return _box_from(node.get("box"), page_width, page_height)


def _page_of(node: Any, fallback: int) -> int:
    if isinstance(node, dict):
        grounding = node.get("grounding")
        if isinstance(grounding, dict) and isinstance(grounding.get("page"), int):
            return grounding["page"]
        if isinstance(node.get("page"), int):
            return node["page"]
    return fallback


class BlockIndex:
    """Flattened, searchable view of one parse response's structure tree."""

    def __init__(self, parse: dict):
        self.pages: list[dict] = []
        self.blocks: list[dict] = []
        self._build(parse)

    def _build(self, parse: dict) -> None:
        structure = parse.get("structure")
        if not isinstance(structure, dict):
            # Fall back to the alternate top-level grounding tree if structure
            # is absent (it carries pixel boxes and `parts` instead of
            # atomic_grounding).
            structure = parse.get("grounding")
        if not isinstance(structure, dict):
            return

        for page_node in structure.get("children") or []:
            if not isinstance(page_node, dict):
                continue
            page_no = _page_of(page_node, len(self.pages) + 1)
            width = page_node.get("width")
            height = page_node.get("height")
            self.pages.append(
                {
                    "page": page_no,
                    "width": width,
                    "height": height,
                    "status": page_node.get("status"),
                    "reason": page_node.get("reason"),
                }
            )
            for block in page_node.get("children") or []:
                self._add_block(block, page_no, width, height)

    def _add_block(self, block: Any, page_no: int, width, height) -> None:
        if not isinstance(block, dict):
            return
        rng = _as_range(block)
        box = _as_box(block, width, height)
        block_page = _page_of(block, page_no)

        # Sub-regions that let us narrow a hit below whole-block granularity:
        # table cells for tables, visual lines for prose.
        sub: list[dict] = []
        for cell in block.get("children") or []:
            if not isinstance(cell, dict):
                continue
            c_rng = _as_range(cell)
            c_box = _as_box(cell, width, height)
            if c_rng and c_box:
                sub.append(
                    {
                        "kind": "cell",
                        "page": _page_of(cell, block_page),
                        "range": c_rng,
                        "box": c_box,
                        "row": cell.get("row"),
                        "col": cell.get("col"),
                    }
                )
        for entry in block.get("atomic_grounding") or block.get("parts") or []:
            if not isinstance(entry, dict):
                continue
            e_rng = _as_range(entry)
            e_box = _as_box(entry, width, height)
            if e_rng and e_box:
                sub.append(
                    {
                        "kind": "line",
                        "page": entry.get("page") or block_page,
                        "range": (int(e_rng[0]), int(e_rng[1])),
                        "box": e_box,
                    }
                )

        if rng and box:
            self.blocks.append(
                {
                    "id": block.get("id"),
                    "type": block.get("type"),
                    "page": block_page,
                    "range": rng,
                    "box": box,
                    "sub": sub,
                }
            )

        # Table cells are also standalone blocks worth matching directly, and a
        # nested table inside a cell still needs indexing.
        for child in block.get("children") or []:
            if isinstance(child, dict) and (child.get("children") or child.get("atomic_grounding")):
                self._add_block(child, page_no, width, height)

    def regions_for_ranges(self, ranges: Iterable[tuple[int, int]]) -> list[dict]:
        """Smallest sensible highlight regions covering the given markdown ranges."""
        out: list[dict] = []
        for start, end in ranges:
            for block in self.blocks:
                b_start, b_end = block["range"]
                if not _overlaps(start, end, b_start, b_end):
                    continue

                # Prefer the narrowest overlapping sub-region: a table cell or a
                # single visual line rather than the whole block.
                hits = [s for s in block["sub"] if _overlaps(start, end, s["range"][0], s["range"][1])]
                if hits:
                    for hit in hits:
                        out.append(
                            {
                                "page": hit["page"],
                                "kind": hit["kind"],
                                "block_id": block["id"],
                                **hit["box"],
                            }
                        )
                else:
                    out.append(
                        {
                            "page": block["page"],
                            "kind": "block",
                            "block_id": block["id"],
                            **block["box"],
                        }
                    )
        return _dedupe(out)

    def page_dimensions(self) -> dict[int, dict]:
        return {p["page"]: p for p in self.pages}


def _dedupe(regions: list[dict]) -> list[dict]:
    seen: set[tuple] = set()
    out: list[dict] = []
    for r in regions:
        key = (
            r["page"],
            round(r["xmin"], 5),
            round(r["ymin"], 5),
            round(r["xmax"], 5),
            round(r["ymax"], 5),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    out.sort(key=lambda r: (r["page"], r["ymin"], r["xmin"]))
    return out


def _is_leaf(node: Any) -> bool:
    """An extraction_metadata leaf is {"value": ..., "ranges": [...]}.

    Checked structurally rather than by key presence alone so a schema field
    literally named "value" cannot be mistaken for a leaf.
    """
    return (
        isinstance(node, dict)
        and "value" in node
        and set(node.keys()) <= {"value", "ranges", "confidence"}
    )


def flatten_metadata(node: Any, prefix: str = "") -> dict[str, dict]:
    """extraction_metadata tree -> {dotted path: {"value", "ranges"}}."""
    out: dict[str, dict] = {}
    if _is_leaf(node):
        if prefix:
            out[prefix] = {"value": node.get("value"), "ranges": node.get("ranges") or []}
        return out
    if isinstance(node, dict):
        for key, child in node.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            out.update(flatten_metadata(child, child_prefix))
    elif isinstance(node, list):
        for i, child in enumerate(node):
            out.update(flatten_metadata(child, f"{prefix}[{i}]"))
    return out


def resolve_regions(parse: dict, extract: dict) -> dict[str, Any]:
    """Build the path -> highlight regions map for one document.

    Returns {"paired": bool, "page_count": int, "regions": {path: [region]}}.
    `paired` is False when the extract did not come from this parse, in which
    case the ranges index into different markdown and must not be trusted.
    """
    parse_job = ((parse.get("metadata") or {}).get("job_id")) or None
    doc_id = ((extract.get("metadata") or {}).get("doc_id")) or None
    paired = bool(parse_job) and bool(doc_id) and parse_job == doc_id

    index = BlockIndex(parse)
    meta = flatten_metadata(extract.get("extraction_metadata") or {})

    regions: dict[str, list[dict]] = {}
    for path, leaf in meta.items():
        ranges: list[tuple[int, int]] = []
        for r in leaf.get("ranges") or []:
            if isinstance(r, dict) and isinstance(r.get("start"), int) and isinstance(r.get("end"), int):
                ranges.append((r["start"], r["end"]))
            elif isinstance(r, list) and len(r) == 2 and all(isinstance(v, int) for v in r):
                ranges.append((r[0], r[1]))
        # No ranges means a synthesized value with no source text. It stays in
        # the map as an empty list: the field is still listed and editable, it
        # simply has nothing to highlight.
        regions[path] = index.regions_for_ranges(ranges) if ranges else []

    page_count = ((parse.get("metadata") or {}).get("page_count")) or len(index.pages) or 1

    return {
        "paired": paired,
        "parse_job_id": parse_job,
        "doc_id": doc_id,
        "page_count": page_count,
        "pages": index.page_dimensions(),
        "regions": regions,
    }
