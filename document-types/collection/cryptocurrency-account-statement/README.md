# Cryptocurrency account statement

Source assets for `landing.ai/document-type/cryptocurrency-account-statement`.

## Sample document

`source/cryptocurrency-account-statement.pdf` is a Blockchair Bitcoin wallet statement
for 2021-08-25 to 2021-09-04. It has **2 pages, portrait (A4)**. Page 1 has a header with
the provider's contact details, the wallet address and statement period, a BTC balance
summary (starting and ending balance, total received, total sent) and the first 10 rows
of the transaction history. Page 2 has rows 11–16, a note, a disclaimer and a QR code for
checking the receipt on Blockchair.

| | |
|---|---|
| Publisher | Blockchair (block explorer that generated the statement) |
| Source | https://www.scribd.com/document/744055556/Wallet-statement-1-1-2021-08-25-2021-09-04-1 (plain text, not a link) |
| Retrieved | 2026-10-03, downloaded by hand by the operator because Scribd blocks scripted downloads |
| Clearance | Redacted |

Full provenance is in `manifest.json` under `source.origin`. This section is the
human-readable version of it.

### Clearance

Scribd is a user-upload site, not the publisher, so this file is treated as a personal
record. The statement names no person and no postal address. However, a wallet address
and its transaction hashes are public identifiers on the Bitcoin blockchain and can be
traced to the owner. These items were replaced before anything was parsed:

- **The wallet address** (1 printed occurrence) is now a random bech32 string of the same
  length and character set. **Its checksum is deliberately invalid, so it cannot be a
  real wallet.**
- **All 16 transaction hashes** are now random lowercase hex of identical length. Each
  hash is printed over two lines, so its two halves were replaced separately (32
  spans).
- **33 hyperlinks** behind the address and the hash halves had URIs containing those
  values. They were rewritten to the stand-ins and then removed by the redaction. The
  only link left is the generic Blockchair statement link on page 2.
- **The QR code** encoded a Blockchair URL containing the wallet address. It was
  re-encoded with the stand-in address.
- **Document metadata** was cleared.

The original values are not recorded anywhere in this repo. The replacement was done
with `document-types/scripts/redact.py`, which removes the underlying text rather than
covering it, after a one-off pre-pass for the links and the QR code. I checked the result:
no original address or hash, and no 12-character fragment of one, can be extracted from
the PDF's text, objects, streams, link URIs or decoded QR code.

**Residual risk, accepted by the operator.** The BTC and USD amounts and the timestamps
(to the second) are kept as printed. Together they could still be matched to the real
transactions on the public blockchain, and from them to the real wallet.

The stand-in hashes and address are set in Courier, at a slightly smaller size, among the
original DM Mono text. This is visible on close inspection.

## Why this document

It is the collection's first **cryptocurrency statement**, and it differs from the bank
and brokerage statements in several ways:

- **Eight-decimal amounts** (0.02314739 BTC), shown next to a USD value at the
  time of each transaction.
- **Long opaque identifiers that wrap.** Each 64-character transaction hash is printed
  over two lines in one cell, and extraction has to join the halves back together.
- **Typewriter-style layout.** The section dividers are rows of asterisks and dashes made
  of text characters, not ruled lines, and the font uses a slashed zero.

## Featured fields: one transaction

All on page 1, row 3 of the transaction history (a send):

| Field | Value |
|---|---|
| Transaction time | 11:12:12 (the cell also holds the date, 2021-08-26) |
| Direction | Sent |
| Amount (BTC) | 0.02314739 |
| Amount (USD) | 1,134.36 |

The four fields make up one complete transaction, so the overlay reads as one thing. The
request also suggested featuring the balance summary's total received and total sent.
Both extract correctly (0.18467513 BTC each) but ground OFF (see below), so they are not
featured. No hash or address is featured: they are stand-ins, and an opaque string does
not show grounding well.

## What it surfaced

**The asterisk and dash dividers confuse the parser's table detection.** The parse
treats the page header's rows of `* * *` and `- - -` as a grid and merges them with the
balance summary into one wide table. As a result each summary figure is split across
cells: `0.18467513 BTC` becomes a `0` cell, a `18467513` cell and stray `B` / `TOC` cells,
and the ending USD balance is read with slashed zeros as `Ø.ØØ`. Extraction still returns
the correct numbers, but their ranges cover only part of each value, so
`inspect_fields.py` reports them `OFF`. The statement period's dates are split in the same
way inside that table, but they also ground `ok` to the header line, which repeats the
period.

**The transaction table is clean.** All 16 rows extract across the page break with the
correct date, time, direction, BTC and USD amounts, and every field grounds `ok` to its
own cell. Received and sent each sum to the printed 0.18467513 BTC totals.

**Hash halves are joined correctly, with one exception.** Extraction joins both halves of
15 of the 16 hashes into the full 64 characters. In row 12, the parse dropped one
character from the second line of the hash, so the extracted value is 63 characters long.
Extraction faithfully reproduces the parse's error. A downstream check on hash length
would catch it.

## Schema

`schema.json` has 20 leaf fields. It covers the provider, the asset, the wallet address,
the statement period, the balance summary, every transaction row (number, date, time,
direction, BTC amount, USD amount, hash) and the generation timestamp.

## Credits

8.40 credits at standard tier (DPT-3 Pro parse plus extract, 2 pages).

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py cryptocurrency-account-statement
.venv/bin/python document-types/scripts/build_images.py cryptocurrency-account-statement
.venv/bin/python document-types/scripts/inspect_fields.py cryptocurrency-account-statement
```

The redaction cannot be regenerated from this repo by design: its rules file and the
original PDF are kept outside it.
