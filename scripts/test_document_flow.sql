PRAGMA foreign_keys = ON;

INSERT INTO payment_methods(id, code, name, active) VALUES (1, 'TRANSFER', 'Transferencia', 1);
INSERT INTO vat_rates(id, code, name, rate, active, created_at, updated_at) VALUES (1, 'IVA21', 'IVA General', 21, 1, datetime('now'), datetime('now'));

INSERT INTO customers(id, customer_code, legal_name, created_at, updated_at)
VALUES (1, 'CLI0001', 'Cliente Industrial SL', datetime('now'), datetime('now'));

INSERT INTO products(id, sku, name, unit, base_price, default_vat_rate_id, created_at, updated_at)
VALUES (1, 'P-100', 'Pieza mecanizada', 'ud', 12.0, 1, datetime('now'), datetime('now'));

INSERT INTO document_series(id, doc_type, code, prefix, next_number, active)
VALUES
  (1, 'quote', 'PRES', 'PRES-2026', 1, 1),
  (2, 'order', 'PED', 'PED-2026', 1, 1),
  (3, 'delivery_note', 'ALB', 'ALB-2026', 1, 1),
  (4, 'invoice', 'FAC', 'FAC-2026', 1, 1);

INSERT INTO orders(id, series_id, number, full_number, customer_id, issue_date, status, subtotal, tax_total, total, created_at, updated_at)
VALUES (1, 2, 1, 'PED-2026-000001', 1, date('now'), 'confirmed', 120, 25.2, 145.2, datetime('now'), datetime('now'));

INSERT INTO order_lines(id, order_id, line_no, product_id, description, quantity, served_quantity, invoiced_quantity, unit_price, discount_pct, vat_rate, tax_base, tax_amount, line_total, created_at)
VALUES (1, 1, 1, 1, 'Pieza mecanizada', 10, 6, 4, 12, 0, 21, 120, 25.2, 145.2, datetime('now'));

-- debe fallar si supera servido
UPDATE order_lines SET invoiced_quantity = 7 WHERE id = 1;
