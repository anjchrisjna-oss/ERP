#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "docs" / "modelos"
ASSETS = ROOT / "assets"
OUT = ROOT / "pdf" / "config" / "reference_profile.json"


def find_first(patterns: list[str], base: Path) -> str | None:
    for pattern in patterns:
        files = sorted(base.glob(pattern))
        if files:
            return str(files[0].relative_to(ROOT))
    return None


def main() -> int:
    profile = {
        "found": False,
        "models": {
            "factura": None,
            "albaran": None,
            "presupuesto": None,
        },
        "logo": None,
        "notes": [],
    }

    if MODELS.exists():
        profile["models"]["factura"] = find_first(["factura.*", "*factura*.*"], MODELS)
        profile["models"]["albaran"] = find_first(["albaran.*", "*albaran*.*"], MODELS)
        profile["models"]["presupuesto"] = find_first(["presupuesto.*", "*presupuesto*.*"], MODELS)

    if ASSETS.exists():
        profile["logo"] = find_first(["logo.*", "*logo*.*"], ASSETS)

    profile["found"] = any(v for v in profile["models"].values()) or bool(profile["logo"])

    if not profile["found"]:
        profile["notes"].append(
            "No se encontraron modelos/logo reales en docs/modelos y assets."
        )
    else:
        profile["notes"].append(
            "Se detectaron referencias reales para calibración PDF."
        )

    OUT.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"reference profile generado: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
