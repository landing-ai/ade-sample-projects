# Allonge to Note

Source assets for `landing.ai/document-type/allonge-to-note`.

## Sample document

`source/allonge-to-note-redacted.pdf`: an allonge to a VA-guaranteed mortgage note. It
endorses the note from PennyMac Corp. to PennyMac Loan Services, LLC, without recourse.
**1 page, portrait, scanned.**

An allonge is a separate sheet attached to a promissory note to carry an endorsement
when the note itself has no room. A lender proves it holds the note through this chain
of endorsements, so an allonge is one of the documents a foreclosure turns on.

| | |
|---|---|
| Publisher | Multnomah County Circuit Court record, posted by the Oregon State Sheriffs' Association sales site |
| Source | [oregonsheriffssales.org/…/384277-Writ.pdf](https://oregonsheriffssales.org/wp-content/uploads/2025/01/384277-Writ.pdf), page 12 of 13 |
| Retrieved | 2026-10-02, by script |
| Clearance | **Redacted**, see below |

The source is a sheriff's-sale packet with four document types. It holds:

- the writ of execution (pages 1–2)
- the general judgment of foreclosure and sale (3–8)
- the promissory note (9–11)
- two allonges (12–13)

This folder is page 12 only: the allonge with a **specific** endorsement. Page 13 is a
second allonge with a **blank** endorsement, and it is not used. The note, writ and
judgment have their own requests, built from the same packet with the same stand-ins.

## Redaction

The packet is a public court record of a foreclosure on a deceased private borrower's
home. On this page:

| Data | Replaced with |
|---|---|
| Borrower's name | `JOHN Q SAMPLE` |
| Property street address | `100 SAMPLE AVE` |
| Property ZIP code | `97000` |

"Portland, OR" is kept, because the court is Multnomah County's. The principal ($360,000)
is kept: with the address and name gone, it identifies no one. The loan number was
already blacked out by whoever filed it, before scanning, and that blackout is kept.

The PennyMac authorized representative's name and signature are kept. They sign in a
corporate capacity, as the title-company officers do on the commitment sample.

### A third redaction route: pixels

This page is a raster scan, with no text layer and no vector glyphs. Neither existing
tool can edit it: `redact.py` replaces text-layer strings, and `redact_outlined.py`
deletes vector glyph paths. The new `document-types/scripts/redact_scan.py` works on the
pixels:

1. It renders the page upright at 300 dpi.
2. It finds each string with Tesseract OCR, using `redact_outlined.py`'s matcher
   (word-bounded, ignores punctuation, follows line breaks).
3. It paints over each hit with the paper's own tone, taken from the 90th percentile of
   nearby non-ink pixels. The median left a patch one grey level darker, and that showed
   as a faint rectangle.
4. It draws the stand-in at the original's cap height and ink colour, compressed to its
   set width.
5. It rebuilds the page from the edited image alone.

The original raster is not in the output, so nothing survives under the paint. The
source's `/Rotate` and metadata are not carried over either.

The replacements are set in Arial, against the scan's Calibri, and are slightly crisper
than the scanned text around them. They read as typed-in form values. A shorter
replacement leaves a gap (`100 SAMPLE AVE , PORTLAND`), and the parse reads that gap as
a space.

Verified by OCR of the output, on literals and bare digits. A separate sweep of every
file in this folder found none of the original values.

## Why this document

It is the collection's first allonge, and the first sample redacted at the pixel level.
The page is sparse: six labelled lines, a large signature that crosses the title line,
and a hand-filled exhibit stamp. It tests reading labelled values off a real scan, and
telling a specific endorsement from a blank one.

`schema.json`: **13 leaf fields** (counted from the schema), all populated.

## Featured fields: the transfer

| Field | Value |
|---|---|
| Property address | 100 SAMPLE AVE , PORTLAND, OR 97000 |
| Principal balance | 360000 |
| Pay to the order of | PennyMac Loan Services, LLC |
| Endorser (without recourse) | PennyMac Corp. |

These identify the note by its property and principal, and say who endorsed it to whom.
The borrower is left out, although the name is a stand-in.

## Grounding notes

- **Each labelled line grounds whole**, label and value together, and every box is on
  its own line of the scan.
- **The blackout reads as `[ILLEGIBLE_TEXT]`** in the parse, which is honest. But
  `loan_number` and `co_borrower` come back as the **string** `"null"`, not JSON `null`,
  even though the schema types them `["string", "null"]`.
- **The signer's name and title ground to a figure.** The parse treats the large
  signature as a figure and writes a `<description>` of it. The signer's name and title
  ground to that description rather than to the printed `TITLE:` line, so they are not
  featured.
- **`endorsement_type` is `specific`** and correct, inferred from the filled "Pay to the
  order of" line. `without_recourse` is `true`. Both read `OFF` only because neither is
  printed as such.
- **The exhibit stamp** ("EXHIBIT 1, PAGE 4 OF 5", partly handwritten) is read whole.

## Cost

**1.30 credits** at standard tier: one-page parse and extraction.

## Regenerating

```bash
# Redaction, from the original packet; the rules file stays outside the repo.
.venv/bin/python document-types/scripts/redact_scan.py <packet>.pdf \
    source/allonge-to-note-redacted.pdf --rules <outside-the-repo>/rules.json \
    --pages 12 --verify-also <the borrower's surname and the street number>

.venv/bin/python document-types/scripts/run_ade.py allonge-to-note
.venv/bin/python document-types/scripts/build_images.py allonge-to-note
.venv/bin/python document-types/scripts/inspect_fields.py allonge-to-note --page 1
```

Requires `tesseract` on the PATH (`brew install tesseract`).
