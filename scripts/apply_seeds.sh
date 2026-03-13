#!/usr/bin/env bash
set -euo pipefail
DB_PATH="${1:-./var/erp.sqlite3}"
sqlite3 "$DB_PATH" < db/seeds/0001_fiscal_defaults.sql
echo "Seeds applied to $DB_PATH"
