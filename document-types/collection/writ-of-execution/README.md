# Writ of Execution

Source assets for `landing.ai/document-type/writ-of-execution`.

## Sample document

`source/writ-of-execution-redacted.pdf`: a writ of execution on real property issued by
the Multnomah County Circuit Court. It orders the county sheriff to sell a foreclosed
home to satisfy $450,797.72 under a General Judgment of Foreclosure and Sale. **2 pages,
portrait, scanned** on 28-line pleading paper.

| | |
|---|---|
| Publisher | Multnomah County Circuit Court record, posted by the Oregon State Sheriffs' Association sales site |
| Source | [oregonsheriffssales.org/…/384277-Writ.pdf](https://oregonsheriffssales.org/wp-content/uploads/2025/01/384277-Writ.pdf), pages 1–2 of 13 |
| Retrieved | 2026-10-02, by script |
| Clearance | **Redacted**, see below |

The writ heads a sheriff's-sale packet. The judgment it enforces, the note and the note's
allonge from the same packet are separate samples, and all four share the same
stand-ins.

## Redaction

| Data | Replaced with |
|---|---|
| Defendants in the caption: the borrower, his alias and three heirs | `JOHN Q SAMPLE`, `JOHN QUINCY SAMPLE`, `JAMES Q SAMPLE`, `JANE Q SAMPLE`, `JUNE Q SAMPLE` |
| Property house number and street | `100 Sample` |
| Property ZIP code | `97000` |
| Subdivision name in the legal description | `SAMPLE` |
| Case number (page header and caption) | `24CV32513` |
| Law firm's file number (footers) | `84-556087` |

Kept, because they appear in an official or professional capacity:

- the court and the judgment creditor
- the creditor's law firm and its attorneys of record
- the signature across the court seal

This was done in the pixels with `document-types/scripts/redact_scan.py`. The writ is
what drove most of its matching:

- **The caption wraps names across lines.** One heir's first name ends one line and
  the surname starts the next. The matcher finds a name across the break and splits the
  stand-in the same way.
- **Single-spaced caption lines touch.** A wrapped surname's OCR box took in the line
  above, so the stand-in was drawn on the wrong line at the wrong size. Size and
  baseline are now measured from the hit's own ink, keeping the heaviest band of rows.
  The painted area is clipped to that band.
- **Highlighter.** The filer highlighted the address. The patch takes its colour from
  inside the box, so the highlighted line stays yellow, if lighter where the number was.
- **Trailing punctuation** (`JR.;`) moves with the stand-in, instead of being left
  stranded after a gap.
- **Capitalisation follows the page.** One rule gives `JOHN Q SAMPLE` in the all-caps
  caption and `John Q Sample` in body text.

Verified by OCR of the output, on literals and bare digits. A separate sweep of every
file in this folder found none of the original values.

## Why this document

A writ is a short court order with the money in prose rather than in a table: the sum,
the date it is stated as of, the post-judgment rate, the per-day interest and the return
deadline all sit in two sentences. It also has a court seal with a signature across it,
and a dense caption.

`schema.json`: **20 leaf fields** (counted from the schema), all populated.

## Featured fields: what the sheriff must collect, for whom

| Field | Value |
|---|---|
| Amount to satisfy | 450797.72 |
| Per-diem interest | 110.96 |
| Property | 100 Sample Avenue, Portland, OR 97000 |
| Judgment creditor | PennyMac Loan Services, LLC |

All four are on page 2, one per printed line. The interest rate (9.00%) and the 60-day
return deadline are correct but share lines with the sum and the per-diem interest, so
they would repeat those crops. `judgment_creditor` is pinned to occurrence 1, the
creditor sentence on page 2; occurrence 0 is the caption on page 1.

## Grounding and extraction notes

- **Each value grounds to its pleading line.** The ruled line numbers down the margin
  did not confuse the reading order.
- **"AKA" split one defendant in two.** The caption reads "Unknown heirs & devisees of
  [borrower] AKA [alias]; [heir]; …". `defendants[0]` came back as "… OF JOHN Q SAMPLE.
  AKA", and the alias as a separate defendant.
- **Seal and signature.** The parse labels the seal and the signature across it
  `[STAMPED][SIGNED]`. `has_court_seal` and `is_signed` are correct and read `OFF`, as
  booleans do. `issued_date` (2024-12-12) is read from the handwritten "12/12/24".
- **Dates read `OFF`** against their long-form text ("December 10, 2024"). The crops are
  correct.

## Cost

**3.40 credits** at standard tier: 2-page parse and extraction.

## Regenerating

```bash
# From the original packet; the rules file stays outside the repo.
.venv/bin/python document-types/scripts/redact_scan.py <packet>.pdf \
    source/writ-of-execution-redacted.pdf --rules <outside-the-repo>/rules.json \
    --pages 1 2 --verify-also <the surnames, street number and original numbers>

.venv/bin/python document-types/scripts/run_ade.py writ-of-execution
.venv/bin/python document-types/scripts/build_images.py writ-of-execution
.venv/bin/python document-types/scripts/inspect_fields.py writ-of-execution --page 2
```

Requires `tesseract` on the PATH (`brew install tesseract`).
