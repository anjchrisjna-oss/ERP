#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PORT="${1:-8765}"
DB_PATH="${2:-./var/erp.sqlite3}"

echo "Iniciando ERP local en http://127.0.0.1:${PORT}"
./scripts/run_local_erp.sh "$DB_PATH" "$PORT"
