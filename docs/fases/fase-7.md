# Fase 7 — Pedidos (conversión desde presupuesto)

## Implementado
- Conversión de presupuesto a pedido con trazabilidad completa.
- Copia fiel de líneas de presupuesto a pedido.
- Actualización de estado del presupuesto a `accepted` tras conversión.
- Registro en `document_relations` con tipo `conversion`.

## Archivos tocados
- `backend/erp_service.py`
- `scripts/test_phase6_7_quotes_orders.py`

## Comandos ejecutados
- `python3 scripts/test_phase6_7_quotes_orders.py`

## Validaciones superadas
- Pedido generado con `source_quote_id` correcto.
- Importes de pedido equivalentes al presupuesto de origen.
- Relación documental almacenada y verificable.

## Estado
Fase 7 consistente y cerrada.
