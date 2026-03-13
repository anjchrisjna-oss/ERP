# Fase 10 — Vencimientos y cobros (ampliada)

## Implementado
- Registro de cobro parcial con aplicación a factura y vencimiento (`register_payment`).
- Marcado automático de vencidas por fecha de corte (`mark_overdue_invoices`).
- Listados operativos por estado (`list_invoices_by_status`):
  - pendientes
  - vencidas
  - cobradas
- Consulta de pendiente por cliente (`pending_amount_by_customer`).
- Registro en auditoría para cobros.

## Archivos tocados
- `backend/erp_service.py`
- `scripts/test_phase5_10_enhanced.py`

## Comandos ejecutados
- `python3 scripts/test_phase5_10_enhanced.py`

## Validaciones superadas
- Factura parcial marcada como vencida al superar fecha de vencimiento.
- Listado por estado devuelve resultados coherentes.
- Saldo pendiente actualizado correctamente tras cobro parcial.

## Estado
COMPLETA en backend y persistencia (SQLite), validada con integración real.
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
