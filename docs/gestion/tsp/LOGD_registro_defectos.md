# Registro de defectos (LOGD) · Prosta-AI

**Versión:** D1 · **Fecha:** 13/10/2026 · **Autor:** Juan David Riascos Erazo (Gerente de calidad y proceso) · TSP adaptado (ver `docs/gestion/metodologia_tsp.md`)

Primera versión: leyenda de tipos y fases y el defecto D-001, encontrado en la revisión del PR #3 (H002).

## Leyenda

**Tipos de defecto (TSP):**

| Tipo | Nombre |
|---:|---|
| 10 | Documentación |
| 20 | Sintaxis |
| 30 | Construcción / paquetes |
| 40 | Asignación |
| 50 | Interfaz |
| 60 | Chequeo |
| 70 | Datos |
| 80 | Función |
| 90 | Sistema |
| 100 | Entorno |

**Fases (donde se inyecta o se remueve el defecto):**

| Fase | Significado |
|---|---|
| REQ | Requisitos |
| DIS | Diseño |
| IMP | Implementación (código) |
| REV | Revisión (por PR o entre pares) |
| EJE | Ejecución / uso |
| PU | Prueba unitaria |
| INT | Integración |

El tiempo de corrección es el tiempo que costó arreglarlo (horas), sin contar el de encontrarlo. «—» significa que sigue abierto.

## Registro

| ID | Fecha | Ciclo | Tarea | Tipo | Fase inyectado | Fase removido | Tiempo de corrección | Descripción | Encontró | Corrigió | Commit / PR |
|---|---|---|---|---:|---|---|---:|---|---|---|---|
| D-001 | 11/10 | H002 | H04 | 10 | REQ | REV | 0,3 h | En `01_requisitos.md` RF-04 quedó sin caso de uso (CU02) y sin origen en la matriz (4.1). | Yimis (revisión del PR #3) | Juan | PR #3 |

## Resumen por ciclo

| Ciclo | Defectos | Inyectados en | Removidos en | Tipos | Tiempo total de corrección | Rendimiento de revisión (% encontrados antes de PU) |
|---|---:|---|---|---|---:|---|
| H002 | 1 | REQ 1 | REV 1 | 10: 1 | 0,3 h | 1 de 1 (100 %) |
| **Acumulado** | 1 | | | | 0,3 h | 1 de 1 (100 %) |

**Defectos por fase (acumulado):**

| Fase | Inyectados | Removidos |
|---|---:|---:|
| REQ | 1 | 0 |
| REV | 0 | 1 |

**Defectos por tipo (acumulado):**

| Tipo | Cantidad |
|---|---:|
| 10 Documentación | 1 |

Rendimiento de revisión = defectos encontrados en revisión (REV) / defectos totales del ciclo. En D-006 la revisión lo encontró pero todavía no está corregido, así que cuenta como encontrado en REV y sigue abierto.

