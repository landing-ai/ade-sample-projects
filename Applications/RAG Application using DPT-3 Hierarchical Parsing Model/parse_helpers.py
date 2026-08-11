"""Helpers for working with DPT-3 v2 parse responses.

Centralizes:
- structure walking
- quote-to-span resolution
- span-to-grounding lookup (block box + precise line/cell boxes)
- chunking for embedding
- precision metric (highlight area %, block-vs-precise ratio)
- overlay rendering

Response shape
--------------
A parse response is `{markdown, metadata, structure}`. `structure` is a single
tree: a `document` root whose children are pages, whose children are blocks.
Every node below the root carries its own location inline:

    "grounding": {
      "page": 1,                                  # 1-indexed
      "range": {"start": 29, "end": 112},         # offsets into `markdown`
      "box": {"xmin": .08, "ymin": .11, ...}      # normalized 0-1
    }

Leaf blocks also carry `atomic_grounding`: a list of the same `{page, range,
box}` shape, one entry per visual line (text/marginalia) or per localizable
segment (figure, logo, card, scan_code, attestation). Tables have no
`atomic_grounding`; their `table_cell` children are the finer granularity, and
each cell's own `atomic_grounding` is empty.

Everything below normalizes that into one internal vocabulary — span as
`[start, end]`, box as `[xmin, ymin, xmax, ymax]` in 0-1 page fractions, page
as a 1-indexed int — so the rest of the app never branches on response shape.
Parses cached before the inline-grounding change (a separate top-level
`grounding` tree, absolute pixel boxes, 0-indexed pages) are converted at the
same boundary, so an existing parsed/ cache keeps working.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from PIL import Image, ImageDraw

LEAF_CHUNK_TYPES = {
    "text", "marginalia", "figure", "table",
    "logo", "card", "scan_code", "attestation",
}

# Table-cell block types. DPT-3 emits `table_cell`; parses cached from earlier
# eras used HTML-style `td`/`th`. Accept all so old caches keep resolving.
CELL_TYPES = {"table_cell", "td", "th"}


@dataclass
class Chunk:
    """One indexable unit: a top-level block with its slice of markdown.
    Tables are emitted as a single chunk; cells stay queryable via grounding."""
    doc_id: str
    element_id: str
    element_type: str
    page: int
    span: list[int]
    text: str


@dataclass
class GroundingMatch:
    """A block whose span overlaps a query span.

    chunk_box = the block's own box (what block-level grounding alone gives you).
    precise_boxes = the atomic_grounding entries (lines / segments) that actually
                    overlap the query, or [chunk_box] when the block has none.
    All boxes are [xmin, ymin, xmax, ymax] as 0-1 fractions of the page."""
    element_id: str
    element_type: str
    page: int
    span: list[int]
    chunk_box: list[float]
    precise_boxes: list[list[float]]
    col: int | None = None   # table-cell column index (None for non-cells)


# ---- shape normalization ----

def _is_legacy(parse_response: dict) -> bool:
    """Pre-inline-grounding parses carried a second top-level `grounding` tree
    parallel to `structure`. Current responses have no such key."""
    return bool(parse_response.get("grounding"))


def _norm_box(box) -> list[float] | None:
    """Accept {xmin,ymin,xmax,ymax} or a bare [l,t,r,b] list."""
    if isinstance(box, dict):
        return [box["xmin"], box["ymin"], box["xmax"], box["ymax"]]
    return list(box) if box else None


def _span_of(node: dict) -> list[int] | None:
    """The node's markdown range as [start, end], from either shape."""
    g = node.get("grounding")
    if isinstance(g, dict) and isinstance(g.get("range"), dict):
        r = g["range"]
        return [r["start"], r["end"]]
    span = node.get("span")
    return list(span) if span else None


def _page_of(node: dict, inherited: int | None) -> int | None:
    """The node's 1-indexed page. Legacy page nodes counted from 0."""
    g = node.get("grounding")
    if isinstance(g, dict) and g.get("page") is not None:
        return g["page"]
    if node.get("page") is not None:
        return node["page"] + 1
    return inherited


def _legacy_page_dims(parse_response: dict) -> dict[int, tuple[float, float]]:
    """Legacy boxes were absolute pixels, so they need the page's own pixel
    dimensions to convert to the 0-1 space used everywhere now. Returns
    {page: (width, height)}; empty for current-shape responses."""
    dims: dict[int, tuple[float, float]] = {}
    for page_node in parse_response["structure"].get("children") or []:
        if page_node.get("type") != "page":
            continue
        width, height = page_node.get("width"), page_node.get("height")
        page = _page_of(page_node, None)
        if width and height and page is not None:
            dims[page] = (float(width), float(height))
    return dims


def _scale_box(box: list[float] | None, dims: tuple[float, float] | None) -> list[float] | None:
    if not box or not dims:
        return box
    width, height = dims
    return [box[0] / width, box[1] / height, box[2] / width, box[3] / height]


def _geometry(
    node: dict,
    legacy_entry: dict | None,
    dims: tuple[float, float] | None,
) -> tuple[list[float] | None, list[tuple[list[int], list[float]]]]:
    """Return (block_box, [(span, box), ...]) for a block, normalized.

    The second element is the block's finer-grained segments: `atomic_grounding`
    on current responses, the legacy grounding entry's `parts` on cached ones."""
    grounding = node.get("grounding")
    if isinstance(grounding, dict):
        box = _norm_box(grounding.get("box"))
        segments = []
        for atom in node.get("atomic_grounding") or []:
            rng = atom.get("range") or {}
            atom_box = _norm_box(atom.get("box"))
            if atom_box and "start" in rng:
                segments.append(([rng["start"], rng["end"]], atom_box))
        return box, segments

    if not legacy_entry:
        return None, []
    box = _scale_box(_norm_box(legacy_entry.get("box")), dims)
    segments = [
        (list(part["span"]), _scale_box(_norm_box(part.get("box")), dims))
        for part in legacy_entry.get("parts") or []
        if part.get("box") and part.get("span")
    ]
    return box, segments


def _spans_overlap(a: list[int], b: list[int]) -> bool:
    """Half-open span overlap test: [a0, a1) overlaps [b0, b1)."""
    return a[0] < b[1] and a[1] > b[0]


def iter_elements(structure: dict) -> Iterator[tuple[dict, int]]:
    """Yield (node, page_number) for every non-document, non-page block.
    Includes intermediate nodes like `table` and their `table_cell` children."""
    def walk(node, current_page):
        ntype = node.get("type")
        if ntype == "page":
            current_page = _page_of(node, current_page)
        elif ntype not in (None, "document"):
            yield node, _page_of(node, current_page)
        for child in node.get("children") or []:
            yield from walk(child, current_page)
    yield from walk(structure, None)


def iter_chunks(parse_response: dict, doc_id: str) -> Iterator[Chunk]:
    """Top-level chunker: one chunk per leaf-ish block (text, table, figure,
    marginalia, logo, card, scan_code, attestation).
    Does NOT recurse into table cells — the table is one chunk; cells remain
    queryable via get_grounding."""
    markdown = parse_response["markdown"]
    structure = parse_response["structure"]

    def walk(node, current_page):
        ntype = node.get("type")
        if ntype == "page":
            current_page = _page_of(node, current_page)
        elif ntype in LEAF_CHUNK_TYPES:
            span = _span_of(node)
            text = markdown[span[0]:span[1]].strip() if span else ""
            if text:
                page = _page_of(node, current_page)
                yield Chunk(
                    doc_id=doc_id,
                    element_id=str(node["id"]),
                    element_type=ntype,
                    page=page if page is not None else 0,
                    span=list(span),
                    text=text,
                )
            return  # do not chunk the table's cells separately
        for child in node.get("children") or []:
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
       search there, then map the match back to original-markdown offsets.

    Offsets are Python string indices, which are code-point based and so line up
    with the API's ranges (metadata.range_units is "unicode_codepoints")."""
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


def grounding_map(parse_response: dict) -> dict[str, dict]:
    """Flatten a legacy parallel `grounding` tree into {id: {box, page, parts}}.

    Current responses carry grounding inline on each structure node and have no
    top-level `grounding` key, so this returns {} for them — it exists only to
    keep a pre-existing parsed/ cache resolvable."""
    root = parse_response.get("grounding") or {}
    if not root:
        return {}
    # Legacy flat form has no tree markers — return as-is.
    if "type" not in root and "children" not in root:
        return root

    out: dict[str, dict] = {}

    def walk(node: dict, page: int | None):
        if node.get("type") == "page":
            page = _page_of(node, page)
        eid = node.get("id")
        if eid is not None:
            out[str(eid)] = {
                "box": node.get("box"),
                "page": page,
                "parts": node.get("parts", []) or [],
            }
        for child in node.get("children") or []:
            walk(child, page)

    walk(root, None)
    return out


def get_grounding(spans: list[list[int]], parse_response: dict) -> list[GroundingMatch]:
    """For each block whose span overlaps any query span, return a
    GroundingMatch with both the block-level box and the precise lines/cells
    that actually contain the overlap.

    For text and marginalia: precise_boxes = the atomic_grounding lines that
    overlap. For tables: no atomic_grounding, but the table's cells match
    separately (each carries its own grounding). For other block types:
    precise_boxes falls back to [chunk_box]."""
    structure = parse_response["structure"]
    markdown = parse_response["markdown"]
    legacy = grounding_map(parse_response)
    dims = _legacy_page_dims(parse_response) if legacy else {}
    matches: dict[str, GroundingMatch] = {}

    for elem, page in iter_elements(structure):
        span = _span_of(elem)
        if not span or not any(_spans_overlap(span, s) for s in spans):
            continue
        etype = elem["type"]
        # Never highlight a blank table cell: when a quote spans a whole row, the
        # empty cells overlap too, but they aren't the answer. Drop them.
        if etype in CELL_TYPES and not markdown[span[0]:span[1]].strip():
            continue
        eid = str(elem["id"])
        if eid in matches:
            continue
        box, segments = _geometry(elem, legacy.get(eid), dims.get(page))
        if not box:
            continue
        precise = [b for seg_span, b in segments if any(_spans_overlap(seg_span, s) for s in spans)]
        if not precise:
            precise = [box]
        matches[eid] = GroundingMatch(
            element_id=eid,
            element_type=etype,
            page=page if page is not None else 0,
            span=list(span),
            chunk_box=list(box),
            precise_boxes=[list(b) for b in precise],
            col=elem.get("col"),
        )
    return list(matches.values())


def cluster_matches(
    matches: list[GroundingMatch],
) -> list[tuple[GroundingMatch, GroundingMatch]]:
    """Group matches whose spans overlap into clusters. For each cluster return
    (outer, inner) — outer has the largest span (the block-level view), inner
    has the smallest (the precise view).

    For a quote inside a table cell, get_grounding returns both the `table` and
    the `table_cell`; this collapses that pair into (table, cell). For a quote
    inside a paragraph, both outer and inner are the paragraph itself."""
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
    """Return the page node (carrying `status`, and `reason` when it failed) for
    a 1-indexed page number."""
    for p in parse_response["structure"].get("children") or []:
        if p.get("type") == "page" and _page_of(p, None) == page:
            return p
    return None


def _box_area(box: list[float]) -> float:
    return max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1])


def precision_metric(matches: list[GroundingMatch]) -> dict:
    """Compare block-level vs precise highlight area, as % of summed page area.
    Returns {chunk_pct, precise_pct, ratio} where ratio = chunk_area / precise_area.

    Boxes are 0-1 page fractions, so each touched page contributes an area of 1.0
    and a box's area is already its share of that page.

    Uses cluster_matches to avoid double-counting nested matches: when a quote
    falls inside a table cell, the table-level chunk_box represents the block
    view and the cell's box represents the precise view; we don't sum both."""
    if not matches:
        return {"chunk_pct": 0.0, "precise_pct": 0.0, "ratio": 0.0}

    chunk_area_by_page: dict[int, float] = {}
    precise_area_by_page: dict[int, float] = {}
    for outer, inner in cluster_matches(matches):
        chunk_area_by_page[outer.page] = chunk_area_by_page.get(outer.page, 0.0) + _box_area(outer.chunk_box)
        for b in inner.precise_boxes:
            precise_area_by_page[inner.page] = precise_area_by_page.get(inner.page, 0.0) + _box_area(b)

    pages_touched = set(chunk_area_by_page) | set(precise_area_by_page)
    total_page_area = float(len(pages_touched))

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
    *,
    outline: tuple[int, int, int, int] = (220, 30, 30, 255),
    fill: tuple[int, int, int, int] | None = (255, 230, 0, 90),
    outline_width: int = 2,
) -> Image.Image:
    """Draw translucent rectangles on a copy of the page image.

    Boxes are 0-1 page fractions, so they scale to whatever rendering of the page
    we happen to be drawing on — multiply by the image's own pixel dimensions."""
    result = image.convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for box in boxes:
        left, top, right, bottom = box
        px_box = (
            left * result.width,
            top * result.height,
            right * result.width,
            bottom * result.height,
        )
        draw.rectangle(px_box, outline=outline, fill=fill, width=outline_width)
    return Image.alpha_composite(result, overlay)


def render_dual_overlay(
    image: Image.Image,
    matches: list[GroundingMatch],
    page: int,
) -> Image.Image:
    """Draw the block-level box (faint gray outline, no fill) UNDER the
    precise boxes (red outline, yellow translucent fill). The contrast
    visually demonstrates the line-/cell-level upgrade over block grounding.

    Kept for backward compatibility; render_overlays is the more flexible
    primitive (supports zoom level + multi-quote color groups)."""
    return render_overlays(
        image,
        [(matches, ((220, 30, 30, 255), (255, 230, 0, 90)))],
        page,
        level="precise",
    )


def render_overlays(
    image: Image.Image,
    quote_groups: list[tuple[list[GroundingMatch], tuple[tuple[int, int, int, int], tuple[int, int, int, int]]]],
    page: int,
    *,
    level: str = "precise",
) -> Image.Image:
    """Render highlights on a page image, parameterized on (zoom level) × (per-quote color).

    quote_groups: list of (matches, (outline_color, fill_color)) tuples. One per
        independent quote. Each match in a group's matches contributes to that
        quote's highlight. Pass a single-element list for the single-quote case.
    level: one of:
        - "page":    just outline the page bounds. Communicates scale.
        - "element": draw the chunk_box for each cluster (block-level grounding view).
                     No precise highlights.
        - "precise": per-quote colored line/cell boxes. The default, and the win.

    The page-level outline always uses a single faint forest line regardless of
    quotes. Block outlines (drawn at "element" level) are gray. Precise boxes
    (drawn at "precise" level) take their color from the quote_groups."""
    out = image.convert("RGBA")

    if level == "page":
        return draw_overlays(
            out, [[0.0, 0.0, 1.0, 1.0]],
            outline=(3, 34, 29, 200),    # forest
            fill=None,
            outline_width=2,
        )

    # For "element" and "precise" levels we walk each quote group separately.
    for matches, (outline_rgba, fill_rgba) in quote_groups:
        page_matches = [m for m in matches if m.page == page]
        if not page_matches:
            continue
        clusters = cluster_matches(page_matches)
        chunk_boxes = [outer.chunk_box for outer, _ in clusters]

        if level == "element":
            # Block outlines with a faint per-quote fill so multi-quote element
            # views still distinguish each source. Single-quote case uses surface.
            out = draw_overlays(
                out, chunk_boxes,
                outline=(120, 120, 120, 200),
                fill=(fill_rgba[0], fill_rgba[1], fill_rgba[2], 35),
                outline_width=2,
            )
        else:  # level == "precise" — ONLY the relevant answer highlight, no gray box
            cells = [m for m in page_matches if m.element_type in CELL_TYPES]
            # Prefer data/value cells (col > 0); fall back to any matched cell.
            value_cells = [m for m in cells if m.col not in (0, None)] or cells
            lines = [m for m in page_matches if m.element_type not in ({"table"} | CELL_TYPES)]
            precise_boxes = (
                [b for m in value_cells for b in m.precise_boxes]
                + [b for m in lines for b in m.precise_boxes]
            )
            out = draw_overlays(
                out, precise_boxes,
                outline=outline_rgba,
                fill=fill_rgba,
                outline_width=2,
            )

    return out


def find_element_node(parse_response: dict, element_id: str) -> dict | None:
    """Walk the structure tree and return the node whose id matches.

    Useful for looking up structural metadata (row/col for cells) that isn't
    carried on GroundingMatch."""
    target = str(element_id)
    for node, _ in iter_elements(parse_response["structure"]):
        if str(node.get("id")) == target:
            return node
    return None
