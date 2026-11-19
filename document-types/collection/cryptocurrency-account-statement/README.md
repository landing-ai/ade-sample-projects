# Cryptocurrency account statement

**On the website:** [landing.ai/document-type/cryptocurrency-account-statement](https://landing.ai/document-type/cryptocurrency-account-statement)

A Blockchair Bitcoin wallet statement for 2021-08-25 to 2021-09-04. It gives the wallet
address and statement period, a BTC balance summary with starting and ending balance,
total received and total sent, and a 16-row transaction history with the date, time,
direction, BTC and USD amounts and transaction hash of each transfer. It ends with a
disclaimer and a QR code for checking the statement on Blockchair.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 20 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:47 | 2026-11-19 02:53 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 7,443 | 7,605 |
| Words under 0.95 confidence | 48 | n/a |
| Words under 0.80 confidence | 18 | n/a |
| Words under 0.50 confidence | 5 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.1 s | 9.9 s |
| Per page | 3.0 s | 4.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.1 credits | 3.0 credits |
| Per page | 0.55 credits | 1.50 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:47 | 2026-11-19 02:54 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 20 | 20 |
| Non-null fields returned | 20 | 20 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 249.3 s | 172.4 s |
| Per schema field (20) | 12.46 s | 8.62 s |
| Per value returned | 1.99 s | 1.38 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 5.4 credits | 5.4 credits |
| Per schema field (20) | 0.270 credits | 0.270 credits |
| Per value returned | 0.043 credits | 0.043 credits |

## Origin

`source/cryptocurrency-account-statement.pdf` is a Blockchair Bitcoin wallet statement
for 2021-08-25 to 2021-09-04. It is **2 pages, portrait (A4)**, with a text layer. Page 1
has a header with the provider's contact details, the wallet address and statement
period, a BTC balance summary and the first 10 rows of the transaction history. Page 2
has rows 11–16, a note, a disclaimer and a QR code for checking the receipt on
Blockchair.

| | |
|---|---|
| Publisher | Blockchair (block explorer that generated the statement) |
| Source | https://www.scribd.com/document/744055556/Wallet-statement-1-1-2021-08-25-2021-09-04-1 (plain text, not a link) |
| Retrieved | 2026-10-03, downloaded by hand by the operator because Scribd blocks scripted downloads |
| Clearance | Redacted |

Scribd is a user-upload site, not the publisher, so this file is treated as a personal
record. The statement names no person and no postal address. However, a wallet address
and its transaction hashes are public identifiers on the Bitcoin blockchain and can be
traced to the owner. These items were replaced:

- **The wallet address** (1 printed occurrence) is now a random bech32 string of the same
  length and character set. **Its checksum is deliberately invalid, so it cannot be a
  real wallet.**
- **All 16 transaction hashes** are now random lowercase hex of identical length. Each
  hash is printed over two lines, so its two halves were replaced separately (32
  spans).
- **33 hyperlinks** behind the address and the hash halves had URIs containing those
  values. They were rewritten to the stand-ins and then removed. The only link left is
  the generic Blockchair statement link on page 2.
- **The QR code** encoded a Blockchair URL containing the wallet address. It was
  re-encoded with the stand-in address.
- **Document metadata** was cleared.

The redaction removed the underlying text rather than covering it. The original values
are not recorded anywhere in this repo. Verified: no original address or hash, and no
12-character fragment of one, can be extracted from the PDF's text, objects, streams,
link URIs or decoded QR code.

**Residual risk, accepted by the operator.** The BTC and USD amounts and the timestamps
(to the second) are kept as printed. Together they could still be matched to the real
transactions on the public blockchain, and from them to the real wallet.

The stand-in hashes and address are set in Courier, at a slightly smaller size, among the
original DM Mono text. This is visible on close inspection. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A wallet statement is how a cryptocurrency holder documents balances and transfers when
someone else needs to see them. It often stands in for a bank statement where crypto is
part of a person's or a business's assets.

- **Tax preparation:** preparers use dated transfers with USD values to work out gains
  and losses.
- **Mortgage and consumer lending:** underwriters review crypto holdings offered as
  assets or as the source of a down payment.
- **Compliance and AML teams:** banks and exchanges review the transaction history
  when funds arrive from a wallet.
- **Accounting and audit:** auditors confirm crypto balances held by a business.
- **Legal and forensic work:** divorce, bankruptcy and estate cases trace transfers
  between wallets.

### What it contains

- **Eight-decimal amounts** (0.02314739 BTC), each beside a USD value at the time of the
  transaction.
- **Long opaque identifiers that wrap.** Each 64-character transaction hash is printed
  over two lines in one cell.
- **A transaction table** that continues across the page break.
- **Text-drawn dividers.** Section rules are rows of asterisks and dashes made of
  characters, not ruled lines.
- **A monospaced font with a slashed zero.**
- **A QR code** on the last page.
