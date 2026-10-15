"""Clear a PDF's document metadata, and check that it is gone.

`doc.set_metadata({})` is not enough: on some files, PyMuPDF 1.28 leaves every /Info
key in place. A power-of-attorney sample kept its preparer's name in `author` through
`set_metadata({})`, `del_xml_metadata()` and a `garbage=4` save. So each key is blanked
explicitly, XMP is deleted, the trailer's /Info reference is dropped, and callers check
the saved file with `remaining()`.

The tagged-PDF structure tree goes too. Its /ActualText and /Alt entries hold their own
copy of the page text, which redaction annotations never touch, and `--drop-pages` does
not remove a dropped page's entries. A Word-made cover letter dropped from a shop drawing
left a name and an email address readable in the tree on the pages that survived.
"""

from __future__ import annotations

import pymupdf

KEYS = ("title", "author", "subject", "keywords", "creator", "producer",
        "creationDate", "modDate", "trapped")


def clear(doc: pymupdf.Document) -> None:
    doc.set_metadata({k: "" for k in KEYS})
    doc.del_xml_metadata()
    doc.xref_set_key(-1, "Info", "null")
    catalog = doc.pdf_catalog()
    for key in ("StructTreeRoot", "MarkInfo"):
        doc.xref_set_key(catalog, key, "null")
    for page in doc:
        doc.xref_set_key(page.xref, "StructParents", "null")


def remaining(doc: pymupdf.Document) -> list[str]:
    """Metadata keys that still carry a value, plus 'xmp' if XMP survives."""
    left = [k for k, v in doc.metadata.items() if v and k not in ("format", "encryption")]
    if (doc.get_xml_metadata() or "").strip():
        left.append("xmp")
    if doc.xref_get_key(doc.pdf_catalog(), "StructTreeRoot")[0] != "null":
        left.append("structure tree")
    return left
