#!/usr/bin/env bash
set -euo pipefail

DB_PATH="${1:-/tmp/erp_flow_test.sqlite3}"
rm -f "$DB_PATH"

./scripts/run_migrations.sh "$DB_PATH" >/dev/null

set +e
OUTPUT=$(sqlite3 "$DB_PATH" < scripts/test_document_flow.sql 2>&1)
STATUS=$?
set -e

if [[ $STATUS -eq 0 ]]; then
  echo "Expected business constraint failure but SQL finished OK"
  exit 1
fi

echo "$OUTPUT" | rg -q "invoiced_quantity no puede superar served_quantity"
echo "Business constraint check OK"
