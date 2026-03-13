#!/usr/bin/env python3
import sqlite3
import subprocess
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.erp_service import ERPService, CustomerInput, ProductInput, LineInput


def main() -> None:
    db = Path(tempfile.gettempdir()) / "erp_phase8_10.sqlite3"
    if db.exists():
        db.unlink()

    subprocess.run(["./scripts/run_migrations.sh", str(db)], check=True)
    subprocess.run(["./scripts/apply_seeds.sh", str(db)], check=True)
    service = ERPService(str(db))

    customer_id = service.create_customer(CustomerInput(customer_code="CLI880", legal_name="Forjas del Norte S.A."))
    product_id = service.create_product(ProductInput(sku="FJ-01", name="Pieza forjada", unit="ud", base_price=100, default_vat_rate_id=101))

    quote_id = service.create_quote(customer_id, "2026-03-13", [LineInput(product_id, "Pieza forjada", 10, 100, 0, 21)])
    order_id = service.convert_quote_to_order(quote_id, "2026-03-14")

    delivery_id = service.create_delivery_note_from_order(order_id, "2026-03-15", {1: 6})
    invoice_id = service.create_invoice_from_delivery_note(delivery_id, "2026-03-16", "2026-04-15")

    with sqlite3.connect(db) as conn:
        due_date_id = conn.execute("SELECT id FROM invoice_due_dates WHERE invoice_id=?", (invoice_id,)).fetchone()[0]

    payment_id = service.register_payment(customer_id, "2026-03-20", 363.0, 101, invoice_id, due_date_id)

    with sqlite3.connect(db) as conn:
        inv = conn.execute("SELECT subtotal, tax_total, total, amount_paid, amount_due, status FROM invoices WHERE id=?", (invoice_id,)).fetchone()
        ol = conn.execute("SELECT served_quantity, invoiced_quantity FROM order_lines WHERE order_id=?", (order_id,)).fetchone()
        rel = conn.execute("SELECT COUNT(*) FROM document_relations WHERE target_doc_type='invoice' AND target_doc_id=?", (invoice_id,)).fetchone()[0]
        pay = conn.execute("SELECT amount FROM payments WHERE id=?", (payment_id,)).fetchone()[0]

    assert inv == (600.0, 126.0, 726.0, 363.0, 363.0, "partially_paid")
    assert ol == (6.0, 6.0)
    assert rel == 1
    assert pay == 363.0
    assert service.pending_amount_by_customer(customer_id) == 363.0

    print("OK phase8-10")


if __name__ == "__main__":
    main()
