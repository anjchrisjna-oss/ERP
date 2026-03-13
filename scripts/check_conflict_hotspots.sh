#!/usr/bin/env bash
set -euo pipefail

FILES=(
  README.md
  backend/erp_service.py
  docs/fases/fase-2.md
  docs/fases/fase-5.md
  docs/fases/fase-10.md
)

echo "== Comprobación de conflictos en archivos críticos =="
for f in "${FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "Falta archivo crítico: $f"
    exit 1
  fi
  if rg -n "^(<<<<<<<|=======|>>>>>>>)" "$f" >/dev/null; then
    echo "Marcadores de conflicto detectados en: $f"
    exit 1
  fi
  echo "OK $f"
done

echo "== Consistencia mínima de contenido =="
rg -n "Fase 2: base técnica \+ UI local conectada" README.md >/dev/null
rg -n "## Estado" docs/fases/fase-2.md >/dev/null
rg -n "PARCIAL" docs/fases/fase-2.md >/dev/null
rg -n "COMPLETA en backend y persistencia" docs/fases/fase-5.md >/dev/null
rg -n "COMPLETA en backend y persistencia" docs/fases/fase-10.md >/dev/null
rg -n "class ERPService" backend/erp_service.py >/dev/null

echo "OK conflict hotspots"
