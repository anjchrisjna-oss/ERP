# AGENTS.md

## Propósito del proyecto
Este repositorio es para desarrollar un **software de escritorio profesional**, en **español**, para gestionar:

- presupuestos
- pedidos
- albaranes
- facturas
- clientes
- productos
- vencimientos
- cobros
- series documentales
- generación de PDFs profesionales

No es una demo. Es un producto real para uso diario en empresa.

---

## Prioridades absolutas
Cuando trabajes en este repositorio, prioriza en este orden:

1. **Corrección funcional**
2. **Mantenibilidad**
3. **Fidelidad documental**
4. **Experiencia de uso**
5. **Rendimiento razonable**
6. **Escalabilidad futura**

Nunca sacrifiques corrección o trazabilidad por rapidez.

---

## Requisitos de producto no negociables
- Aplicación de **escritorio**
- Interfaz **totalmente en español**
- Pensada para **uso local** en ordenadores de fábrica y personales
- No es multiusuario por ahora
- Debe incluir lógica fiscal orientada a **España**
- El **IVA debe ser configurable**
- Debe existir gestión de **series independientes**
- Debe existir gestión de **vencimientos y cobros**
- Los PDFs deben parecerse **lo máximo posible** a los modelos reales aportados
- Debe poder incorporar el **logo corporativo**

---

## Arquitectura preferida
Salvo justificación técnica fuerte, usa esta base:

- **Tauri** para escritorio
- **React + TypeScript** para interfaz
- **SQLite** como base de datos local
- Arquitectura modular
- Validación de datos
- Lógica de negocio separada de la UI
- Lógica de PDFs separada de la lógica de negocio

Si propones otro stack, debes justificar claramente por qué mejora esta opción para este caso.

---

## Idioma y estilo
- Todo el software debe estar **en español**
- Todos los textos visibles al usuario deben estar en español
- Nombres funcionales claros y profesionales
- Evitar tecnicismos innecesarios en la interfaz
- Etiquetas, menús, formularios, mensajes y estados en español
- README y documentación del proyecto en español, salvo motivos técnicos puntuales

---

## Reglas de negocio obligatorias

### Clientes
Debe existir gestión completa de clientes con, como mínimo:
- código
- nombre fiscal
- nombre comercial
- CIF/NIF
- dirección
- código postal
- población
- provincia
- país
- teléfono
- email
- persona de contacto
- observaciones
- forma de pago por defecto
- vencimiento habitual

### Productos
Debe existir gestión de artículos con, como mínimo:
- referencia
- nombre
- descripción
- unidad
- precio base
- IVA por defecto
- activo/inactivo
- observaciones

### Presupuestos
Debe existir:
- serie de presupuestos
- numeración automática
- estados
- líneas con cantidad, precio, descuento, IVA y total
- posibilidad de convertir presupuesto en pedido

### Pedidos
Debe existir:
- serie de pedidos si se implementa numeración diferenciada
- numeración automática
- estados
- líneas
- trazabilidad documental
- posibilidad de servir parcial o totalmente

### Albaranes
Debe existir:
- serie independiente de albaranes
- numeración automática
- posibilidad de generar albaranes parciales o completos
- estado de entrega
- PDF profesional

### Facturas
Debe existir:
- serie independiente de facturas
- numeración automática
- fecha de emisión
- fecha de vencimiento
- estados de cobro
- facturación parcial o total cuando proceda
- PDF profesional

### Cobros y vencimientos
Debe existir:
- registro de cobros parciales
- registro de cobros totales
- fecha de cobro
- método de cobro
- referencia opcional
- saldo pendiente
- control de facturas vencidas

---

## Fiscalidad e IVA
El proyecto está orientado a España.

Reglas:
- El IVA **no es fijo**
- Los tipos de IVA deben ser **editables desde configuración**
- Debe poder elegirse IVA por producto y también ajustarse por línea
- La factura debe agrupar bases imponibles y cuotas por tipo de IVA
- No hardcodear porcentajes de IVA en la lógica
- Todo ajuste fiscal básico debe poder modificarse sin tocar código

---

## Series documentales
Deben existir series configurables, como mínimo, para:
- presupuestos
- albaranes
- facturas

Las series deben estar desacopladas de la interfaz y almacenadas en datos/configuración.
No hardcodear series en el código.

---

## PDFs: requisito crítico
Los PDFs son una parte esencial del proyecto.

### Regla principal
**Nunca generes un PDF genérico si existen modelos reales en el repositorio.**

Debes buscar y usar como referencia principal archivos como:
- `docs/modelos/factura.*`
- `docs/modelos/albaran.*`
- `docs/modelos/presupuesto.*`
- `assets/logo.*`
- o rutas equivalentes

### Objetivo
Reproducir lo más fielmente posible:
- estructura
- bloques
- cabecera
- tablas
- pie
- posición de totales
- logo
- proporciones
- espaciados
- estilo visual general

### Regla técnica
Mantén separadas:
- la lógica de negocio
- la lógica de plantillas PDF
- la configuración visual ajustable

### Ajustabilidad
Deja preparado el sistema para poder ajustar:
- márgenes
- tamaños
- posiciones
- anchuras de columnas
- textos de pie
- bloques de empresa/cliente

Si una parte del modelo no puede replicarse exactamente, documenta:
- qué parte no coincide
- por qué
- cómo corregirla

---

## Configuración obligatoria
Debe existir un módulo de configuración con capacidad para editar al menos:
- nombre de empresa
- CIF
- dirección fiscal
- teléfono
- email
- logo
- cuentas bancarias
- pie documental
- tipos de IVA
- series
- condiciones de pago por defecto

No esconder configuración importante dentro del código.

---

## Trazabilidad documental
Debe mantenerse relación clara entre documentos.

Como mínimo:
- presupuesto -> pedido
- pedido -> albarán
- pedido y/o albarán -> factura
- factura -> cobros

Debe poder consultarse desde cada documento:
- origen
- documentos relacionados
- importes pendientes
- estado

---

## Base de datos
Debe diseñarse con enfoque profesional y trazable.

Entidades recomendadas:
- company_settings
- document_series
- vat_rates
- customers
- products
- quotes
- quote_lines
- orders
- order_lines
- delivery_notes
- delivery_note_lines
- invoices
- invoice_lines
- payments
- payment_methods
- app_settings
- audit_logs (recomendable)

Evita incoherencias de datos.
No permitir flujos que rompan trazabilidad o importes.

---

## Interfaz de usuario
Quiero una interfaz:
- limpia
- sobria
- empresarial
- fácil de usar muchas horas

Pantallas mínimas:
- dashboard
- clientes
- productos
- presupuestos
- pedidos
- albaranes
- facturas
- cobros
- configuración

Debe incluir:
- menú lateral
- tablas claras
- filtros
- buscador
- formularios cómodos
- estados visuales claros
- confirmación antes de borrar o anular

---

## Calidad de código
Exigencias mínimas:
- TypeScript fuerte cuando aplique
- componentes reutilizables
- separación por módulos
- validación de formularios
- manejo de errores
- nombres coherentes
- sin lógica duplicada
- sin mocks absurdos en la versión final
- sin parches rápidos que degraden el diseño

Antes de cerrar una fase:
- revisar consistencia
- compilar o arrancar
- corregir errores
- dejar la fase funcional

---

## Forma de trabajar en este repositorio
Trabaja por fases y con cambios verificables.

En cada fase:
1. explica brevemente qué vas a hacer
2. crea o modifica archivos reales
3. ejecuta comprobaciones razonables
4. corrige errores
5. deja el proyecto consistente antes de seguir

No te quedes en teoría.
No des por hecho que algo funciona sin validarlo.

---

## Definición de “terminado”
Una funcionalidad no está terminada si falta cualquiera de estos puntos:
- integración real
- validación mínima
- persistencia correcta
- estados coherentes
- navegación usable
- manejo de errores básico
- revisión visual razonable
- prueba manual mínima

---

## Restricciones
- No convertir esto en una simple demo
- No usar PDFs genéricos si hay modelos reales
- No hardcodear IVA, series o datos de empresa
- No cambiar de arquitectura sin justificarlo
- No cerrar tareas importantes con soluciones a medias
- No romper trazabilidad documental
- No introducir complejidad innecesaria

---

## Qué hacer al empezar
Al comenzar cualquier tarea:
1. inspecciona la estructura del proyecto
2. localiza modelos reales de documentos y logo
3. localiza dónde está la lógica de datos
4. localiza dónde está la lógica de renderizado PDF
5. respeta las decisiones ya correctas del proyecto
6. mejora sin reescribir innecesariamente

---

## Qué hacer antes de terminar
Antes de dar una tarea por finalizada:
1. comprueba que compila o arranca
2. revisa errores obvios
3. verifica que los textos de UI estén en español
4. confirma que no has roto series, IVA o trazabilidad
5. documenta cambios relevantes de forma breve

---

## Nota final
En caso de duda, elige siempre la opción que:
- mantenga mejor el proyecto
- reproduzca mejor los documentos reales
- respete mejor la lógica empresarial
- permita crecer más adelante sin rehacer todo
