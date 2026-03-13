INSERT INTO company_settings(
  id, business_name, tax_id, fiscal_address, postal_code, city, province, country,
  phone, email, logo_path, footer_text, default_payment_terms, created_at, updated_at
) VALUES (
  1, 'Tu Empresa S.L.', 'B00000000', 'Dirección fiscal', '00000', 'Ciudad', 'Provincia', 'España',
  '', '', 'assets/logo.png', 'Gracias por su confianza.', '30 días fecha factura', datetime('now'), datetime('now')
);

INSERT INTO vat_rates(id, code, name, rate, active, created_at, updated_at)
VALUES
  (101, 'IVA21', 'IVA General', 21, 1, datetime('now'), datetime('now')),
  (102, 'IVA10', 'IVA Reducido', 10, 1, datetime('now'), datetime('now')),
  (103, 'IVA4', 'IVA Superreducido', 4, 1, datetime('now'), datetime('now'));

INSERT INTO document_series(id, doc_type, code, description, prefix, year, next_number, active)
VALUES
  (101, 'quote', 'PRES', 'Serie presupuestos', 'PRES-2026', 2026, 1, 1),
  (102, 'delivery_note', 'ALB', 'Serie albaranes', 'ALB-2026', 2026, 1, 1),
  (103, 'invoice', 'FAC', 'Serie facturas', 'FAC-2026', 2026, 1, 1),
  (104, 'order', 'PED', 'Serie pedidos', 'PED-2026', 2026, 1, 1);

INSERT INTO payment_methods(id, code, name, active)
VALUES
  (101, 'TRANSFER', 'Transferencia', 1),
  (102, 'CASH', 'Efectivo', 1),
  (103, 'RECEIPT', 'Recibo domiciliado', 1);
