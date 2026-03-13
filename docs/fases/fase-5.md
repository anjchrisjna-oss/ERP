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
Fase 5 consistente y cerrada.
