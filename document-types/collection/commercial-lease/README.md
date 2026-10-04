# Commercial Lease

Source assets for `landing.ai/document-type/commercial-lease`.

## Sample document

`source/commercial-lease-serve-robotics.pdf`: page 1 of an office **Lease Agreement**
for 730 Broadway, Redwood City, California, between Bauen Fund 2018-730, LLC (landlord)
and Serve Robotics Inc. (tenant), dated February 25, 2021. **1 page, portrait.**

The page is the lease's **Basic Lease Information** summary: lease date, landlord and
tenant notice blocks, the premises (an entire 4,200 rentable-square-foot building), a
48-month term, an escalating base-rent table with a one-month rent waiver, permitted
use, security deposit, and the brokers on each side. It is the part of a commercial
lease that a lease-abstraction workflow actually needs; the remaining 26 pages are the
standard lease terms, exhibits and conformed signatures.

| | |
|---|---|
| Publisher | Serve Robotics Inc. (filing as Patricia Acquisition Corp.), as filed with the SEC |
| Source | [SEC EDGAR, ea180762ex10-6_patriciaacq.htm](https://www.sec.gov/Archives/edgar/data/1832483/000121390023063662/ea180762ex10-6_patriciaacq.htm) |
| Filing | Exhibit 10.6 (material contract) to Form 8-K, accession 0001213900-23-063662, 2023 |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** |

Serve Robotics filed this lease publicly on EDGAR as a material contract; the filing
index lists `ea180762ex10-6_patriciaacq.htm`. Landlord and tenant are companies. The
people named on the page (a notice contact for each party and the landlord's broker)
appear in a professional capacity. No private individual's personal data is present,
so nothing was replaced.

### How the PDF was made

EDGAR publishes this exhibit as HTML, not PDF. The EDGAR URL above remains the source
of record; the PDF here is a rendering of it:

1. Downloaded the `.htm` exhibit from EDGAR by script.
2. Stripped the EDGAR SGML wrapper (the `<DOCUMENT>`, `<TYPE>`, `<SEQUENCE>`,
   `<FILENAME>`, `<DESCRIPTION>` and `<TEXT>` header lines and their closing tags) and a
   tracking `<script>` tag EDGAR injects, keeping the exhibit's own `<HTML>` document
   unchanged.
3. Printed it to a US Letter PDF with headless Chrome, as a local renderer only with a
   throwaway profile: `--headless=new --print-to-pdf --no-pdf-header-footer`. The full
   exhibit renders to 27 pages.
4. Kept page 1, the Basic Lease Information, as the request asked, and cleared the PDF
   metadata (Chrome creator/producer, a temp-file title, creation dates).

The result has a clean text layer, since it was born digital.

## Why this document

Most lease samples are residential forms with typed blanks. This is a negotiated
commercial office lease, and its summary page is laid out the way commercial leases
usually are: a two-column "Defined Terms / Information" grid with no ruling, holding
prose (premises, term, use) alongside a real table (the base-rent schedule with per-
square-foot rates and a footnoted partial-month rate). It tests whether extraction can
pull numbers out of sentences (4,200 square feet from "four thousand two hundred
(4,200) rentable square feet") as well as out of table cells, and whether it can turn a
rent schedule into structured rows.

## Schema

`schema.json` covers the title and lease date, landlord and tenant (name, notice
address, attention line), the premises (description, address, rentable square feet),
the term and what it runs from, the base-rent schedule as an array (period, start and
end month, monthly rent, rate per square foot), the rent-waiver months, permitted use,
security deposit, and both brokers.

**23 leaf fields** (counted from the schema; 43 once the five rent rows are expanded).

Every field came back correct on the first extraction, including `rent_waiver_months`
(1), which is stated only in prose.

## Featured fields: the deal summary, from page 1

| Field | Value |
|---|---|
| Tenant | Serve Robotics Inc. |
| Rentable square feet | 4,200 |
| Term (months) | 48 |
| Monthly base rent (months 2-12) | $16,800.00 |
| Security deposit | $73,431.24 |

Read together: who leases how much space, for how long, at what rent, against what
deposit. These are the five fields the request suggested, and all five ground `ok` on
page 1. The tenant is a company; no person is featured.

## Grounding notes

- **The rent table grounds cell by cell.** Every amount and rate in all five rows
  grounds to its own cell, and `start_month` / `end_month` ground to the period cell
  they were parsed from. The months 2-12 rent crop boxes exactly `$ 16,800.00**`,
  footnote marker included; the extracted value correctly drops it.
- **Prose fields ground to the whole paragraph.** Rentable square feet and term both
  box their full Premises or Term paragraph rather than the number inside it. The value
  is in the box, but the box is a paragraph, not a figure.
- **The tenant box takes two lines.** It covers "Tenant: Serve Robotics Inc." and the
  next line, "730 Broadway," because the parse groups the label and first two lines of
  the notice block together.
- **`OFF` fields:** the lease date (ISO `2021-02-25` vs printed "February 25 , 2021"),
  the landlord's notice address (joined across lines), the permitted use (a value
  spanning two lines) and `rent_waiver_months` (a count inferred from "the first full
  month"). All values are correct; none was a candidate for featuring.

## Cost

**3.40 credits** at standard tier: one 1-page parse and one extraction.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py commercial-lease
.venv/bin/python document-types/scripts/build_images.py commercial-lease
.venv/bin/python document-types/scripts/inspect_fields.py commercial-lease --page 1
```
