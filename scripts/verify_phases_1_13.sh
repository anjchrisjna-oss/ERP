#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== Verificación secuencial fases 1 -> 13 =="

# Fase 1
echo "[Fase 1] Auditoría arquitectura y materiales"
./scripts/phase1_audit.sh

# Fase 2
echo "[Fase 2] Núcleo técnico (Rust)"
(cd src-tauri && cargo test)

# Fase 3
echo "[Fase 3] Migraciones y restricciones"
./scripts/run_migrations.sh /tmp/erp_fase3_verify.sqlite3 >/dev/null
./scripts/validate_document_flow.sh /tmp/erp_fase3_flow_verify.sqlite3

# Fase 4
echo "[Fase 4] Configuración fiscal inicial"
./scripts/run_migrations.sh /tmp/erp_fase4_verify.sqlite3 >/dev/null
./scripts/apply_seeds.sh /tmp/erp_fase4_verify.sqlite3 >/dev/null
sqlite3 /tmp/erp_fase4_verify.sqlite3 "SELECT code, rate FROM vat_rates ORDER BY id;"
sqlite3 /tmp/erp_fase4_verify.sqlite3 "SELECT doc_type, code, next_number FROM document_series ORDER BY id;"

# Fase 5
echo "[Fase 5] Clientes y productos"
python3 scripts/test_phase5_customers_products.py

# Fase 6
echo "[Fase 6] Presupuestos"
python3 scripts/test_phase6_7_quotes_orders.py

# Fase 7
echo "[Fase 7] Pedidos"
python3 scripts/test_phase6_7_quotes_orders.py

# Fase 8
echo "[Fase 8] Albaranes"
python3 scripts/test_phase8_10_delivery_invoice_payment.py

# Fase 9
echo "[Fase 9] Facturas"
python3 scripts/test_phase8_10_delivery_invoice_payment.py

# Fase 10
echo "[Fase 10] Cobros y vencimientos"
python3 scripts/test_phase5_10_enhanced.py

# Fase 11
echo "[Fase 11] PDFs"
python3 scripts/validate_pdf_templates.py
./scripts/check_reference_assets.sh

# Fase 12
echo "[Fase 12] Calidad técnica"
python3 -m py_compile backend/erp_service.py scripts/test_phase5_customers_products.py scripts/test_phase6_7_quotes_orders.py scripts/test_phase8_10_delivery_invoice_payment.py scripts/test_phase5_10_enhanced.py
(cd src-tauri && cargo fmt --check)

# Fase 13
echo "[Fase 13] Documentación operativa"
rg -n "run_migrations|apply_seeds|backup|restaur" README.md

echo "== Verificación completa OK =="
