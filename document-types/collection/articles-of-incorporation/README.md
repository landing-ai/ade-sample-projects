# Articles of Incorporation

Source assets for `landing.ai/document-type/articles-of-incorporation`.

## Sample document

`source/articles-of-incorporation-wyoming-top-tier-sports.pdf` — **Profit Corporation
Articles of Incorporation** for Top Tier Sports (USA) Inc., generated and filed by the
**Wyoming Secretary of State** on November 5, 2024. **4 pages, portrait**, a native PDF
with a text layer:

1. The articles: office-use filing stamp and Original ID, then Articles I–VI (name,
   registered agent, mailing and principal office addresses, authorized shares and par
   values, incorporator) and a typed e-signature block.
2. The filer's checkbox attestations, the statutory penalty notice, and the signature block
   again.
3. The registered agent's consent to appointment.
4. The Secretary of State's Certificate of Incorporation, with the Great Seal and the
   Secretary's signature.

| | |
|---|---|
| Publisher | Wyoming Secretary of State; filed on SEC EDGAR by Top Tier Sports (USA) Inc. as Exhibit D to its Form C |
| Source | [sec.gov/Archives/edgar/data/2045455/000204545524000001/exhibit_d.pdf](https://www.sec.gov/Archives/edgar/data/2045455/000204545524000001/exhibit_d.pdf) |
| Filing index | [0002045455-24-000001](https://www.sec.gov/Archives/edgar/data/2045455/000204545524000001/0002045455-24-000001-index.html) |
| Retrieved | 2026-10-28, downloaded directly by script |
| Clearance | Public |

The company filed these articles with the SEC as an exhibit to a Regulation
Crowdfunding offering statement, so the document sits in a public government repository.
EDGAR served it as a PDF, so no HTML rendering was needed.

**Used as published, unredacted, by explicit decision of the operator.** The filing names
one incorporator, an attorney at the registered-agent law firm acting in a professional
capacity, with a typed e-signature, a business email and a business phone on pages 1–3,
and the Secretary of State, a public official, with his signature and the state seal on
page 4. This follows the business-registration and arbitration-award folders, where the
operator likewise chose to keep a public record as published. None of the individuals or
their contact details is featured. The PDF metadata holds only the producing software
(PDFium) and a creation timestamp.

## Why this document

The collection's first **articles of incorporation**, and its first corporate formation
document with a **capital structure**. Business registration covers an LLC's certificate
of organization, which has no shares. This one tests:

- **Two-column label/value pairs.** Article V prints the share counts and par values side
  by side on two lines, which is the layout most likely to cross values between columns.
- **A non-numeric quantity.** Common shares are authorized as "Unlimited", not a number.
- **Repeated addresses.** The mailing and principal office addresses are identical, and
  the registered agent's address reappears on page 3 in running prose.
- **A state certificate page** with seal and signature, and a page of checkbox
  attestations.

## Featured fields: what the state filed

All on page 1. The request suggested the filed stamp and Original ID, the corporation name,
the registered agent, and both share counts and par values, as suggestions only.

| Field | Value |
|---|---|
| Original ID | 2024-001549080 |
| Corporation name | Top Tier Sports (USA) Inc. |
| Registered agent | Cloud Peak Law, LLC |
| Common shares authorized | Unlimited |
| Preferred shares authorized | 110,000 |

What the state assigned, what was formed, who accepts service for it, and the capital it
may issue. With a five-field limit, three suggestions were left out, though all three
ground `ok`: the filed timestamp (`Nov 5 2024 12:37PM`) and the two par values. Both par
values read `$0.0001`, so featuring them would add two identical crops. The registered
agent is featured by its firm name, an organization, and not by the attorney who signed.

## What it surfaced

**The side-by-side shares layout grounds cleanly.** Each share-count box covers
"Number of Common Shares: Unlimited" or "Number of Preferred Shares: 110,000" and stops
before the par-value column beside it. The par values ground to their own
"Common Par Value" and "Preferred Par Value" boxes. Nothing crossed between columns.

**Multi-line addresses ground OFF.** The registered agent, mailing and principal office
addresses all extract correctly, but each value joins two printed lines and each range
covers only one line, so `inspect_fields.py` reports them `OFF`. The incorporator's address,
printed on one line, grounds `ok`.

**Page 2's checkboxes come through.** The parse renders each attestation as `[x]`, and the
"Filer is" choice as `[ ] An Individual` / `[x] An Organization`, so the filer type is
readable from the markdown. Only two signatures are tagged `[SIGNED]`: the typed
e-signature on page 1 and the Secretary's handwritten one on page 4. The identical typed
e-signatures on pages 2 and 3 come through as plain text, and the seal on page 4 as
`[GREAT SEAL OF THE STATE OF WYOMING]`.

**Dates are kept as printed.** The schema asks for dates exactly as printed, so the filed
timestamp and signature date ground `ok`. Elsewhere in the collection, dates normalised to
ISO have grounded `OFF`.

**Inferred booleans ground OFF by design.** `registered_agent_consent_given` and
`certificate_of_incorporation.great_seal_affixed` are `true`, grounded to the consent
paragraph on page 3 and to the certificate text and seal on page 4, which support the
value without containing it.

## Extraction

**24 leaf fields** in the schema, written for this run: the filing office's record
(office, state, entity type, Original ID, filed timestamp), corporation name, registered
agent, mailing and principal office addresses, authorized share classes, incorporators,
signatory, registered-agent consent, and the certificate of incorporation. All 10 top-level
fields populate.

## Cost

**5.80 credits** at standard tier for 4 pages (parse and extract).

## Regenerating

```bash
curl -sS -A "LandingAI research <your email>" \
  -o document-types/collection/articles-of-incorporation/source/articles-of-incorporation-wyoming-top-tier-sports.pdf \
  "https://www.sec.gov/Archives/edgar/data/2045455/000204545524000001/exhibit_d.pdf"
.venv/bin/python document-types/scripts/run_ade.py articles-of-incorporation                # 5.80 credits
.venv/bin/python document-types/scripts/run_ade.py articles-of-incorporation --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py articles-of-incorporation           # free
.venv/bin/python document-types/scripts/inspect_fields.py articles-of-incorporation --page 1
```

SEC EDGAR requires a descriptive User-Agent and rate-limits scripted downloads.
