# Quality of Earnings Report

Source assets for `landing.ai/document-type/quality-of-earnings-report`.

## Sample document

`source/qoe-prep-sample-report.pdf`: a sample Quality of Earnings (QoE) report dated
February 2025, published by QOE Prep, a CPA firm. **25 pages, landscape (792×612)**, a
PowerPoint deck printed to PDF with a full text layer. It covers a fictional
fixed-wireless internet provider: key findings, the EBITDA bridge, P&L and revenue
trends, vendor analysis, net working capital, cash conversion and proof-of-cash
reconciliations.

| | |
|---|---|
| Publisher | QOE Prep (Caleb PA Basile, LLC) |
| Source | [img1.wsimg.com/…/Sample report - Qoe Prep 12.4.pdf](https://img1.wsimg.com/blobby/go/2975c323-0167-4a10-81f0-60981f4243c3/Sample%20report%20-%20Qoe%20Prep%2012.4.pdf), linked from qoeprep.com/sample |
| Retrieved | 2026-10-28, by script |
| Clearance | Redacted (one page dropped) |

The publisher distributes this as a public sample, and its cover states that all figures
are fictional. The target company, its owners and staff are already anonymized in the
document (`XXXX`, "Company 2", "Vendor 1"). The only real person named in the report is
the publisher's own principal, as signatory of the cover letter and contact on the
closing page. He is named in his professional capacity, so his name is kept, as the
executives are in the investor presentation.

**One page was removed.** The original page 2, "Happy Customers", was a set of
screenshot Google reviews naming eight private reviewers, one with a profile photo. It is
publisher marketing rather than part of the report, and the names were in images, so no
text rule could reach them. The page was dropped with `redact.py --drop-pages 2`, which
also cleared the PDF metadata. No text was replaced. The folder was swept for the
reviewers' names afterwards and none appear. Because of the drop, every PDF page number
here is one lower than the "Page N" footer printed on the slide.

## Why this document

- **A financial-diligence deliverable**, not a statement or a form: an analyst's
  argument built on tables, with the reasoning in prose beside them. Nothing else in the
  collection is shaped like this.
- **Table on the left, commentary on the right.** The EBITDA bridge slide pairs a dense
  ruled table with a panel explaining each adjustment, so the schema asks for both the
  number and the rationale for each line.
- **The same table twice.** The bridge is printed on page 8 and again on page 9, with
  different commentary. A value can ground to either copy.
- **A units trap.** The table header says `In $000's`, but the figures are whole dollars:
  the Key Findings prose gives revenue as $8.7M against a table value of 8,657,602. The
  schema asks for amounts as printed, and they come back unscaled.

## Extraction

`schema.json` has **26 leaf fields** in three groups: `report` (preparer, date, target
description, periods), `ebitda_bridge` (one entry per period column with the subtotals
and margins, plus every adjustment line with its category, TTM amount and rationale), and
`key_findings` (average NWC, inventory, DSO/DIO/DPO, cash conversion cycle, customer
count, unpaid PTO).

Everything extracted correctly: all four period columns, all ten adjustment lines with
the right management or due-diligence category, dashes read as 0, parenthesized amounts
as negatives, and the key-findings figures. The extraction output has 92 leaf values.

## Featured fields

All on **page 8** (the "QoE" slide, printed "Page 9"), down the TTM column of the bridge:

| Field | Value |
|---|---|
| Reported EBITDA (TTM) | 619,882 |
| Total management adjustments (TTM) | 820,085 |
| Legal settlement add-back (TTM) | 285,000 |
| Adjusted EBITDA (TTM) | 1,654,372 |
| Adjusted EBITDA margin (TTM) | 20.1% |

Together they read as one walk from reported to adjusted EBITDA, which is the point of a
QoE report. These are the fields the request suggested; the request left the diligence
adjustment open, and the legal settlement line was picked because it grounds to its TTM
cell and is the most concrete adjustment in the commentary. Its amount also appears in
the 2024 column, and the margin 20.1% appears in both the 2024 and TTM columns; the
crops confirm each box is on the TTM cell.

## Grounding

- **The ruled table grounds cleanly.** Every period subtotal and margin, and every
  non-zero adjustment amount, boxes its own cell, with no off-by-one drift.
- **Extraction used the first copy of the table only.** Every table value grounds to
  page 8; nothing points at the duplicate on page 9.
- **Dash cells cannot be shown.** A dash extracted as 0 grounds to the markdown `---`,
  which does not contain the value, so those rows read `OFF`.
- **Prose figures ground to the sentence, not the number.** Values stated as `$764K`,
  `$56K` or `($297K)` extract correctly as 764000, 56000 and -297000, but the box covers
  the whole finding, so they cannot be featured. Average NWC is featurable only where it
  appears as `(297,000)` in the NWC table on page 19.
- **Summarized rationales ground OFF.** The schema asks for a one-sentence summary, so
  the text is a paraphrase of the commentary, and the rationales for the due-diligence
  adjustments ground to the commentary on page 9, a page away from their amounts.

## Cost

**39.60 credits** at standard tier for 25 pages, parse and extract together.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py quality-of-earnings-report                 # 39.60 credits
.venv/bin/python document-types/scripts/run_ade.py quality-of-earnings-report --extract-only  # schema iteration
.venv/bin/python document-types/scripts/build_images.py quality-of-earnings-report            # free
.venv/bin/python document-types/scripts/inspect_fields.py quality-of-earnings-report --page 8
```

The committed PDF was produced from the original download with
`redact.py <original>.pdf source/qoe-prep-sample-report.pdf --rules <empty rules> --drop-pages 2`.
