#!/usr/bin/env bash
set -euo pipefail

DB_PATH="${1:-./var/erp.sqlite3}"
mkdir -p "$(dirname "$DB_PATH")"

sqlite3 "$DB_PATH" < db/migrations/0001_init.sql
sqlite3 "$DB_PATH" < db/migrations/0002_business_constraints.sql

echo "Migrations applied to $DB_PATH"
