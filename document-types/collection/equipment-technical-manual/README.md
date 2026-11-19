# Equipment Technical Manual

**On the website:** [landing.ai/document-type/equipment-technical-manual](https://landing.ai/document-type/equipment-technical-manual)

Five service-reference pages from John Deere's 1996 Technical Manual TM1360, the repair
manual for the 655, 755, 855, 955, 756 and 856 Compact Utility Tractors. They give
metric and inch fastener torque tables, torque charts and service steps for O-ring face
seal and O-ring boss fittings, and the diesel fuel specifications for North America.

| | |
|---|---|
| Pages | 5 |
| Fields in the extraction schema | 66 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:54 | 2026-11-19 03:00 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 20,526 | 20,327 |
| Words under 0.95 confidence | 40 | n/a |
| Words under 0.80 confidence | 30 | n/a |
| Words under 0.50 confidence | 7 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 8.1 s | 12.8 s |
| Per page | 1.6 s | 2.6 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.9 credits | 7.6 credits |
| Per page | 0.58 credits | 1.52 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:55 | 2026-11-19 03:00 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 66 | 66 |
| Non-null fields returned | 66 | 66 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 214.7 s | 157.1 s |
| Per schema field (66) | 3.25 s | 2.38 s |
| Per value returned | 0.34 s | 0.25 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 19.4 credits | 20.3 credits |
| Per schema field (66) | 0.294 credits | 0.308 credits |
| Per value returned | 0.031 credits | 0.033 credits |

## Origin

`source/john-deere-tm1360-torque-and-fuel.pdf` is five pages from **Deere & Company's
Technical Manual TM1360** (John Deere Lawn & Grounds Care Division, June 1996), the
repair manual for the 655, 755, 855, 955, 756 and 856 Compact Utility Tractors. They are
the service-reference pages a technician looks things up on:

- Page 1 (printed 10-15-1): **Metric fastener torque values**. Property-class head and
  nut markings drawn as vector diagrams, then a 14-row table, M6 to M36, with two header
  tiers above the size rows: property class (4.8, 8.8 or 9.8, 10.9, 12.9), then
  lubricated or dry, then N·m and lb-ft. Footnote markers sit on the header cells.
- Page 2 (printed 10-15-2): **Inch fastener torque values**, the same layout for SAE
  grades 1, 2, 5 and 8, sizes 1/4 to 1-1/2.
- Page 3 (printed 10-15-3): **O-ring face seal fittings**: a fitting drawing, six service
  steps, and a torque chart by tube O.D., dash size and thread (swivel nut and bulkhead
  nut torque).
- Page 4 (printed 10-15-4): **O-ring boss fittings**: numbered steps interleaved with
  drawings beside a straight-fitting torque table that gives N·m, lb-ft and a number of
  flats to turn when a torque wrench cannot be used.
- Page 5 (printed 10-20-1): **Diesel fuel** specifications for North America: ASTM D975
  grades, cetane, cold filter plugging point, sulfur, lubricity (BOCLE) and storage.

It is **5 pages, portrait**, with a born-digital text layer throughout (producer
VERSACOMP/MASTER), and the fastener markings and fitting drawings as vector paths.

| | |
|---|---|
| Publisher | Deere & Company (John Deere Lawn & Grounds Care Division) |
| Source | [golftechs.us/Manuals/JDtractors.pdf](http://www.golftechs.us/Manuals/JDtractors.pdf) |
| Retrieved | 2026-10-14, by script |
| Clearance | Public, by the operator's decision (see below) |

The manual is marked COPYRIGHT 1996 Deere & Company, and Deere still sells it (for
example through deeremanuals.com as TM1360). The copy used here is hosted on
golftechs.us, a site unrelated to Deere whose home page is a placeholder and whose
Manuals folder is not browsable; nothing found links to the file. It is a mirror, not a
publisher distribution. That doubt was put to the operator, who chose to use the
document with clearance `public` on 2026-10-14.

The original is 570 pages. This sample keeps original pages 21-25 only, in order, and
the PDF metadata was cleared. The pages carry no personal data, so nothing was redacted.
Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Equipment manufacturers publish technical manuals for every model they build, and the
specifications inside them drive repair, maintenance and parts work long after the
equipment is sold.

- **Dealers and service technicians:** they look up torque values, fitting procedures
  and fluid specifications during repairs.
- **Fleet and facilities maintenance:** golf courses, grounds crews and municipalities
  build maintenance schedules from manufacturer specifications.
- **Equipment manufacturers:** service and documentation teams maintain and reissue
  manuals across model years.
- **Parts and aftermarket suppliers:** they map specifications to fasteners, fittings
  and fluids they sell.
- **Field service and knowledge-base tools:** maintenance software turns manual pages
  into searchable reference data.

### What it contains

- **Dense numeric lookup tables** with multi-tier column headers: size rows under class
  or grade, then lubricated or dry, then N·m and lb-ft, for 16 value columns per row.
- **Footnote markers** on header cells.
- **Vector diagrams** of fastener head markings and fittings beside the tables.
- **Numbered procedures** interleaved with drawings, with steps that wrap across lines.
- **Specification text** with standards references and units (ASTM D975, cetane,
  sulfur, lubricity).
- **A printed error** in the metric table, where one lb-ft value does not match its N·m
  value.
