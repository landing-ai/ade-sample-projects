# Invoice

Source assets for `landing.ai/document-type/invoice`.

## Sample document

`source/invoice_1.pdf` — a single-page Zoom subscription invoice.

> **This is a development placeholder, not the final sample.**
>
> It was copied from `Use_Cases/Invoices/input_folder/`, where it has been committed to
> this public repository for some time, so using it here publishes nothing new. It exists
> to prove the pipeline end to end and to give the page template something real to render
> against.
>
> It should be replaced before the page ships. It is a real third-party invoice carrying a
> real-looking email address and account number, and it was not gathered with publication
> on a LandingAI marketing page in mind. A purpose-sourced or synthesised invoice, with
> its provenance recorded here, is what belongs in this folder.

**Replacement checklist**

- [ ] Sourced synthetically, from a vendor sample, or explicitly cleared
- [ ] Personal data obviously non-real and not colliding with real identifiers
- [ ] Provenance and clearance recorded in this file
- [ ] `run_ade.py` and `build_images.py` re-run, images checked by eye

## Why this document

It is the simplest case in the pilot — one page, portrait, a short schema — and it is the
baseline the template has to get right before the harder types are attempted.

It also exercises both box-resolution paths in `build_images.py`, which is why it was
useful for developing the script:

| Field | Resolved via | Why |
|---|---|---|
| `invoice_number`, `invoice_date`, `vendor_name` | `atomic_grounding` | Line-level boxes inside a text block |
| `total_amount`, `balance_due` | `table_cell` children | Values inside table cells |

The text block holding the invoice metadata covers seven lines — Invoice Date through
Currency and the billing address — so boxing the block would have pointed at the whole
region instead of the value. Line-level grounding is what makes the crop tight.

## Extraction

`schema.json` defines eight fields; all eight populated on this document.
`manifest.json` names the five featured on the page.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py invoice      # spends credits
.venv/bin/python document-types/scripts/build_images.py invoice # free
```

Both calls run through the jobs API at the **standard** service tier: 1.60 credits for
this document, against 3.10 for the same work synchronously. Synchronous calls always
bill at priority whatever tier you ask for, so the jobs API is the only route to the
cheaper rate. Web content is never urgent.

Output files carry the parse model — `parse-pro.json`, `extract-pro.json`,
`images/pro/` — so a Verity run can sit beside the Pro one without overwriting it once
that model is GA.

## A note on repeated values

`total_amount` and `balance_due` each appear **twice** on this invoice: in CHARGE DETAILS
and again in INVOICE TOTALS. ADE returns both locations, and their order is not
guaranteed stable between runs — re-parsing moved the box from one to the other.

`manifest.json` pins both to `"occurrence": 0` so the rendered box does not wander.
`build_images.py` warns whenever a field has several occurrences and none is pinned.
