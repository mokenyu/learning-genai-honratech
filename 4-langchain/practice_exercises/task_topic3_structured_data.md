# Student Assessment Task: Structured I/O, Schema Validation & JSON Pipelines

## 🎯 Objective
Build a production-grade automated information extraction and validation service that parses unstructured vendor invoices from `docs/sample_invoice.txt`, validates all fields against strongly-typed Pydantic v2 schemas, and outputs formatted JSON to `docs/invoice_record.json`.

---

## 📋 Task Requirements

### 1. Schema Definition
- Define the following nested Pydantic v2 models:
  - `LineItem`: `description: str`, `quantity: int`, `unit_price: float`, `total_price: float`.
  - `VendorInfo`: `name: str`, `tax_id: Optional[str]`, `contact_email: Optional[str]`.
  - `InvoiceRecord`: `invoice_number: str`, `invoice_date: str`, `vendor: VendorInfo`, `items: List[LineItem]`, `subtotal: float`, `tax_amount: float`, `total_amount: float`, `currency: Enum`.

### 2. Strict Structured Output Enforcement
- Initialize the model with `temperature = 0.0`.
- Apply `model.with_structured_output(InvoiceRecord)` to enforce schema compliance.

### 3. File Processing Pipeline
- Ingest raw invoice data from `docs/sample_invoice.txt`.
- Invoke the structured extractor on the text.
- Verify calculation consistency: assert that `subtotal + tax_amount == total_amount`.

### 4. JSON Serialization & Output
- Use `.model_dump_json(indent=2)` to serialize the validated object.
- Save the JSON string to `docs/invoice_record.json`.
- Demonstrate round-trip validation using `InvoiceRecord.model_validate_json(...)`.

---

## 🏆 Submission Deliverables
1. Runnable script or notebook implementing the extraction pipeline.
2. The generated JSON record saved in `docs/invoice_record.json`.
