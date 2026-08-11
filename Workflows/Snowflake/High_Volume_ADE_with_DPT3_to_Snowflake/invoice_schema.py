"""
invoice_schema.py
-----------------
Pydantic schema for invoice extraction with ADE DPT-3.

The DPT-3 Extract endpoint (``client.v2.extract``) accepts a Pydantic model
directly as its ``schema`` argument, so this class is passed straight through —
no JSON-schema conversion needed.

Design notes:
- Group related fields into nested models (ADE supports one level of nesting).
- Give every field a description; it steers extraction accuracy.
- Keep ``line_items`` a list so multi-row invoices flatten cleanly into the
  INVOICE_LINE_ITEMS table.

Develop and test schemas quickly in the Visual Playground:
https://va.landing.ai/demo/doc-extraction
"""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class InvoiceInfo(BaseModel):
    invoice_date_raw: str = Field(..., description="Invoice date exactly as printed; do not reformat.")
    invoice_date: Optional[date] = Field(..., description="Invoice date normalized to YYYY-MM-DD.")
    invoice_number: str = Field(..., description="Invoice number/identifier.")
    order_date: Optional[str] = Field(None, description="Order or purchase date, if present.")
    po_number: Optional[str] = Field(None, description="Customer purchase order (PO) number.")
    status: Optional[str] = Field(None, description="Payment status (e.g., PAID, UNPAID).")


class CustomerInfo(BaseModel):
    sold_to_name: str = Field(..., description="Name of the customer billed (person or organization).")
    sold_to_address: Optional[str] = Field(None, description="Billing address of the customer.")
    customer_email: Optional[str] = Field(None, description="Customer email address.")


class SupplierInfo(BaseModel):
    supplier_name: str = Field(..., description="Name of the supplier/issuing company.")
    supplier_address: Optional[str] = Field(None, description="Supplier address.")
    email: Optional[str] = Field(None, description="Supplier email address.")
    phone: Optional[str] = Field(None, description="Supplier phone number.")


class TermsAndShipping(BaseModel):
    payment_terms: Optional[str] = Field(None, description="Payment terms (e.g., Net 30).")
    ship_via: Optional[str] = Field(None, description="Carrier/service (e.g., UPS Ground).")
    ship_date: Optional[str] = Field(None, description="Ship date, if present.")
    tracking_number: Optional[str] = Field(None, description="Shipment tracking number.")


class TotalsSummary(BaseModel):
    currency: Optional[str] = Field(None, description="ISO currency code (e.g., USD).")
    total_due_raw: Optional[str] = Field(None, description="Total due exactly as printed.")
    total_due: float = Field(..., description="Total amount due as a number (no symbols).")
    subtotal: Optional[float] = Field(None, description="Subtotal as a number.")
    tax: Optional[float] = Field(None, description="Tax as a number.")
    shipping: Optional[float] = Field(None, description="Shipping charge as a number.")


class LineItem(BaseModel):
    line_number: Optional[str] = Field(None, description="Printed line number.")
    sku: Optional[str] = Field(None, description="SKU / item code / part number.")
    description: str = Field(..., description="Item or service description.")
    quantity: Optional[float] = Field(None, description="Quantity / unit count.")
    unit_price: Optional[float] = Field(None, description="Unit price as a number.")
    amount: Optional[float] = Field(None, description="Extended line amount as a number.")


class InvoiceExtractionSchema(BaseModel):
    invoice_info: InvoiceInfo = Field(description="Key identifiers and dates for the invoice.")
    customer_info: CustomerInfo = Field(description="Details about the customer billed.")
    company_info: SupplierInfo = Field(description="Details about the issuing supplier.")
    order_details: TermsAndShipping = Field(description="Payment and shipping information.")
    totals_summary: TotalsSummary = Field(description="Financial totals for the invoice.")
    # default_factory keeps the field out of the schema as required-but-null
    line_items: List[LineItem] = Field(default_factory=list, description="Invoice line items.")
