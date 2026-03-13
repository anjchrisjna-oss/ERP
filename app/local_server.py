#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.erp_service import ERPService, CustomerInput, ProductInput

UI_DIR = ROOT / "desktop_ui"
DB_PATH = Path(os.environ.get("ERP_DB_PATH", str(ROOT / "var" / "erp.sqlite3")))
service = ERPService(str(DB_PATH))


class ERPHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        rel = path.split("?", 1)[0].lstrip("/")
        if not rel:
            rel = "index.html"
        return str(UI_DIR / rel)

    def _json(self, data: dict | list, status: int = 200) -> None:
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/customers":
            include = parse_qs(parsed.query).get("include_inactive", ["0"])[0] == "1"
            self._json(service.list_customers(include_inactive=include))
            return
        if parsed.path == "/api/products":
            qs = parse_qs(parsed.query)
            include = qs.get("include_inactive", ["0"])[0] == "1"
            search = qs.get("search", [None])[0]
            self._json(service.list_products(include_inactive=include, search=search))
            return
        return super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            self._json({"error": "JSON inválido"}, status=400)
            return

        try:
            if parsed.path == "/api/customers":
                customer_id = service.create_customer(
                    CustomerInput(
                        customer_code=payload["customer_code"],
                        legal_name=payload["legal_name"],
                        tax_id=payload.get("tax_id"),
                        email=payload.get("email"),
                    )
                )
                self._json({"id": customer_id}, status=201)
                return

            if parsed.path == "/api/products":
                product_id = service.create_product(
                    ProductInput(
                        sku=payload["sku"],
                        name=payload["name"],
                        unit=payload["unit"],
                        base_price=float(payload["base_price"]),
                        default_vat_rate_id=payload.get("default_vat_rate_id"),
                    )
                )
                self._json({"id": product_id}, status=201)
                return

            self._json({"error": "Ruta no encontrada"}, status=404)
        except Exception as exc:
            self._json({"error": str(exc)}, status=422)


def run(port: int = 8765) -> None:
    UI_DIR.mkdir(exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", port), ERPHandler)
    print(f"ERP local server en http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    run(port)
