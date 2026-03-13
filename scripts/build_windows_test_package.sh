#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT/dist/windows"
PKG_DIR="$OUT_DIR/erp_local_win"
ZIP_PATH="$OUT_DIR/erp_local_win.zip"

rm -rf "$PKG_DIR" "$ZIP_PATH"
mkdir -p "$PKG_DIR"

cp -r "$ROOT/backend" "$PKG_DIR/"
cp -r "$ROOT/app" "$PKG_DIR/"
cp -r "$ROOT/desktop_ui" "$PKG_DIR/"
cp -r "$ROOT/db" "$PKG_DIR/"
cp -r "$ROOT/pdf" "$PKG_DIR/"
cp -r "$ROOT/scripts" "$PKG_DIR/"
cp "$ROOT/README.md" "$PKG_DIR/"
cp "$ROOT/WORKFLOW.md" "$PKG_DIR/"
cp -r "$ROOT/packaging/windows" "$PKG_DIR/packaging"

mkdir -p "$OUT_DIR"
(cd "$OUT_DIR" && zip -rq "$(basename "$ZIP_PATH")" "$(basename "$PKG_DIR")")

echo "$ZIP_PATH"
