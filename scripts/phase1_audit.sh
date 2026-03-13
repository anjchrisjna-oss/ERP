#!/usr/bin/env bash
set -euo pipefail

echo "== Auditoría Fase 1 =="
echo "Repositorio: $(pwd)"

echo
echo "[1] Estado de componentes clave"
for p in db/migrations backend pdf/templates pdf/config src-tauri/src/domain src/frontend/modules; do
  if [[ -d "$p" ]]; then
    echo " - OK  $p"
  else
    echo " - MISS $p"
  fi
done

echo
echo "[2] Referencias PDF/logo (modelos reales)"
found=0
for g in "docs/modelos/factura" "docs/modelos/albaran" "docs/modelos/presupuesto" "assets/logo"; do
  hits=$(find . -maxdepth 5 -type f | rg "$g" || true)
  if [[ -n "$hits" ]]; then
    echo "$hits"
    found=1
  fi
done
if [[ $found -eq 0 ]]; then
  echo " - No se han encontrado modelos/logo en rutas esperadas."
fi

echo
echo "[3] Toolchain"
python3 -V
sqlite3 --version | awk '{print $1, $2}'
cargo -V
npm -v || true
