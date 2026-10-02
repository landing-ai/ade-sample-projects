# Bailee Letter

Source assets for `landing.ai/document-type/bailee-letter`.

## Sample document

`source/bailee-letter-ocrolus-sample.pdf`: a synthetic bailee letter. **4 pages,
portrait.** The pages are the letter (1–2), the signed acknowledgment (3) and a one-loan
Schedule A (4).

In a bailee letter, a warehouse lender that funded a mortgage sends the note to the
investor buying the loan. The investor holds the note as the lender's *bailee*, and
ownership passes only once the investor wires the purchase price. If it does not fund
within the window, it must send the note back.

| | |
|---|---|
| Publisher | Ocrolus |
| Source | [Google Drive](https://drive.google.com/file/d/1UF9p9L2zcjz8UlyrZucuDTAqiT4lIAg_/edit), linked as the sample from [docs.ocrolus.com/docs/bailee-letter](https://docs.ocrolus.com/docs/bailee-letter) |
| Retrieved | 2026-10-02, by script (Drive's standard download link) |
| Clearance | **Public** |

The Drive link alone does not say who made the file. The Ocrolus documentation page for
this document type links this exact file as its sample, which establishes the publisher.
Every value is synthetic: "Fake Home Mortgage", "ABC Sample Inc.", "XYZ Bank", borrower
"John Sample" at "123 Fake Street", signers "Jack Sample" and "James Fake", and loan
`123456789`. The signatures are drawn to match those invented names. The PDF metadata
holds only the Google Docs renderer and "Untitled document". Nothing needed redacting.

> Ocrolus sells document AI, so this is a competitor's published sample.

## Why this document

It is the first one in the collection made in Google Docs. Its structure is light:
labelled lines at the top, then dense legal paragraphs where the parties' roles have to
be read from the prose. It is also the first with **two signature blocks side by side**,
and that layout is where the run failed (see below).

## Schema

As the request asked, `schema.json` follows the field list on Ocrolus's bailee-letter
page. It covers **20 of their 21 fields**: payee name, funding date, mortgagor name and
address, loan number, lender, warehouse lender, funding expiration days, two signature
blocks (company, signer, title, signed) and loan amount. The signature blocks are an
array. The one left out is the mortgagor's address line 2, because this sample prints
the borrower's address on a single line. It adds the payee's address, the purchase
price, the bank name and the party the bailee acts for, which this document carries.

**23 leaf fields** (counted from the schema), all populated. Ocrolus's *funding date*
maps to `letter_date`, since this sample prints no separate funding date.

## Featured fields: the deal, from page 1

| Field | Value |
|---|---|
| Loan number | 123456789 |
| Letter date | 2024-12-12 |
| Investor (payee) | Fake Home Mortgage |
| Warehouse lender | ABC Sample Inc. |
| Funding window (business days) | 10 |

These say which loan, when, who receives the note, who keeps the security interest, and
how long the investor has to pay. `funding_expiration_days` is pinned to occurrence 1,
the sentence "no later than ten (10) business days". Occurrence 0 is an earlier sentence
about an option to buy "within ten days", which reads `OFF`.

## What went wrong: the signature blocks are cross-paired

On page 3, **Jack Sample, Custodian** signs under **First Fake Inc.** in the left column,
and **James Fake, President** signs under **Sample Inc.** in the right. Extraction
returned them swapped: Jack Sample for Sample Inc., and James Fake for First Fake Inc.

The cause is the parse's reading order, not the extraction. The parse writes the page as:

```
First Fake Inc. / 123 Fake Grant Avenue, / Fake City NY 12345
Sample Inc.
[SIGNED] Signature … Printed Name: Jack Sample / Title: Custodian
[SIGNED] Signature … Printed Name: James Fake / Title: President
```

Both company headers come first and then both signature blocks, so the markdown no
longer says which column each signer was in. Extraction sees only the markdown, so it
has to guess the pairing. A rerun with descriptions anchored to the columns did not help:
block 1 kept the wrong company and block 2 lost its company entirely. That rerun was
discarded, and the committed output is the first run.

The boxes in `parse-pro.json` still show the two columns, so a pipeline could re-pair
by position. Anyone extracting Ocrolus's `signatureBlock1/2:companyName` from
side-by-side layouts should check this.

## Other grounding notes

- **`lender_name` and `payee.name` are the same party.** The document names Fake Home
  Mortgage both as the "Investor" and as the originator. So `lender_name` grounds first
  to the "Investor Name" line. That inconsistency is in the sample, not the extraction.
- **`warehouse_lender_name` has 14 occurrences** across three pages, all of them inside
  prose. The featured one is the first line naming it as holding the interest.
- **`is_signed`** grounds to the parse's `[SIGNED]` / `[HANDWRITTEN_SIGNATURE]` labels.
  It is correct, and reads `OFF` only because a boolean is not printed.
- **`loan_amount` ($50,000) and `purchase_price` ($250,000) differ.** The sample says
  so itself: Schedule A gives the loan amount, and the letter body gives the wire amount.
  Neither was featured, since both sit off page 1.

## Cost

**5.30 credits** at standard tier for the committed output: 4-page parse and extraction.
The discarded extract-only rerun cost another 1.90.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py bailee-letter
.venv/bin/python document-types/scripts/build_images.py bailee-letter
.venv/bin/python document-types/scripts/inspect_fields.py bailee-letter --page 1
```
