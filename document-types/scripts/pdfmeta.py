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

import re

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
    for xref in range(1, doc.xref_length()):
        if doc.xref_get_key(xref, "Metadata")[0] != "null":
            doc.xref_set_key(xref, "Metadata", "null")
        jpeg = _jpeg_bytes(doc, xref)
        if jpeg is not None:
            stripped = _strip_jpeg(jpeg)
            if stripped != jpeg:
                doc.update_stream(xref, stripped, compress=False)
                doc.xref_set_key(xref, "Filter", "/DCTDecode")
                doc.xref_set_key(xref, "DecodeParms", "null")


def remaining(doc: pymupdf.Document) -> list[str]:
    """Metadata keys that still carry a value, plus 'xmp' if XMP survives."""
    left = [k for k, v in doc.metadata.items() if v and k not in ("format", "encryption")]
    if (doc.get_xml_metadata() or "").strip():
        left.append("xmp")
    if doc.xref_get_key(doc.pdf_catalog(), "StructTreeRoot")[0] != "null":
        left.append("structure tree")
    if any((j := _jpeg_bytes(doc, x)) is not None and _strip_jpeg(j) != j
           for x in range(1, doc.xref_length())):
        left.append("image EXIF/XMP")
    if any(doc.xref_get_key(x, "Metadata")[0] != "null" and x != doc.pdf_catalog()
           for x in range(1, doc.xref_length())):
        left.append("object metadata")
    return left


# APP1 holds EXIF and XMP, APP13 Photoshop's IPTC record (byline, caption), COM a free
# comment. APP0 (JFIF), APP2 (ICC profile) and APP14 (Adobe colour transform) stay: they
# change how the image renders.
_DROP = {0xE1, 0xED, 0xFE}


def _jpeg_bytes(doc: pymupdf.Document, xref: int) -> bytes | None:
    """The JPEG file a DCTDecode stream holds, or None if the stream is not one.

    A filter array such as [/ASCII85Decode /DCTDecode] wraps the JPEG in other encodings;
    the outer ones are undone so its metadata segments can be found.
    """
    kind, value = doc.xref_get_key(xref, "Filter")
    if kind == "null":
        return None
    filters = re.findall(r"/[^\s/\[\]]+", value)
    if filters == ["/DCTDecode"]:
        return doc.xref_stream_raw(xref)
    if "/DCTDecode" not in filters:
        return None
    image = doc.extract_image(xref)
    return image["image"] if image and image.get("ext") in ("jpeg", "jpg") else None


def _strip_jpeg(data: bytes) -> bytes:
    """The JPEG without its metadata segments, or unchanged if it cannot be parsed."""
    if data[:2] != b"\xff\xd8":
        return data
    out, i = bytearray(data[:2]), 2
    while i + 4 <= len(data):
        if data[i] != 0xFF:
            return data
        marker = data[i + 1]
        if marker == 0xDA:  # start of scan: the image data follows, untouched
            out += data[i:]
            return bytes(out)
        length = int.from_bytes(data[i + 2:i + 4], "big")
        if marker not in _DROP:
            out += data[i:i + 2 + length]
        i += 2 + length
    return data
