# Fase 9 — Facturas

## Implementado
- Generación de factura desde albarán.
- Cálculo automático de bases, IVA y total desde líneas servidas.
- Alta de vencimiento inicial asociado a factura.
- Actualización de `invoiced_quantity` en líneas de pedido.
- Trazabilidad `delivery_note -> invoice`.

## Archivos tocados
- `backend/erp_service.py`
- `scripts/test_phase8_10_delivery_invoice_payment.py`

## Comandos ejecutados
- `python3 scripts/test_phase8_10_delivery_invoice_payment.py`

## Validaciones superadas
- Factura parcial consistente con albarán parcial.
- Importes fiscales calculados y persistidos correctamente.

## Estado
Fase 9 consistente y cerrada.
