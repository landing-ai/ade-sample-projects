# Wire Instructions

Source assets for `landing.ai/document-type/wire-instructions`.

## Sample document

`source/wire-instructions-redacted.pdf`: First Integrity Title Company's wire instructions
for closing funds. **1 page, portrait.**

It is page 11 of the title commitment in
[`../commitment-for-title-insurance/`](../commitment-for-title-insurance/), split out to
stand on its own, as the request asked. That folder dropped the page. This one is only
that page.

| | |
|---|---|
| Publisher | First Integrity Title Company |
| Source | [adc-tenbox-prod.imgix.net/…/PRELIMINARY_TITLE_REPORT/…pdf](https://adc-tenbox-prod.imgix.net/resi/propertyDocuments/1300098/PRELIMINARY_TITLE_REPORT/40C02EC5FCCE4D3BBF40A5C6B9BEF65F.v1.pdf), page 11 |
| Retrieved | 2026-10-02, by script |
| Clearance | **Redacted**, see below |

## Redaction

The page held a live title-company trust account. Wire instructions are what
wire-fraud schemes forge, so a sample that names a real company, a real bank and a
working account number is a template for the fraud.

| Data | Replaced with |
|---|---|
| Beneficiary bank account number | Random stand-in, same length |
| ABA routing number | Random 9-digit stand-in that **fails the ABA checksum**, so it cannot route a wire |
| Reference order number | `FIN-78796415`, the commitment folder's stand-in |
| Property address | `100 SAMPLE RD`, `Anytown`, `CA 90000`, as in the commitment folder |
| PDF metadata | cleared |

Reusing the commitment's stand-ins keeps the two samples consistent: the order number on
this page is the commitment's order number.

The title company's and the receiving bank's names, addresses and published phone
numbers are kept. They are businesses, and with the account and routing numbers
replaced the page cannot send money anywhere real.

Like the rest of the commitment, the page has no text layer: every glyph is a vector
path. It was redacted with `document-types/scripts/redact_outlined.py`, using the same
rules as the commitment plus the two bank numbers. Verified by OCR on literals and bare
digits: no original value survives in the PDF or anywhere in this folder.

## Why this document

It is a one-page key–value form, the opposite of the commitment's long legal text. It
is also the document a closing workflow most needs to check, because a changed account
number on wire instructions is the classic closing fraud. Extracting and grounding every
payment field lets a reviewer compare it against a known-good copy.

`schema.json`: **15 leaf fields**, all populated.

## Featured fields: the payment route

The five fields run down the instruction block in order: where the money goes, how it is
routed, which account, whose account, and what to quote.

| Field | Value |
|---|---|
| Receiving bank | First Western Trust Bank |
| ABA routing number | 796630226 |
| Account number | 6677087 |
| Account name | First Integrity Title Company, a California Corporation - California IOLTA Account |
| Reference order number | FIN-78796415 |

Every box covers the label and its value together, because the parse treats each
`Label: value` pair as one block. The crops read naturally as a result.

## Grounding notes

- **`issuer.name` came back as `FIN TITLE`.** The model read it off the logo, though the
  opening paragraph names the payee in full ("First Integrity Title Company, a California
  Corporation"). The schema asked for "the letterhead or the opening paragraph", which
  allowed both readings. Not featured.
- **`account_type` is `IOLTA`** and correct, but it grounds to the same line as
  `account_name`, so featuring it would repeat that crop.
- **`wire_only: true` and `ach_accepted: false`** are correct. Each grounds to the
  sentence that says it, and both read `OFF` only because a boolean is not printed.
- **`receiving_bank.address`** spans two lines, so each of its two ranges holds half the
  value.

## Cost

**1.60 credits** at standard tier: one-page parse and extraction.

## Regenerating

```bash
# Split page 11 from the original download, then redact; the rules stay outside the repo.
.venv/bin/python -c "import pymupdf; s=pymupdf.open('<original>.pdf'); d=pymupdf.open(); \
    d.insert_pdf(s, from_page=10, to_page=10); d.save('<page-11>.pdf')"
.venv/bin/python document-types/scripts/redact_outlined.py <page-11>.pdf \
    source/wire-instructions-redacted.pdf --rules <outside-the-repo>/wire-rules.json

.venv/bin/python document-types/scripts/run_ade.py wire-instructions
.venv/bin/python document-types/scripts/build_images.py wire-instructions
.venv/bin/python document-types/scripts/inspect_fields.py wire-instructions --page 1
```
