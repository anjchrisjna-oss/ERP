# Fase 8 — Albaranes

## Implementado
- Generación de albarán desde pedido con cantidades parciales por línea.
- Validación para impedir servir por encima de la cantidad pendiente.
- Actualización de `served_quantity` por línea de pedido.
- Trazabilidad `order -> delivery_note` en `document_relations`.

## Archivos tocados
- `backend/erp_service.py`
- `scripts/test_phase8_10_delivery_invoice_payment.py`

## Comandos ejecutados
- `python3 scripts/test_phase8_10_delivery_invoice_payment.py`

## Validaciones superadas
- Albarán parcial emitido correctamente.
- Cantidad servida reflejada en pedido sin superar máximos.

## Estado
Fase 8 consistente y cerrada.
