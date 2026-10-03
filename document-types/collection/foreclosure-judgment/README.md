# Foreclosure Judgment

Source assets for `landing.ai/document-type/foreclosure-judgment`.

## Sample document

`source/foreclosure-judgment-redacted.pdf`: a General Judgment of Foreclosure and Sale
from the Multnomah County Circuit Court, with its Certificate of Readiness under UTCR
5.100. It orders a foreclosed home sold and awards the lender $443,537.60 plus fees and
costs. **6 pages, portrait, scanned** on 28-line pleading paper.

| | |
|---|---|
| Publisher | Multnomah County Circuit Court record, posted by the Oregon State Sheriffs' Association sales site |
| Source | [oregonsheriffssales.org/…/384277-Writ.pdf](https://oregonsheriffssales.org/wp-content/uploads/2025/01/384277-Writ.pdf), pages 3–8 of 13 |
| Retrieved | 2026-10-02, by script |
| Clearance | **Redacted**, see below |

It sits in a sheriff's-sale packet with the writ that enforces it, the note and the
note's allonge. All four are separate samples sharing the same stand-ins.

## Redaction

| Data | Replaced with |
|---|---|
| The borrower's and defendants' names: caption, default recital, paragraphs 2 and 3 | `JOHN Q SAMPLE`, `JOHN QUINCY SAMPLE`, `JAMES Q SAMPLE`, `JANE Q SAMPLE`, `JUNE Q SAMPLE` (title case in body text) |
| Property house number and street | `100 Sample` |
| Property ZIP code | `97000` |
| Subdivision name in the legal description | `SAMPLE` |
| Deed of trust recording number | `2019-201618` |
| Case number | `24CV32513` |
| Law firm's file number (every footer) | `84-556087` |

Kept, because they appear in an official or professional capacity:

- the court, the judge and the plaintiff
- the plaintiff's law firm and its attorneys of record
- their signatures

The money award is kept too: with the parties and the property replaced, it identifies
no one.

This was done in the pixels with `document-types/scripts/redact_scan.py`. The
judgment's body text set the last fix in it. In mixed case, the busy band of ink is the
x-height, so a name like "Doe, Jr." was redrawn at half size, with the tops of the
original capitals left as specks. The measurement now climbs through the ascenders to
the capitals. The judgment was re-redacted and re-run after that fix.

Verified by OCR of the output, on literals and bare digits. A separate sweep of every
file in this folder found none of the original values.

## Why this document

This is where the money in a foreclosure is set out. The award is a ruled table of
principal, interest, charges and fees, with nested sub-items and a negative in
parentheses. A second table lists fees and costs. Around them run five pages of numbered
findings and orders. It tests table extraction from a scan, alongside facts written in
legal prose.

`schema.json`: **30 leaf fields** (counted from the schema), all populated.

## Featured fields: the award table

| Field | Value |
|---|---|
| Principal | 352970.28 |
| Prejudgment interest | 59253.99 |
| Prejudgment interest rate (%) | 3.875 |
| Late charges | 98.6 |
| Other costs and fees | 31214.73 |

All five are on page 3, in the paragraph 11 table. The subtotal ($384,283.61) and the
total with prejudgment interest ($443,537.60) are on page 4, where the table continues.

## Grounding and extraction notes

- **Every table amount grounds to its own cell**, across the award table's page break
  and in the fees table. The suspense balance, printed "($2,214.32)", extracts as
  −2214.32. The prejudgment rate and per-diem interest ground to the row-label cell that
  states them ("…at 3.875% … at $37.47 per diem").
- **The caption's line breaks split the defendants.** The borrower's name wraps across
  two caption lines, so `defendants[0]` ends "… OF JOHN" and `defendants[1]` begins
  "Q SAMPLE. AKA …". The writ shows the same pattern.
- **Findings in prose extract cleanly:** the deed of trust's dates and recording number,
  the note's date and amount, the 9% post-judgment rate, no deficiency judgment, and no
  homestead exemption. The booleans and the long-form dates read `OFF`, as they do in
  every sample.
- **The judge's signature** is a proxy signature. The parse labels it `[SIGNED]` and
  transcribes "Proxy signed by HCW". `judgment_signed_date` is the printed timestamp,
  "12/3/2024 3:09:22 PM".

## Cost

**9.20 credits** at standard tier for the committed output: 6-page parse and extraction.
The first run, before the redaction fix, cost another 9.20.

## Regenerating

```bash
# From the original packet; the rules file stays outside the repo.
.venv/bin/python document-types/scripts/redact_scan.py <packet>.pdf \
    source/foreclosure-judgment-redacted.pdf --rules <outside-the-repo>/rules.json \
    --pages 3 4 5 6 7 8 --verify-also <the surnames, street number and original numbers>

.venv/bin/python document-types/scripts/run_ade.py foreclosure-judgment
.venv/bin/python document-types/scripts/build_images.py foreclosure-judgment
.venv/bin/python document-types/scripts/inspect_fields.py foreclosure-judgment --page 3
```

Requires `tesseract` on the PATH (`brew install tesseract`).
