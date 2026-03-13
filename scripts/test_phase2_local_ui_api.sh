#!/usr/bin/env bash
set -euo pipefail

DB_PATH="/tmp/erp_phase2_ui.sqlite3"
PORT="8878"

rm -f "$DB_PATH"

./scripts/run_migrations.sh "$DB_PATH" >/dev/null
./scripts/apply_seeds.sh "$DB_PATH" >/dev/null

ERP_DB_PATH="$DB_PATH" python3 app/local_server.py "$PORT" >/tmp/erp_phase2_ui_server.log 2>&1 &
PID=$!
trap 'kill $PID >/dev/null 2>&1 || true' EXIT
sleep 1

curl -s "http://127.0.0.1:$PORT/api/customers" | rg -q '^\[\]$'

curl -s -X POST "http://127.0.0.1:$PORT/api/customers" \
  -H 'Content-Type: application/json' \
  -d '{"customer_code":"CLI900","legal_name":"Cliente Interfaz","email":"cli@ui.es"}' | rg -q '"id"'

curl -s "http://127.0.0.1:$PORT/api/customers" | rg -q 'Cliente Interfaz'

curl -s -X POST "http://127.0.0.1:$PORT/api/products" \
  -H 'Content-Type: application/json' \
  -d '{"sku":"UI-P1","name":"Producto Interfaz","unit":"ud","base_price":9.99,"default_vat_rate_id":101}' | rg -q '"id"'

curl -s "http://127.0.0.1:$PORT/api/products" | rg -q 'Producto Interfaz'

echo "OK phase2-local-ui-api"
