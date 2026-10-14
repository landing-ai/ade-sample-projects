# D&O Insurance Policy

Source assets for `landing.ai/document-type/directors-and-officers-insurance-policy`.

## Sample document

`source/directors-and-officers-insurance-policy-travelers.pdf`: a complete, issued
**Travelers SelectOne+ Investment Advisers and Funds** policy with **Mutual Fund
Liability** coverage, for the policy year March 16, 2022 to March 16, 2023. **26 pages,
portrait**, with a text layer.

The named insured is Monteagle Funds, a registered investment company (a fund trust with
seven series). The policy is laid out the way most management liability policies are:

- **Declarations** (pages 1-3): policy number, insurer, named insured, policy period,
  claim notice addresses, coverages, limit of liability, retention, prior or pending
  proceeding date, premium, extended reporting period, shared limit, forms attached,
  producer, and the insurer's facsimile officer signatures.
- **Terrorism endorsements** (pages 4-5).
- **General Terms and Conditions** (pages 6-16), the common definitions and conditions.
- **Endorsements** (pages 17-18 and 25-26): specified entities (the seven funds), global
  coverage compliance, defense expenses for investigating and monitoring claims, and mock
  regulatory examination.
- **Mutual Fund Liability Coverage part** (pages 19-24): insuring agreements,
  definitions and exclusions.

**This is a mutual-fund management liability policy, not a classic corporate D&O
policy.** It covers the fund trust and its directors, trustees and officers (with
optional independent-director coverage, not purchased here) rather than the board of an
operating company. The structure and the key terms (claims-made basis, defense inside
limits, retention, prior or pending proceeding date, extended reporting period) are the
same as a corporate D&O policy, which is why it serves as the sample.

| | |
|---|---|
| Publisher | Monteagle Funds, as filed with the SEC; policy issued by Travelers Casualty and Surety Company of America |
| Source | [SEC EDGAR, monteagle4017g.pdf](https://www.sec.gov/Archives/edgar/data/1045701/000116204422000446/monteagle4017g.pdf) |
| Filing | Form 40-17G (fidelity bond and insurance filing by a registered investment company), accession 0001162044-22-000446, CIK 1045701 |
| Retrieved | 2026-10-04, by script |
| Clearance | **Public** |

Registered investment companies file their bonds and insurance policies on EDGAR under
Rule 17g-1, so this policy is a public record. The kept pages name only organizations:
the fund trust and its series, the insurer, and the broker, plus the insurer's corporate
claims email, fax and phone lines. Nothing was replaced.

Two changes from the filed PDF:

- **Pages 1-3 were dropped.** They are the fund's cover letter, a secretary's
  certificate and the board resolutions approving the coverage, which are not part of
  the policy and name individuals and a direct phone line. Page numbers here are the
  filing's minus three. (The cover letter also describes a different policy from the one
  attached, a filing error; dropping it removes that inconsistency too.)
- **PDF metadata was cleared** (the filer's Word document title, author initials,
  producer and dates). The policy pages are otherwise unchanged.

The declarations carry the insurer's two pre-printed facsimile officer signatures
(President and Corporate Secretary), with no printed names. They are part of every
Travelers policy of this form and were left in place.

## Why this document

It is a real, issued policy rather than a specimen form, so the declarations are filled
in, and it is long: 26 pages in which the values that matter sit on two declarations
pages and the rest is dense two-level legal prose. That is the realistic shape of an
insurance policy, and it tests two things:

- **Finding the declarations among the boilerplate.** The limit, retention and premium
  appear once, on page 2. Terms such as "Limit of Liability" and "Retention" are used
  dozens of times in the conditions that follow.
- **Reading terms that are stated in prose, not fields.** Whether the policy is
  claims-made, whether defense costs erode the limit and whether the insurer has a duty
  to defend are never labelled values. They are stated in the capitalized warning on the
  declarations and repeated in the conditions. The 60-day deadline for electing the
  extended reporting period appears only in the general terms on page 9.

## Schema

`schema.json` covers the policy number and form title, the insurer, the named insured
and address, the policy period, claim notice contacts, coverages included, coverage
details (limit, derivative investigation limit, independent-director coverage,
retention, prior or pending proceeding date), premium, the extended reporting period
(premium percentage, months, election deadline), shared limit, forms attached, the
producer, three policy-character flags (claims-made, defense inside limits, duty to
defend), the specified entities, and the attached endorsements.

**45 leaf fields** (counted from the schema). Every value extracted correctly on the
first run, including all three prose-derived flags and the 60-day election deadline.

## Featured fields: the economics, from page 2

| Field | Value |
|---|---|
| Limit of liability | 1,000,000 |
| Retention per claim | 75,000 |
| Policy premium | 14,366 |
| Extended reporting premium (%) | 125 |
| Extended reporting months | 12 |

Read together: how much cover the fund bought, what it pays itself on each claim before
the cover starts, what the year costs, and what it would cost to keep reporting claims
for a year after the policy ends. All five come from ITEMs 5-7 on one page. The request
suggested these plus the prior or pending proceeding date, which could not be featured
(see below). No person is featured.

## Grounding notes

- **The declarations ground cleanly, line by line.** Each amount boxes its own row
  ("$1,000,000 for all Claims", "$75,000 for each Claim"), and the two extended reporting
  lines get separate boxes.
- **The prior or pending proceeding date grounds `OFF`.** The value is right
  (1998-03-16, reformatted from "March 16, 1998"), but its range points at the
  "Not Applicable / Supplemental Independent Director" lines above it rather than its
  own line, one line below the retention. `retention_basis` ("for each Claim") has the
  same misplaced range, although it is printed on the retention line itself.
- **Policy period dates ground `OFF`** because the ISO dates are not printed; the box is
  the right line ("Inception Date: March 16, 2022 Expiration Date: ...").
- **The prose flags point at the right sentences.** `duty_to_defend` grounds to "THE
  COMPANY HAS NO DUTY TO DEFEND ANY CLAIM" and to the matching condition on page 10, and
  `defense_expenses_within_limits` to the capitalized warning and the limits condition on
  page 9. They are `OFF` only because a boolean is never printed.
- **The policy number grounds on five pages**: the declarations and every endorsement
  that repeats it, which is what the occurrence index is for.
- **Endorsement titles split across two lines ground `OFF`**: "Cap On Losses From
  Certified Acts Of / Terrorism Endorsement" is two blocks, and each half alone does not
  contain the whole title. Single-line titles ground `ok`.
- **The parse transcribed the facsimile signatures as names.** Each signature becomes
  `[SIGNED]` followed by a reading of the handwriting, which is approximate. The schema
  does not ask for the signers.
- **Every form number in ITEM 9 grounds to the same line**, since the eight numbers are
  one semicolon-separated run of text.

## Cost

**55.50 credits** at standard tier: one 26-page parse and one extraction. No reruns.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py directors-and-officers-insurance-policy
.venv/bin/python document-types/scripts/build_images.py directors-and-officers-insurance-policy
.venv/bin/python document-types/scripts/inspect_fields.py directors-and-officers-insurance-policy --page 2
```
