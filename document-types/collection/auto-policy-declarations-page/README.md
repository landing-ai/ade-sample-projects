# Auto Policy Declarations Page

Source assets for `landing.ai/document-type/auto-policy-declarations-page`.

## Sample document

`source/national-indemnity-business-auto-declarations.pdf`: National Indemnity Company's
**Business Auto Coverage Declarations** for an LLC limousine and party-bus operator in
Aliquippa, Pennsylvania, policy period 10/01/2019 to 10/01/2020. **1 page, portrait.** It
is a slightly skewed scan with an OCR text layer.

| | |
|---|---|
| Publisher | Pennsylvania Public Utility Commission public filings repository; the declarations were issued by National Indemnity Company |
| Source | [puc.pa.gov/pcdocs/1644171.pdf](https://www.puc.pa.gov/pcdocs/1644171.pdf) |
| Retrieved | 2026-10-25 (downloaded by script) |
| Clearance | **Public** |

The filing is a motor carrier's proof of insurance, posted by the PA PUC in its public
document repository. The original is four pages: the filer's cover letter, this
declarations page, a Form E certificate of insurance and a date-stamped mailing
envelope. **Only the declarations page was kept**; pages 1, 3 and 4 were dropped without
being reviewed for individual names.

**No page text was redacted.** The kept page names only organizations: the insured LLC at
its business address, the insurer, the producing agency and the countersigning agency.
The two signatures at the foot are the insurer's pre-printed facsimile officer signatures
(Secretary and President), which carry no printed name and appear on every policy of this
form, so they were left in place, as on the other insurer forms in this collection. The
authorized-signature line is blank. The PDF's metadata (format and dates) was cleared.

## Why this document

A declarations page is the one page of an auto policy that every downstream process reads:
who is insured, by whom, for how long, and which coverages were bought at what limit and
price. This one tests a dense ruled coverage schedule from a scan, where most rows are
empty or carry a preprinted `$` with no amount, and where some limits are a reference to
an endorsement ("See M 3912b (08/2001)") rather than a number.

It is a **commercial** (business auto) declarations page, not a personal auto one. No
plain, specimen-filled personal auto dec page could be found; the candidates were
annotated consumer-guide specimens, which were rejected. The layout and vocabulary
(covered-auto symbols, CSL limits, UM/UIM, comprehensive and collision) are the same
ones a personal auto dec page uses.

Item Three, the schedule of covered autos, reads **AS ATTACHED** and is not in the
filing, so the sample has no vehicle rows.

## Schema

`schema.json` resolves to **24 leaf fields**: insurer and form title, policy and renewal
numbers, the named insured (name, address, form and description of business), the
producer, the policy period, every row of the coverage schedule (coverage, covered-auto
symbols, limit, premium), the premium totals, forms and endorsements, the minimum earned
premium, the Item Three reference, the countersigning agency, the form number and the
issue date.

## Featured fields: what the policy buys and for how long

All on page 1:

| Field | Value |
|---|---|
| Policy period from | 10/01/2019 |
| Policy period to | 10/01/2020 |
| Liability limit | 1,000,000 CSL |
| Liability premium | 5,293 |
| Estimated total premium | $7,173 |

The request suggested, as suggestions only, the policy number, the policy period, the
form of business, the liability row and the estimated total premium. All of them ground
correctly; the overlay takes five, leaving out the policy number and form of business so
it reads as one coverage-and-cost story.

## Grounding

The coverage schedule grounds well: every populated limit and premium cell resolves to
its own cell, including `INCL` and the endorsement references. The empty rows ground to
their blank or `$`-only cells, which is right but not illustrable.

- **Coverage names in multi-line cells ground loosely.** The LIABILITY row's coverage name
  grounds to the table's COVERAGES header rather than its own cell, and names that wrap
  onto a second line (P.I.P., Underinsured Motorists) come back with the second line
  attached, which the match check flags.
- **The policy number is unlabelled.** The large bold number in the top-left block is
  the policy's identifier, but it sits beside a CROSS REFERENCE NUMBER caption, and the
  parse reads it as the cross reference number. The first extraction returned the policy
  number empty; it came back correctly once the schema description said where to look.
- **Policy period boxes include their labels.** The effective date box spans "POLICY
  PERIOD: Policy covers FROM ... TO", because the parse keeps the period as one line of
  text. The value is inside it.
- OCR inside the box could not read the liability premium `5,293`; the crop was checked
  and the value is there.

## Credits

7.90 credits at the standard tier: 4.70 for the parse and first extraction, 3.20 for one
re-extraction after the policy number description was refined.

## Regenerate

```bash
# source PDF: page 2 of the filing, metadata cleared (empty rules file, kept outside the repo)
.venv/bin/python document-types/scripts/redact.py 1644171.pdf \
    document-types/collection/auto-policy-declarations-page/source/national-indemnity-business-auto-declarations.pdf \
    --rules <outside-the-repo>/rules.json --drop-pages 1 3 4

.venv/bin/python document-types/scripts/run_ade.py auto-policy-declarations-page
.venv/bin/python document-types/scripts/build_images.py auto-policy-declarations-page
```
