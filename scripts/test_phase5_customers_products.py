#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.erp_service import ERPService, CustomerInput, ProductInput
import sqlite3
import subprocess
import tempfile
from pathlib import Path


def main() -> None:
    tmp_db = Path(tempfile.gettempdir()) / "erp_phase5.sqlite3"
    if tmp_db.exists():
        tmp_db.unlink()

    subprocess.run(["./scripts/run_migrations.sh", str(tmp_db)], check=True)
    subprocess.run(["./scripts/apply_seeds.sh", str(tmp_db)], check=True)

    service = ERPService(str(tmp_db))
    customer_id = service.create_customer(CustomerInput(customer_code="CLI_500", legal_name="Metalúrgica Norte S.L.", email="compras@metalurgica.es"))
    product_id = service.create_product(ProductInput(sku="ART-001", name="Pletina cortada", unit="ud", base_price=23.5, default_vat_rate_id=101))

    assert customer_id > 0
    assert product_id > 0

    with sqlite3.connect(tmp_db) as conn:
      c = conn.execute("SELECT customer_code, legal_name FROM customers WHERE id = ?", (customer_id,)).fetchone()
      p = conn.execute("SELECT sku, base_price FROM products WHERE id = ?", (product_id,)).fetchone()

    assert c == ("CLI_500", "Metalúrgica Norte S.L.")
    assert p == ("ART-001", 23.5)
    print("OK phase5")


if __name__ == "__main__":
    main()
