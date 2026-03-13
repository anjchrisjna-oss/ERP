# Fase 5 — Clientes y productos (ampliada)

## Implementado
- CRUD profesional de clientes:
  - alta (`create_customer`)
  - edición parcial (`update_customer`)
  - baja lógica (`delete_customer`)
  - listado (`list_customers`) con histórico agregado de presupuestos, pedidos, albaranes y facturas, e importe pendiente.
- CRUD profesional de productos:
  - alta (`create_product`)
  - edición parcial (`update_product`)
  - baja lógica (`delete_product`)
  - listado con filtro de búsqueda (`list_products`).
- Validaciones de negocio en entrada:
  - formato de código cliente
  - email básico
  - precio no negativo
- Registro en `audit_logs` para acciones críticas de clientes/productos.

## Archivos tocados
- `backend/erp_service.py`
- `scripts/test_phase5_10_enhanced.py`

## Comandos ejecutados
- `python3 scripts/test_phase5_10_enhanced.py`

## Validaciones superadas
- Alta, edición, listado y baja lógica de cliente/producto sobre SQLite real.
- Filtros de búsqueda operativos.
- Persistencia correcta de cambios y coherencia en listados.

## Estado
COMPLETA en backend y persistencia (SQLite), validada con integración real.
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
