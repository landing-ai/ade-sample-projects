# Credit Agreement

A revolving credit agreement under which Truist Bank and STI Institutional & Government,
Inc. lend to the Hillsborough County Aviation Authority, the Florida special district that
runs Tampa International Airport. Truist Bank acts as agent. The facility is up to
$100,000,000 and is drawn through two subordinated revenue notes, Series 2020A
(tax-exempt) and Series 2020B (taxable). It is the execution copy, dated as of April 20,
2020. **76 pages, portrait (612×792)**: cover and table of contents, then the agreement
(pages 6–50: definitions, the commitment, interest and fees, conditions, covenants, events
of default and miscellaneous provisions), a scanned signature page with the Authority's seal
(page 51), and exhibits (pages 52–76): the two forms of note, advance requests,
certificates and the form of authorizing resolution.

| | |
|---|---|
| Publisher | Hillsborough County Aviation Authority (Tampa International Airport) |
| Source | [tampaairport.com, document 2020-67](https://tampaairport.com/sites/default/master/files/2020-67%20-%20HCAA%20Revolving%20Credit%20Agreement%20-%20April%2020,%202020.pdf) |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | `public` |

## Clearance

The Authority is the borrower. It publishes the executed agreement on its own website as
document 2020-67, a public record of a public body. The same site also posts the later
Amendment Two and the board minutes that discuss the facility.

The agreement names some people: Authority officers and a staff member, and a bank
officer. They appear in the signature blocks, on the signature page (wet-ink signatures,
on a scan) and in the notice addresses on page 13 (work email addresses and phone
numbers). **The operator chose to keep these names, signatures and contact details exactly
as the Authority published them.** No visible content was changed. The only change was
clearing the hidden PDF metadata. It held the Word file name and a document author
username. Text layer, pages and images are otherwise as published.

## Why this document

The collection's other lending documents are short consumer instruments, such as
promissory notes and retail installment contracts. This is the first long commercial loan
agreement: 50 pages of defined terms and cross-referenced sections, where each economic
term sits in its own definition, far from the others. The facility size is on page 12,
the margin on page 7, and the unused fee and minimum advance on page 32.
Extraction has to find them all in a document that mostly says "as defined in Section
X". It is also a mixed document: a text-layer body around a single low-resolution
scanned signature page.

## Featured fields

All are on page 6 (printed page 1): the opening paragraph, which says who the deal is
between in one sentence.

- **Agreement date**: April 20, 2020. Pinned to occurrence 1, because occurrence 0 is the
  cover.
- **Borrower**: Hillsborough County Aviation Authority.
- **Lender (bank)**: Truist Bank.
- **Lender (STI)**: STI Institutional & Government, Inc.
- **Agent**: Truist Bank. Pinned to occurrence 1, the "as agent" clause in the opening
  paragraph, because occurrence 0 is the cover.

None of them is a person. Grounding is at the line level, so the date and the borrower
share one boxed line. The two Truist Bank fields box different lines: the bank as lender
on the second line, as agent on the fourth.

The request suggested the agreement date, borrower, lenders and agent, the maximum
commitment amount and the applicable margin, as suggestions only. It noted that these
are on different pages. The commitment amount ($100,000,000, page 12) and the margin (46
basis points, page 7) both ground correctly. They cannot share an overlay with the
parties, so they are extracted but not featured.

## Grounding notes

- **Definitions ground precisely.** Every economic term grounds to its own definition
  line: Applicable Margin, Maximum Commitment Amount, Maximum Lawful Rate, Default Rate,
  LIBOR Rate, the unused commitment fee and the minimum advance. These are on six
  different pages, and none landed on a cross-reference that merely mentions them.
- **ISO dates cannot be featured.** The first schema asked for dates as YYYY-MM-DD.
  Extraction returned 2020-04-20, grounded to the right words ("into as of April 20,
  2020"), but the boxed text did not contain the value, so it could not be shown as a
  crop. Asking for the date "exactly as printed" fixed it. The prior agreement's date
  was changed the same way.
- **Summarised clauses ground off.** `governing_law` ("State of Florida") grounds to the
  capitalised governing-law clause of the form of note on page 54, not to Section 11.09
  of the agreement, and `commitment_termination` grounds to its definition. Both are
  correct but paraphrased, so they are marked `OFF`. `venue` has one exact grounding on
  page 45.
- **The scanned signature page.** DPT-3 tags the page with `[SIGNED]`, `[SEALED]` and
  `[ILLEGIBLE_SIGNATURE]` and reads the seal's text. The bank officer's printed name
  appears three times, each time crossed by his signature at low resolution, and it was
  read as three different surnames. The Authority officers' names, which the signatures
  cross less, were read correctly.

## Schema

26 leaf fields (31 extracted values, as the lenders and notes arrays hold two items each): the title, date and copy label; the borrower (name, entity type, defined
term, enabling law); the lenders and their defined terms; the agent; the notes (series,
full name, tax status); the economic terms (maximum commitment, applicable margin,
benchmark rate, unused fee rate and threshold, default rate spread, maximum lawful rate,
minimum advance); the commitment termination rule; the prior credit agreement; governing
law and venue. It has no fields for people.

## Credits

183.00 credits at standard tier. That is 137.80 for the 76-page parse and the first
extract, then 45.20 for one extract-only run after changing the date fields to "as
printed".

## Regenerate

```bash
# source/ is the published PDF with its metadata cleared (document-types/scripts/pdfmeta.py)
.venv/bin/python document-types/scripts/run_ade.py credit-agreement
.venv/bin/python document-types/scripts/build_images.py credit-agreement
```
