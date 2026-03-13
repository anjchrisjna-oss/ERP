# Fase 10 — Vencimientos y cobros

## Implementado
- Registro de cobro parcial con asignación a vencimiento/factura.
- Actualización de `amount_paid`, `amount_due` y estado de factura.
- Actualización de estado del vencimiento (`pending`, `partial`, `paid`).
- Consulta de pendiente por cliente.

## Archivos tocados
- `backend/erp_service.py`
- `scripts/test_phase8_10_delivery_invoice_payment.py`

## Comandos ejecutados
- `python3 scripts/test_phase8_10_delivery_invoice_payment.py`

## Validaciones superadas
- Cobro parcial registrado y conciliado correctamente.
- Saldo pendiente por cliente calculado sin inconsistencias.

## Estado
Fase 10 consistente y cerrada.
