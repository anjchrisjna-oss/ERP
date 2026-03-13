# Fase 1 — Análisis real del proyecto, arquitectura final y plan secuencial

## 1) Estado actual detectado del repositorio

El proyecto ya dispone de una base técnica previa con:

- esquema SQL y migraciones (`db/migrations/*`)
- servicios de dominio/aplicación en Python (`backend/erp_service.py`)
- núcleo de reglas en Rust (`src-tauri/src/domain/*`)
- plantillas PDF desacopladas (`pdf/templates/*`, `pdf/config/*`)
- scripts de validación y pruebas de integración (`scripts/*`)
- documentación por fases (`docs/fases/*`)

Conclusión: existe una base sólida de lógica de negocio y persistencia, pero la parte de aplicación de escritorio UI (Tauri + React) no está todavía funcional como producto final de uso diario.

---

## 2) Revisión de materiales de referencia para PDF (crítico)

Rutas solicitadas:

- `docs/modelos/factura.*`
- `docs/modelos/albaran.*`
- `docs/modelos/presupuesto.*`
- `assets/logo.*`

En el estado actual del repositorio **no se detectan aún esos archivos**. Sin esos modelos reales no es posible calibrar fidelidad visual 1:1 por superposición.

Decisión técnica: mantener la capa de plantillas desacoplada ya implementada y dejar un flujo de calibración explícito para aplicar en cuanto se suban los originales.

---

## 3) Arquitectura final adoptada (producción)

Se mantiene la arquitectura objetivo solicitada por defecto:

- **Desktop shell:** Tauri
- **Frontend:** React + TypeScript
- **Persistencia local:** SQLite
- **Servicios de negocio y trazabilidad:** capa backend transaccional
- **PDF:** plantillas desacopladas + configuración visual editable

### Justificación breve

- local-first, rendimiento alto y operación en equipos de oficina/fábrica
- reglas críticas de negocio centralizadas y testeables
- mantenimiento a largo plazo por modularidad y separación de capas

---

## 4) Estructura modular objetivo (validada sobre el estado actual)

- `db/migrations/`: esquema y restricciones
- `db/seeds/`: configuración fiscal inicial
- `backend/`: casos de uso de negocio
- `pdf/templates/` + `pdf/config/`: render y ajuste visual
- `src-tauri/src/domain/`: reglas puras de dominio
- `src/frontend/modules/`: módulos funcionales UI en español

---

## 5) Flujo documental y trazabilidad obligatoria

Flujo objetivo y ya parcialmente implementado:

1. Cliente/producto
2. Presupuesto
3. Conversión a pedido
4. Albarán parcial/completo desde pedido
5. Factura desde pedido/albarán
6. Vencimientos
7. Cobros parciales/totales

Trazabilidad requerida:

- presupuesto -> pedido
- pedido -> albarán
- pedido/albarán -> factura
- factura -> cobros

---

## 6) Riesgos detectados en Fase 1

1. Falta de modelos reales PDF y logo en el repositorio (bloquea fidelidad 1:1).
2. Frontend Tauri+React no inicializado completamente en este entorno por restricción de acceso al registry npm.
3. Necesidad de endurecer UX y capa de presentación para uso intensivo diario.

---

## 7) Plan secuencial de ejecución desde este punto

- **Fase 2:** consolidar bootstrap de escritorio (cuando haya acceso a dependencias o mirror), manteniendo backend actual.
- **Fase 3-10:** endurecer módulos y endpoints de negocio con cobertura de tests y estados completos.
- **Fase 11:** calibración visual PDF contra modelos reales y logo.
- **Fase 12:** UX profesional en español y manejo de errores.
- **Fase 13:** documentación operativa final y despliegue local.

---

## 8) Cierre de Fase 1

### Qué se ha implementado
- Auditoría arquitectónica y de estado real del repositorio.
- Definición explícita de arquitectura final y riesgos/bloqueos reales.
- Plan secuencial técnico para continuar sin perder consistencia.

### Archivos tocados
- `docs/fases/fase-1.md`

### Comandos ejecutados
- inventario de archivos del proyecto
- comprobación de rutas de referencia PDF/logo

### Validaciones pasadas
- consistencia entre arquitectura declarada, estructura actual y flujo documental
- identificación explícita de bloqueos reales para fidelidad PDF 1:1
