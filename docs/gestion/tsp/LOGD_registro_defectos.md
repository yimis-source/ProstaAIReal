# Registro de defectos (LOGD) · Prosta-AI

**Versión:** D4 · **Fecha:** 09/11/2026 · **Autor:** Juan David Riascos Erazo (Gerente de calidad y proceso) · TSP adaptado (ver `docs/gestion/metodologia_tsp.md`)

Se agrega D-007 (ciclo 3). D-006 sigue abierto.

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
| D-002 | 19/10 | C1 | 1204 | 80 | IMP | REV | 0,3 h | `inventario_datos.py` contaba «con máscara» la unión de `imagesTr` y `labelsTr` (contaría imágenes sin etiqueta); debe ser la intersección. | Juan (revisión del PR) | Yeison | PR #7 |
| D-003 | 23/10 | C1 | 1203 | 10 | DIS | REV | 0,2 h | La ficha de PROMISE12 dejaba «por verificar» si la carpeta de prueba trae máscaras; el inventario muestra 30 máscaras. | Fernando | Juan | PR #10 |
| D-004 | 29/10 | C2 | 1301 | 60 | IMP | PU | 1,5 h | Un `.nii.gz` truncado pasaba el control de calidad: SimpleITK lo abre sin error y rellena con ceros los cortes faltantes. Ahora se comprueba el flujo gzip completo antes de leer. | Fernando (prueba `test_archivo_truncado_se_excluye`) | Yeison | PR #19 |
| D-005 | 29/10 | C2 | 1304 | 80 | IMP | PU | 0,2 h | `verificar_fuga.py` comparaba el Dice de las máscaras con `== 1.0` (flotante) y no marcaba prostate_16 ≡ Case23 como misma máscara. | Fernando | Fernando (con Juan) | PR #19 |
| D-006 | 28/10 | C2 | 1307 | 50 | DIS | REV (detectado; sin corregir) | — (abierto) | La pantalla CU03 y el diagrama de navegación dicen «Ejecutar»; debe ser «Procesar». Se corrige al implementar la interfaz en el ciclo 6. | Juan (revisión del PR #17) | Sergio (pendiente) | PR #17 (abierto) |
| D-007 | 05/11 | C3 | 1407 | 80 | IMP | PU | 2,5 h | Sin `.eval()` el dropout (0,15) y la normalización por lotes seguían en modo entrenamiento: prostate_13 Dice 0,2065 (61 289 vóxeles) y prostate_28 0,1726; con `.eval()` 0,9012 (22 172 vóxeles) y 0,8320. Prueba de regresión `assert not modelo.training`. | Fernando (depuración en pareja) | Yeison | PR #29 |

## Resumen por ciclo

| Ciclo | Defectos | Inyectados en | Removidos en | Tipos | Tiempo total de corrección | Rendimiento de revisión (% encontrados antes de PU) |
|---|---:|---|---|---|---:|---|
| H002 | 1 | REQ 1 | REV 1 | 10: 1 | 0,3 h | 1 de 1 (100 %) |
| C1 | 2 | IMP 1, DIS 1 | REV 2 | 80: 1, 10: 1 | 0,5 h | 2 de 2 (100 %) |
| C2 | 3 | IMP 2, DIS 1 | PU 2, REV 1 | 60: 1, 80: 1, 50: 1 | 1,7 h | 1 de 3 (33 %) |
| C3 | 1 | IMP 1 | PU 1 | 80: 1 | 2,5 h | 0 de 1 (0 %) |
| **Acumulado** | 7 | | | | 5,0 h | 4 de 7 (57 %) |

**Defectos por fase (acumulado):**

| Fase | Inyectados | Removidos |
|---|---:|---:|
| REQ | 1 | 0 |
| DIS | 2 | 0 |
| IMP | 4 | 0 |
| REV | 0 | 4 |
| PU | 0 | 3 |

**Defectos por tipo (acumulado):**

| Tipo | Cantidad |
|---|---:|
| 10 Documentación | 2 |
| 50 Interfaz | 1 |
| 60 Chequeo | 1 |
| 80 Función | 3 |

Rendimiento de revisión = defectos encontrados en revisión (REV) / defectos totales del ciclo. En D-006 la revisión lo encontró pero todavía no está corregido, así que cuenta como encontrado en REV y sigue abierto.

