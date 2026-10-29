# Executive employment agreement

Source assets for `landing.ai/document-type/executive-employment-agreement`.

## Sample document

`source/executive-employment-agreement.pdf` is the superintendent employment agreement
between the Bethlehem Central School District (Delmar, NY) and its Superintendent of
Schools, approved July 1, 2025, for a term running from July 1, 2025 to June 30, 2030.
**13 pages, portrait (612×792).** It is a wet-ink executed scan: every page is one
image, with an invisible OCR text layer over it. Pages 1 to 12 hold the recitals and 18
numbered sections (term, compensation, duties, benefits, leave, renewal, termination
and so on). Page 12 ends with a side-by-side signature block, and page 13 holds two
notary acknowledgments with stamps and seals.

| | |
|---|---|
| Publisher | Bethlehem Central School District |
| Source | [bethlehemschools.org](https://www.bethlehemschools.org/wp-content/uploads/2025/09/J-Monroe-Employment-Contract-Approved-7-1-2025-with-signatures-accessible.pdf), linked from the district's [Employment Contracts](https://www.bethlehemschools.org/employment-contracts/) page |
| Retrieved | 2026-10-28, by script |
| Clearance | Public |

## Clearance: published as filed

The district posts this agreement for public access, and in New York a public
employee's contract is a public record. **The operator chose not to redact it.** All 13
pages are committed as the district filed them, including the parties' names, their
signatures and the notaries' details on pages 12 and 13. This is a deliberate exception
to the collection's usual rule that personal data is replaced before parsing. The
decision was made explicitly on 2026-10-28.

Only the PDF's document metadata was cleared: the `/Info` dictionary, the XMP and the
tagged-PDF structure tree. The page images and the OCR text layer are untouched. No
person is featured on the page. Every featured field is an impersonal contract term.

## Why this document

The collection's first **executive contract**, and a long scanned legal instrument
rather than a form:

- **Terms stated in prose.** No value sits in a labelled box. The salary is written
  out in words and then in figures ("two hundred and thirty-five thousand, five hundred
  and fifty-three dollars ($235,553.00)"), and the increase is given as "four percent
  (4.0%)".
- **Schedules buried in sentences.** The longevity benefit is three payments, each with
  its own trigger, inside one paragraph.
- **A scan with an OCR layer.** The text layer is a scanner's, not the author's, so
  parsing has to work from the image.
- **Execution artifacts.** Handwritten dates, wet-ink signatures and two notary
  stamps, which DPT-3 labels `[SIGNED]`, `[HANDWRITTEN_SIGNATURE]` and `[STAMPED]` in the
  markdown.

## Featured fields: the deal on page 2

All on **page 2**, which the request suggested, together with these terms:

| Field | Value |
|---|---|
| Term start | July 1, 2025 |
| Term end | June 30, 2030 |
| Base salary | 235553 |
| Annual increase | 4.0 |
| Longevity payment | 7500 |

Together they give the commercial core of the contract: how long it runs, what it pays,
how pay grows, and the top longevity payment. Base salary and the annual increase are
pinned to their second occurrence, the line that prints the figure. The first occurrence
of each grounds to the line with the spelled-out words, which does not contain the
digits. Of the three longevity payments, the $7,500 one is featured because its line
carries both the amount and its effective date (July 1, 2028).

## What it surfaced

**Prose terms ground well when the figure is printed.** Every numeric term in the
compensation, benefits and leave sections has at least one `ok` occurrence. Each one
lands on the line that prints the figure.

**Values stated twice ground twice.** Salary, increase and the longevity milestones each
come back with two ranges: one on the words and one on the figure. The words occurrence
is flagged `OFF` because the digits are not in it. This is why the manifest pins
occurrences.

**Paraphrased values never match.** The agreement date, the work year ("12 months, from
July 1 to June 30"), the pay frequency, the governing law and the position title extract
correctly. But they are restated values, not substrings, so their ranges cover the
sentence that supports them, and every occurrence reads `OFF`.

**The side-by-side signature block reads as two stacks.** On page 12 the district's
column and the superintendent's column come back one after the other, with each
signature tagged. The two "Dated" lines and the column captions interleave, though,
so pairing a date with its signer from the markdown alone takes care.

28 of 51 grounded occurrences are `ok` and 23 are `OFF`. None is `SYNTH`.

## Extraction

`schema.json` was written for this agreement, with **27 leaf fields**: agreement date,
employer name and address, executive name and position, term (start, end, work year),
compensation (base salary and its period, pay frequency, annual increase, longevity
payments with milestone and amount), benefits (life insurance, health and dental
employer shares, retiree health share, family health buy-out, maximum retirement
contribution), leave (sick, bereavement, personal, vacation days), renewal notice
deadline, resignation notice and governing law. Everything populates, with no
warnings. The field names are generic, so the schema fits a corporate executive
agreement as well as this school district one.

## Cost

**23.30 credits** at standard tier for 13 pages, parse and extract together.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py executive-employment-agreement                # 23.30 credits
.venv/bin/python document-types/scripts/run_ade.py executive-employment-agreement --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py executive-employment-agreement           # free
.venv/bin/python document-types/scripts/inspect_fields.py executive-employment-agreement --page 2
```

The source PDF's metadata was cleared with `document-types/scripts/pdfmeta.py`
(`clear()`), with the page content left as downloaded.
