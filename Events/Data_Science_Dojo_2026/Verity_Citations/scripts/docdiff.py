"""Compare two parsed versions of a document, word by word.

The pipeline:
  1. words()   flatten a DPT-3 Verity parse into one reading-order list of words,
               each carrying its page, box, confidence and section.
  2. diff()    align the two word lists. Line breaks never enter the comparison,
               so a document that only re-flowed shows no changes.
  3. classify  a change is "noise" when it looks like a misread rather than an
               edit: the two sides differ by a character or two, at least one
               side is low-confidence, and no digits are involved.
  4. render()  draw every change on the original pages.
"""
import base64
import difflib
import html
import io
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PARSED_DIR = ROOT / "data" / "parsed"
PDF_DIR = ROOT / "data" / "pdfs"

# Below this, a word is "low confidence". 0.95 is the threshold the ADE
# Playground uses to highlight words for review.
CONFIDENCE_THRESHOLD = 0.95
# Two strings this similar (0-1, by characters) could be one misread word.
NEAR_MISS_SIMILARITY = 0.75
# Block types compared. Marginalia (headers, footers, page numbers) is left out:
# it moves whenever pages break differently.
CONTENT_TYPES = ("text", "table_cell")

HEADING = re.compile(r"^\s*\d+\.\s+\S")
EDGE_PUNCT = ".,;:"


@dataclass
class Word:
    text: str
    page: int
    box: dict
    confidence: float
    block: str
    section: str
    cell: tuple = None  # (row, col) for table cells

    @property
    def norm(self):
        return self.text.strip(EDGE_PUNCT)


def words(name):
    """Every word in a parse, in reading order, with location and confidence."""
    parse = json.loads((PARSED_DIR / f"{name}.json").read_text())
    md = parse["markdown"]
    out = []
    section = ""

    def visit(node):
        nonlocal section
        if node["type"] in CONTENT_TYPES:
            r = node["grounding"]["range"]
            first_line = md[r["start"]:r["end"]].strip().split("\n")[0]
            if node["type"] == "text" and HEADING.match(first_line):
                section = first_line
            cell = (node["row"], node["col"]) if node["type"] == "table_cell" else None
            for a in node.get("atomic_grounding", []):
                text = md[a["range"]["start"]:a["range"]["end"]].strip()
                if not text:  # signature lines etc. have a box but no characters
                    continue
                out.append(Word(text, a["page"], a["box"], a.get("confidence", 1.0),
                                node["id"], section, cell))
        for child in node.get("children", []):
            visit(child)

    visit(parse["structure"])
    return out


@dataclass
class Change:
    id: str
    kind: str          # added | removed | modified
    status: str        # change | noise
    section: str
    old_text: str
    new_text: str
    min_confidence: float
    reason: str
    old_words: list = field(default_factory=list)
    new_words: list = field(default_factory=list)


def _text(ws):
    return " ".join(w.text for w in ws)


def _classify(old, new, rule="guarded"):
    """Return (status, reason) for one aligned difference.

    rule="guarded"  the default, described in the module docstring
    rule="off"      ignore confidence: every difference is a change
    rule="naive"    any difference touching a low-confidence word is noise
    """
    low = [w for w in old + new if w.confidence < CONFIDENCE_THRESHOLD]
    if rule == "off":
        return "change", "confidence not used"
    if rule == "naive":
        return ("noise", "touches a low-confidence word") if low else ("change", "all words confident")
    if not (old and new):
        return "change", "words added or removed"
    a, b = _text(old), _text(new)
    if any(ch.isdigit() for ch in a + b):
        reason = "numbers changed"
        if low:
            reason += f"; kept for review although confidence is {min(w.confidence for w in low):.2f}"
        return "change", reason
    similarity = difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()
    if low and similarity >= NEAR_MISS_SIMILARITY:
        worst = min(low, key=lambda w: w.confidence)
        return "noise", (f"'{a}' vs '{b}' differ by a few characters and "
                         f"'{worst.text}' has confidence {worst.confidence:.2f}")
    return "change", "wording changed"


def diff(old_name, new_name, rule="guarded"):
    """Align two parsed versions and return the list of changes."""
    old, new = words(old_name), words(new_name)
    matcher = difflib.SequenceMatcher(None, [w.norm for w in old], [w.norm for w in new],
                                      autojunk=False)
    changes = []
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            continue
        ow, nw = old[i1:i2], new[j1:j2]
        kind = {"insert": "added", "delete": "removed", "replace": "modified"}[op]
        status, reason = _classify(ow, nw, rule)
        anchor = (nw or ow)[0]
        changes.append(Change(
            id=f"C{len(changes) + 1}", kind=kind, status=status,
            section=anchor.section or "(preamble)",
            old_text=_text(ow), new_text=_text(nw),
            min_confidence=min(w.confidence for w in ow + nw),
            reason=reason, old_words=ow, new_words=nw))
    return changes


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
COLORS = {"removed": (220, 38, 38), "added": (22, 163, 74), "noise": (148, 148, 148)}
SCALE = 2.0


def _line_boxes(ws):
    """Merge one change's words into one box per text line (words whose boxes overlap vertically)."""
    lines = []  # [page, box]
    for w in ws:
        b = w.box
        for line in lines:
            page, lb = line
            mid = (b["ymin"] + b["ymax"]) / 2
            if page == w.page and lb["ymin"] <= mid <= lb["ymax"]:
                line[1] = {"xmin": min(lb["xmin"], b["xmin"]), "ymin": min(lb["ymin"], b["ymin"]),
                           "xmax": max(lb["xmax"], b["xmax"]), "ymax": max(lb["ymax"], b["ymax"])}
                break
        else:
            lines.append([w.page, dict(b)])
    return [tuple(line) for line in lines]


def render_pages(name, marks):
    """marks: list of (change_id, color, words). Returns {page: PIL image}."""
    pdf = pdfium.PdfDocument(str(PDF_DIR / f"{name}.pdf"))
    pages = {i + 1: pdf[i].render(scale=SCALE).to_pil().convert("RGB") for i in range(len(pdf))}
    overlays = {p: Image.new("RGBA", im.size, (0, 0, 0, 0)) for p, im in pages.items()}
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    used = {p: [] for p in pages}  # badge slots already taken in each page's margin
    for cid, color, ws in marks:
        first = True
        for page, b in _line_boxes(ws):
            W, H = pages[page].size
            x0, y0, x1, y1 = b["xmin"] * W - 3, b["ymin"] * H - 3, b["xmax"] * W + 3, b["ymax"] * H + 3
            d = ImageDraw.Draw(overlays[page])
            d.rectangle([x0, y0, x1, y1], fill=color + (60,), outline=color + (255,), width=2)
            d.rectangle([0.06 * W - 5, y0, 0.06 * W, y1], fill=color + (255,))  # change bar
            if first:  # badge in the left margin; shift right if another badge sits on this line
                tw = d.textlength(cid, font=font)
                bx = 0.012 * W
                while any(abs(y0 - uy) < 26 and abs(bx - ux) < 40 for ux, uy in used[page]):
                    bx += tw + 14
                used[page].append((bx, y0))
                d.rectangle([bx, y0, bx + tw + 10, y0 + 24], fill=color + (255,))
                d.text((bx + 5, y0 + 1), cid, font=font, fill=(255, 255, 255, 255))
                first = False
    return {p: Image.alpha_composite(im.convert("RGBA"), overlays[p]).convert("RGB")
            for p, im in pages.items()}


def _png(im):
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def report(old_name, new_name, changes, out_dir):
    """Write changes.json, annotated page PNGs and a self-contained report.html."""
    out_dir.mkdir(parents=True, exist_ok=True)
    old_marks, new_marks = [], []
    for c in changes:
        noise = c.status == "noise"
        old_marks.append((c.id, COLORS["noise"] if noise else COLORS["removed"], c.old_words))
        new_marks.append((c.id, COLORS["noise"] if noise else COLORS["added"], c.new_words))
    old_pages = render_pages(old_name, [m for m in old_marks if m[2]])
    new_pages = render_pages(new_name, [m for m in new_marks if m[2]])
    for p, im in old_pages.items():
        im.save(out_dir / f"{old_name}_p{p}.png")
    for p, im in new_pages.items():
        im.save(out_dir / f"{new_name}_p{p}.png")

    (out_dir / "changes.json").write_text(json.dumps(
        [{k: v for k, v in asdict(c).items() if k not in ("old_words", "new_words")} |
         {"old_boxes": [{"page": w.page, **w.box} for w in c.old_words],
          "new_boxes": [{"page": w.page, **w.box} for w in c.new_words]}
         for c in changes], indent=2))

    real = [c for c in changes if c.status == "change"]
    noise = [c for c in changes if c.status == "noise"]
    e = html.escape

    def rows(cs):
        return "".join(
            f"<tr class='{c.status}'><td><b>{c.id}</b></td><td>{e(c.kind)}</td><td>{e(c.section)}</td>"
            f"<td class='old'>{e(c.old_text) or '&mdash;'}</td><td class='new'>{e(c.new_text) or '&mdash;'}</td>"
            f"<td>{c.min_confidence:.2f}</td><td class='why'>{e(c.reason)}</td></tr>" for c in cs)

    def gallery(name, pages):
        return "".join(f"<figure><figcaption>{e(name)} &middot; page {p}</figcaption>"
                       f"<img src='data:image/png;base64,{_png(im)}'></figure>" for p, im in pages.items())

    head = ("<tr><th>#</th><th>Kind</th><th>Section</th><th>Before</th><th>After</th>"
            "<th>Min conf.</th><th>Why</th></tr>")
    page = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(old_name)} vs {e(new_name)}</title>
<style>
:root{{--bg:#fff;--fg:#1a1a1a;--muted:#666;--line:#e3e3e3;--old:#fde8e8;--new:#e6f6ec;--noise:#f2f2f2}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151515;--fg:#eaeaea;--muted:#9a9a9a;--line:#333;--old:#4a1f1f;--new:#1d3d28;--noise:#262626}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;margin:0 auto;max-width:1400px;padding:24px 16px}}
h1{{font-size:22px;margin:0 0 4px}} h2{{font-size:17px;margin:28px 0 8px}} .sub{{color:var(--muted);margin:0 0 16px}}
table{{border-collapse:collapse;width:100%;font-size:14px}} th,td{{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}}
td.old{{background:var(--old)}} td.new{{background:var(--new)}} tr.noise td{{background:var(--noise);color:var(--muted)}} td.why{{color:var(--muted);font-size:13px}}
.wrap{{overflow-x:auto}} .pages{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} @media (max-width:800px){{.pages{{grid-template-columns:1fr}}}}
figure{{margin:0}} figcaption{{color:var(--muted);font-size:13px;margin-bottom:4px}} img{{width:100%;border:1px solid var(--line)}}
</style></head><body>
<h1>What changed: {e(old_name)} &rarr; {e(new_name)}</h1>
<p class="sub">{len(real)} change(s) to review &middot; {len(noise)} likely misread(s) set aside &middot;
red = before, green = after, grey = set aside as probable transcription noise</p>
<h2>Changes</h2><div class="wrap"><table>{head}{rows(real) or "<tr><td colspan=7>No changes.</td></tr>"}</table></div>
{f'<h2>Set aside as transcription noise</h2><div class="wrap"><table>{head}{rows(noise)}</table></div>' if noise else ''}
<h2>On the page</h2>
<div class="pages"><div>{gallery(old_name, old_pages)}</div><div>{gallery(new_name, new_pages)}</div></div>
</body></html>"""
    (out_dir / "report.html").write_text(page)
    return out_dir / "report.html"
