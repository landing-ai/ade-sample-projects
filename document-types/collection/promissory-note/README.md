# Promissory Note

Source assets for `landing.ai/document-type/promissory-note`.

## Sample document

`source/promissory-note-redacted.pdf`: a residential mortgage note on the Fannie Mae /
Freddie Mac Multistate Fixed Rate Note (Form 3200), VA-guaranteed. It records $360,000
at 3.875% over 30 years, owed to Mortgage Express, LLC. **3 pages, portrait, scanned.**

| | |
|---|---|
| Publisher | Multnomah County Circuit Court record, posted by the Oregon State Sheriffs' Association sales site |
| Source | [oregonsheriffssales.org/…/384277-Writ.pdf](https://oregonsheriffssales.org/wp-content/uploads/2025/01/384277-Writ.pdf), pages 9–11 of 13 |
| Retrieved | 2026-10-02, by script |
| Clearance | **Redacted**, see below |

It was filed as Exhibit 1 (pages 1–3 of 5) to a foreclosure judgment, in a sheriff's-sale
packet. Its allonge, the writ and the judgment from the same packet are separate samples,
and all four share the same stand-ins.

## Redaction

| Data | Replaced with |
|---|---|
| Borrower's printed name | `JOHN Q SAMPLE` |
| Borrower's handwritten signature | "John Q Sample" in a handwriting font |
| Borrower's handwritten initials, on every page | "JQS" in a handwriting font |
| Property house number and street | `100 Sample` (the printed "Ave" is kept) |
| Property ZIP code | `97000` |

The loan number, case number and MIN were blacked out by whoever filed it, before
scanning, and those blackouts are kept.

The lender's office address and the loan originator's name and NMLS ID are kept. They
appear in a professional capacity, and NMLS IDs are public registrations.

All of it was done in the pixels with `document-types/scripts/redact_scan.py`, which
this sample extended:

- **Signature and initials.** `--erase` paints out a region and redraws a stand-in in
  Indie Flower, an openly licensed handwriting font, in the region's own ink. The note
  still shows it was signed and initialled. Where the original strokes crossed a
  signature line or an initials line, that segment of line is redrawn (`=__`).
- **Bold.** The property address is printed in bold, so it is replaced in bold with
  `--bold`. Measuring stroke weight did not separate bold from regular on type this
  small: the bold address measured only 1.08× its neighbours. So bold is set explicitly
  rather than detected.
- **Rules that survive OCR.** The scan's small type reads "Ave" as "Avo" and "Jr." as
  "Yr.". So the address rule matches the house number and street only, leaving the
  printed suffix, and the name has an explicit `YR` variant in the rules file.

The redrawn signature line is a little heavier than the original segment beside it.

Verified by OCR of the output, on literals and bare digits. A separate sweep of every
file in this folder found none of the original values.

## Why this document

A promissory note is the core loan document: amount, rate, payment, maturity, late
charges. This one is a standard uniform instrument, scanned at low resolution with small
type. It tests whether the terms come out correctly from dense, slightly degraded print.

`schema.json`: **24 leaf fields** (counted from the schema). 19 of the 20 top-level
fields populate. `loan_number` stays blank because it is blacked out.

## Featured fields: the loan's terms

| Field | Value |
|---|---|
| Lender | Mortgage Express, LLC |
| Principal | 360000.0 |
| Interest rate (%) | 3.875 |
| Monthly payment | 1692.85 |

All four are on page 1, and each boxes the sentence that states it. No person is
featured.

## Grounding and extraction notes

- **"Oregon" was read as "Orogon"** by the parse, in the small bold date line, and
  `state` extracts it that way. Everything else on the page read correctly, including
  the dates, payment terms and the lender's office address.
- **A blank field grounds to the whole page.** `loan_number` is blacked out and comes
  back as an empty string with **57 ranges** spanning nearly all of page 1, where it
  should have no ranges at all.
- **Dates read `OFF`** (`note_date` 2019-03-08 against "March 8, 2019") because the
  check compares digits. The crops are correct.
- **Signed and initialled.** `borrower.is_signed` grounds to the parse's
  `[SIGNED][SEALED]` label on the stand-in signature. `initialed_pages` is 3.

## Cost

**7.00 credits** at standard tier: 3-page parse and extraction.

## Regenerating

```bash
# From the original packet; the rules file stays outside the repo.
.venv/bin/python document-types/scripts/redact_scan.py <packet>.pdf \
    source/promissory-note-redacted.pdf --rules <outside-the-repo>/rules.json \
    --pages 9 10 11 --bold "9:<the house number and street rule>" \
    --handwriting-font document-types/scripts/fonts/IndieFlower-Regular.ttf \
    --erase "9:448,653,495,676=JQS" "10:452,654,499,675=JQS" "10:452,675,466,678.3" \
            "10:452,675.2,466,675.9=__" "11:452,654,493,676.4=JQS" "11:452,676.4,467,679" \
            "11:452,676.6,467,677.3=__" "11:204,172,421,198=John Q Sample" \
            "11:204,198,421,203.5" "11:300,203.5,421,212" "11:204,199.4,421,200.2=__" \
    --verify-also <the surnames and street number>

.venv/bin/python document-types/scripts/run_ade.py promissory-note
.venv/bin/python document-types/scripts/build_images.py promissory-note
.venv/bin/python document-types/scripts/inspect_fields.py promissory-note --page 1
```

Requires `tesseract` on the PATH (`brew install tesseract`).
