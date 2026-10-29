# Certificate of insurance

Source assets for `landing.ai/document-type/certificate-of-insurance`.

## Sample document

`source/Sample_COI_2026-27.pdf` is an **ACORD 25 Certificate of Liability Insurance**
(form edition 2025/12). The American Baseball Coaches Association publishes it as proof
of coverage for its member liability program. Its broker, Sadler Insurance (a division
of Specialty Program Group), issued it on 07/29/2026. It names the ABCA as the insured
and covers the 2026-27 policy year, with Sirius American Insurance Company as insurer A.
It is **1 page, portrait (US Letter)**, with a text layer and a pale diagonal SAMPLE
watermark. Two policy rows are filled in, Commercial General Liability and Professional
Liability, along with a full description of operations. The certificate holder box is
blank.

| | |
|---|---|
| Publisher | American Baseball Coaches Association; certificate issued by Sadler Insurance, Div of Specialty Program Group, LLC |
| Source | https://www.abca.org/common/Uploaded%20files/Membership%20Documents/Sample_COI_2026-27.pdf |
| Retrieved | 2026-10-28, downloaded by script from the publisher's site |
| Clearance | Public |

The ABCA links this certificate from its insurance page (https://www.abca.org/insurance)
as a sample of the proof of coverage members can request. It is used as published, with
no redaction. The producer box names a broker contact and gives a phone number, a fax
number and an email address, and the authorized-representative box carries a
handwritten signature. All of these were kept as the publisher filed them, by the
operator's decision, and none of them is featured. Full provenance is in `manifest.json`
under `source.origin`.

## Why this document

The certificate of insurance is the most widely exchanged insurance document there is,
and the ACORD 25 is its standard form. Its layout differs from the policies and
declarations already in this collection:

- **A dense ruled grid with merged cells.** Each coverage row spans up to seven lines,
  with the policy number and dates in tall merged cells and the limits in a two-column
  label/amount ladder beside them.
- **Checkboxes carry meaning**: occurrence or claims-made, and what the general
  aggregate limit applies per.
- **Mostly blank by design.** The auto, umbrella, workers compensation and insurer B–F
  rows are empty, so the schema has to skip them rather than invent values.
- **A watermark crosses the content**, over the coverage grid.

## Featured fields: who covers the insured, under which policy, when, and for how much

All on page 1.

| Field | Value |
|---|---|
| Insurer A | Sirius American Insurance Company |
| General liability policy number | PLH03GL00001432 |
| Policy effective date | 09/01/2026 |
| Policy expiration date | 09/01/2027 |
| Each occurrence limit | $ 1,000,000 |

A certificate holder opens a COI to check one thing: that the insured has liability
cover, from which insurer, under which policy, for which period, and up to what amount.
These five fields answer it, and all of them are impersonal.

The request's notes also suggested the insurer's **NAIC number** and the **general
aggregate limit**. Both extract correctly and ground `ok`. They were left out only to
stay within five fields.

## What it surfaced

**The limits ladder grounds cell by cell.** All eight limits, six for general liability
and two for professional liability, pair with the right label, and each amount grounds
`ok` to its own cell. The two-column layout the request flagged as a risk caused no
trouble.

**Merged cells give tall boxes.** The policy number and the two dates ground to the
merged cells that span the whole general liability row. The boxes sit on the right row
and contain the values, but they are much taller than the text.

**The checkboxes read correctly where it matters.** The parse renders the general
liability boxes as `[x]`/`[ ]`, and extraction returns `occurrence` and `policy`.
Both fields ground `OFF`, though, because their range is the whole type-of-insurance
cell.

**The watermark caused one misread.** A stroke of the SAMPLE watermark crosses the
umbrella row's CLAIMS-MADE box, and the parse marks it `[x]`, although the umbrella row
is otherwise blank. The schema skips blank coverage rows, so this does not reach the
extraction.

**One value was dropped by the parse.** The producer's phone number is missing from
`parse-pro.md`: the PHONE cell came back as a label alone, so `producer.phone`
extracted as an empty string. The fax and email beside it came through.

**The signature is tagged, not transcribed.** It parses as `[Signature]`. The
`authorized_representative_signed` boolean is right but grounds `OFF`, since `true` never
appears on the page. The blank certificate holder box comes back as `null`.

**The same policy number on two rows.** As printed, the general liability and
professional liability rows carry the same policy number. Extraction keeps them as two
coverages, each with its own limits.

## Extraction

**26 leaf fields** in the schema (47 extracted values with two coverages and their
limits): the certificate date and number, the form edition, the producer (name, address,
contact, phone, fax, email), the insured (name, address), the insurers with their NAIC
numbers, the coverages with type, insurer letter, policy number, effective and expiration
dates, occurrence basis, what the aggregate applies per, and the named limits, the
description of operations, the certificate holder, and whether it is signed.

## Credits

**6.0 credits at standard tier**, for one parse and one extraction.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py certificate-of-insurance            # parse + extract (spends credits)
.venv/bin/python document-types/scripts/run_ade.py certificate-of-insurance --extract-only
.venv/bin/python document-types/scripts/build_images.py certificate-of-insurance       # images, no API calls
.venv/bin/python document-types/scripts/inspect_fields.py certificate-of-insurance
```
