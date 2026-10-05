# Life insurance policy

Source assets for `landing.ai/document-type/life-insurance-policy`.

## Sample document

`source/pacific-life-term-art-sample-policy.pdf` — Pacific Life's specimen of an issued
**annual renewable term life insurance policy** (product PAC ART, policy form P08TRM):
$500,000 of cover to age 95, convertible, non-participating, with a premium waiver rider.
**14 pages, portrait**, born-digital with a text layer. Page 1 is the cover with the
policy data block, pages 3–7 are the policy specifications and the guaranteed premium
tables, pages 8–13 are the contract provisions and index, and page 14 is the back cover.
Page 2 is intentionally blank. Every data page carries a red SAMPLE stamp.

| | |
|---|---|
| Publisher | Pacific Life Insurance Company |
| Source | [pacificlife.com/…/Sample Policy_Term ART.pdf](https://www.pacificlife.com/content/dam/paclife/lid/public/sample-policies/Sample%20Policy_Term%20ART.pdf) |
| Retrieved | 2026-10-04, downloaded directly by script |
| Clearance | Public |

The carrier publishes this file on its own domain, in a `public` sample-policies asset
folder that also holds its other sample policies. No HTML page linking it was found; the
carrier-owned URL is the provenance of record.

It is the carrier's own specimen, not a customer's policy. The insured and owner are a
19th-century historical figure used as a placeholder, and the policy number is a dummy.
The two officer signatures on page 1 are the corporate signatures printed on the
carrier's policy forms. No redaction was needed. All 14 pages are kept as published;
only the PDF's document metadata was cleared, because it carried an author username.

## Why this document

The collection's first **life insurance policy**, and a contract rather than a statement
or a form:

- **Two-column data block.** The cover's policy data sits in two label–value columns side
  by side. The parse reads each column top to bottom rather than interleaving the rows.
- **Long continuation tables.** The basic coverage premiums run 60 policy years across
  two pages, plus a 30-year rider table on a third, each with right-aligned figures, a
  dollar sign only on the first row and a SAMPLE stamp over the middle.
- **Terms buried in prose.** The grace period, reinstatement window, incontestability
  and suicide exclusion periods, claim timing and guaranteed interest rates are stated
  once, in running text, across six pages of provisions.
- **Arithmetic that reconciles.** The initial monthly premium ($36.00) is the year-1
  basic premium ($350) plus the waiver rider ($50), times the monthly factor 0.090.

## Featured fields: the coverage at a glance

All on page 1. The request named no fields; its notes suggested five.

| Field | Value |
|---|---|
| Product | TERM LIFE INSURANCE |
| Policy number | VF99999990 |
| Face amount | 500000 |
| Initial monthly premium | 36 |
| Risk class | STANDARD NONSMOKER |

What an underwriter, a lender taking a collateral assignment, or a policy-review service
reads first: what kind of policy, which one, how much cover, what it costs and at what
rating. Each box sits tightly on its label and value.

**The suggested policy date was replaced.** The schema asks for ISO dates, so
`2008-05-01` grounds `OFF` against the printed "MAY 1, 2008": correct, but the crop
would not show the value printed beside it. The product type took its place. The
insured's and owner's names ground `ok` but are not featured, because an impersonal field
makes the same point.

## What it surfaced

**Everything extracted is correct.** All 21 top-level fields populate with no warnings,
including all 90 rows of the three premium tables, every one of which grounds `ok` on its
own row. The extraction also reads the bracketed "[20]" days of the free-look period and
the "[MONTHLY]" interval as plain values.

**Every `OFF` is a normalization, not a misreading.** 36 of 262 grounded occurrences are
`OFF`, and each one is a value the schema asked to be transformed: the ISO policy,
conversion, expiration and rider cease dates; the convertible and participating
booleans, which ground to every sentence about conversion (23 occurrences) or
participation; and provision periods printed as words ("two years", "five years").

**The insurer's name grounds three times on page 1,** once to the address line (`ok`),
once to the logo's "PACIFIC LIFE" wordmark and once to the opening paragraph (`OFF`).

**Signatures and stamps are labelled.** The parse marks the cover's officer signatures
`[SIGNED]` and each page's SAMPLE stamp `[STAMPED]`, and transcribes the stamp's word.

## Extraction

**39 leaf fields**: insurer name and address; policy number and form number; product
type and policy date; the insured (name, sex, issue age, risk class) and the owner; face
amount; initial premium and payment interval; coverage-to age, expiration and conversion
end dates; convertible and participating flags; free-look days; riders (form, name, cease
date); modal premium factors; the annual policy fee; the basic coverage and premium
waiver premium schedules (policy year, annual premium); and eight provision terms (grace
period, reinstatement period and interest, incontestability and suicide exclusion
periods, claim payment period, late-claim interest, minimum income benefit interest).

## Cost

**24.30 credits** at standard tier for 14 pages: 13.80 to parse, 10.50 to extract.

## Regenerating

```bash
curl -sSL -o source/pacific-life-term-art-sample-policy.pdf \
  "https://www.pacificlife.com/content/dam/paclife/lid/public/sample-policies/Sample%20Policy_Term%20ART.pdf"
# clear the document metadata with PyMuPDF (set_metadata({}), del_xml_metadata()) and save
.venv/bin/python document-types/scripts/run_ade.py life-insurance-policy                # 24.30 credits
.venv/bin/python document-types/scripts/run_ade.py life-insurance-policy --extract-only # 10.50, schema iteration
.venv/bin/python document-types/scripts/build_images.py life-insurance-policy           # free
.venv/bin/python document-types/scripts/inspect_fields.py life-insurance-policy --page 1
```
