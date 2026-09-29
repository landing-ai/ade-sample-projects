# Residential lease

Source assets for `landing.ai/document-type/residential-lease`.

## Sample document

`source/residential-lease-redacted.pdf` — a residential lease on the Arkansas REALTORS®
Association's standard Residential Lease/Rental Agreement form, completed and e-signed
through a Century 21 brokerage on November 17, 2023, redacted. **6 pages, portrait
(612×792)**: the filled-in terms on page 1, standard clauses on pages 2 to 5, and the
signature page.

| | |
|---|---|
| Publisher | Arkansas REALTORS® Association (form), completed by a Century 21 Prestige Realty agent |
| Source | [scribd.com/document/746241294/Residential-Lease-Rental-Agreement](https://www.scribd.com/document/746241294/Residential-Lease-Rental-Agreement) |
| Retrieved | 2026-09-28, downloaded manually |
| Clearance | Redacted |

## Redaction

This is a real lease, uploaded to Scribd by a third party and downloaded by hand, because
Scribd blocks scripted requests. **At the document owner's decision only the tenant's name
is replaced.** Every other detail is kept as printed: the rental property's address, which
is what the page demonstrates, the agent's and principal broker's names, e-signatures and
contact details, the form serial number and the e-signature session ID.

| What | Replaced with | Occurrences |
|---|---|---|
| Tenant's name, printed and as the typed e-signature | Jane Q Sample | 3 |

The replacement was made with `document-types/scripts/redact.py`, which removes the
underlying text rather than covering it, and the PDF metadata was cleared.

**The tenant's signature still reads as a signature.** It was a typed e-signature in a
handwriting font, so replacing it in Helvetica would have turned it into a printed name
and removed the evidence that the tenant signed. `redact.py` now takes
`--handwriting-font`: text set in a handwriting font is replaced in that font instead, and
in the original's colour. The stand-in signature is in Indie Flower, an openly licensed
(SIL OFL) handwriting font kept at `document-types/scripts/fonts/`, in the same navy as the
two real signatures beside it. The printed name keeps its bold italic.

**Verified:** the tenant's name is not extractable from the committed PDF and appears
nowhere in this folder. The rules file used by `redact.py` stays outside the repo.

An earlier version of this folder replaced every name, contact detail and identifier in
the lease. The owner asked for only the tenant's name to be replaced, and for the
signatures to stay.

**This sample also fixed two things in `redact.py`:**

- **A 2pt line escaped redaction.** Each page carries a near-invisible "Prepared by" line
  in 2-point type. On text that small, the fixed trim the script took off every redaction
  rectangle emptied it, and the name survived. The narrowing to the letters now replaces
  the fixed trim.
- **Fill lines were broken.** A filled form types each value over a line of underscores,
  and redacting the value took the underscores beneath it. The script now draws back
  exactly the underscores it removed; the lease keeps its original 2,301.

## Why this document

The collection's first **lease**, and its first **filled-in form** in the typed-over-a-blank
sense: every value is typed on top of the form's own underscore lines, in bold italic,
inside long clauses. That makes it a test of whether a value typed into a sentence can be
found as precisely as a value in a table cell.

## Featured fields: proof of address

All on **page 1**. The owner asked for the property address to be highlighted, for use as
a **proof-of-address** example; the other fields support it:

| Field | Value |
|---|---|
| Property address | 909 Shall Court Studio Jacksonville AR 72076 |
| Tenant | Jane Q Sample |
| Lease term | 12 Months |
| Security deposit | 700.00 |

Where the tenant lives, who the tenant is (the stand-in name), for how long, and the
deposit paid. The address box covers the opening lines of the Term and Description
paragraph, which contain the typed address, and the tenant box covers the opening block;
see below.

## What it surfaced

**Typed-in values ground to the paragraph they are typed into.** The address, typed onto
the form's blank line, grounds to the opening lines of the Term and Description paragraph
around it, and the tenant's name to the whole opening block. The Rent section is the
extreme case: monthly rent, due day, late charge, the day after which it applies, and the
insufficient-funds fee all ground to the entire paragraph and would render the same crop,
so none is featured. The security deposit and the lease term, whose lines stand apart,
ground to their own line.

**Every value is right, but the signatures are paired wrongly.** The signature page sets
Management signatures down the left and Tenant signatures down the right. Extraction
returns all five signature lines but matches names and roles across the columns: the
tenant's name comes back under "Management as Authorized Agent of Owner", both agents
under "Tenant", and the signed/unsigned flags follow the wrong lines. The rest of the lease
extracts correctly, including the fixed-term checkbox, the dates and every amount.

**Normalized dates are flagged.** The agreement and term dates come back as ISO dates from
the split "(month) November (day) 17 (year) 2023" blanks, which is right but no longer
matches the printed text.

## Extraction

`schema.json` was written for this lease, with **18 leaf fields**: the agreement date, the
parties, the property, the term (type, length, start, end), the rent terms, the security
deposit, and a `signatures` array (role, signed, printed name). Everything populates, with
no warnings.

## Cost

**16.40 credits** at standard tier for 6 pages, 10.00 to parse and 6.40 to extract. The earlier, fully redacted version cost another 16.50.

## Regenerating

```bash
# Redaction, from the manual download, with the rules file kept outside the repo:
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    document-types/collection/residential-lease/source/residential-lease-redacted.pdf \
    --rules <outside-the-repo>/rules.json \
    --handwriting-font document-types/scripts/fonts/IndieFlower-Regular.ttf

.venv/bin/python document-types/scripts/run_ade.py residential-lease                # 16.40 credits
.venv/bin/python document-types/scripts/run_ade.py residential-lease --extract-only # 6.40, schema iteration
.venv/bin/python document-types/scripts/build_images.py residential-lease           # free
.venv/bin/python document-types/scripts/inspect_fields.py residential-lease --page 1
```

`manifest.json` sets `preview_pages` to 1, 2, 4 and 6, so the signature page is shown.
