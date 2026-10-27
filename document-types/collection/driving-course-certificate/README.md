# Driving Course Certificate

Source assets for `landing.ai/document-type/driving-course-certificate`.

## Sample document

`source/texas-driving-safety-course-certificate-redacted.pdf` is a **State of Texas Driving
Safety Course Uniform Certificate of Completion**. A Texas driver gets one after a six-hour
driving safety (defensive driving) course approved by the Texas Department of Licensing and
Regulation (TDLR). The course provider issues it, and the driver files it with a court to
dismiss a traffic ticket or sends it to an insurer for a discount.

**1 page, portrait, fillable form with a text layer.** The page prints the certificate
twice: a **court copy** above an **insurance copy**, divided by a dashed cut line. Each copy
has a title block, the certification statement, a student signature line with an orange
SIGN tab, and a right-hand panel. The panel holds the certificate number, student name,
driver licence number and date of birth, course provider, school-classroom code,
completion and issue dates, instructor licence number and reason. Each panel field has a
"Changed from:" line under it. The court copy also has a Court Information block. A large
grey TDLR logo watermark sits behind both copies.

The sample was issued for a traffic ticket in an Ellis County municipal court. The course
was completed and the certificate issued on 24 January 2022. Both signature lines are blank.

| | |
|---|---|
| Publisher | TDLR uniform certificate form, issued by a TDLR-approved course provider. Uploaded to Scribd by a third party |
| Source | [scribd.com/document/998399674](https://www.scribd.com/document/998399674) |
| Retrieved | 2026-10-26, downloaded manually (Scribd blocks scripted downloads) |
| Clearance | **Redacted**, see below |

The Scribd account that uploaded it is not the issuer. This is a real student's record, not
a publisher's sample. The Scribd listing URL ends in a slug that was the student's driver
licence number, so the URL recorded here is the bare document ID with the slug removed.

## Redaction

The certificate carried the student's real identity. Each value was replaced with
`document-types/scripts/redact.py`. The values live in fillable form fields, so the rules
were applied to the field values and how they display:

| What | Replaced with | Count |
|---|---|---|
| Student's name (Last, First), panel and mailing block of both copies | `Sample, Jane` | 4 |
| Student's street address | `100 Main St.` | 2 |
| Certificate number (TDLR can look it up) | `CP275-63203533`, randomly drawn | 2 |
| Student's Texas driver licence number | `89449885`, randomly drawn | 2 |
| Student's date of birth | `08/23/1984` | 2 |

Kept: city, state and ZIP; the court; the course provider's trade name, school-classroom
code and instructor licence number; the dates; and the reason. The PDF metadata carried the
form designer's name and was cleared. The file's owner-password encryption was dropped. The
originals are not recorded anywhere in this folder, and the rules file stays outside the
repo. Verified by redact.py's text check, by eye on a render, and by
`ship.py check --rules` over every file in this folder.

## Why this document

This is a short state certificate with layout traps that other documents in the collection
do not have:

- **Every value is printed twice.** The court and insurance copies repeat the same
  certificate, so every field has two candidate locations. The Court Information block
  appears only on the court copy.
- **A large watermark runs behind the text.** It cuts through the warning footer and the
  middle of each copy.
- **The provider name is letter-spaced and wraps:** `F R E E - C E R` / `T I F I C A T E`.
- **A SIGN tab sits by the signature line,** which is blank.
- **Every field has a "Changed from:" line,** all empty, which a reader has to skip.

## Featured fields

All on **page 1**, pinned to the top (court) copy:

| Field | Label | Value |
|---|---|---|
| `certificate_number` | Certificate number | CP275-63203533 |
| `court` | Court | Ellis County: Municipal Garrett (Garrett) |
| `reason` | Reason for course | Traffic Ticket |
| `completion_date` | Completion date | 2022-01-24 |
| `issue_date` | Issue date | 2022-01-24 |

Together they describe one filing: which certificate it is, which court it goes to, why the
course was taken, and when the course was completed and the certificate issued. The student
name, licence number and date of birth (all stand-ins) also ground correctly. They are not
featured because the impersonal fields make the same point. The instructor licence number
also grounds correctly, but it identifies a real instructor.

## Grounding notes

- **The two copies were kept apart.** Every featured field has an occurrence in the court
  copy, with a tight box on the value. The certificate number's crop triggers
  `build_images.py`'s OCR warning. The box is on the right line; the red text under the
  orange highlight is just hard for OCR to read.
- **DPT-3 reported a signature that is not there.** It labelled the insurance copy's
  signature area `[E-SIGNED]`, apparently because of the orange SIGN tab, and extraction
  returned `student_signed: true`. Both signature lines are blank. The schema was not
  changed, so this miss stays visible.
- **The watermark broke the reading order.** The court copy's warning footer was split into
  fragments around the logo. The court copy's `Pearland, TX 77581` line was moved to the end
  of the markdown, after the insurance copy, but extraction still assembled the address
  correctly.
- **The letter-spaced provider name** was joined into `FREE CERTIFICATE` by extraction, as
  the schema asked. Because of that, its ranges are OFF: the value is not literally in the
  boxed text.
- **The school-classroom code** reads `C3344` in the form field, with `-001` printed beside
  it. The parse joined the two into `C3344-001`. Its first range points into the insurance
  copy, and its second points at the whole court-copy panel.

## Schema

`schema.json` has **21 leaf fields**: the certificate title, regulating agency, course
hours and the copy labels; the certificate number; the student (name, licence state and
number, date of birth, and street, city, state and ZIP); the court; the course provider,
school-classroom code and instructor licence number; the completion and issue dates; the
reason; and whether the student signed. All 14 top-level fields were populated with no
warnings. `student_signed` came back wrong, as noted above.

## Credits

**2.9 credits** at the standard tier: 1.4 for parsing 1 page with DPT-3 Pro and 1.5 for
extraction.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py driving-course-certificate               # spends credits
.venv/bin/python document-types/scripts/run_ade.py driving-course-certificate --extract-only
.venv/bin/python document-types/scripts/build_images.py driving-course-certificate          # free
.venv/bin/python document-types/scripts/inspect_fields.py driving-course-certificate --page 1
```
