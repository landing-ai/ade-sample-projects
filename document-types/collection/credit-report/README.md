# Credit report

Source assets for `landing.ai/document-type/credit-report`.

## Sample document

`source/credit-report-redacted.pdf` — a consumer credit report built on TransUnion data,
with a VantageScore 3.0 of 766, report date January 30, 2022. **8 pages, portrait (A4)**,
rendered from a web page to PDF: a score gauge, personal information, an account summary,
eleven credit card and charge accounts with 24-month payment grids, a hard inquiry, a
collection account, public records and a creditor directory.

| | |
|---|---|
| Publisher | Unknown (a TransUnion-based report, saved from a web page) |
| Source | [scribd.com/document/978216898](https://www.scribd.com/document/978216898) |
| Retrieved | 2026-09-28, downloaded manually |
| Clearance | Redacted |

**Provenance is poor, and every identifying detail was replaced.** This is a real
individual's full credit report, uploaded to Scribd by a third party under a title
giving the person's name and a sequence number. A numbered upload of a named person's
report, complete with SSN, date of birth and fifteen years of addresses, is the pattern
of a leaked or fraud-traded identity record, not a document its subject chose to publish.
It was flagged as unusable; the document owner decided to use it on the condition that
nothing identifying survives.

Replaced with `document-types/scripts/redact.py`, which removes the underlying text
rather than covering it:

| What | With |
|---|---|
| Consumer's name | Jane Q Sample |
| Social Security number | 987-65-4323, from the reserved 987-65-4320–4329 range |
| Date of birth | 1957-01-16 |
| Employer and job title | Clerk (employer removed) |
| Six reported addresses | 100 Main St to 600 Maple Dr, Anytown, ZIP 000000000; states kept |
| Twelve account numbers | Plausible random stand-ins of the same length (`scripts/plausible.py`) |

Kept as printed: the score, every balance, limit and payment, creditor names, dates,
payment histories, remarks, and the creditors' and collection agency's business addresses
and phone numbers. None of it identifies anyone once the identity is gone. The PDF
metadata was cleared (the original carried Chromium/Skia producer data). Verified: no
original value is extractable from the committed PDF, no other line of text changed, and
no original value, including as bare digits, appears in any file in this folder.

The url is recorded without the listing's title slug, which contains the person's name,
and the request file omits the local download path for the same reason.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **credit report**, and a web page rather than a form:

- **A dashboard printed to paper.** The headline figures are big-number tiles, the score
  is a gauge graphic, and each account is a card with a colour-coded month-by-month grid.
- **The same figure, twice.** The account summary prints balances, payments and account
  counts in large tiles and again in a detail table beneath.
- **Many repeated records.** Eleven tradelines, each with the same fifteen fields, across
  six pages, plus a collection account in a different layout.

> **`suppress_caption` on the score.** The web page writes a caption under any
> crop whose grounded text differs from its value. The score's range covers the
> chart's `Rating` label, so that caption would tell a reader the range landed on
> text beside the value, while the crop plainly shows 766. The field carries
> `suppress_caption: true` so the page prints the crop and no caption.

## Featured fields: the score and the account summary tiles

All on page 1. The request named no fields, so these were chosen:

| Field | Value |
|---|---|
| Credit score | 766 |
| Total balances | $4,180 |
| Monthly payments | $2,170 |
| Open accounts | 8 |
| Closed accounts | 4 |

The score and the four headline tiles, the part of the report an underwriter reads
first, and all impersonal. The score's box is loose and its grounding is flagged; see
below. It is featured at the document owner's decision, because it is the value anyone
opening a credit report looks for first. Each value is printed twice; occurrence 1 is the tile, and each box takes in
the small label above the figure. The identity block on the same page grounds cleanly but
is stand-in data and is not featured.

## What it surfaced

**Extraction "corrected" the printed totals, wrongly.** The first schema asked for total
balances and payments. Extraction returned 2,842 and 2,066, which it appears to have
recomputed from the collection-type accounts, against the printed $4,180 and $2,170. The
printed figures are right: $2,114 across the tradelines plus the $2,066 collection
account, and $104 plus $2,066. Telling the schema to take the totals exactly as printed,
and not to compute them, fixed both.

**A charged-off card was filed as a collection.** The same first pass listed BP-VISA, a
credit card with status Charge Off, under collections as well as among the accounts. A
description saying that collections are the accounts in the Collections section fixed it.

**The score grounds to the whole chart.** 766, the rating GREAT and the 300–850 scale
are drawn inside the gauge graphic. The parse turns the chart into a small data table
(score model / 766, Rating / GREAT, Range / 300–850), and extraction reads every value
correctly, but its range for the score points one cell off, at the Rating label. The table
has no box of its own, so the highlight falls back to the whole chart: gauge, line chart
and report date. 766 is plainly inside it and the crop reads as right, but
`build_images.py` warns that the value is not in the boxed text, and the box is about
twenty times the area of the tiles'. Featured anyway, at the document owner's decision.

**The tradelines extract completely.** All eleven accounts come back with every balance,
limit, high balance, account number, status, late-payment count and remark matching the
page. So does the collection account, with its original creditor, and the one hard
inquiry.

## Extraction

**46 leaf fields**: report date, bureau, the score, the consumer, the account summary,
and arrays of accounts, collections and hard inquiries. Everything extracts correctly
after the one schema revision described above.

## Cost

**26.10 credits** at standard tier for 8 pages: 13.20 to parse, 12.90 to extract. The
first extraction, before the schema revision, cost a further 13.10, for 39.20 in all.

## Regenerating

```bash
# The source is a manual download from the Scribd url, redacted with redact.py and a
# rules file kept outside the repo. The committed PDF is the redacted one.
.venv/bin/python document-types/scripts/run_ade.py credit-report                # 26.10 credits
.venv/bin/python document-types/scripts/run_ade.py credit-report --extract-only # 12.90, schema iteration
.venv/bin/python document-types/scripts/build_images.py credit-report           # free
.venv/bin/python document-types/scripts/inspect_fields.py credit-report --page 1
```
