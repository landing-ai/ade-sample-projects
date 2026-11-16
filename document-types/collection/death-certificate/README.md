# Death Certificate

A certified copy of a Missouri **Certification of Death**, issued January 17, 2017 by the Missouri
Department of Health and Senior Services. It is a one-page landscape photocopy of the state's
green security-bordered certificate. The certificate is a mix of preprinted labels in sans-serif
type and values typed in a monospace typewriter face. It has a printed signature and the
department's seal.

## Provenance

| | |
|---|---|
| Published by | KCUR 89.3, Kansas City's NPR member station, as an image in a 2017 news story |
| Issued by | Missouri Department of Health and Senior Services, Bureau of Vital Records |
| Source URL | https://npr.brightspotcdn.com/dims4/default/5dd4623/2147483647/strip/true/crop/2544x2120+0+0/resize/880x733!/quality/90/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2Flegacy%2Fsites%2Fkcur%2Ffiles%2F201712%2FDeathCertificate_white_out_2.png |
| Retrieved | 2026-11-15 |
| Clearance | `public` |

The URL above is an 880-pixel resize. The source PDF was built from the full-size 2544×2120
original behind it, flattened onto white, with no metadata.

KCUR had already whited out the Social Security number and the residence address before
publishing. The PNG has a transparency channel, so it was checked: those boxes are blank in the
pixels themselves, not hidden by transparency.

The document is otherwise published exactly as KCUR printed it, at the operator's decision:

- The decedent is deceased.
- The state registrar and his signature appear in an official capacity.
- The funeral home is a business.
- The surviving spouse's name is the only living private individual on the page. It was kept
  because the operator chose to use the image as published.

## Why this document

A vital record is a fixed government form completed on a typewriter. Each value sits beside its
label rather than in a cell, and some labels wrap onto two lines ("DATE OF / DEATH:"). The cause
of death is a short free-text list that mixes underlying causes, with intervals, and a
contributing condition marked "SIG COND". The page is a photocopy, with a heavy guilloche border
and a seal.

## Featured fields (page 1)

| Field | Value |
|---|---|
| State file number | 124-17-000830 |
| County of death | COLE |
| Underlying cause | LIVER FAILURE |
| Significant condition | HEPATITIS C |
| Manner of death | NATURAL |

These are the certificate's record of the death rather than of the people involved: where it is
filed, where it happened, what caused it, and the manner. No individual is featured.

## Grounding on this document

Every value grounds to its own line, including the two-line labels and the cause-of-death lines.

- **Label and value share a box.** "STATE FILE NUMBER: 124-17-000830" is one line, and so is
  "MANNER: NATURAL".
- **The blanks come back null.** The whited-out SSN and residence boxes extract as null and
  ground to their bare labels. The model did not invent values for them.
- **Dates read `OFF`, and they are right.** The schema asks for dates as YYYY-MM-DD, so the
  value "2017-01-16" does not appear literally in "JANUARY 16, 2017". The ranges point at the
  correct lines.
- **"Issued by" is incomplete.** `issued_by` came back as just "CHRISTIAN", the county after the
  colon, rather than the whole line.

## Credits

1.90 credits at standard tier: parse plus extract, 1 page.

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py death-certificate
.venv/bin/python document-types/scripts/inspect_fields.py death-certificate --page 1
.venv/bin/python document-types/scripts/build_images.py death-certificate
```

The schema has 23 leaf fields.
