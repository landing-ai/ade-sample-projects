# Vehicle Registration

**On the website:** [landing.ai/document-type/vehicle-registration](https://landing.ai/document-type/vehicle-registration)

A Florida vehicle registration printed by the Florida Department of Highway Safety and
Motor Vehicles as a system test, marked TEST DOCUMENT. It names a sample registrant and
describes a blue 2005 Chevrolet four-door with its VIN, plate, decal, expiry and title
number, followed by an itemized fee block and a grand total.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 26 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:58 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 1,999 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 5.3 s |
| Per page | 5.3 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 1.0 credits |
| Per page | 1.00 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:58 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 26 |
| Non-null fields returned | 22 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 85.4 s |
| Per schema field (26) | 3.29 s |
| Per value returned | 3.88 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 1.1 credits |
| Per schema field (26) | 0.042 credits |
| Per value returned | 0.050 credits |

## Origin

`source/flhsmv-vehicle-registration-test-print.pdf` is a Florida vehicle registration
printed by the Florida Department of Highway Safety and Motor Vehicles (FLHSMV) as a
system test. The header reads **TEST DOCUMENT**. The registrant is "SAMPLE SAMPLE, SAMMY
D SAMPLE JR" at 2900 Neil Kirkman Building, which is the agency's own Tallahassee
address. The vehicle is a blue 2005 Chevrolet four-door with the VIN
`1POLKTESTPRINT123`. The card carries the plate, decal, expiry, title number and an
itemized fee block (registration tax 68.15 plus a 3.00 county fee, for a grand total of
71.15). It is **1 page, landscape, scanned**: a low-resolution raster (about 140 dpi as
placed in the handout) with no text layer.

| | |
|---|---|
| Publisher | FLHSMV (test print), republished by the City of Bloomington, Indiana, Parking Services |
| Source | [bloomington.in.gov/…/Sample Vehicle Registrations_0.pdf](https://bloomington.in.gov/sites/default/files/2022-07/Sample%20Vehicle%20Registrations_0.pdf) |
| Linked from | "Sample of vehicle registrations" on the city's [neighborhood parking page](https://bloomington.in.gov/transportation/parking/neighborhood-parking) |
| Retrieved | 2026-10-13, by script |
| Clearance | **Redacted**: cropped from a larger handout, and one value replaced. See below. |

Provenance is secondary. The city's handout is a compilation, and the original FLHSMV
page this test print came from was not found.

The city's handout has 4 pages and shows registrations from several states. Apart from
this Florida test print, the cards appear to be real people's registrations. **None of
them were ever written to this repo.** Only the Florida card was taken: it is a single
embedded JPEG on handout page 3 (914 x 479 px), and its bytes were placed unchanged on a
new page of 468 x 245.28 pt, the size the image had on the handout page. Everything else
in the handout was dropped: pages 1, 2 and 4, the second card image lower on page 3, and
page 3's caption text. The PDF's metadata was cleared.

Almost every value on the card is obvious test data: the "SAMPLE" registrant, the
agency's own address and a VIN that spells out "TEST PRINT". Those were left as printed.
One value was replaced:

| What | Replaced with | Count |
|---|---|---|
| DL/FEID (driver licence or federal employer ID) value: a letter and 12 digits, in a real Florida licence-number format | `S101074959542`. The letter and every digit were drawn at random, so nothing was kept from the original. | 1 |

The original is not recorded anywhere in this folder. OCR could not match the value on
this low-resolution scan, so the stand-in was placed by region and set in Arial Bold.
The page was rebuilt from a 300 dpi render of the edited image, so the cropped JPEG
itself is not carried into the committed PDF. An OCR pass found no original surviving,
as literals or as digits. The result was also checked by eye on 200 and 600 dpi renders,
and every file in this folder was swept for the original. The stand-in renders a little
lighter than the neighbouring bold values. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

A vehicle registration ties a vehicle to its registered owner and shows that the state
fees are paid. People are asked for it whenever ownership or residence has to be shown.

- **Auto insurance:** insurers match the VIN, vehicle and owner to the policy at quote
  and claim time.
- **Auto lending and dealers:** lenders and dealers check registration and title details
  when financing, refinancing or taking a trade-in.
- **Parking and municipal permits:** cities ask for registrations to issue residential
  parking permits, as Bloomington does here.
- **Fleet management and rental:** fleets track registration expiry and fees across
  their vehicles.
- **Law enforcement and toll agencies:** they match plates and VINs to registered
  owners.

### What it contains

- **A borderless grid,** with labels and values in loose columns and no rules.
- **A value that overflows its column,** the VIN running under the next label.
- **Blank fee lines** beside printed amounts that must reconcile to the grand total.
- **A decorative logo** in one corner.
- **A low-resolution scan with no text layer,** so every value has to be read from the
  page image.
