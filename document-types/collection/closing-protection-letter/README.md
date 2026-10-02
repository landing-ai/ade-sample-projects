# Closing Protection Letter

Source assets for `landing.ai/document-type/closing-protection-letter`.

## Sample document

`source/sample-cpl.pdf`: a sample closing protection letter (CPL) issued by Fidelity
National Title Insurance Company to a lender, for a Virginia closing conducted by
Covenant Real Estate Services. It is on Fidelity's form CPL80446 (12/2018). **2 pages,
portrait.**

A CPL is the title insurer's promise to a lender that it will cover losses caused by the
closing agent: not following the lender's closing instructions, or fraud and theft of the
lender's funds. Lenders ask for one on every closing, so it sits beside the title
commitment and the wire instructions in the closing package.

| | |
|---|---|
| Publisher | Covenant Real Estate Services LLC |
| Source | [covenantreal.com/…/Sample-CPL.pdf](https://covenantreal.com/wp-content/uploads/2023/03/Sample-CPL.pdf) |
| Retrieved | 2026-10-02, by script |
| Clearance | **Public** |

The settlement agent publishes this sample on its own website for lenders, with a red
`SAMPLE` watermark. The transaction data is specimen: borrowers "John Doe and Jane
Doe", addressee "Lending Bank, LLC", property "1212 ABC Drive". The settlement agent
named on it is the publisher itself. The one real person is the insurer's chief
underwriting counsel, as a facsimile corporate signature. Nothing needed redacting.

## Why this document

It is a short contract that is mostly boilerplate, with the transaction-specific values
packed into the letterhead block. The test is picking those few values out from the
pages of conditions around them, and the coverage cap, which sits inside a numbered
requirement rather than in a labelled field.

It has a normal text layer, unlike the title commitment and wire instructions, which are
vector outlines.

`schema.json`: **22 leaf fields**, all populated.

## Featured fields: who is protected, for what

All five are on page 1. Together they say what this letter covers.

| Field | Value |
|---|---|
| Lender protected | Lending Bank, LLC |
| Settlement agent | Covenant Real Estate Services LLC |
| File number | CRES-23-003S |
| Loan number | 2003001 |
| Maximum funds covered | 5000000.0 ($5,000,000.00) |

The borrowers are specimen names, but the transaction is identified just as well by
its file and loan numbers, so no person is featured.

## Grounding notes

- **The coverage cap grounds to Requirement 3**, a full sentence: "The aggregate of all
  Funds You transmit … does not exceed $5,000,000.00". The box is the whole line, which
  is correct, but it makes the widest crop of the five.
- **The settlement agent's name is printed twice**, once under "SETTLEMENT AGENT OR
  APPROVED ATTORNEY" and again as a second address block. Extraction cited only the first.
- **Footer identifiers ground cleanly** from a dense, tightly kerned footer line:
  `letter_id`, the agent number `133819.1.27.46`, and the correspondence address and
  phone all read `ok`.
- **`is_sample`** grounds to the `SAMPLE` watermark and **`is_signed`** to the parse's
  `[SIGNED]` label on page 2. Both are correct, and both read `OFF` only because a
  boolean is not printed.
- **Two-line addresses** read `OFF`, with each range holding one line, as on the other
  title documents.

## Cost

**7.70 credits** at standard tier: 2-page parse and extraction.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py closing-protection-letter
.venv/bin/python document-types/scripts/build_images.py closing-protection-letter
.venv/bin/python document-types/scripts/inspect_fields.py closing-protection-letter --page 1
```
