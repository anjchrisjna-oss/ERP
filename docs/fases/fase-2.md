# Fase 2 — Base del proyecto y arranque técnico

## Implementado
- Se crea base backend de escritorio en `src-tauri` con módulos de dominio.
- Se define punto de arranque (`main.rs`) y healthcheck.
- Se preparan reglas de negocio nucleares en Rust:
  - numeración de series
  - control de entrega/facturación parcial
  - cálculo fiscal por línea (base, cuota, total)
- Se deja estructura de frontend modular preparada para React+TS en `src/frontend/modules/*`.

## Archivos tocados
- `src-tauri/Cargo.toml`
- `src-tauri/src/main.rs`
- `src-tauri/src/app/*`
- `src-tauri/src/domain/*`
- `src/frontend/README.md`
- `src/frontend/modules/*/index.ts`

## Comandos ejecutados
- `cargo test`
- `cargo run`

## Validaciones superadas
- Tests unitarios de reglas críticas de numeración, parciales y cálculo fiscal.
- Arranque del ejecutable backend con salida de healthcheck `ok`.

## Estado
Fase 2 consistente y cerrada.
