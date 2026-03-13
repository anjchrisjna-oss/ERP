-- Fase 1 - Esquema lógico inicial ERP (SQLite)
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS company_settings (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  business_name TEXT NOT NULL,
  tax_id TEXT NOT NULL,
  fiscal_address TEXT NOT NULL,
  postal_code TEXT,
  city TEXT,
  province TEXT,
  country TEXT DEFAULT 'España',
  phone TEXT,
  email TEXT,
  logo_path TEXT,
  footer_text TEXT,
  default_payment_terms TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS app_settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS document_series (
  id INTEGER PRIMARY KEY,
  doc_type TEXT NOT NULL CHECK (doc_type IN ('quote','order','delivery_note','invoice')),
  code TEXT NOT NULL,
  description TEXT,
  prefix TEXT,
  year INTEGER,
  next_number INTEGER NOT NULL DEFAULT 1,
  active INTEGER NOT NULL DEFAULT 1,
  UNIQUE(doc_type, code)
);

CREATE TABLE IF NOT EXISTS vat_rates (
  id INTEGER PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  rate REAL NOT NULL,
  surcharge_rate REAL NOT NULL DEFAULT 0,
  active INTEGER NOT NULL DEFAULT 1,
  valid_from TEXT,
  valid_to TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS payment_methods (
  id INTEGER PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS customers (
  id INTEGER PRIMARY KEY,
  customer_code TEXT NOT NULL UNIQUE,
  legal_name TEXT NOT NULL,
  trade_name TEXT,
  tax_id TEXT,
  address TEXT,
  postal_code TEXT,
  city TEXT,
  province TEXT,
  country TEXT DEFAULT 'España',
  phone TEXT,
  email TEXT,
  contact_person TEXT,
  notes TEXT,
  default_payment_method_id INTEGER,
  default_due_days INTEGER,
  bank_account TEXT,
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (default_payment_method_id) REFERENCES payment_methods(id)
);

CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY,
  sku TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  description TEXT,
  unit TEXT NOT NULL,
  base_price REAL NOT NULL,
  default_vat_rate_id INTEGER,
  default_discount_pct REAL NOT NULL DEFAULT 0,
  active INTEGER NOT NULL DEFAULT 1,
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (default_vat_rate_id) REFERENCES vat_rates(id)
);

CREATE TABLE IF NOT EXISTS quotes (
  id INTEGER PRIMARY KEY,
  series_id INTEGER NOT NULL,
  number INTEGER NOT NULL,
  full_number TEXT NOT NULL UNIQUE,
  customer_id INTEGER NOT NULL,
  issue_date TEXT NOT NULL,
  valid_until TEXT,
  status TEXT NOT NULL CHECK (status IN ('draft','sent','accepted','rejected','expired')),
  subtotal REAL NOT NULL,
  tax_total REAL NOT NULL,
  total REAL NOT NULL,
  notes TEXT,
  terms TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (series_id) REFERENCES document_series(id),
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS quote_lines (
  id INTEGER PRIMARY KEY,
  quote_id INTEGER NOT NULL,
  line_no INTEGER NOT NULL,
  product_id INTEGER,
  description TEXT NOT NULL,
  quantity REAL NOT NULL,
  unit_price REAL NOT NULL,
  discount_pct REAL NOT NULL DEFAULT 0,
  vat_rate REAL NOT NULL,
  tax_base REAL NOT NULL,
  tax_amount REAL NOT NULL,
  line_total REAL NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (quote_id) REFERENCES quotes(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id),
  UNIQUE (quote_id, line_no)
);

CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY,
  series_id INTEGER NOT NULL,
  number INTEGER NOT NULL,
  full_number TEXT NOT NULL UNIQUE,
  customer_id INTEGER NOT NULL,
  issue_date TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft','confirmed','in_preparation','partially_served','fully_served','partially_invoiced','fully_invoiced')),
  source_quote_id INTEGER,
  subtotal REAL NOT NULL,
  tax_total REAL NOT NULL,
  total REAL NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (series_id) REFERENCES document_series(id),
  FOREIGN KEY (customer_id) REFERENCES customers(id),
  FOREIGN KEY (source_quote_id) REFERENCES quotes(id)
);

CREATE TABLE IF NOT EXISTS order_lines (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  line_no INTEGER NOT NULL,
  product_id INTEGER,
  source_quote_line_id INTEGER,
  description TEXT NOT NULL,
  quantity REAL NOT NULL,
  served_quantity REAL NOT NULL DEFAULT 0,
  invoiced_quantity REAL NOT NULL DEFAULT 0,
  unit_price REAL NOT NULL,
  discount_pct REAL NOT NULL DEFAULT 0,
  vat_rate REAL NOT NULL,
  tax_base REAL NOT NULL,
  tax_amount REAL NOT NULL,
  line_total REAL NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id),
  FOREIGN KEY (source_quote_line_id) REFERENCES quote_lines(id),
  UNIQUE (order_id, line_no)
);

CREATE TABLE IF NOT EXISTS delivery_notes (
  id INTEGER PRIMARY KEY,
  series_id INTEGER NOT NULL,
  number INTEGER NOT NULL,
  full_number TEXT NOT NULL UNIQUE,
  customer_id INTEGER NOT NULL,
  order_id INTEGER,
  issue_date TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending','delivered','partial','signed')),
  notes TEXT,
  signed_by TEXT,
  signed_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (series_id) REFERENCES document_series(id),
  FOREIGN KEY (customer_id) REFERENCES customers(id),
  FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE IF NOT EXISTS delivery_note_lines (
  id INTEGER PRIMARY KEY,
  delivery_note_id INTEGER NOT NULL,
  line_no INTEGER NOT NULL,
  order_line_id INTEGER,
  product_id INTEGER,
  description TEXT NOT NULL,
  quantity REAL NOT NULL,
  unit TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (delivery_note_id) REFERENCES delivery_notes(id) ON DELETE CASCADE,
  FOREIGN KEY (order_line_id) REFERENCES order_lines(id),
  FOREIGN KEY (product_id) REFERENCES products(id),
  UNIQUE (delivery_note_id, line_no)
);

CREATE TABLE IF NOT EXISTS invoices (
  id INTEGER PRIMARY KEY,
  series_id INTEGER NOT NULL,
  number INTEGER NOT NULL,
  full_number TEXT NOT NULL UNIQUE,
  customer_id INTEGER NOT NULL,
  issue_date TEXT NOT NULL,
  due_date TEXT,
  status TEXT NOT NULL CHECK (status IN ('draft','issued','pending_payment','partially_paid','paid','overdue','cancelled')),
  source_order_id INTEGER,
  source_delivery_note_id INTEGER,
  subtotal REAL NOT NULL,
  tax_total REAL NOT NULL,
  total REAL NOT NULL,
  amount_paid REAL NOT NULL DEFAULT 0,
  amount_due REAL NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (series_id) REFERENCES document_series(id),
  FOREIGN KEY (customer_id) REFERENCES customers(id),
  FOREIGN KEY (source_order_id) REFERENCES orders(id),
  FOREIGN KEY (source_delivery_note_id) REFERENCES delivery_notes(id)
);

CREATE TABLE IF NOT EXISTS invoice_lines (
  id INTEGER PRIMARY KEY,
  invoice_id INTEGER NOT NULL,
  line_no INTEGER NOT NULL,
  source_order_line_id INTEGER,
  source_delivery_line_id INTEGER,
  product_id INTEGER,
  description TEXT NOT NULL,
  quantity REAL NOT NULL,
  unit_price REAL NOT NULL,
  discount_pct REAL NOT NULL DEFAULT 0,
  vat_rate REAL NOT NULL,
  tax_base REAL NOT NULL,
  tax_amount REAL NOT NULL,
  line_total REAL NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
  FOREIGN KEY (source_order_line_id) REFERENCES order_lines(id),
  FOREIGN KEY (source_delivery_line_id) REFERENCES delivery_note_lines(id),
  FOREIGN KEY (product_id) REFERENCES products(id),
  UNIQUE (invoice_id, line_no)
);

CREATE TABLE IF NOT EXISTS invoice_due_dates (
  id INTEGER PRIMARY KEY,
  invoice_id INTEGER NOT NULL,
  due_date TEXT NOT NULL,
  amount REAL NOT NULL,
  amount_paid REAL NOT NULL DEFAULT 0,
  status TEXT NOT NULL CHECK (status IN ('pending','partial','paid','overdue')),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS payments (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  payment_date TEXT NOT NULL,
  amount REAL NOT NULL,
  payment_method_id INTEGER,
  reference TEXT,
  notes TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id),
  FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id)
);

CREATE TABLE IF NOT EXISTS payment_allocations (
  id INTEGER PRIMARY KEY,
  payment_id INTEGER NOT NULL,
  invoice_id INTEGER NOT NULL,
  invoice_due_date_id INTEGER,
  allocated_amount REAL NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (payment_id) REFERENCES payments(id) ON DELETE CASCADE,
  FOREIGN KEY (invoice_id) REFERENCES invoices(id),
  FOREIGN KEY (invoice_due_date_id) REFERENCES invoice_due_dates(id)
);

CREATE TABLE IF NOT EXISTS document_relations (
  id INTEGER PRIMARY KEY,
  source_doc_type TEXT NOT NULL,
  source_doc_id INTEGER NOT NULL,
  source_line_id INTEGER,
  target_doc_type TEXT NOT NULL,
  target_doc_id INTEGER NOT NULL,
  target_line_id INTEGER,
  relation_type TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id INTEGER PRIMARY KEY,
  entity_type TEXT NOT NULL,
  entity_id INTEGER NOT NULL,
  action TEXT NOT NULL,
  payload TEXT,
  created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_quotes_customer ON quotes(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_delivery_notes_customer ON delivery_notes(customer_id);
CREATE INDEX IF NOT EXISTS idx_invoices_customer ON invoices(customer_id);
CREATE INDEX IF NOT EXISTS idx_invoice_due_dates_status ON invoice_due_dates(status, due_date);
CREATE INDEX IF NOT EXISTS idx_payments_customer ON payments(customer_id, payment_date);
CREATE INDEX IF NOT EXISTS idx_document_relations_source ON document_relations(source_doc_type, source_doc_id);
CREATE INDEX IF NOT EXISTS idx_document_relations_target ON document_relations(target_doc_type, target_doc_id);
