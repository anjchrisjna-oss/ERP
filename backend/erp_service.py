#!/usr/bin/env python3
from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Any


@dataclass
class CustomerInput:
    customer_code: str
    legal_name: str
    tax_id: str | None = None
    email: str | None = None


@dataclass
class ProductInput:
    sku: str
    name: str
    unit: str
    base_price: float
    default_vat_rate_id: int | None = None


@dataclass
class LineInput:
    product_id: int | None
    description: str
    quantity: float
    unit_price: float
    discount_pct: float
    vat_rate: float


class ERPService:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys=ON;")
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def _round2(value: float) -> float:
        return round(value + 1e-9, 2)

    def _now(self) -> str:
        return datetime.utcnow().isoformat()

    def _log(self, conn: sqlite3.Connection, entity_type: str, entity_id: int, action: str, payload: str | None = None) -> None:
        conn.execute(
            "INSERT INTO audit_logs(entity_type, entity_id, action, payload, created_at) VALUES(?, ?, ?, ?, ?)",
            (entity_type, entity_id, action, payload, self._now()),
        )

    def _next_series_number(self, conn: sqlite3.Connection, doc_type: str) -> tuple[int, int, str]:
        row = conn.execute(
            "SELECT id, prefix, next_number FROM document_series WHERE doc_type = ? AND active = 1 ORDER BY id LIMIT 1",
            (doc_type,),
        ).fetchone()
        if not row:
            raise ValueError(f"No existe serie activa para {doc_type}")
        series_id, prefix, next_number = int(row[0]), row[1], int(row[2])
        full_number = f"{prefix}-{next_number:06d}"
        conn.execute("UPDATE document_series SET next_number = next_number + 1 WHERE id = ?", (series_id,))
        return series_id, next_number, full_number

    # ------------------------
    # Fase 5: Clientes
    # ------------------------
    def create_customer(self, payload: CustomerInput) -> int:
        if not re.fullmatch(r"[A-Z0-9_-]{3,20}", payload.customer_code):
            raise ValueError("customer_code inválido")
        if payload.email and "@" not in payload.email:
            raise ValueError("email inválido")

        now = self._now()
        with self._conn() as conn:
            cur = conn.execute(
                "INSERT INTO customers(customer_code, legal_name, tax_id, email, active, created_at, updated_at) VALUES(?, ?, ?, ?, 1, ?, ?)",
                (payload.customer_code, payload.legal_name, payload.tax_id, payload.email, now, now),
            )
            customer_id = int(cur.lastrowid)
            self._log(conn, "customer", customer_id, "create", payload.customer_code)
            return customer_id

    def update_customer(self, customer_id: int, **fields: Any) -> None:
        allowed = {
            "legal_name",
            "trade_name",
            "tax_id",
            "address",
            "postal_code",
            "city",
            "province",
            "country",
            "phone",
            "email",
            "contact_person",
            "notes",
            "default_payment_method_id",
            "default_due_days",
            "bank_account",
        }
        if not fields:
            return
        unknown = set(fields.keys()) - allowed
        if unknown:
            raise ValueError(f"Campos no permitidos: {', '.join(sorted(unknown))}")
        if "email" in fields and fields["email"] and "@" not in str(fields["email"]):
            raise ValueError("email inválido")

        pairs = [f"{k} = ?" for k in fields.keys()]
        values = list(fields.values()) + [self._now(), customer_id]
        with self._conn() as conn:
            cur = conn.execute(
                f"UPDATE customers SET {', '.join(pairs)}, updated_at = ? WHERE id = ? AND active = 1",
                values,
            )
            if cur.rowcount == 0:
                raise ValueError("Cliente no encontrado o inactivo")
            self._log(conn, "customer", customer_id, "update", ",".join(fields.keys()))

    def delete_customer(self, customer_id: int) -> None:
        with self._conn() as conn:
            cur = conn.execute("UPDATE customers SET active = 0, updated_at = ? WHERE id = ? AND active = 1", (self._now(), customer_id))
            if cur.rowcount == 0:
                raise ValueError("Cliente no encontrado o ya inactivo")
            self._log(conn, "customer", customer_id, "soft_delete")

    def list_customers(self, include_inactive: bool = False) -> list[dict[str, Any]]:
        active_filter = "" if include_inactive else "WHERE c.active = 1"
        with self._conn() as conn:
            rows = conn.execute(
                f"""
                SELECT
                  c.id,
                  c.customer_code,
                  c.legal_name,
                  c.city,
                  c.tax_id,
                  c.email,
                  c.active,
                  COALESCE((SELECT COUNT(*) FROM quotes q WHERE q.customer_id = c.id), 0) as quotes_count,
                  COALESCE((SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id), 0) as orders_count,
                  COALESCE((SELECT COUNT(*) FROM delivery_notes d WHERE d.customer_id = c.id), 0) as delivery_notes_count,
                  COALESCE((SELECT COUNT(*) FROM invoices i WHERE i.customer_id = c.id), 0) as invoices_count,
                  COALESCE((SELECT SUM(i.amount_due) FROM invoices i WHERE i.customer_id = c.id AND i.status IN ('pending_payment','partially_paid','overdue')), 0) as pending_amount
                FROM customers c
                {active_filter}
                ORDER BY c.customer_code
                """
            ).fetchall()
            return [dict(r) for r in rows]

    # ------------------------
    # Fase 5: Productos
    # ------------------------
    def create_product(self, payload: ProductInput) -> int:
        if payload.base_price < 0:
            raise ValueError("base_price no puede ser negativo")
        if not payload.unit.strip():
            raise ValueError("unit es obligatorio")

        now = self._now()
        with self._conn() as conn:
            cur = conn.execute(
                "INSERT INTO products(sku, name, unit, base_price, default_vat_rate_id, active, created_at, updated_at) VALUES(?, ?, ?, ?, ?, 1, ?, ?)",
                (payload.sku, payload.name, payload.unit, payload.base_price, payload.default_vat_rate_id, now, now),
            )
            product_id = int(cur.lastrowid)
            self._log(conn, "product", product_id, "create", payload.sku)
            return product_id

    def update_product(self, product_id: int, **fields: Any) -> None:
        allowed = {"name", "description", "unit", "base_price", "default_vat_rate_id", "default_discount_pct", "notes"}
        if not fields:
            return
        unknown = set(fields.keys()) - allowed
        if unknown:
            raise ValueError(f"Campos no permitidos: {', '.join(sorted(unknown))}")
        if "base_price" in fields and float(fields["base_price"]) < 0:
            raise ValueError("base_price no puede ser negativo")

        pairs = [f"{k} = ?" for k in fields.keys()]
        values = list(fields.values()) + [self._now(), product_id]
        with self._conn() as conn:
            cur = conn.execute(
                f"UPDATE products SET {', '.join(pairs)}, updated_at = ? WHERE id = ? AND active = 1",
                values,
            )
            if cur.rowcount == 0:
                raise ValueError("Producto no encontrado o inactivo")
            self._log(conn, "product", product_id, "update", ",".join(fields.keys()))

    def delete_product(self, product_id: int) -> None:
        with self._conn() as conn:
            cur = conn.execute("UPDATE products SET active = 0, updated_at = ? WHERE id = ? AND active = 1", (self._now(), product_id))
            if cur.rowcount == 0:
                raise ValueError("Producto no encontrado o ya inactivo")
            self._log(conn, "product", product_id, "soft_delete")

    def list_products(self, include_inactive: bool = False, search: str | None = None) -> list[dict[str, Any]]:
        conditions = []
        params: list[Any] = []
        if not include_inactive:
            conditions.append("p.active = 1")
        if search:
            conditions.append("(p.sku LIKE ? OR p.name LIKE ? OR COALESCE(p.description, '') LIKE ?)")
            term = f"%{search}%"
            params.extend([term, term, term])

        where_sql = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        with self._conn() as conn:
            rows = conn.execute(
                f"""
                SELECT p.id, p.sku, p.name, p.description, p.unit, p.base_price, p.default_vat_rate_id, p.active
                FROM products p
                {where_sql}
                ORDER BY p.sku
                """,
                params,
            ).fetchall()
            return [dict(r) for r in rows]

    # ------------------------
    # Fases 6-10: flujo documental
    # ------------------------
    def create_quote(self, customer_id: int, issue_date: str, lines: Iterable[LineInput], valid_until: str | None = None) -> int:
        lines = list(lines)
        if not lines:
            raise ValueError("Un presupuesto requiere al menos una línea")

        now = self._now()
        with self._conn() as conn:
            series_id, number, full_number = self._next_series_number(conn, "quote")
            subtotal = 0.0
            tax_total = 0.0
            line_rows = []
            for idx, line in enumerate(lines, start=1):
                base = self._round2(line.quantity * line.unit_price * (1 - line.discount_pct / 100.0))
                tax_amount = self._round2(base * (line.vat_rate / 100.0))
                line_total = self._round2(base + tax_amount)
                subtotal += base
                tax_total += tax_amount
                line_rows.append((idx, line, base, tax_amount, line_total))

            subtotal = self._round2(subtotal)
            tax_total = self._round2(tax_total)
            total = self._round2(subtotal + tax_total)

            cur = conn.execute(
                "INSERT INTO quotes(series_id, number, full_number, customer_id, issue_date, valid_until, status, subtotal, tax_total, total, created_at, updated_at) VALUES(?, ?, ?, ?, ?, ?, 'draft', ?, ?, ?, ?, ?)",
                (series_id, number, full_number, customer_id, issue_date, valid_until, subtotal, tax_total, total, now, now),
            )
            quote_id = int(cur.lastrowid)

            for line_no, line, base, tax_amount, line_total in line_rows:
                conn.execute(
                    "INSERT INTO quote_lines(quote_id, line_no, product_id, description, quantity, unit_price, discount_pct, vat_rate, tax_base, tax_amount, line_total, created_at) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (quote_id, line_no, line.product_id, line.description, line.quantity, line.unit_price, line.discount_pct, line.vat_rate, base, tax_amount, line_total, now),
                )
            self._log(conn, "quote", quote_id, "create", full_number)
            return quote_id

    def convert_quote_to_order(self, quote_id: int, issue_date: str) -> int:
        now = self._now()
        with self._conn() as conn:
            quote = conn.execute("SELECT customer_id, subtotal, tax_total, total FROM quotes WHERE id = ?", (quote_id,)).fetchone()
            if not quote:
                raise ValueError("Presupuesto no encontrado")

            series_id, number, full_number = self._next_series_number(conn, "order")
            cur = conn.execute(
                "INSERT INTO orders(series_id, number, full_number, customer_id, issue_date, status, source_quote_id, subtotal, tax_total, total, created_at, updated_at) VALUES(?, ?, ?, ?, ?, 'confirmed', ?, ?, ?, ?, ?, ?)",
                (series_id, number, full_number, int(quote[0]), issue_date, quote_id, float(quote[1]), float(quote[2]), float(quote[3]), now, now),
            )
            order_id = int(cur.lastrowid)

            q_lines = conn.execute("SELECT id, line_no, product_id, description, quantity, unit_price, discount_pct, vat_rate, tax_base, tax_amount, line_total FROM quote_lines WHERE quote_id = ? ORDER BY line_no", (quote_id,)).fetchall()
            for ql in q_lines:
                conn.execute(
                    "INSERT INTO order_lines(order_id, line_no, product_id, source_quote_line_id, description, quantity, unit_price, discount_pct, vat_rate, tax_base, tax_amount, line_total, created_at) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (order_id, ql[1], ql[2], ql[0], ql[3], ql[4], ql[5], ql[6], ql[7], ql[8], ql[9], ql[10], now),
                )

            conn.execute("UPDATE quotes SET status = 'accepted', updated_at = ? WHERE id = ?", (now, quote_id))
            conn.execute("INSERT INTO document_relations(source_doc_type, source_doc_id, target_doc_type, target_doc_id, relation_type, created_at) VALUES('quote', ?, 'order', ?, 'conversion', ?)", (quote_id, order_id, now))
            self._log(conn, "order", order_id, "create_from_quote", str(quote_id))
            return order_id

    def create_delivery_note_from_order(self, order_id: int, issue_date: str, served_quantities: dict[int, float]) -> int:
        now = self._now()
        with self._conn() as conn:
            order = conn.execute("SELECT customer_id FROM orders WHERE id = ?", (order_id,)).fetchone()
            if not order:
                raise ValueError("Pedido no encontrado")

            series_id, number, full_number = self._next_series_number(conn, "delivery_note")
            cur = conn.execute(
                "INSERT INTO delivery_notes(series_id, number, full_number, customer_id, order_id, issue_date, status, created_at, updated_at) VALUES(?, ?, ?, ?, ?, ?, 'partial', ?, ?)",
                (series_id, number, full_number, int(order[0]), order_id, issue_date, now, now),
            )
            delivery_id = int(cur.lastrowid)

            lines = conn.execute("SELECT id, line_no, product_id, description, quantity, served_quantity, unit_price FROM order_lines WHERE order_id = ?", (order_id,)).fetchall()
            inserted_lines = 0
            for row in lines:
                line_id, line_no, product_id, desc, qty, served, unit_price = row
                serve_now = float(served_quantities.get(line_id, 0.0))
                if serve_now <= 0:
                    continue
                if served + serve_now > qty:
                    raise ValueError("Cantidad servida excede la pendiente del pedido")

                conn.execute(
                    "INSERT INTO delivery_note_lines(delivery_note_id, line_no, order_line_id, product_id, description, quantity, unit, created_at) VALUES(?, ?, ?, ?, ?, ?, 'ud', ?)",
                    (delivery_id, line_no, line_id, product_id, desc, serve_now, now),
                )
                conn.execute("UPDATE order_lines SET served_quantity = served_quantity + ? WHERE id = ?", (serve_now, line_id))
                inserted_lines += 1

            if inserted_lines == 0:
                raise ValueError("No se han indicado cantidades a servir")

            pending = conn.execute("SELECT COUNT(*) FROM order_lines WHERE order_id = ? AND served_quantity < quantity", (order_id,)).fetchone()[0]
            order_status = "partially_served" if pending > 0 else "fully_served"
            dn_status = "partial" if pending > 0 else "delivered"
            conn.execute("UPDATE orders SET status = ?, updated_at = ? WHERE id = ?", (order_status, now, order_id))
            conn.execute("UPDATE delivery_notes SET status = ?, updated_at = ? WHERE id = ?", (dn_status, now, delivery_id))

            conn.execute("INSERT INTO document_relations(source_doc_type, source_doc_id, target_doc_type, target_doc_id, relation_type, created_at) VALUES('order', ?, 'delivery_note', ?, 'fulfillment', ?)", (order_id, delivery_id, now))
            self._log(conn, "delivery_note", delivery_id, "create_from_order", str(order_id))
            return delivery_id

    def create_invoice_from_delivery_note(self, delivery_note_id: int, issue_date: str, due_date: str) -> int:
        now = self._now()
        with self._conn() as conn:
            dn = conn.execute("SELECT customer_id, order_id FROM delivery_notes WHERE id = ?", (delivery_note_id,)).fetchone()
            if not dn:
                raise ValueError("Albarán no encontrado")

            series_id, number, full_number = self._next_series_number(conn, "invoice")
            lines = conn.execute(
                """
                SELECT dnl.id, dnl.line_no, dnl.order_line_id, dnl.product_id, dnl.description, dnl.quantity,
                       ol.unit_price, ol.discount_pct, ol.vat_rate
                FROM delivery_note_lines dnl
                JOIN order_lines ol ON ol.id = dnl.order_line_id
                WHERE dnl.delivery_note_id = ?
                ORDER BY dnl.line_no
                """,
                (delivery_note_id,),
            ).fetchall()
            if not lines:
                raise ValueError("No hay líneas para facturar")

            subtotal = 0.0
            tax_total = 0.0
            normalized = []
            for ln in lines:
                qty, unit_price, discount_pct, vat_rate = float(ln[5]), float(ln[6]), float(ln[7]), float(ln[8])
                base = self._round2(qty * unit_price * (1 - discount_pct / 100.0))
                tax = self._round2(base * (vat_rate / 100.0))
                total = self._round2(base + tax)
                subtotal += base
                tax_total += tax
                normalized.append((ln, base, tax, total))

            subtotal = self._round2(subtotal)
            tax_total = self._round2(tax_total)
            grand_total = self._round2(subtotal + tax_total)

            cur = conn.execute(
                "INSERT INTO invoices(series_id, number, full_number, customer_id, issue_date, due_date, status, source_order_id, source_delivery_note_id, subtotal, tax_total, total, amount_paid, amount_due, created_at, updated_at) VALUES(?, ?, ?, ?, ?, ?, 'pending_payment', ?, ?, ?, ?, ?, 0, ?, ?, ?)",
                (series_id, number, full_number, int(dn[0]), issue_date, due_date, int(dn[1]), delivery_note_id, subtotal, tax_total, grand_total, grand_total, now, now),
            )
            invoice_id = int(cur.lastrowid)

            for ln, base, tax, total in normalized:
                conn.execute(
                    "INSERT INTO invoice_lines(invoice_id, line_no, source_order_line_id, source_delivery_line_id, product_id, description, quantity, unit_price, discount_pct, vat_rate, tax_base, tax_amount, line_total, created_at) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (invoice_id, ln[1], ln[2], ln[0], ln[3], ln[4], ln[5], ln[6], ln[7], ln[8], base, tax, total, now),
                )
                conn.execute("UPDATE order_lines SET invoiced_quantity = invoiced_quantity + ? WHERE id = ?", (ln[5], ln[2]))

            conn.execute("INSERT INTO invoice_due_dates(invoice_id, due_date, amount, amount_paid, status, created_at, updated_at) VALUES(?, ?, ?, 0, 'pending', ?, ?)", (invoice_id, due_date, grand_total, now, now))
            conn.execute("INSERT INTO document_relations(source_doc_type, source_doc_id, target_doc_type, target_doc_id, relation_type, created_at) VALUES('delivery_note', ?, 'invoice', ?, 'billing', ?)", (delivery_note_id, invoice_id, now))
            self._log(conn, "invoice", invoice_id, "create_from_delivery_note", str(delivery_note_id))
            return invoice_id

    # ------------------------
    # Fase 10: Cobros y vencimientos
    # ------------------------
    def register_payment(self, customer_id: int, payment_date: str, amount: float, payment_method_id: int, invoice_id: int, due_date_id: int) -> int:
        now = self._now()
        with self._conn() as conn:
            cur = conn.execute(
                "INSERT INTO payments(customer_id, payment_date, amount, payment_method_id, created_at) VALUES(?, ?, ?, ?, ?)",
                (customer_id, payment_date, amount, payment_method_id, now),
            )
            payment_id = int(cur.lastrowid)
            conn.execute(
                "INSERT INTO payment_allocations(payment_id, invoice_id, invoice_due_date_id, allocated_amount, created_at) VALUES(?, ?, ?, ?, ?)",
                (payment_id, invoice_id, due_date_id, amount, now),
            )

            conn.execute("UPDATE invoice_due_dates SET amount_paid = amount_paid + ?, status = CASE WHEN amount_paid + ? >= amount THEN 'paid' ELSE 'partial' END, updated_at = ? WHERE id = ?", (amount, amount, now, due_date_id))
            conn.execute("UPDATE invoices SET amount_paid = amount_paid + ?, amount_due = amount_due - ?, status = CASE WHEN amount_due - ? <= 0 THEN 'paid' ELSE 'partially_paid' END, updated_at = ? WHERE id = ?", (amount, amount, amount, now, invoice_id))
            self._log(conn, "payment", payment_id, "register", f"invoice:{invoice_id}")
            return payment_id

    def mark_overdue_invoices(self, as_of_date: str) -> int:
        now = self._now()
        with self._conn() as conn:
            cur_due = conn.execute(
                "UPDATE invoice_due_dates SET status='overdue', updated_at=? WHERE status IN ('pending','partial') AND due_date < ?",
                (now, as_of_date),
            )
            conn.execute(
                "UPDATE invoices SET status='overdue', updated_at=? WHERE status IN ('pending_payment','partially_paid') AND due_date < ?",
                (now, as_of_date),
            )
            return int(cur_due.rowcount)

    def list_invoices_by_status(self) -> dict[str, list[dict[str, Any]]]:
        result = {"pending": [], "overdue": [], "paid": []}
        with self._conn() as conn:
            pending_rows = conn.execute("SELECT id, full_number, customer_id, due_date, total, amount_due, status FROM invoices WHERE status IN ('pending_payment','partially_paid') ORDER BY due_date").fetchall()
            overdue_rows = conn.execute("SELECT id, full_number, customer_id, due_date, total, amount_due, status FROM invoices WHERE status='overdue' ORDER BY due_date").fetchall()
            paid_rows = conn.execute("SELECT id, full_number, customer_id, due_date, total, amount_due, status FROM invoices WHERE status='paid' ORDER BY due_date DESC").fetchall()
            result["pending"] = [dict(r) for r in pending_rows]
            result["overdue"] = [dict(r) for r in overdue_rows]
            result["paid"] = [dict(r) for r in paid_rows]
            return result

    def pending_amount_by_customer(self, customer_id: int) -> float:
        with self._conn() as conn:
            row = conn.execute("SELECT COALESCE(SUM(amount_due), 0) FROM invoices WHERE customer_id = ? AND status IN ('pending_payment','partially_paid','overdue')", (customer_id,)).fetchone()
            return float(row[0])
