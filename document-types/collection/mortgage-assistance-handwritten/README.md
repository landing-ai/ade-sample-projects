# Mortgage Assistance (Handwritten)

Page 1 of Chase's **Request for Mortgage Assistance Form** (D19693 RMA 09/13): the borrower and
co-borrower section, servicemember status, property and occupancy, assistance history, listing
and counselling details, and taxes and insurance. It has been **filled in by hand** and scanned.
The source is one portrait page, a raster scan with no text layer.

## Provenance

| | |
|---|---|
| Publisher | LandingAI; the form itself is JPMorgan Chase's published form |
| Source | Not published online. A specimen filled in by hand by LandingAI staff, from LandingAI's internal marketing document library (doc35) |
| Retrieved | 2026-11-16 |
| Clearance | `public` |

A LandingAI staff member printed the blank form, filled it in by hand with **invented data**,
and scanned it. Everything handwritten on the page is fictitious, written for this specimen:

- names, Social Security numbers and dates of birth
- phone numbers (the 555 range) and email addresses
- the mailing address and loan number
- the credit counselor's details

No real borrower's data is present, so nothing was redacted. The PDF metadata was cleared. The
Chase name and logo appear because they are printed on the form; Chase did not produce or endorse
this specimen.

## Why this document

It has two kinds of hand input on a dense, faint, small-print bank form:

- **Handwritten values**, in print and cursive, written into labelled boxes.
- **Hand-drawn ticks** in checkboxes, often overrunning the box and the label beside it.

It is the handwritten counterpart to the collection's typed forms.

## Schema

The schema was supplied with the request and used unchanged. It has 27 leaf fields:

- the loan number
- the borrower and co-borrower (name, SSN, date of birth, phone, email, mailing address)
- servicemember status
- property type and occupancy
- assistance history
- tax and insurance details

## Featured fields (page 1)

| Field | Value |
|---|---|
| Loan number | 443781220 |
| Borrower | Stephanie Carter |
| Property use | Primary Residence (ticked) |
| Occupancy | Owner Occupied (ticked) |

Two handwritten values and two hand-ticked checkboxes. The borrower's name is featured because
the data is an invented specimen.

## Grounding on this document

**Handwritten values ground to their boxes.** The loan number, both names, both SSNs, the phone
number and the mailing address each ground `ok`, to the box that holds the label and the
handwriting.

**Ticks ground to their row in the upper part of the form.** There the ticked option comes back
as "[x] Primary Residence" and "[x] Owner Occupied", and the box sits on the right row.

**Lower down, the checkbox boxes drift.** The real estate tax and insurance questions near the
foot of the page extract correctly, and their ranges point at the right option ("[x] Lender
does"). But the boxes land one and two rows below it: on "Are the taxes current?" and on
"Insurance Company Phone Number(s)". Both were tried as a fifth featured field and dropped. The
crops showed the wrong row, though `inspect_fields.py` read `ok`. This is the line-drift failure
that only opening the crops catches.

**Answers derived from ticks ground `OFF`.** Yes/no booleans, such as "is the property listed for
sale", ground to the question rather than to the tick that answers it.

**Blank fields come back empty.** Blank boxes, such as the co-borrower's home phone and the
insurance company, extract as empty values.

## Credits

3.80 credits at standard tier: parse plus extract, 1 page.

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py mortgage-assistance-handwritten
.venv/bin/python document-types/scripts/inspect_fields.py mortgage-assistance-handwritten --page 1
.venv/bin/python document-types/scripts/build_images.py mortgage-assistance-handwritten
```
