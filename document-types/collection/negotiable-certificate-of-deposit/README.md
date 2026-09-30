# Negotiable certificate of deposit

Source assets for `landing.ai/document-type/negotiable-certificate-of-deposit`.

## Sample document

`source/occ-first-negotiable-cd.jpg` — a Barclays Bank D.C.O. negotiable certificate of
deposit, No. 301, issued in Johannesburg on 25 July 1964 for R100,000 at 3.65% for 180
days, due 21 January 1965. **1 image, landscape (600×461)**, a black-and-white
reproduction of the printed certificate, completed by hand and typewriter, with three
South African revenue stamps and two signatures.

| | |
|---|---|
| Publisher | Office of the Comptroller of the Currency (image credited to A. P. Faure / South African Financial Markets Journal) |
| Source | [occ.gov/images/history/img-barclays-cd-600px.jpg](https://www.occ.gov/images/history/img-barclays-cd-600px.jpg) |
| Retrieved | 2026-09-30 |
| Clearance | Public |

The OCC publishes the image on its history page,
[The Negotiable CD: National Bank Innovation in the 1960s](https://www.occ.gov/about/who-we-are/history/history-of-the-occ/1936-1966/1936-1966-negotiable-cd.html),
with the caption "In July 1964 the British bank Barclays, in amalgamation with the
National Bank of South Africa, issued a negotiable CD (above) at 100,000 Rand" and the
credit **A. P. Faure / South African Financial Markets Journal**. It is therefore a
third-party image the OCC republishes, not a US government work, and the credit line
should go with it; the manifest carries it in `origin.credit`.

The certificate is payable to the bearer and names no individual. The two signatures are
the bank's General Manager and Chief Accountant, signing in their official capacity. No
redaction was needed.

**Not the first negotiable CD.** The request describes this as the first negotiable CD
ever issued. The OCC page says First National City Bank of New York issued the first, in
February 1961, and presents this 1964 certificate as an early international one.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **historical financial instrument**, and its first document
completed by hand on a printed form:

- **Handwriting over print.** The dates, amount, term and rate are written or typed into
  blanks on an engraved form, in a mix of scripts.
- **A small, old reproduction.** 600 pixels wide, black and white, with a decorative
  border and ornamented type.
- **A form with a choice left in.** "payable to *the Bearer of this Certificate *the
  Order of", with a footnote to delete whichever is inapplicable.
- **Revenue stamps** stacked down the right edge, each with its value.

## Featured fields: the instrument's terms

All on the certificate. The request named no fields, so these were chosen:

| Field | Value |
|---|---|
| Issuing bank | BARCLAYS BANK D.C.O. |
| Principal | R100,000 |
| Interest rate | 3.65% |
| Term in days | 180 |
| Value at maturity | R101,800 |

The whole instrument in five values, and they reconcile: R100,000 at 3.65% for 180 days
earns R1,800 (100,000 × 0.0365 × 180/365), which gives the printed value at maturity of
R101,800. The principal grounds to the whole "the sum of R100,000-00 (One hundred thousand
Rand)" line and the term to the whole "180 days after date hereof…" line.

The maturity date is not featured: it is extracted as the ISO date 1965-01-21 and flagged
against the printed "21st January 1965", and the value at maturity makes the same point.

## What it surfaced

**The handwritten issue date comes apart, and extraction puts it back together.** "25th
July 1964" is written across the form's printed date line; the parse returns it in two
fragments, "25th." near the top and "ly 1964." at the end of the markdown. Extraction
still returns 1964-07-25.

**A small printed title is lost.** The second signature's title, "Chief Accountant", is
printed in small type under the signature and does not appear in the parse, so only the
General Manager comes back as a signatory.

**Everything else extracts correctly,** including the amalgamated bank, the certificate
number, the amount in words, the bearer choice and all three revenue stamps' values, read
from the stamps themselves.

## Extraction

**16 leaf fields**: issuer, amalgamated bank, place and number, issue and maturity
dates, currency, principal in figures and words, value at maturity, term, rate, payee,
place of repayment, signatories and revenue stamps.

## Cost

**2.00 credits** at standard tier for 1 image: 1.00 to parse, 1.00 to extract.

## Regenerating

```bash
curl -sSL -o document-types/collection/negotiable-certificate-of-deposit/source/occ-first-negotiable-cd.jpg \
  "https://www.occ.gov/images/history/img-barclays-cd-600px.jpg"
.venv/bin/python document-types/scripts/run_ade.py negotiable-certificate-of-deposit                # 2.00 credits
.venv/bin/python document-types/scripts/run_ade.py negotiable-certificate-of-deposit --extract-only # 1.00, schema iteration
.venv/bin/python document-types/scripts/build_images.py negotiable-certificate-of-deposit           # free
.venv/bin/python document-types/scripts/inspect_fields.py negotiable-certificate-of-deposit --page 1
```
