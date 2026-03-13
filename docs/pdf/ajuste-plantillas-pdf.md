# Ajuste fino de plantillas PDF (presupuesto, albarán, factura)

## Estado actual

Se ha implementado una capa de plantillas desacoplada en:

- `pdf/templates/*.html`
- `pdf/templates/base.css`
- `pdf/config/*.layout.json`

Esta estructura separa:

- **lógica de negocio** (cálculo de importes, impuestos y estados)
- **lógica de presentación** (posiciones, márgenes, columnas, tipografía y bloques)

## Parámetros retocables (sin tocar lógica de negocio)

### 1) Márgenes y tipografía por documento

Archivo: `pdf/config/<documento>.layout.json`, bloque `layout`.

- `margin_top`, `margin_right`, `margin_bottom`, `margin_left` (mm)
- `font_size_base` (px)
- `title_size` (px)

### 2) Anchos de columnas

Archivo: `pdf/config/<documento>.layout.json`, bloque `table`.

- Factura/presupuesto: `ref`, `desc`, `qty`, `price`, `disc`, `vat`, `total`
- Albarán: `ref`, `desc`, `qty`, `unit`

> La suma de columnas debe ser 100.

### 3) Estructura visual

Archivo: `pdf/templates/base.css`.

Zonas principales para ajustes milimétricos:

- `.top` (cabecera logo + bloque título)
- `.panel-grid` (bloques empresa/cliente)
- `.lines-table` (tabla de líneas)
- `.bottom-grid` (totales/observaciones/firma)
- `.footer` (pie)

### 4) Textos fijos

Archivos `pdf/templates/*.html`:

- títulos de secciones (`Empresa emisora`, `Cliente`, `Observaciones`, etc.)
- textos de firma en albarán
- etiquetas de metadatos

## Proceso recomendado de afinado visual

1. Ajustar `margin_*`.
2. Ajustar anchuras de columnas en `table`.
3. Ajustar alturas/espaciados en `base.css` (`--table-header-height`, `--line-row-height`, `--section-gap`).
4. Ajustar tipografía (`--font-family`, `font_size_base`, `title_size`).
5. Revisar pie y bloques de datos largos.

## Validación rápida

Ejecutar:

```bash
python3 scripts/validate_pdf_templates.py
```

Valida:

- existencia de plantillas y configs
- tokens obligatorios
- suma de anchos de columnas = 100

## Observación importante sobre modelos reales

Para una réplica visual 1:1 es imprescindible disponer en el repositorio de los modelos reales y el logo en rutas accesibles.
Actualmente, en este árbol no se detectan archivos en rutas tipo:

- `docs/modelos/factura.*`
- `docs/modelos/albaran.*`
- `docs/modelos/presupuesto.*`
- `assets/logo.*`

En cuanto se incorporen, el siguiente paso es calibrar medidas y estilos contra esos originales (superposición visual página a página).
