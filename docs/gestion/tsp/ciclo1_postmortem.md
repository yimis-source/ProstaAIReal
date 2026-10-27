# Postmortem del ciclo 1 · Adquisición y comprensión de datos

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha:** 26/10/2026 · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2


## 1. Resumen

El ciclo 1 se cerró a tiempo el 25/10 (PR #13 a `main`, etiqueta `v0.1-ciclo1`). Plan 47 h, real 54,5 h, desviación +16 %. Hallazgos de datos: inventario de 4 conjuntos con SHA-256, verificación de anonimización sin hallazgos (844 NIfTI de Prostate158, 80 de MSD, 100 + 60 MetaImage de PROMISE12) y elección de MSD Task05 como conjunto principal (32 casos con máscara y 16 sin máscara).

## 2. Plan frente a real

| ID | Tarea | Responsable | Plan h | Real h | Desviación | Ayuda recibida |
|---|---|---|---:|---:|---:|---|
| 1200 | Lanzamiento del ciclo 1 (metas, roles, plan, LOGD/LOGT) | Fernando | 3 | 3 | 0 % | Juan 1 h (crea LOGD) |
| 1201 | Criterios de selección de conjuntos | Juan | 4 | 4,5 | +12 % | — |
| 1202 | Elección del conjunto principal (MSD Task05) y respaldo | Juan | 5 | 6 | +20 % | — |
| 1203 | Una ficha de licencia por conjunto | Juan | 6 | 7 | +17 % | Yimis 1,5 h |
| 1204 | Descarga e inventario con SHA-256 | Yeison | 6 | 8 | +33 % | — |
| 1205 | Verificación de anonimización | Fernando | 5 | 5,5 | +10 % | — |
| 1206 | Análisis de tamaños, espaciado y casos | Juan | 6 | 7 | +17 % | Yeison 2 h |
| 1207 | Revisión visual en 3D Slicer | Sergio | 5 | 6 | +20 % | Juan 1,5 h |
| 1208 | Informe de datos | Juan | 4 | 4,5 | +12 % | Sergio 0,5 h |
| 1209 | Cierre: trazabilidad, LOGD/LOGT, etiqueta | Yimis | 3 | 3 | 0 % | — |
| | **Total** | | **47** | **54,5** | **+16 %** | 6,5 h de ayuda en total |

Por persona:

| Persona | Plan h | Real h | Desviación | Ayuda dada h | Total trabajado h | h/día (días con tarea) |
|---|---:|---:|---:|---:|---:|---:|
| Yimis | 3 | 3 | 0 % | 1,5 | 4,5 | 2,2 |
| Juan | 25 | 29 | +16 % | 2,5 | 31,5 | 3,9 |
| Sergio | 5 | 6 | +20 % | 0,5 | 6,5 | 3,2 |
| Yeison | 6 | 8 | +33 % | 2 | 10 | 3,3 |
| Fernando | 8 | 8,5 | +6 % | 0 | 8,5 | 2,8 |
| **Equipo** | 47 | 54,5 | +16 % | 6,5 | 61 | |

Las desviaciones más grandes: 1204 (descarga e inventario, +33 %), 1203 y 1206 (+17 %). Juan concentró 29 h de 54,5 (más de la mitad) porque el ciclo es de análisis de datos.

## 3. Fechas

| Hito | Plan | Real |
|---|---|---|
| Inicio del ciclo | 13/10 | 13/10 (lanzamiento, PR #5 el 14/10) |
| Cierre | 25/10 | 25/10 (PR #13, 12:00) |
| Desviación de fecha | | 0 días |

## 4. Defectos del ciclo

| ID | Tarea | Tipo | Inyectado → removido | Corrección | Resumen |
|---|---|---|---|---:|---|
| D-002 | 1204 | 80 | IMP → REV | 0,3 h | El inventario contaba la unión de imágenes y etiquetas en lugar de la intersección |
| D-003 | 1203 | 10 | DIS → REV | 0,2 h | La ficha de PROMISE12 dejaba «por verificar» algo que el inventario ya mostraba (30 máscaras) |

Los dos se encontraron en revisión, antes de pasar a la siguiente fase (rendimiento de revisión 2 de 2). Tiempo total de corrección: 0,5 h. (D-001 es de H002 y no cuenta en este ciclo.)

## 5. Valor ganado

Todas las tareas quedaron terminadas: valor ganado = 47 h plan de 47 (100 %). Valor ganado acumulado del proyecto (Inicio + H002 + ciclos cerrados): **91 h plan**.

## 6. Ayudas

| Quién ayudó | A quién | Horas | Tarea |
|---|---|---:|---|
| Juan | Fernando | 1 | 1200 Lanzamiento del ciclo 1 (metas, roles, plan, LOGD/LOGT) (crea LOGD) |
| Yimis | Juan | 1,5 | 1203 Una ficha de licencia por conjunto |
| Yeison | Juan | 2 | 1206 Análisis de tamaños, espaciado y casos |
| Juan | Sergio | 1,5 | 1207 Revisión visual en 3D Slicer |
| Sergio | Juan | 0,5 | 1208 Informe de datos |

Total de ayuda: 6,5 h. La más grande fue Yeison a Juan en el análisis de geometría (2 h).

## 7. Qué funcionó

- La revisión de cada PR por otra persona detectó los dos defectos del ciclo antes del cierre.
- Crear el LOGD y el LOGT desde el lanzamiento (1200): no tuvimos que reconstruir nada al final.
- Trabajar en parejas en las tareas nuevas (Slicer, lectura de formatos): nos sirvió para el riesgo 2 del Acta (curva de aprendizaje).
- Guardar SHA-256 de todo desde el inicio.

## 8. Qué no funcionó

- Subestimamos todas las tareas de análisis: el real salió +16 % sobre el plan.
- Una persona (Juan) con más de la mitad de las horas; si se hubiera enfermado, el ciclo se habría atrasado.
- PROMISE12 trae un `a.py` que no es dato: lo tratamos como archivo no esperado y no se abre, pero faltó preverlo en el plan de descarga.
- La ficha de PROMISE12 salió con una duda que el inventario ya resolvía (D-003): revisamos fichas antes de tener el inventario.

## 9. Lecciones

1. Al estimar tareas de análisis hay que sumar un margen cercano a 15 %.
2. Las fichas y los informes se escriben con el inventario a la vista.
3. Repartir tareas entre más personas, aunque al principio cueste más coordinar.

## 10. Acciones para el ciclo 2

| Acción | Responsable |
|---|---|
| Estimar con un margen de 15 % | Fernando |
| Dejar la verificación de pacientes repetidos y de fuga entre conjuntos como tarea propia del Tester (1304) | Fernando |
| Empezar los diseños desde el 22/10 en paralelo, porque el ciclo 2 dura solo 5 días | Yimis |
| Incluir en las pruebas de control de calidad archivos dañados | Yeison |


*Las horas son las del registro de tiempos (`LOGT_registro_tiempos.md`), reconstruidas a partir de la bitácora del equipo (simuladas para este registro).*
