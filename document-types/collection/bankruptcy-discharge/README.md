# Bankruptcy Discharge

A US Bankruptcy Court order in a Chapter 7 case, from the District of South Carolina.
One order does three things: it discharges the debtor, discharges the trustee and closes
the case. It is court form 166BNC, issued through the court's electronic filing system
and signed by the bankruptcy judge. **2 pages, portrait (595×792)**. Page 1 is the order.
Page 2 is the standard back page, "Explanation of Bankruptcy Discharge in a Chapter 7
Case", which is generic text with no personal data apart from the case number in the
filing header.

| | |
|---|---|
| Publisher | United States Bankruptcy Court, District of South Carolina (a court record, posted to Scribd by a third party) |
| Source | scribd.com/document/489929789/Discharging-Debtor-7-Trustee-Closing-Case-Auto-Part-1 (the website shows this URL as plain text, not as a link) |
| Retrieved | 2026-10-03, downloaded manually |
| Clearance | `redacted` |

## Clearance

Scribd blocks scripted requests, so the operator downloaded the file by hand. Scribd is a
user-upload site, not a publisher, so this order is treated as a private person's
record. The court is kept. The debtor is replaced.

| What | Replaced with | Occurrences |
|---|---|---|
| Debtor's name | Jane Q Sample | 1 |
| Other names used by the debtor (aka and fka) | Jane Sample, John Q Sample | 2 |
| Debtor's street address | 100 Main St | 1 |
| Debtor's city and ZIP code (state kept) | Anytown, SC 29000 | 1 |
| Last four digits of the SSN | xxx-xx-4321 | 1 |
| Case number | 09-30789-dd | 3 |
| Judge's handwritten signature | a stand-in signature in Indie Flower | 1 |

The case number is printed twice on page 1: in the body, and in the electronic case
filing (ECF) header line at the top. It is printed once more in page 2's header. The
body and the header set it in different fonts and with different dashes. All three
places use **one stand-in** from `plausible.py`. The year prefix and the judge-initials
suffix are kept.

Text was replaced with `document-types/scripts/redact.py`, which removes the underlying
text rather than covering it, and the PDF metadata was cleared.

**Two differences from the original can be seen on the page:**

- **The judge's signature was an inline image.** The scan of the signature was embedded
  in the page's content stream as an inline image (`BI … ID … EI`), not as an image
  XObject. Neither `redact.py --remove-images` nor a PyMuPDF redaction annotation can
  reach an inline image, so the `BI…EI` block was cut out of the content stream directly
  and checked to be gone. A stand-in signature, "J Q Sample", was then drawn in its place in Indie Flower,
  an openly licensed (SIL OFL) handwriting font kept at `document-types/scripts/fonts/`.
  The order still shows that it was signed. No judge's name is printed on the order, so
  no name was kept or replaced.
- **Minus signs became hyphens in the body.** The body sets the dashes in the case number
  and in the masked SSN as U+2212 minus signs. The replacement font (Helvetica) cannot
  draw that character, so the stand-ins use ASCII hyphens, as the ECF header already did.
  Every other minus sign on the page is unchanged.

Kept as printed: the court and its address, the clerk of court's printed name (official
capacity), the dates, the docket number and the ECF timestamp.

**Verified:** no original value can be extracted from the committed PDF, checked both as
literal strings and as bare digits, and no original value appears anywhere in this
folder. The rules file stays outside the repo.

## Why this document

It is a short court order, and the facts a lender or servicer needs from it are spread
across three kinds of layout: a filing header in large type, a heading block with bordered
"Entered" and "Filed" stamps, and numbered ordering paragraphs. One heading carries three
stacked order titles, and the debtor block lists other names used ("aka", "fka") on one
line. The back page turns a lettered list of debts that are not discharged into an
array. It is also the first sample in the collection with an inline-image signature.

## Featured fields

All on page 1, and none of them is a person:

- **Court**: the heading line, "United States Bankruptcy Court – District of South Carolina".
- **Chapter**: pinned to the "Chapter: 7" line (occurrence 1), not the ECF header's
  "Desc Ch 7".
- **Order**: the first order title, "DISCHARGE OF DEBTOR".
- **Statute cited**: section 727 of title 11, United States Code, grounded to paragraph 1.
- **Entered (ECF timestamp)**: "11/30/09 02:00:37", grounded to the header line.

The request suggested the chapter, the court, the discharge or entry date, and the
statute. The entry, filed and signed dates come back as ISO dates (`2009-11-30`) from
"11/30/09" and "November 30, 2009". So they read `OFF` in the digit check and could not
be featured. The ECF entry timestamp, printed as-is, stands in for the entry date.

## Grounding

- **Every featured field grounds to its own line**, and the crops are tight.
- **The debtor's other names split correctly.** The "aka …, fka …" line comes back as two
  names, with the prefixes dropped.
- **Dates and booleans read `OFF`**, as expected. The dates are normalized to ISO.
  `trustee_discharged` and `case_closed` ground to ordering paragraphs 2 and 3, and
  `is_signed` grounds to the parse's `[SIGNED]` label on the stand-in signature.
- **One stray range.** `case_number` has three ranges. Two are right: the header and the
  "Case Number:" line. The third runs from the signature block across the page break to
  page 2's header. It contains the case number at its very end, but `inspect_fields.py`
  resolves it to the signature block on page 1.
- **The last two items in the lettered list read `OFF`.** Items (i) and (j) wrap onto a
  second line, and each splits into two ranges. The values are right.
- **The parse transcribes the stand-in signature** as "J Q Sample" under `[SIGNED]`.

## Schema

`schema.json` was written for this order, with **22 leaf fields**: the court, form
number, case number, chapter and docket number; the debtor (name, other names, address,
SSN last four); the order titles; the entered and filed dates and the clerk; the statute
cited; whether the trustee is discharged and the case closed; the place, date, signer's
title and signed flag; the ECF entry timestamp; and the list of debts that are not
discharged from page 2. All 19 top-level fields populate, with no warnings.

## Cost

**4.90 credits** at standard tier: 2-page parse and extraction.

## Regenerating

```bash
# 1. Cut the inline-image signature out of page 1 and draw the stand-in (PyMuPDF):
#    find the BI/ID/EI block in the page's content stream, delete it with
#    doc.update_stream(), then page.insert_text(..., "J Q Sample",
#    fontfile="document-types/scripts/fonts/IndieFlower-Regular.ttf", fontsize=26)
#    at the image's former position.
# 2. Replace the text. The rules file stays outside the repo.
.venv/bin/python document-types/scripts/redact.py <signature-replaced>.pdf \
    document-types/collection/bankruptcy-discharge/source/bankruptcy-discharge.pdf \
    --rules <outside-the-repo>/rules.json

.venv/bin/python document-types/scripts/run_ade.py bankruptcy-discharge
.venv/bin/python document-types/scripts/build_images.py bankruptcy-discharge
.venv/bin/python document-types/scripts/inspect_fields.py bankruptcy-discharge --page 1
```
