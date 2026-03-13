# Criterio de trabajo en producción

Este repositorio aplica un enfoque incremental para cambios funcionales:

1. **Descomponer en tareas pequeñas**: cada cambio se divide en bloques ejecutables y verificables.
2. **Validar cada bloque**: tras cada bloque relevante se ejecutan checks, tests o validaciones razonables.
3. **Elegir mantenibilidad**: ante varias opciones técnicas se prioriza la alternativa más explícita, con menor coste de mantenimiento futuro.
4. **Respetar lógica de negocio**: no simplificar reglas de pedidos, albaranes y facturas sin una decisión funcional explícita.

## Plantilla de ejecución por bloque

- Objetivo del bloque.
- Cambios implementados.
- Validación ejecutada y resultado.
- Riesgos y siguientes pasos.

## Política de decisiones técnicas

Cuando existan varias alternativas:

- Favorecer estructuras legibles sobre atajos implícitos.
- Mantener separación clara entre dominio, aplicación e infraestructura.
- Documentar en pocas líneas por qué se eligió una opción.
