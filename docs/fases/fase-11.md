# Fase 11 — PDFs (base profesional y calibración)

## Implementado
- Sistema desacoplado de plantillas HTML/CSS para presupuesto, albarán y factura.
- Configuración editable por documento (márgenes, tipografía y columnas).
- Validación automatizada de consistencia de plantillas/config.

## Archivos tocados
- `pdf/templates/*`
- `pdf/config/*`
- `docs/pdf/ajuste-plantillas-pdf.md`
- `scripts/validate_pdf_templates.py`
- `scripts/check_reference_assets.sh`

## Comandos ejecutados
- `python3 scripts/validate_pdf_templates.py`
- `./scripts/check_reference_assets.sh`

## Validaciones superadas
- Plantillas y configuración consistentes.
- Sistema de descubrimiento de modelos funcionando.

## Estado
Fase 11 cerrada en cuanto a infraestructura de render.
Para réplica visual 1:1 falta incorporar modelos reales y logo en `docs/modelos/*` y `assets/logo.*`.
