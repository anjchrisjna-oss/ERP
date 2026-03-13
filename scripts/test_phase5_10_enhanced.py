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
    db = Path(tempfile.gettempdir()) / "erp_phase5_10_enhanced.sqlite3"
    if db.exists():
        db.unlink()

    subprocess.run(["./scripts/run_migrations.sh", str(db)], check=True)
    subprocess.run(["./scripts/apply_seeds.sh", str(db)], check=True)
    service = ERPService(str(db))

    # Fase 5: CRUD clientes/productos
    c1 = service.create_customer(CustomerInput(customer_code="CLI900", legal_name="Industrias Sol S.L.", email="admin@sol.es"))
    p1 = service.create_product(ProductInput(sku="SOL-01", name="Chapa galvanizada", unit="ud", base_price=75.0, default_vat_rate_id=101))

    service.update_customer(c1, phone="954000111", city="Sevilla", notes="Cliente estratégico")
    service.update_product(p1, base_price=79.5, notes="Actualizar tarifa Q2")

    customers = service.list_customers()
    products = service.list_products(search="galva")
    assert len(customers) == 1
    assert customers[0]["city"] == "Sevilla"
    assert len(products) == 1 and products[0]["base_price"] == 79.5

    # Fase 6-10: flujo para generar factura pendiente y vencida
    quote_id = service.create_quote(c1, "2026-03-01", [LineInput(p1, "Chapa galvanizada", 2, 79.5, 0, 21)])
    order_id = service.convert_quote_to_order(quote_id, "2026-03-02")
    dn_id = service.create_delivery_note_from_order(order_id, "2026-03-03", {1: 2})
    inv_id = service.create_invoice_from_delivery_note(dn_id, "2026-03-04", "2026-03-10")

    # pago parcial
    with sqlite3.connect(db) as conn:
        due_id = conn.execute("SELECT id FROM invoice_due_dates WHERE invoice_id=?", (inv_id,)).fetchone()[0]
    service.register_payment(c1, "2026-03-05", 50.0, 101, inv_id, due_id)

    # marcar vencidas y listar
    changed = service.mark_overdue_invoices("2026-03-20")
    status = service.list_invoices_by_status()

    assert changed >= 1
    assert len(status["overdue"]) == 1
    assert status["overdue"][0]["id"] == inv_id

    # soft delete
    service.delete_product(p1)
    assert len(service.list_products()) == 0
    assert len(service.list_products(include_inactive=True)) == 1

    print("OK phase5-10-enhanced")


if __name__ == "__main__":
    main()
