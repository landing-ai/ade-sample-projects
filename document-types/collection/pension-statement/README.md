# Pension statement

Source assets for `landing.ai/document-type/pension-statement`.

## Sample document

`source/nys-ers-pension-pay-stub-2022-specimen.pdf` is the specimen pension pay stub
that the New York State and Local Retirement System shows its retirees. It is the
monthly payment advice the Employees' Retirement System (ERS) issues to a retiree, for
the period 8/01/2023 to 8/31/2023. **1 page, landscape.** It has a header with the pay
group, pay period, advice number and date, then a recipient block and federal tax data,
earnings and taxes tables, before-tax and after-tax deduction tables, a summary band
with current and year-to-date totals, and a net pay distribution table.

| | |
|---|---|
| Publisher | Office of the New York State Comptroller (New York State and Local Retirement System) |
| Source | [web.osc.state.ny.us/…/pay-stub-2022-for-web.svg](https://web.osc.state.ny.us/retire/retirees/paystub-tutorial/pay-stub-2022-for-web.svg) |
| Retrieved | 2026-10-03, by script |
| Clearance | Public (specimen) |

The Comptroller's "Your Pension Pay Stub" tutorial page for retirees embeds this image
and explains each part of the stub. Every personal value is a placeholder: John Smith,
123 Main Street, Any Town NY 12345-0000, employee ID R12345678, and an account number
masked as XXXXXXX1234. The only real address is the Comptroller's own office. Nothing
needed redacting.

### How the PDF was made

The publisher distributes the stub as an **SVG**, not a PDF. It was exported from Adobe
Illustrator with every character outlined as a vector path, so it has no text at all.
PyMuPDF renders this SVG as a solid black page, so the SVG was printed to PDF with
headless Chrome, run as a local renderer with a throwaway profile. The SVG was placed in
a small local HTML page sized to its 615.27 x 459.91 viewBox, which gave a one-page
11 x 8.2225 in landscape page with no margins:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
    --disable-gpu --user-data-dir=<scratch>/chrome-profile --no-pdf-header-footer \
    --print-to-pdf=out.pdf file://<scratch>/wrap.html
```

`wrap.html` sets `@page { size: 11in 8.2225in; margin: 0 }` and shows the SVG as an
`<img>` filling the page. The PDF's document metadata (Chrome's title and producer
strings) was then cleared. The result was rendered with PyMuPDF and checked by eye
against the SVG. **The PDF has no text layer**, so ADE parses this sample from the page
image alone.

## Why this document

The collection's first **pension payment**. It is a defined-benefit annuity, as opposed
to a balance invested in a plan like the workplace plan at `retirement-statement`, the
IRA at `ira-statement` or the 401(k) at `401k-statement`. Strictly it is a payment
advice, not an award letter or an annual benefit statement: it shows one month's
pension payment and what came out of it.

- **It looks like a pay stub, but the earnings are a pension.** The single earnings line
  is a Monthly Service Annuity. The layout matches `pay-stub`, so the schema has to name
  the retiree, not an employee.
- **Pension-specific deductions.** An equitable distribution, which is the share of the
  pension paid to a former spouse under a divorce order, is taken before tax. A county
  retiree health premium is taken after tax.
- **Current and year-to-date figures side by side,** in every table and in the summary
  band, so each value has a twin in the next column.
- **Outlined text, no text layer.** Nothing on the page can be read as text. Every value
  comes from the page image.

## Featured fields: one month's pension payment

All on page 1. The request named no page or fields, but its notes suggested these four,
and all four ground cleanly:

| Field | Value |
|---|---|
| Monthly service annuity | 2,148.58 |
| Federal withholding | 257.82 |
| Total deductions | 802.50 |
| Net pay | 1,088.26 |

They reconcile: 2,148.58 less 257.82 withheld and 802.50 in deductions (723.88 + 78.62)
is 1,088.26. Deductions and net pay come from the Current row of the summary band, not
the YTD row beneath it, and not the matching 1,088.26 in the distribution table.

## What it surfaced

**Every value extracts correctly,** with no text layer to lean on. All 36 leaves match the
page, including the advice number with its leading zeros and the masked account number.

**The table cells ground at cell size.** The annuity and withholding boxes cover the whole
tall data cell of their table, most of which is blank space below the value. The value is
inside the box, so the crop is right, but the box is larger than the number. The summary
band values ground tightly to the number.

**The payer's address grounds OFF.** Its two lines ground as two separate pieces, so the
two-line value does not match either one. It is not featured.

**The date and the file name disagree.** The file is named for 2022 but the stub is for
August 2023. Fields record what is printed.

## Extraction

**36 leaf fields**: the payer, the retiree, the payment period and advice identifiers,
the federal tax data, each line of the earnings, taxes, before-tax and after-tax
deduction tables with current and YTD amounts, the summary band, and the net pay
distribution.

## Cost

**2.80 credits** at standard tier for 1 page, for parse and extract together. There was
one run, with no schema revisions.

## Regenerating

```bash
# The source is the publisher's SVG printed to PDF with headless Chrome (see above);
# the committed PDF is that print with its metadata cleared.
.venv/bin/python document-types/scripts/run_ade.py pension-statement                # 2.80 credits
.venv/bin/python document-types/scripts/run_ade.py pension-statement --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py pension-statement           # free
.venv/bin/python document-types/scripts/inspect_fields.py pension-statement --page 1
```
