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
    db = Path(tempfile.gettempdir()) / "erp_phase6_7.sqlite3"
    if db.exists():
        db.unlink()

    subprocess.run(["./scripts/run_migrations.sh", str(db)], check=True)
    subprocess.run(["./scripts/apply_seeds.sh", str(db)], check=True)

    service = ERPService(str(db))
    customer_id = service.create_customer(CustomerInput(customer_code="CLI777", legal_name="Aceros Rivera S.L."))
    product_id = service.create_product(ProductInput(sku="ACR-01", name="Perfil UPN", unit="m", base_price=50, default_vat_rate_id=101))

    quote_id = service.create_quote(
        customer_id=customer_id,
        issue_date="2026-03-13",
        valid_until="2026-04-13",
        lines=[
            LineInput(product_id=product_id, description="Perfil UPN 80", quantity=4, unit_price=50, discount_pct=10, vat_rate=21),
            LineInput(product_id=None, description="Corte y preparación", quantity=1, unit_price=30, discount_pct=0, vat_rate=21),
        ],
    )

    order_id = service.convert_quote_to_order(quote_id, issue_date="2026-03-14")

    with sqlite3.connect(db) as conn:
        q = conn.execute("SELECT status, subtotal, tax_total, total FROM quotes WHERE id=?", (quote_id,)).fetchone()
        o = conn.execute("SELECT source_quote_id, status, subtotal, tax_total, total FROM orders WHERE id=?", (order_id,)).fetchone()
        rel = conn.execute("SELECT source_doc_type, target_doc_type, relation_type FROM document_relations WHERE source_doc_id=? AND target_doc_id=?", (quote_id, order_id)).fetchone()
        ol_count = conn.execute("SELECT COUNT(*) FROM order_lines WHERE order_id=?", (order_id,)).fetchone()[0]

    assert q[0] == "accepted"
    assert q[1:] == (210.0, 44.1, 254.1)
    assert o[0] == quote_id and o[1] == "confirmed"
    assert o[2:] == (210.0, 44.1, 254.1)
    assert rel == ("quote", "order", "conversion")
    assert ol_count == 2

    print("OK phase6-7")


if __name__ == "__main__":
    main()
