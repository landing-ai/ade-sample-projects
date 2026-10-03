"""Clear a PDF's document metadata, and check that it is gone.

`doc.set_metadata({})` is not enough: on some files, PyMuPDF 1.28 leaves every /Info
key in place. A power-of-attorney sample kept its preparer's name in `author` through
`set_metadata({})`, `del_xml_metadata()` and a `garbage=4` save. So each key is blanked
explicitly, XMP is deleted, the trailer's /Info reference is dropped, and callers check
the saved file with `remaining()`.
"""

from __future__ import annotations

import pymupdf

KEYS = ("title", "author", "subject", "keywords", "creator", "producer",
        "creationDate", "modDate", "trapped")


def clear(doc: pymupdf.Document) -> None:
    doc.set_metadata({k: "" for k in KEYS})
    doc.del_xml_metadata()
    doc.xref_set_key(-1, "Info", "null")


def remaining(doc: pymupdf.Document) -> list[str]:
    """Metadata keys that still carry a value, plus 'xmp' if XMP survives."""
    left = [k for k, v in doc.metadata.items() if v and k not in ("format", "encryption")]
    if (doc.get_xml_metadata() or "").strip():
        left.append("xmp")
    return left
