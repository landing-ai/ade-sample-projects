# Invoice

Source assets for `landing.ai/document-type/invoice`.

## Sample document

`source/invoice_4.pdf` — a single-page A.E. Blake Sales invoice, bilingual
French/English, with a three-row line-item table.

> **This is a development placeholder, not the final sample.**
>
> It was copied from `Use_Cases/Invoices/input_folder/`, where it has been committed to
> this public repository for some time, so using it here publishes nothing new. It exists
> to prove the pipeline end to end and to give the page template something real to render
> against.
>
> It should be replaced before the page ships. It is a real third-party invoice naming two
> real companies and carrying real contact details, and it was not gathered with
> publication on a LandingAI marketing page in mind. A purpose-sourced or synthesised
> invoice, with its provenance recorded here, is what belongs in this folder.

**Replacement checklist**

- [ ] Sourced synthetically, from a vendor sample, or explicitly cleared
- [ ] Personal data obviously non-real and not colliding with real identifiers
- [ ] Provenance and clearance recorded in this file
- [ ] `run_ade.py` and `build_images.py` re-run, images checked by eye

## Why this document

One page and portrait, so it is the simplest case in the pilot — but it carries a real
line-item table, which the schema and the page both need to handle. A one-line invoice
would not have shown whether nested array fields can be grounded and boxed. They can:
`line_items[1].description` resolves to the second row of the table.

It exercises both box-resolution paths in `build_images.py`:

| Field | Resolved via |
|---|---|
| `invoice_info.invoice_number`, `company_info.supplier_name`, `customer_info.sold_to_name` | `atomic_grounding` line-level boxes |
| `line_items[1].description`, `totals_summary.total_due` | `table_cell` children |

## Extraction

`schema.json` is the schema from `Use_Cases/Invoices/v2/schema/invoice_demo_schema.json`,
unchanged: six top-level groups — `invoice_info`, `customer_info`, `company_info`,
`order_details`, `totals_summary`, `line_items` — with currency in `totals_summary` and a
nested array of line items. All six groups populate on this document, with three line
items.

`company_info.pan` comes back null with a schema warning. PAN is an Indian tax
identifier and this is a Canadian invoice, so that is correct behaviour, not a failure.

`manifest.json` names the five fields featured on the page. **Currency is in the schema
but not featured**: on this invoice it shares a table cell with `total_due`, so both
would render the identical crop.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py invoice      # spends credits
.venv/bin/python document-types/scripts/build_images.py invoice # free
```

Both calls run through the jobs API at the **standard** service tier. This document cost
3.10 credits; the cost is dominated by the extract step, which scales with schema size,
and this schema is 13 KB. Synchronous calls always
bill at priority whatever tier you ask for, so the jobs API is the only route to the
cheaper rate. Web content is never urgent.

Output files carry the parse model — `parse-pro.json`, `extract-pro.json`,
`images/pro/` — so a Verity run can sit beside the Pro one without overwriting it once
that model is GA.

## A note on repeated values

A value printed in more than one place comes back with several ranges, and their order is
not guaranteed stable between runs — on an earlier sample, re-parsing moved a box from one
occurrence to the other. Set `"occurrence"` on a field in `manifest.json` to pin which one
is boxed. `build_images.py` warns whenever a field has several and none is pinned.
