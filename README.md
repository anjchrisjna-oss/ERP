# ERP Escritorio PyME Industrial (España)

Proyecto ERP local-first para ciclo comercial completo: presupuestos, pedidos, albaranes, facturas, vencimientos, cobros y PDFs profesionales.

## Estado actual por fases

- Fase 1: arquitectura y esquema base ✅
- Fase 2: base técnica + UI local conectada (PARCIAL, pendiente shell Tauri completo) ⚠️
- Fase 2: base técnica backend y estructura frontend ✅
- Fase 3: migraciones y reglas de integridad ✅
- Fase 4: configuración fiscal inicial (IVA/series) ✅
- Fase 5: clientes y productos (servicio base) ✅
- Fase 6: presupuestos ✅
- Fase 7: pedidos y conversión ✅
- Fase 8: albaranes parciales ✅
- Fase 9: facturas desde albarán ✅
- Fase 10: vencimientos y cobros ✅
- Fase 11: capa PDF desacoplada y afinable ✅
- Fase 12: validaciones y hardening técnico ✅
- Fase 13: documentación operativa ✅

## Requisitos

- Python 3.10+
- SQLite3 CLI
- Rust + Cargo (para core de dominio en `src-tauri`)

## Arranque técnico

### 1) Aplicar migraciones

```bash
./scripts/run_migrations.sh ./var/erp.sqlite3
```

### 2) Cargar datos fiscales iniciales (IVA, series, métodos de cobro)

```bash
./scripts/apply_seeds.sh ./var/erp.sqlite3
```

### 3) Validar reglas de negocio críticas

```bash
./scripts/validate_document_flow.sh /tmp/erp_flow.sqlite3
python3 scripts/test_phase5_customers_products.py
python3 scripts/test_phase6_7_quotes_orders.py
python3 scripts/test_phase8_10_delivery_invoice_payment.py
```

### 4) Arrancar interfaz local (UI en español + API + SQLite)

```bash
./scripts/run_local_erp.sh ./var/erp.sqlite3 8765
```

Abrir en navegador local: `http://127.0.0.1:8765`

Verificación automática mínima:

```bash
./scripts/test_phase2_local_ui_api.sh
```

### 5) Validar plantillas PDF
### 4) Validar plantillas PDF

```bash
python3 scripts/validate_pdf_templates.py
```

## Uso básico de la capa de servicios

Archivo: `backend/erp_service.py`

Funciones principales:
- `create_customer(...)`
- `create_product(...)`
- `create_quote(...)`
- `convert_quote_to_order(...)`
- `create_delivery_note_from_order(...)`
- `create_invoice_from_delivery_note(...)`
- `register_payment(...)`
- `pending_amount_by_customer(...)`

## Estructura clave

- `src-tauri/`: núcleo Rust de reglas de dominio
- `db/migrations/`: esquema y restricciones de integridad
- `db/seeds/`: configuración inicial fiscal
- `backend/`: servicios de aplicación sobre SQLite
- `pdf/templates/`: plantillas HTML/CSS desacopladas
- `pdf/config/`: ajuste de márgenes y columnas por documento
- `docs/fases/`: cierre y trazabilidad de cada fase

## Ajuste de PDFs

- Plantillas: `pdf/templates/*.html`
- Estilos base: `pdf/templates/base.css`
- Ajustes por documento: `pdf/config/*.layout.json`

Sube tus modelos de referencia en:
- `docs/modelos/factura.*`
- `docs/modelos/albaran.*`
- `docs/modelos/presupuesto.*`
- `assets/logo.*`

## Copia de seguridad de base de datos

### Backup manual

```bash
mkdir -p backup
cp ./var/erp.sqlite3 ./backup/erp_$(date +%F_%H%M%S).sqlite3
```

### Restauración

```bash
cp ./backup/erp_YYYY-MM-DD_HHMMSS.sqlite3 ./var/erp.sqlite3
```

## Notas

- Existe una UI local usable en español (`desktop_ui/*`) conectada a backend+SQLite.
- Queda pendiente empaquetar/validar esa UI dentro de shell Tauri completo en este entorno.
- El núcleo de reglas de negocio y trazabilidad documental está implementado y validado con pruebas reales sobre SQLite.
- El frontend React+Tauri está estructurado pero pendiente de bootstrap con registry npm/mirror disponible.
- El núcleo de reglas de negocio y trazabilidad documental ya está implementado y validado con pruebas reales sobre SQLite.
