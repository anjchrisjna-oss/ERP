# Fase 1 — Arquitectura objetivo ERP escritorio (España)

## 1) Resumen ejecutivo

Se adopta arquitectura **local-first** con:

- **Desktop shell:** Tauri (Rust)
- **Frontend:** React + TypeScript + Vite
- **UI:** componentes reutilizables con estilo sobrio empresarial
- **Persistencia local:** SQLite
- **Acceso a datos y migraciones:** `sqlx` en backend Tauri (queries tipadas + migraciones versionadas)
- **Validación de datos:** Zod en frontend + validación de dominio en backend
- **PDF profesional:** motor de plantillas HTML/CSS renderizado a PDF por backend (wkhtmltopdf/Chromium headless encapsulado)

Esta opción prioriza mantenibilidad, rendimiento local, despliegue sencillo en Windows/Linux, y separación clara de capas.

---

## 2) Decisiones técnicas clave

1. **Tauri frente a Electron**
   - Menor consumo de memoria/CPU para uso diario intensivo en oficina.
   - Binarios más ligeros y arranque más rápido.

2. **Backend de dominio en Rust (Tauri commands)**
   - Reglas críticas (numeración, trazabilidad, facturación parcial, cobros) en backend para garantizar integridad.
   - Evita depender de lógica duplicada en UI.

3. **SQLite + sqlx**
   - Base de datos local robusta y madura para entorno monousuario.
   - Migraciones reproducibles en cada versión.

4. **Arquitectura modular por bounded contexts**
   - Módulos: clientes, productos, presupuestos, pedidos, albaranes, facturas, cobros, configuración, dashboard.
   - Cada módulo con DTOs, validación, repositorio y servicios de aplicación.

5. **Plantillas PDF separadas de negocio**
   - Dominio calcula importes e impuestos.
   - Capa de renderizado aplica plantilla y estilos.
   - Ajustes finos de márgenes/posiciones en archivos de plantilla sin tocar reglas de negocio.

---

## 3) Estructura de carpetas propuesta

```text
ERP/
  src-tauri/
    src/
      app/
        mod.rs
        state.rs
        errors.rs
      config/
        company_settings.rs
        document_series.rs
        vat_rates.rs
      modules/
        customers/
        products/
        quotes/
        orders/
        delivery_notes/
        invoices/
        payments/
        dashboard/
      pdf/
        templates/
        renderer/
      db/
        mod.rs
        pool.rs
        migrations.rs
      audit/
      commands/
    migrations/
      0001_init.sql
      0002_indexes.sql
      ...
    Cargo.toml
    tauri.conf.json

  src/
    app/
      router.tsx
      providers/
    ui/
      components/
      layout/
      tables/
      forms/
      feedback/
    modules/
      customers/
      products/
      quotes/
      orders/
      delivery-notes/
      invoices/
      payments/
      settings/
      dashboard/
    shared/
      api/
      validation/
      utils/
      types/
    styles/

  docs/
    arquitectura/
    db/
    pdf/

  assets/
    logo/
    pdf-templates/

  README.md
```

---

## 4) Flujo documental completo y trazabilidad

### Flujo principal

1. Cliente y artículos dados de alta.
2. Presupuesto (serie PRES) con líneas e IVA por línea.
3. Conversión opcional a pedido (serie PED).
4. Pedido puede servirse parcial o completo en uno o varios albaranes (serie ALB).
5. Factura (serie FAC) desde pedido o albarán, con control de cantidades facturables.
6. Generación de vencimientos según forma de pago.
7. Registro de cobros parciales/totales contra vencimientos/factura.

### Reglas de integridad (núcleo)

- No facturar cantidades superiores a las servidas (si origen albarán) o disponibles (si origen pedido).
- No servir cantidades superiores a las pendientes del pedido.
- Actualización automática de estados agregados (parcial/completo).
- Numeración por serie con bloqueo transaccional y registro de incidencias.
- Cada línea derivada mantiene referencia al documento y línea origen.

---

## 5) Modelo de datos (alto nivel)

Ver detalle SQL en `docs/db/schema-fase1.sql`.

Entidades nucleares:

- Configuración: `company_settings`, `app_settings`, `document_series`, `vat_rates`, `payment_methods`
- Maestros: `customers`, `products`
- Documentos: `quotes`, `quote_lines`, `orders`, `order_lines`, `delivery_notes`, `delivery_note_lines`, `invoices`, `invoice_lines`
- Cobros: `invoice_due_dates`, `payments`, `payment_allocations`
- Soporte: `document_relations`, `audit_logs`

---

## 6) Estrategia de validación y calidad

- **Frontend:** validación inmediata de formularios (obligatorios, formatos, rangos).
- **Backend:** validaciones de negocio y transacciones ACID.
- **Pruebas por fases:**
  - Unitarias para cálculos (bases, IVA, descuentos, saldos).
  - Integración para conversiones documentales y cobros parciales.
  - Smoke test de arranque Tauri y migraciones.

---

## 7) Gestión de IVA y fiscalidad española

- IVA configurable por línea y por artículo.
- Tipos editables desde configuración (`vat_rates`).
- Agrupación por tipo de IVA en factura para PDF.
- Cálculo explícito por línea: base, cuota, total, con redondeo bancario definido.
- Persistencia de snapshot fiscal en documento para trazabilidad histórica.

---

## 8) PDFs profesionales (preparación)

- Plantillas separadas por tipo: presupuesto, albarán, factura.
- Motor de render desacoplado del dominio.
- Variables de plantilla tipadas (cabecera, bloques, tabla líneas, totales, pie).
- Ajustes de layout en configuración de plantilla (márgenes, tamaños, offsets).

> Nota: actualmente no existen en el repositorio modelos reales en `docs/modelos/*` ni logo en `assets/logo/*`; en Fase 11 se incorporarán y se realizará ajuste visual fiel.

---

## 9) Plan de ejecución por fases (resumen)

- **Fase 2:** bootstrap Tauri + React + TypeScript con navegación y layout base.
- **Fase 3:** migraciones SQLite + repositorios + capa de servicios.
- **Fase 4:** configuración empresa/series/IVA.
- **Fases 5-10:** módulos funcionales (clientes, productos, presupuestos, pedidos, albaranes, facturas, cobros).
- **Fase 11:** PDFs basados en modelos reales.
- **Fase 12:** hardening UX, validaciones y pruebas.
- **Fase 13:** documentación operativa y backup.

