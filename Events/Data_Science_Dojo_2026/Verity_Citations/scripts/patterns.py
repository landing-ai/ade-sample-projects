"""Three things word-level grounding and confidence make possible.

  cite()     find an exact phrase and point at it on the page
  route()    send low-confidence content to a person, let the rest flow through
  verify()   check each extracted value against the words it came from

All three read the same DPT-3 Verity parse that docdiff.py uses: every word carries
its page, its box and a confidence score, plus its character range in the markdown.
"""
import json
import re
from dataclasses import dataclass

from PIL import ImageDraw

import docdiff

AMBER, BLUE, RED, GREEN = (217, 119, 6), (37, 99, 235), (220, 38, 38), (22, 163, 74)


@dataclass
class Word:
    text: str
    page: int
    box: dict
    confidence: float
    block: str
    start: int
    end: int

    @property
    def key(self):
        return re.sub(r"[^\w$.%-]", "", self.text.lower()).strip(".")


def words(name):
    """Every grounded word in the parse, including headers and footers, in reading order."""
    parse = json.loads((docdiff.PARSED_DIR / f"{name}.json").read_text())
    md, out = parse["markdown"], []

    def visit(node):
        for a in node.get("atomic_grounding") or []:
            s, e = a["range"]["start"], a["range"]["end"]
            if md[s:e].strip():
                out.append(Word(md[s:e].strip(), a["page"], a["box"], a.get("confidence", 1.0),
                                node["id"], s, e))
        for child in node.get("children", []):
            visit(child)

    visit(parse["structure"])
    return out


def _tokens(s):
    return [t for t in (re.sub(r"[^\w$.%-]", "", x.lower()).strip(".") for x in s.split()) if t]


def _show(name, marks, pad=0.04):
    """Render the pages with marks drawn, and crop to the marked region so it reads in a notebook."""
    pages = docdiff.render_pages(name, marks)
    ws = [w for _, _, group in marks for w in group]
    if not ws:
        return pages[1]
    p = ws[0].page
    im = pages[p]
    W, H = im.size
    same = [w for w in ws if w.page == p]
    y0 = max(0, min(w.box["ymin"] for w in same) - pad) * H
    y1 = min(1, max(w.box["ymax"] for w in same) + pad) * H
    return im.crop((0, int(y0), W, int(y1)))


# ---------------------------------------------------------------- cite
def cite(name, phrase):
    """Every place `phrase` occurs, word for word. Returns a list of hits (lists of Words)."""
    ws, want = words(name), _tokens(phrase)
    if not want:
        return []
    keys = [w.key for w in ws]
    return [ws[i:i + len(want)] for i in range(len(ws) - len(want) + 1) if keys[i:i + len(want)] == want]


def describe(hit):
    """Where a hit sits: one x/y range per text line, the same boxes show_cite() draws."""
    lines = docdiff._line_boxes(hit)
    pages = sorted({page for page, _ in lines})
    ranges = " | ".join((f"page {page}, " if len(pages) > 1 else "")
                        + f"x {b['xmin']:.2f}-{b['xmax']:.2f}, y {b['ymin']:.2f}-{b['ymax']:.2f}"
                        for page, b in lines)
    where = (f"page {pages[0]}, " if len(pages) == 1 else "") \
        + (f"{len(lines)} lines: " if len(lines) > 1 else "") + ranges
    return f"{where}, lowest confidence {min(w.confidence for w in hit):.2f}"


def show_cite(name, hit):
    return _show(name, [("Q", BLUE, hit)])


# ---------------------------------------------------------------- route
def route(name, threshold=docdiff.CONFIDENCE_THRESHOLD):
    """Split the document's blocks: any block holding a word below `threshold` goes to a person."""
    ws = words(name)
    blocks = {}
    for w in ws:
        blocks.setdefault(w.block, []).append(w)
    review = {b: g for b, g in blocks.items() if min(w.confidence for w in g) < threshold}
    low = [w for w in ws if w.confidence < threshold]
    return {"words": len(ws), "low_words": low, "blocks": len(blocks),
            "review_blocks": review, "straight_through": len(blocks) - len(review)}


def show_route(name, threshold=docdiff.CONFIDENCE_THRESHOLD):
    r = route(name, threshold)
    return _show(name, [(f"{w.confidence:.2f}", AMBER, [w]) for w in r["low_words"]], pad=0.06)


# ---------------------------------------------------------------- verify
def _as_number(t):
    try:
        return float(re.sub(r"[$,]", "", t).rstrip(".,;"))
    except ValueError:
        return None


def verify(name, extraction, evidence):
    """For each extracted value, look for it in the words inside the spans Extract cited.

    Extract's evidence points at whole blocks (a paragraph, a table). Verity's words narrow
    that to the exact words, with their own boxes and confidence. A value that is not
    among the cited words goes to review.
    """
    ws = words(name)
    cited = {f["field"]: f.get("spans") or [] for f in evidence["fields"]}
    rows = []
    for field, value in extraction.items():
        spans = cited.get(field, [])
        # A word that ends a line carries the line break in its range, one past the span: match on start.
        pool = [w for w in ws if any(s <= w.start < e for s, e in spans)]
        hit = []
        if isinstance(value, (int, float)):
            hit = [w for w in pool if _as_number(w.text) == float(value)][:1]
        elif isinstance(value, str):
            want, keys = _tokens(value), [w.key for w in pool]
            hit = next((pool[i:i + len(want)] for i in range(len(pool) - len(want) + 1)
                        if keys[i:i + len(want)] == want), [])
        status = "verified" if hit else ("no evidence" if not spans else "not in cited words")
        rows.append({"field": field, "value": value, "status": status, "words": hit,
                     "where": describe(hit) if hit else "", "confidence": min((w.confidence for w in hit), default=None)})
    return rows


def show_verify(name, rows):
    marks = [(str(i), GREEN, r["words"]) for i, r in enumerate(rows, 1) if r["words"]]
    return _show(name, marks)
