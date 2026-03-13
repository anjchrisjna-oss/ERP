# Fase 2 — Base del proyecto y arranque técnico

## Estado
PARCIAL

## Qué estaba hecho
- Núcleo de reglas de dominio en Rust validado con tests.
- Estructura inicial de frontend por módulos.

## Qué faltaba
- Arranque usable de interfaz conectada a backend y SQLite.
- Flujo ejecutable para operar localmente con datos reales.

## Qué se ha terminado
- Implementada UI local en español (`desktop_ui/index.html`, `styles.css`, `app.js`) con:
  - menú lateral
  - vista de inicio
  - gestión básica de clientes
  - gestión básica de productos
- Implementado servidor local (`app/local_server.py`) conectado a `ERPService` + SQLite.
- Script de arranque local (`scripts/run_local_erp.sh`) para levantar base + servidor.
- Test de integración de fase 2 (`scripts/test_phase2_local_ui_api.sh`) para verificar API y persistencia reales.

## Validación real ejecutada
- `scripts/test_phase2_local_ui_api.sh`
- comprobaciones `curl` sobre endpoints `/api/customers` y `/api/products`

## Pendiente para cerrar COMPLETA
- Ejecutar la misma UI dentro de shell Tauri en entorno con dependencias de escritorio (GUI/WebView/Node) disponibles.
