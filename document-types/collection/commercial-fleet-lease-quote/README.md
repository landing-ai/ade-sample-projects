# Commercial Fleet Lease Quote

Source assets for `landing.ai/document-type/commercial-fleet-lease-quote`.

## Sample document

`source/enterprise-fleet-lease-rate-quotes-redacted.pdf` is a set of **Open-End (Equity)
Lease Rate Quotes** from **Enterprise Fleet Management**, with Enterprise FM Trust as the
lessor, prepared for **Hidalgo County, Texas** in May 2019. Each quote prices one vehicle
for the county's fleet on a 60-month open-end lease: capitalized cost, depreciation
reserve, monthly lease charge, a full maintenance program, the all-in monthly rental and
the reduced book value the vehicle is expected to carry at the end of the term.

**32 pages, portrait, text layer.** Seven quotes run back to back, of 4 to 6 pages each:

- A **rate page** (pages 1, 5, 9, 13, 17, 23, 28): a header block (vehicle, term, state,
  customer number), a long dollar column with its labels to the right, an Order
  Information box in the right-hand column, notes and an unsigned lessee line.
- Sometimes an **Other Totals** or **Aftermarket Equipment** page (24, 29).
- A **Vehicle Information** page: invoice and MSRP pricing summary, colours and a
  selected-options table.
- Two pages of **configured features**, as label/value lists.

The vehicles are two Ford F-250s, three Ford F-150s, a Chevrolet Colorado and a
Chevrolet Express 2500. Page 19 is blank apart from its footer, as in the original.

| | |
|---|---|
| Publisher | Enterprise Fleet Management / Enterprise FM Trust (lessor); posted by the Hidalgo County, Texas Commissioners Court |
| Source | [public.destinyhosted.com/hidaldocs/2019/CC/20190604_3330/70466_Quotes.pdf](https://public.destinyhosted.com/hidaldocs/2019/CC/20190604_3330/70466_Quotes.pdf) |
| Retrieved | 2026-10-25, by script |
| Clearance | **Redacted**, see below |

The county published the quotes as an attachment to agenda item 70466 of its
Commissioners Court meeting of 4 June 2019, on its public agenda-publishing host. They
are part of the public meeting record.

## Redaction

The quotes carry no signatures (the lessee line is blank), phone numbers or addresses.
Three identifiers were replaced with `document-types/scripts/redact.py`, which removes the
underlying text rather than drawing a box over it:

| What | Replaced with | Count |
|---|---|---|
| County employee's name under Prepared For | `Sample, Jane` | 7 |
| Enterprise account representatives' initials (AE/AM) | `0AB/CD0` | 7 |
| The county's Enterprise customer number (Customer#) | A random 6-digit stand-in from `plausible.py` | 7 |

The PDF metadata, which carried an Enterprise user ID, was cleared. Quote numbers,
prices, dates and vehicle details are kept. The originals are not recorded anywhere in
this folder, and the rules file stays outside the repo. Verified by redact.py's text
check, by eye on renders, and by `ship.py check --rules` over every file in this folder.

## Why this document

It is a financial quote laid out as a **two-column form whose values sit to the left of
their labels**, with a boxed Order Information panel in the right-hand column beside
them. A value can easily pair with the wrong label, or with text from the other column.
It also repeats one layout seven times with different numbers, so extraction has to keep
each quote's values with their own quote. The schema is an array of quotes for that
reason.

## Featured fields

All on **page 5**, the rate page of the second quote (Quote No. 4270567, a 2019 Ford
F-250 XL crew cab):

| Field | Label | Value |
|---|---|---|
| `quotes[1].vehicle.model` | Vehicle model | F-250 |
| `quotes[1].term_months` | Lease term (months) | 60 |
| `quotes[1].total_capitalized_amount` | Total capitalized amount | 38,000.00 |
| `quotes[1].total_monthly_rental_including_services` | Total monthly rental | 679.71 |
| `quotes[1].reduced_book_value_at_term` | Reduced book value at term | 8,360.00 |

Together they tell one quote: which truck, for how long, what it costs to put on the
road, what the county pays each month, and what the truck is worth at the end of the term.

The request suggested page 1 and the lessee as well. On page 1, the total monthly
rental and the reduced book value grounded to their **labels** instead of the dollar
amounts, so those crops would have shown the wrong text. On page 5, whose quote has the
same amounts as page 1's and differs only in colour and quote number, both ground on the
values. The lessee was dropped because on page 5 its range resolves to a line of the
Notes paragraph rather than to "Prepared For" or "LESSEE". The term box covers the whole
Vehicle Order Type / Term / State / Customer# line, including the stand-in customer
number.

## Grounding notes

- **DPT-3 turned the dollar column into a two-column table**, value on the left and
  label on the right, and paired them correctly on every rate page, including the
  subtotal and total rows. That is the hard part of this layout, and it went well.
- **Some text from the right-hand column ended up in the label cells.** On several rate
  pages, fragments of the right-hand column ("All language … apply to", "Order Int",
  "Drive") appear in the label cell of the row beside them. Extraction ignored them.
- **The same value grounded differently on near-identical pages.** On page 1 two totals
  ground to the label cell; on page 5, with the same layout and the same amounts, they
  ground to the value cell. The parse of page 9 also repeats the bottom five rows of the
  dollar column as a second table. Extraction was right in every case, but where its
  ranges pointed varied from one copy of the layout to the next.
- **Contract Miles grounded OFF on every quote**, usually to the maintenance fee in the
  same table row (`$ 39.16` on page 1) and sometimes to the "Full Maintenance Program"
  label, because the parse put the inline "Contract Miles 50,000" in the label cell of
  that row.
- Header fields (year, make, model, term, state) ground to whole header lines, so their
  boxes are wide but correct.

## Schema

`schema.json` has **33 leaf fields**: the lessor, fleet manager and lessee, and an array
of quotes, each with its number, date, vehicle (year, make, model, series, exterior
colour), order type, term, state, the dollar column from capitalized price to service
charge at termination, maintenance contract miles and over-mileage rate, estimated annual
mileage, and the invoice/MSRP pricing summary. The individual contact and the customer
number are left out on purpose. All 7 quotes were extracted with no warnings.

## Credits

**67.7 credits** at the standard tier: 40.9 for parsing 32 pages with DPT-3 Pro and 26.8
for extraction.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py commercial-fleet-lease-quote               # spends credits
.venv/bin/python document-types/scripts/run_ade.py commercial-fleet-lease-quote --extract-only
.venv/bin/python document-types/scripts/build_images.py commercial-fleet-lease-quote          # free
.venv/bin/python document-types/scripts/inspect_fields.py commercial-fleet-lease-quote --page 5
```
