#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "factura": {
        "template": ROOT / "pdf/templates/factura.html",
        "config": ROOT / "pdf/config/factura.layout.json",
        "cols": ["ref", "desc", "qty", "price", "disc", "vat", "total"],
    },
    "albaran": {
        "template": ROOT / "pdf/templates/albaran.html",
        "config": ROOT / "pdf/config/albaran.layout.json",
        "cols": ["ref", "desc", "qty", "unit"],
    },
    "presupuesto": {
        "template": ROOT / "pdf/templates/presupuesto.html",
        "config": ROOT / "pdf/config/presupuesto.layout.json",
        "cols": ["ref", "desc", "qty", "price", "disc", "vat", "total"],
    },
}

TOKENS = [
    "{{company.block}}",
    "{{customer.block}}",
    "{{lines_rows}}",
    "{{footer_text}}",
]




def check_reference_profile(errors: list[str]) -> None:
    profile_path = ROOT / "pdf/config/reference_profile.json"
    if not profile_path.exists():
        errors.append("[reference] falta pdf/config/reference_profile.json (ejecuta scripts/prepare_pdf_reference_profile.py)")
        return
    data = json.loads(profile_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "found" not in data:
        errors.append("[reference] profile inválido")

def validate() -> list[str]:
    errors: list[str] = []
    for name, cfg in REQUIRED.items():
        template = cfg["template"]
        layout = cfg["config"]

        if not template.exists():
            errors.append(f"[{name}] falta template: {template}")
            continue
        if not layout.exists():
            errors.append(f"[{name}] falta config: {layout}")
            continue

        content = template.read_text(encoding="utf-8")
        for token in TOKENS:
            if token not in content:
                errors.append(f"[{name}] token obligatorio ausente en html: {token}")

        data = json.loads(layout.read_text(encoding="utf-8"))
        for block in ("layout", "table"):
            if block not in data:
                errors.append(f"[{name}] bloque obligatorio ausente en config: {block}")

        if "table" in data:
            missing_cols = [c for c in cfg["cols"] if c not in data["table"]]
            if missing_cols:
                errors.append(f"[{name}] columnas sin ancho configurado: {', '.join(missing_cols)}")
            else:
                total = sum(float(data["table"][c]) for c in cfg["cols"])
                if abs(total - 100.0) > 0.001:
                    errors.append(f"[{name}] suma de columnas debe ser 100 y es {total}")

    check_reference_profile(errors)
    return errors


if __name__ == "__main__":
    errs = validate()
    if errs:
        print("ERRORS:")
        for err in errs:
            print(f" - {err}")
        sys.exit(1)
    print("OK: plantillas y configuración PDF consistentes")
