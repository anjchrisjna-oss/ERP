# Fase 3 — Base de datos, migraciones y consistencia documental

## Implementado
- Se formaliza esquema SQLite en migraciones (`db/migrations/0001_init.sql`).
- Se añaden restricciones de negocio con triggers (`0002_business_constraints.sql`) para:
  - evitar servir por encima de pedido
  - evitar facturar por encima de servido
  - evitar asignar cobros por encima del importe cobrado
- Se crean scripts operativos de migración y validación de flujo documental.

## Archivos tocados
- `db/migrations/0001_init.sql`
- `db/migrations/0002_business_constraints.sql`
- `scripts/run_migrations.sh`
- `scripts/test_document_flow.sql`
- `scripts/validate_document_flow.sh`

## Comandos ejecutados
- `./scripts/run_migrations.sh /tmp/erp_phase3.sqlite3`
- `./scripts/validate_document_flow.sh /tmp/erp_flow.sqlite3`

## Validaciones superadas
- Migraciones aplicadas sin errores sobre SQLite real.
- Test de integridad documental validado: bloqueo de sobre-facturación por trigger.

## Estado
Fase 3 consistente y cerrada.
