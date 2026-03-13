# Fase 5 — Clientes y productos

## Implementado
- Se implementa servicio de aplicación (`backend/erp_service.py`) para:
  - alta de clientes con validación de código/email
  - alta de productos con validación de unidad y precio
  - cálculo de pendiente de cobro por cliente
- Se añade prueba ejecutable de integración para altas reales en SQLite.

## Archivos tocados
- `backend/erp_service.py`
- `scripts/test_phase5_customers_products.py`

## Comandos ejecutados
- `python3 scripts/test_phase5_customers_products.py`

## Validaciones superadas
- Inserción real de cliente y producto en SQLite.
- Verificación de persistencia por consulta directa.

## Estado
Fase 5 consistente y cerrada.
