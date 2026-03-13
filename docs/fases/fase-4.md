# Fase 4 — Configuración fiscal, series e IVA

## Implementado
- Se añaden semillas iniciales para configuración de empresa, IVA, series y métodos de cobro.
- Se crea script de aplicación de seeds reutilizable.

## Archivos tocados
- `db/seeds/0001_fiscal_defaults.sql`
- `scripts/apply_seeds.sh`

## Comandos ejecutados
- `./scripts/apply_seeds.sh /tmp/erp_phase4.sqlite3`
- `sqlite3 /tmp/erp_phase4.sqlite3 "select code,rate from vat_rates order by id;"`
- `sqlite3 /tmp/erp_phase4.sqlite3 "select doc_type,code,next_number from document_series order by id;"`

## Validaciones superadas
- Tipos de IVA insertados correctamente y consultables.
- Series documentales independientes por tipo presentes y activas.

## Estado
Fase 4 consistente y cerrada.
