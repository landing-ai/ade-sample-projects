# Search Warrant

The face page of a Los Angeles County search warrant and affidavit. It is a printed court
form with the affiant's sworn statement, the Penal Code 1524 grounds as a row of
X-or-blank lines, the magistrate's signature and issuance block, the Superior Court seal,
a "FILED" stamp and a fax header printed upside down along the bottom edge. One portrait
page, a faxed and scanned image with an OCR text layer.

| | |
|---|---|
| Publisher | Superior Court of California, County of Los Angeles (court filing; the affidavit is by a Los Angeles Police Department detective) |
| Source URL | https://www.scribd.com/document/81929901/Chris-Brown-Police-Report |
| File | Page 3 of the 11-page upload. The operator extracted it and downloaded it manually |
| Retrieved | 2026-11-16 |
| Clearance | `public` |

## Clearance

This is a court filing from the 2009 Chris Brown case. The detective's affidavit was
widely published by news media in March 2009, for example by NBC Washington ("LAPD
Detective's Affidavit Details Alleged Beating By Chris Brown Of Rihanna"). Scribd is not
the publisher. The uploader there is only where this copy came from.

This page names only officials acting in their role: the detective who swore the
affidavit and the Superior Court judge who issued the warrant. The people and places to
be searched are on the pages it refers to ("SEE PAGE NO. 2 thru 4"), which are not
included. The request described the page as already redacted. In fact it had nothing to
redact, and its text layer was read to confirm that. The PDF's metadata was cleared, and
nothing else was changed. The signatures stay as written.

## Why this document

It is a legal form that has been faxed, filed and scanned. A stamp runs vertically
through the text, the fax header is upside down, the grounds are marked with a bare "X"
in a blank, and the handwritten date, time, district and department sit on the form's
underlines. It tests whether extraction can tell which ground was marked and read the
issuance block through the noise.

## Schema

No schema was supplied, so one was written: the warrant number, the court (state, county,
judicial district, department), the affiant (name and the two requests the affiant
checks), the marked grounds, the search scope, and issuance (judge, title, date, time and
the two approvals). That is 16 leaf fields.

## Featured fields, page 1

| Field | Label | Value |
|---|---|---|
| `affiant.name` | Affiant (sworn officer) | De Shon Andrews |
| `grounds[0]` | Ground marked (Penal Code 1524) | tends to show that a felony has been committed or that a particular person has committed a felony. |
| `issuance.issuing_judge` | Issuing judge | Patricia M. Schnegg |
| `court.department` | Department | 123 |

The request asked for page 3 of the original fax. That is this file's only page.

The marked ground is the strongest field. The extraction returned only the line marked X,
of six possible grounds, and boxed exactly that line. The judge's title and the judicial
district are also correct, but they share one line box with the department, so only the
department is featured from that line.

## What the extraction got wrong

The handwritten values are where this page is hard, and three came back wrong. None is
featured.

- **Warrant number.** The page reads `58168`. The extraction returned `581168`, with an
  extra 1, probably from the vertical stroke in the handwriting.
- **Issue date.** It came back as `2007-07-20`. The day (20) is right. The month and
  year are hard to read, but the warrant cannot predate the February 2009 case, and the
  page was faxed on 03/05/2009.
- **Issue time.** It came back as `4:55 a.m./p.m.`, without resolving which is circled
  (p.m.).

The Hobbs sealing and night search booleans are all correctly `false`, but they ground
`OFF`, because a boolean has no matching text to box.

## Grounding

- **The affiant's name boxes its whole first line.** The name opens the sworn
  paragraph, and the box covers that one line, not the paragraph.
- **The judge's box takes in the title line below**, because the printed name is
  partly overprinted by the signature.
- **The stamp text is parsed as stray lines** ("FILED", "PM 4 3", fragments of the clerk
  stamp). It did not disturb any featured value.

## Credits

2.60 credits at standard tier (parse and extract).

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py search-warrant
.venv/bin/python document-types/scripts/inspect_fields.py search-warrant --page 1
.venv/bin/python document-types/scripts/build_images.py search-warrant
```
