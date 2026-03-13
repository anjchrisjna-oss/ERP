#!/usr/bin/env bash
set -euo pipefail

DB_PATH="${1:-./var/erp.sqlite3}"
PORT="${2:-8765}"

./scripts/run_migrations.sh "$DB_PATH" >/dev/null
if [[ "${SEED_IF_EMPTY:-1}" == "1" ]]; then
  set +e
  sqlite3 "$DB_PATH" "select count(*) from document_series;" >/tmp/erp_seed_check.txt 2>/dev/null
  status=$?
  set -e
  if [[ $status -eq 0 ]] && [[ "$(cat /tmp/erp_seed_check.txt)" == "0" ]]; then
    ./scripts/apply_seeds.sh "$DB_PATH" >/dev/null
  fi
fi

ERP_DB_PATH="$DB_PATH" python3 app/local_server.py "$PORT"
