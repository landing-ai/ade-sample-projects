# Show Me Where It Says That: Agents That Cite Every Word in a Document
### Data Science Dojo 2026 — LandingAI ADE hands-on

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/landing-ai/ade-sample-projects/blob/main/Events/Data_Science_Dojo_2026/Verity_Citations/hands_on.ipynb)

LandingAI's **DPT-3 Verity** parsing model, part of Agentic Document Extraction (ADE), returns **every
word** of a digitally created document with its page, its box on the page and a confidence score.
This hands-on notebook shows what you can build from those two signals, location and confidence, and
ends with a complete use case: finding every edit between versions of a contract.

**No API key needed.** Every parse and extraction is saved in `data/`, so every cell runs offline.

---

## What You'll Build

| Part | Pattern | What you'll have | Code |
|---|---|---|---|
| 0 | What Verity returns | One grounded word: text, page, box, confidence | `patterns.words()` |
| A | Cite | An exact phrase, boxed on the page | `patterns.cite()` |
| B | Route | Low-confidence words sent to a person | `patterns.route()` |
| C | Verify | Every extracted value tied to the words it came from | `patterns.verify()` |
| D | **Use case:** version control | Every edit between lease revisions, drawn on the page, layout-only changes ignored | `docdiff.py` |

Each part ends with a **Your turn** exercise. `hands_on_solutions.ipynb` is the same notebook with every
exercise solved.

---

## The Pipeline (part D)

```
PDF v_old ──► Parse (DPT-3 Verity) ──► words: text · page · box · confidence · section ─┐
                                                                                        ├─► align ──► classify ──► report.html
PDF v_new ──► Parse (DPT-3 Verity) ──► words: text · page · box · confidence · section ─┘   (difflib)   change / noise   pages with highlights
```

1. **Parse.** Every word comes back with its location and a confidence score, in tables as well as text.
2. **Flatten.** Words from text blocks and table cells go into one reading-order stream. Line breaks
   aren't part of it, so re-flowed text can't create differences. Headers and footers are left out
   because they move whenever pages break differently.
3. **Align.** `difflib.SequenceMatcher` lines up the two word streams. Whatever doesn't match becomes an
   *added*, *removed* or *modified* change.
4. **Classify.** A change is set aside as probable transcription noise only when the two sides are at
   least 75% similar by characters, a word on either side is below 0.95 confidence, **and** no digits
   are involved.
5. **Render.** Each change keeps its words' boxes, so it's drawn on the original pages: red for before,
   green for after, grey for set aside.

---

## Results on the Demo Set

Four revisions of a two-page lease. `lease_v1_reflow.pdf` has the same words as v1 with a new font and
margins, so a good diff reports nothing for it.

| Pair | Planned edits | Found | False positives | Misreads set aside |
|---|---|---|---|---|
| v1 → v1 re-flowed (same words, new layout) | 0 | 0 | 0 | 0 |
| v1 → v2 | 6 | 6 | 0 | 1 |
| v2 → v3 | 5 | 5 | 0 | 1 |

A plain line diff of the PDFs' text reports **64 changed lines** for the re-flowed copy, where not a
single word changed.

### The confidence trap

| Noise rule | Edits found | False positives | Real edits hidden |
|---|---|---|---|
| off: every difference is a change | 11/11 | 2 | 0 |
| naive: hide anything low-confidence | 10/11 | 0 | **1**, the $75 → $95 late fee |
| guarded: near-miss + low confidence, no digits | **11/11** | **0** | **0** |

Both false positives are the same real Verity misread, seen once in each pair that includes v2: it
read the heading *Alterations* as *Alteratioos* (confidence 0.68). The naive rule hides it, but it also hides the late-fee change, because
Verity read `$75.00` correctly yet scored it only 0.87. **A low score means "check this", not "this is
wrong".**

---

## Setup

### Option A — Google Colab (recommended, nothing to install)

1. Open **[hands_on.ipynb in Colab](https://colab.research.google.com/github/landing-ai/ade-sample-projects/blob/main/Events/Data_Science_Dojo_2026/Verity_Citations/hands_on.ipynb)**
   (solutions: [hands_on_solutions.ipynb](https://colab.research.google.com/github/landing-ai/ade-sample-projects/blob/main/Events/Data_Science_Dojo_2026/Verity_Citations/hands_on_solutions.ipynb)).
2. Run the **Running in Google Colab** cell. It downloads just this folder and installs `pypdfium2` and
   `pdfplumber`, in about 15 seconds.
3. Run the cells in order from the setup check.

Colab opens a read-only copy; use **File › Save a copy in Drive** to keep your answers. If the runtime
restarts, run the Colab cell again.

### Option B — Locally

**1. Clone the repo and go to this project**
```bash
git clone https://github.com/landing-ai/ade-sample-projects.git
cd ade-sample-projects/Events/Data_Science_Dojo_2026/Verity_Citations
```

**2. Create a virtual environment and install dependencies**
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**3. Open the notebook**
```bash
jupyter lab hands_on.ipynb
```

Start Jupyter from this folder: the notebook imports from `scripts/` and reads from `data/`. The first
cell is a setup check; you should see four leases of about 550 words each.

---

## Running the Pipeline from the Command Line

```bash
python scripts/text_diff_baseline.py      # the line-diff baseline
python scripts/diff_versions.py --all     # diff every pair, write outputs/<old>__<new>/report.html
python scripts/evaluate.py --compare      # score against data/ground_truth.json, compare noise rules
```

### Try your own documents

Re-parsing needs the `ade` CLI and an ADE API key (`ade login` first; get a key at
[va.landing.ai](https://va.landing.ai)).

```bash
# put your PDFs in data/pdfs/, then
python scripts/parse.py                         # parse with DPT-3 Verity at the standard tier
python scripts/diff_versions.py <old_stem> <new_stem>
```

Each 2-page lease costs 0.7 credits to parse, and a re-run is served from the CLI's local store for free.
To redo part C's extraction: `ade extract <job_item_id> --schema data/schema/lease_terms.json --tier standard`.

The noise rule's thresholds, `CONFIDENCE_THRESHOLD` and `NEAR_MISS_SIMILARITY`, sit at the top of
`scripts/docdiff.py`.

---

## Project Structure

```
data/
  pdfs/                   the four lease revisions
  parsed/                 raw DPT-3 Verity parse responses
  extracted/              saved extraction + evidence for part C
  schema/                 extraction schema for part C
  ground_truth.json       every planned edit, per pair
scripts/
  patterns.py             cite / route / verify (parts 0–C)
  docdiff.py              the pipeline: words → diff → classify → render
  text_diff_baseline.py   the line-diff baseline
  evaluate.py             scores the pipeline, compares noise rules
  diff_versions.py        CLI: diff a pair, write a report
  parse.py                parses with DPT-3 Verity via the ade CLI
hands_on.ipynb            the session notebook, with Your turn exercises
hands_on_solutions.ipynb  the same notebook, every exercise solved
requirements.txt
```

---

## Limits Worth Knowing

- **Verity reads digitally created, Latin-script documents.** It doesn't handle scans or handwriting.
  For those, parse with DPT-3 Pro, which grounds by line (not word) and returns no confidence scores.
- **Confidence is a ranking for review, not a probability.** 0.95 is the threshold the ADE Playground
  uses to highlight words; tune it on your own documents.
- **Moved text shows up as removed in one place and added in another.** Nothing here detects moves.
- **Punctuation at word edges is ignored when aligning** (`Premises.` matches `Premises,`), so a
  punctuation-only edit isn't reported.
- **The demo set is small and synthetic**: one lease, 11 planned edits, 1 real misread. The thresholds
  were set on this set, so check them on your own documents before relying on them.
