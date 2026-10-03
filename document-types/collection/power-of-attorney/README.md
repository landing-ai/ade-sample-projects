# Power of Attorney

Source assets for `landing.ai/document-type/power-of-attorney`.

## Sample document

`source/power-of-attorney-ocrolus-sample.pdf`: a specimen corporate power of attorney.
**1 page, portrait.**

A mortgage lender (the principal) appoints another company (the agent) to execute,
endorse, assign and deliver its promissory notes, the mortgage rights securing them, and
the related loan documents. The power is irrevocable and survives the principal's
bankruptcy, dissolution or incapacity. Below the operative text are the execution line,
two signature blocks side by side (principal left, agent right) and a notarial
acknowledgment.

| | |
|---|---|
| Publisher | Ocrolus |
| Source | [Google Drive](https://drive.google.com/file/d/1HBbJsyyhp90pAaS4sYdq-nokH1f25BeW/view), linked as the sample from [docs.ocrolus.com/docs/power-of-attorney](https://docs.ocrolus.com/docs/power-of-attorney) |
| Retrieved | 2026-10-03, by script (Drive's standard download link) |
| Clearance | **Public** |

The Drive link alone does not say who made the file. The Ocrolus documentation page for
this document type links this exact file as its sample, which establishes the publisher.
Every value is specimen: principal "Fake Mortgage Company" at "123 Main Fake Street,
Anycity", agent "Sample Financial Services, Inc." at "123 Fake Grant Avenue", signer
"James Doe" and notary "John Doe", with script signatures drawn to go with those
invented names. The page is used exactly as published.

The one change: the PDF's metadata author field held the name of the person who prepared
the file, so the metadata (Info dictionary and XMP) was cleared. The rendered page is
pixel-identical to the original and the text layer is unchanged.

> Ocrolus sells document AI, so this is a competitor's published sample.

## Why this document

It is a mixed-layer PDF: the printed form (about 3,300 vector paths) has no text layer,
and only the typed-in values are text. Its values sit in fill-in blanks threaded through
legal prose, and both dates are split across separate blanks ("01 day of 01, 20 25";
"01, 15, 2025"), so they have to be assembled. It is also a second test of side-by-side
signature blocks, the layout that cross-paired the signers on the
[bailee letter](../bailee-letter/README.md).

## Schema

`schema.json` covers the parties (principal with its office, county, state and
authorized representative; agent with its address), the granted powers as an array, two
legal properties (irrevocable, survives incapacity), the execution date, both signature
blocks, and the notarial acknowledgment (state, county, date, commission expiry,
notarized flag).

**23 leaf fields** (counted from the schema). All populated, and all correct.

## Featured fields: the grant, from page 1

| Field | Value |
|---|---|
| Principal | Fake Mortgage Company |
| Agent | Sample Financial Services, Inc. |
| Execution date | 2025-01-01 |
| Notarized on | 2025-01-15 |
| Notary commission expires | 2029-12-14 |

Read top to bottom, these are who grants the power, to whom, when it was signed, when it
was acknowledged before a notary, and how long that notary can act. Both parties are
companies, so no person is featured. The request's notes suggested these plus the
notary's state and county, which also ground `ok`, and a signed or notarized flag, which
does not (see below).

## Grounding notes

- **Split dates assemble and ground cleanly.** `execution_date` and
  `notary.acknowledgment_date` are each built from three blanks and ground to the one
  line holding all three.
- **The side-by-side signature blocks were read in the right order.** Unlike the bailee
  letter, the parse wrote the left block in full before the right one, so the principal's
  signer and title stayed with the principal, and the agent's block came back with its
  company and no signer, as printed.
- **Grounding is line-level.** The agent's box covers the whole "appoint, and constitute
  … Auburn NY 12345" line, address included, and the principal's covers the line with
  "(the "Principal")". The value is always inside the box.
- **The booleans are correct but ground `OFF`.** `principal_signature.is_signed` grounds
  to "By: James Doe", `notary.is_notarized` to a `[SIGNED]` tag, and `is_irrevocable` and
  `survives_incapacity` to the prose that establishes them. A boolean is not printed, so
  none can be featured.
- **`powers_granted` is a summary**, so every element reads `OFF` against the clause it
  paraphrases. It is right, but a crop would not show the words.
- The parse transcribed both script signatures as text ("By: James Doe" and "John Doe"
  under the notary line) and placed its `[SIGNED]` tag ahead of the notary block rather
  than beside the notary's signature.
- `agent_signature.signer_name` came back as an empty string rather than null for the
  blank "Name:" line.

## Cost

**3.30 credits** at standard tier: 1-page parse and extraction.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py power-of-attorney
.venv/bin/python document-types/scripts/build_images.py power-of-attorney
.venv/bin/python document-types/scripts/inspect_fields.py power-of-attorney --page 1
```
