# Fase 11 — PDFs (base profesional y calibración)

## Implementado
- Sistema desacoplado de plantillas HTML/CSS para presupuesto, albarán y factura.
- Configuración editable por documento (márgenes, tipografía y columnas).
- Validación automatizada de consistencia de plantillas/config.
- Perfil de referencias reales `pdf/config/reference_profile.json` generado automáticamente por `scripts/prepare_pdf_reference_profile.py`.

## Archivos tocados
- `pdf/templates/*`
- `pdf/config/*`
- `scripts/validate_pdf_templates.py`
- `scripts/prepare_pdf_reference_profile.py`

## Comandos ejecutados
- `python3 scripts/prepare_pdf_reference_profile.py`
- `python3 scripts/validate_pdf_templates.py`

## Validaciones superadas
- Plantillas y configuración consistentes.
- Detección automática de modelos/logo operativa.

## Estado
Fase 11 cerrada en infraestructura de render.
En esta copia actual no existen archivos en `docs/modelos/*` ni `assets/*`, por lo que la calibración visual 1:1 queda pendiente de incorporar esos originales.
