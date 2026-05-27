"""Helpers for working with DPT-3 v2 parse responses.

Centralizes:
- structure walking
- quote-to-span resolution
- span-to-grounding lookup (chunk box + precise parts/cell boxes)
- chunking for embedding
- coordinate scaling for overlay rendering
- precision metric (highlight area %, chunk-vs-precise ratio)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from PIL import Image, ImageDraw

LEAF_CHUNK_TYPES = {
    "text", "marginalia", "figure", "table",
    "logo", "card", "scan_code", "attestation",
}


@dataclass
class Chunk:
    """One indexable unit: a top-level element with its slice of markdown.
    Tables are emitted as a single chunk; cells stay queryable via grounding."""
    doc_id: str
    element_id: str
    element_type: str
    page: int
    span: list[int]
    text: str


@dataclass
class GroundingMatch:
    """An element whose span overlaps a query span.
    chunk_box = element-level box (what v1-style grounding would have given).
    precise_boxes = the actual parts/cells overlapping the query, or [chunk_box]
                    for non-text elements that have empty parts."""
    element_id: str
    element_type: str
    page: int
    span: list[int]
    chunk_box: list[float]
    precise_boxes: list[list[float]]


def _spans_overlap(a: list[int], b: list[int]) -> bool:
    """Half-open span overlap test: [a0, a1) overlaps [b0, b1)."""
    return a[0] < b[1] and a[1] > b[0]


def iter_elements(structure: dict) -> Iterator[tuple[dict, int]]:
    """Yield (node, page_number) for every non-document, non-page element.
    Includes intermediate nodes like `table` and their `td`/`th` cell children."""
    def walk(node, current_page):
        ntype = node.get("type")
        if ntype == "page":
            current_page = node["page"]
        elif ntype not in (None, "document"):
            yield node, current_page
        for child in node.get("children", []):
            yield from walk(child, current_page)
    yield from walk(structure, None)


def iter_chunks(parse_response: dict, doc_id: str) -> Iterator[Chunk]:
    """Top-level chunker: one chunk per leaf-ish element (text, table, figure,
    marginalia, logo, card, scan_code, attestation).
    Does NOT recurse into table cells — the table is one chunk; cells remain
    queryable via the grounding map."""
    markdown = parse_response["markdown"]
    structure = parse_response["structure"]

    def walk(node, current_page):
        ntype = node.get("type")
        if ntype == "page":
            current_page = node["page"]
        elif ntype in LEAF_CHUNK_TYPES:
            span = node["span"]
            text = markdown[span[0]:span[1]].strip()
            if text:
                yield Chunk(
                    doc_id=doc_id,
                    element_id=str(node["id"]),
                    element_type=ntype,
                    page=current_page if current_page is not None else 0,
                    span=list(span),
                    text=text,
                )
            return  # do not chunk the table's cells separately
        for child in node.get("children", []):
            yield from walk(child, current_page)

    yield from walk(structure, None)


def find_quote_span(quote: str, markdown: str) -> list[list[int]] | None:
    """Locate a verbatim quote in markdown.

    Returns [[start, end]] (half-open offsets into the original markdown) or
    None on miss.

    Two-stage matching:
    1. Exact str.find — fast path when the LLM preserved formatting.
    2. Whitespace-normalized fallback — LLMs typically collapse newlines to
       spaces when quoting, but the source has hard line breaks. We collapse
       all whitespace runs to a single space in both quote and markdown,
       search there, then map the match back to original-markdown offsets."""
    quote = quote.strip()
    if not quote:
        return None

    # Stage 1: exact match
    idx = markdown.find(quote)
    if idx != -1:
        return [[idx, idx + len(quote)]]

    # Stage 2: whitespace-normalized match
    norm_quote = " ".join(quote.split())
    if not norm_quote:
        return None

    norm_chars: list[str] = []
    norm_to_orig: list[int] = []  # for each char in norm_md, its position in markdown
    last_was_space = True  # treat leading whitespace as already-collapsed
    for i, ch in enumerate(markdown):
        if ch.isspace():
            if not last_was_space:
                norm_chars.append(" ")
                norm_to_orig.append(i)
                last_was_space = True
        else:
            norm_chars.append(ch)
            norm_to_orig.append(i)
            last_was_space = False
    norm_md = "".join(norm_chars)

    norm_idx = norm_md.find(norm_quote)
    if norm_idx == -1:
        return None
    last_norm_idx = norm_idx + len(norm_quote) - 1
    if last_norm_idx >= len(norm_to_orig):
        return None
    orig_start = norm_to_orig[norm_idx]
    orig_end = norm_to_orig[last_norm_idx] + 1  # half-open
    return [[orig_start, orig_end]]


def get_grounding(spans: list[list[int]], parse_response: dict) -> list[GroundingMatch]:
    """For each element whose span overlaps any query span, return a
    GroundingMatch with both the chunk-level box and the precise lines/cells
    that actually contain the overlap.

    For text and marginalia: precise_boxes = parts entries that overlap.
    For tables: parts is empty, but td/th children get matched separately
    (each cell has its own grounding entry).
    For other non-text elements: precise_boxes = [chunk_box]."""
    structure = parse_response["structure"]
    grounding = parse_response["grounding"]
    matches: dict[str, GroundingMatch] = {}

    for elem, page in iter_elements(structure):
        if not any(_spans_overlap(elem["span"], s) for s in spans):
            continue
        eid = str(elem["id"])
        if eid in matches:
            continue
        g = grounding.get(eid)
        if not g:
            continue
        parts = g.get("parts", []) or []
        precise = [p["box"] for p in parts if any(_spans_overlap(p["span"], s) for s in spans)]
        if not precise:
            precise = [g["box"]]
        matches[eid] = GroundingMatch(
            element_id=eid,
            element_type=elem["type"],
            page=page if page is not None else g.get("page", 0),
            span=list(elem["span"]),
            chunk_box=list(g["box"]),
            precise_boxes=[list(b) for b in precise],
        )
    return list(matches.values())


def cluster_matches(
    matches: list[GroundingMatch],
) -> list[tuple[GroundingMatch, GroundingMatch]]:
    """Group matches whose spans overlap into clusters. For each cluster return
    (outer, inner) — outer has the largest span (v1-style "chunk" view), inner
    has the smallest (v2 precise view).

    For a quote inside a table cell, get_grounding returns both the `table` and
    the `td`; this collapses that pair into (table, td). For a quote inside a
    paragraph, both outer and inner are the paragraph itself."""
    if not matches:
        return []
    sorted_m = sorted(matches, key=lambda m: (m.span[0], -m.span[1]))
    clusters: list[list[GroundingMatch]] = []
    for m in sorted_m:
        for cluster in clusters:
            if any(_spans_overlap(m.span, mm.span) for mm in cluster):
                cluster.append(m)
                break
        else:
            clusters.append([m])
    return [
        (
            max(c, key=lambda m: m.span[1] - m.span[0]),
            min(c, key=lambda m: m.span[1] - m.span[0]),
        )
        for c in clusters
    ]


def get_page_meta(parse_response: dict, page: int) -> dict | None:
    """Return the page node (with width, height, dpi, unit, status) for a given page index."""
    for p in parse_response["structure"]["children"]:
        if p.get("type") == "page" and p.get("page") == page:
            return p
    return None


def _box_area(box: list[float]) -> float:
    return max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1])


def precision_metric(matches: list[GroundingMatch], parse_response: dict) -> dict:
    """Compare chunk-level vs precise highlight area, as % of summed page area.
    Returns {chunk_pct, precise_pct, ratio} where ratio = chunk_area / precise_area.

    Uses cluster_matches to avoid double-counting nested matches: when a quote
    falls inside a table cell, the table-level chunk_box represents the v1 view
    and the cell's box represents the v2 view; we don't sum both."""
    if not matches:
        return {"chunk_pct": 0.0, "precise_pct": 0.0, "ratio": 0.0}

    chunk_area_by_page: dict[int, float] = {}
    precise_area_by_page: dict[int, float] = {}
    for outer, inner in cluster_matches(matches):
        chunk_area_by_page[outer.page] = chunk_area_by_page.get(outer.page, 0.0) + _box_area(outer.chunk_box)
        for b in inner.precise_boxes:
            precise_area_by_page[inner.page] = precise_area_by_page.get(inner.page, 0.0) + _box_area(b)

    pages_touched = set(chunk_area_by_page) | set(precise_area_by_page)
    total_page_area = 0.0
    for page in pages_touched:
        pmeta = get_page_meta(parse_response, page)
        if pmeta and pmeta.get("width") and pmeta.get("height"):
            total_page_area += pmeta["width"] * pmeta["height"]

    total_chunk = sum(chunk_area_by_page.values())
    total_precise = sum(precise_area_by_page.values())
    chunk_pct = (total_chunk / total_page_area * 100) if total_page_area else 0.0
    precise_pct = (total_precise / total_page_area * 100) if total_page_area else 0.0
    ratio = (total_chunk / total_precise) if total_precise > 0 else 0.0
    return {"chunk_pct": chunk_pct, "precise_pct": precise_pct, "ratio": ratio}


# ---- Rendering ----

def draw_overlays(
    image: Image.Image,
    boxes: list[list[float]],
    page_width: float,
    page_height: float,
    *,
    outline: tuple[int, int, int, int] = (220, 30, 30, 255),
    fill: tuple[int, int, int, int] | None = (255, 230, 0, 90),
    outline_width: int = 2,
) -> Image.Image:
    """Draw translucent rectangles on a copy of the page image.

    Boxes are in API coordinate space (pt for PDFs, px for images) and are
    rescaled to the actual image pixel dimensions using page_width/height
    from the parse response's page metadata."""
    result = image.convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    scale_x = result.width / page_width if page_width else 1.0
    scale_y = result.height / page_height if page_height else 1.0
    for box in boxes:
        l, t, r, b = box
        px_box = (l * scale_x, t * scale_y, r * scale_x, b * scale_y)
        draw.rectangle(px_box, outline=outline, fill=fill, width=outline_width)
    return Image.alpha_composite(result, overlay)


def render_dual_overlay(
    image: Image.Image,
    matches: list[GroundingMatch],
    page: int,
    page_width: float,
    page_height: float,
) -> Image.Image:
    """Draw the chunk-level box (faint gray outline, no fill) UNDER the
    precise boxes (red outline, yellow translucent fill). The contrast
    visually demonstrates the line-/cell-level upgrade over chunk grounding.

    Uses cluster_matches so nested matches (table+cell) render as one chunk
    outline (the table) and one precise highlight (the cell), not both."""
    page_matches = [m for m in matches if m.page == page]
    clusters = cluster_matches(page_matches)
    chunk_boxes = [outer.chunk_box for outer, _ in clusters]
    precise_boxes = [b for _, inner in clusters for b in inner.precise_boxes]

    img = draw_overlays(
        image, chunk_boxes, page_width, page_height,
        outline=(120, 120, 120, 180),
        fill=None,
        outline_width=2,
    )
    img = draw_overlays(
        img, precise_boxes, page_width, page_height,
        outline=(220, 30, 30, 255),
        fill=(255, 230, 0, 90),
        outline_width=2,
    )
    return img
