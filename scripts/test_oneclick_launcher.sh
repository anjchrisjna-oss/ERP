#!/usr/bin/env bash
set -euo pipefail

PORT=8892
DB=/tmp/erp_oneclick_test.sqlite3
rm -f "$DB"

python3 app/start_erp.py "$PORT" "$DB" >/tmp/erp_oneclick_test.log 2>&1 &
PID=$!
trap 'kill $PID >/dev/null 2>&1 || true' EXIT
sleep 1

curl -s "http://127.0.0.1:$PORT/api/customers" | rg -q '^\[\]$'

echo "OK oneclick"
