#!/usr/bin/env python3
from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def apply_sql_file(db_path: Path, sql_file: Path) -> None:
    sql = sql_file.read_text(encoding="utf-8")
    with sqlite3.connect(db_path) as conn:
        conn.executescript(sql)


def ensure_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    apply_sql_file(db_path, ROOT / "db" / "migrations" / "0001_init.sql")
    apply_sql_file(db_path, ROOT / "db" / "migrations" / "0002_business_constraints.sql")

    with sqlite3.connect(db_path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM document_series").fetchone()[0]
    if count == 0:
        apply_sql_file(db_path, ROOT / "db" / "seeds" / "0001_fiscal_defaults.sql")


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    db_path = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "var" / "erp.sqlite3"

    ensure_db(db_path)
    os.environ["ERP_DB_PATH"] = str(db_path)
    os.execvp(sys.executable, [sys.executable, str(ROOT / "app" / "local_server.py"), str(port)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
