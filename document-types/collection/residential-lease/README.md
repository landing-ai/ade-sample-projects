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

This is a real lease, uploaded to Scribd by a third party. Scribd is a user-upload site,
so the uploader is not the publisher, and the lease is treated as a personal record.
Scribd also blocks scripted requests, so the file was downloaded by hand.

Eight identifiers were replaced using `document-types/scripts/redact.py`, which removes
the underlying text rather than covering it, 45 replacements across six pages:

| What | Replaced with | Occurrences |
|---|---|---|
| Tenant's name, including the typed e-signature | Jane Q Sample | 3 |
| Agent's name, including the e-signature and page footers | Alex Q Sample | 9 |
| Principal broker's name, including the e-signature | Pat Q Example | 2 |
| Agent's personal email, page footers | agent@example.com | 6 |
| Agent's mobile number, page footers | 5015550142 | 6 |
| Rental property address | 100 Main Street Studio Anytown AR 00000 | 1 |
| Form serial number | 511613-318086-5101236 | 12 |
| E-signature session ID | 036c330d-1e06-4896-b9c0-05f6e7b7d3fe | 6 |

Names, the address and the email are obviously fake. The phone number is in the 555-01xx
range reserved for fiction, the serial number is a plausible random stand-in from
`plausible.py`, and the session ID is a freshly generated random ID: `plausible.py` keeps
letters, and a session ID's hex letters would have stayed in their original positions.
The PDF metadata was also cleared. The brokerage's name, logo and office address, and the
lease's terms and amounts, are left as printed.

The e-signatures were typed text in a script font, so they came out in Helvetica and now
read as typed names rather than signatures.

**Verified:** no original identifier is extractable from the committed PDF, and none
appears anywhere in this folder. The original values are deliberately not recorded here
or in `manifest.json`. The rules file used by `redact.py` stays outside the repo.

**This sample fixed two more things in `redact.py`:**

- **A 2pt line escaped redaction.** Each page carries a near-invisible "Prepared by" line
  in 2-point type. The script trimmed a fixed 3pt from every redaction rectangle before
  narrowing it to the letters, and on text that small the fixed trim emptied the rectangle,
  so the agent's name survived and verification failed. The narrowing to the letters now
  replaces the fixed trim instead of following it.
- **Fill lines were broken.** A filled form types each value over a line of underscores,
  and the two overlap completely, so redacting the value took the underscores beneath it
  and left gaps in the lines under the tenant and the address. The script now records the
  underscores before redacting and draws back only the ones actually removed. The document
  keeps exactly its original 2,301 underscores.

## Why this document

The collection's first **lease**, and its first **filled-in form** in the typed-over-a-blank
sense: every value is typed on top of the form's own underscore lines, in bold italic,
inside long clauses. That makes it a test of whether a value typed into a sentence can be
found as precisely as a value in a table cell.

## Featured fields: the lease's basics

All on **page 1**. The request named no fields, so these were chosen:

| Field | Value |
|---|---|
| Management | Century 21 Prestige Realty |
| Lease term | 12 Months |
| Monthly rent | 800.00 |
| Security deposit | 700.00 |

Who manages the lease, how long it runs, and what it costs to move in and to stay. No
person is featured.

## What it surfaced

**Typed-in values ground to the paragraph they are typed into.** The whole Rent section,
monthly rent, due day, late charge, the day after which it applies, and the
insufficient-funds fee, grounds to the entire paragraph: the typed values parse into the
paragraph's text, so each one's range is the paragraph. All five would render the same
crop, so only the monthly rent is featured, and its box covers the whole section.
Management and the security deposit, whose lines stand alone, ground to their own line.

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

**16.50 credits** at standard tier for 6 pages: 10.00 to parse, 6.50 to extract.

## Regenerating

```bash
# Redaction, from the manual download, with the rules file kept outside the repo:
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    document-types/collection/residential-lease/source/residential-lease-redacted.pdf \
    --rules <outside-the-repo>/rules.json

.venv/bin/python document-types/scripts/run_ade.py residential-lease                # 16.50 credits
.venv/bin/python document-types/scripts/run_ade.py residential-lease --extract-only # 6.50, schema iteration
.venv/bin/python document-types/scripts/build_images.py residential-lease           # free
.venv/bin/python document-types/scripts/inspect_fields.py residential-lease --page 1
```

`manifest.json` sets `preview_pages` to 1, 2, 4 and 6, so the signature page is shown.
