# Postmortem del ciclo 3 · Segmentación 3D, modelo e inferencia

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha:** 11/11/2026 · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2


## 1. Resumen

El ciclo 3 se cerró el 10/11 (PR #39, `v0.3-ciclo3`) con las **fechas replanificadas** (31/10–10/11; plan original 31/10–13/11). Plan 76 h, real 87,5 h, desviación +15 %. Usamos el modelo preentrenado `prostate_mri_anatomy`, sin entrenamiento propio; el ajuste fino quedó preparado y no se ejecutó.

Resultados (informes `reports/evaluacion/` y `reports/rendimiento/`):

| Medida | Valor |
|---|---|
| Dice en los 5 casos de prueba (06/11, CPU) | 0,8925 ± 0,0340 (meta del Acta: ≥ 0,80) |
| IoU | 0,8071 ± 0,0534 |
| Tiempo por caso | 14,9 ± 2,6 s |
| 1408 (prostate_13, CPU, 3 repeticiones) | total 16,0 s en frío, 13,1 s y 15,1 s; inferencia 12,0–14,9 s; preparación ≈ 1,0 s |
| Memoria | pico RSS de 2 048 MB |
| GPU | no disponible; medición pendiente en Colab |
| Pruebas | 42 en `backend/tests` + 20 en la raíz |

## 2. Plan frente a real

| ID | Tarea | Responsable | Plan h | Real h | Desviación | Ayuda recibida |
|---|---|---|---:|---:|---:|---|
| 1401 | Lanzamiento, postmortem C2 y replanificación | Fernando | 4 | 4 | 0 % | Yimis 1 h (aprobación y riesgos) |
| 1402 | Selección del modelo preentrenado y licencias | Juan | 6 | 7 | +17 % | — |
| 1403 | Entorno: versiones fijadas de MONAI/torch y guía de instalación | Sergio | 4 | 5 | +25 % | — |
| 1404 | Núcleo del pipeline (stages, errors, io, validators, progress) | Yeison | 8 | 9 | +12 % | — |
| 1405 | Descarga del modelo con versión fija y SHA-256 | Yeison | 3 | 3 | 0 % | — |
| 1406 | Preparación (mismas transformaciones, RF-09) | Yeison | 4 | 4,5 | +12 % | Juan 1 h |
| 1407 | Segmentación e inferencia por ventana deslizante | Yeison | 8 | 11 | +38 % | Fernando 2,5 h (depuración en pareja, D-007) |
| 1408 | Tiempos de preparación e inferencia y memoria (CPU; GPU pendiente) | Fernando | 4 | 5 | +25 % | Yeison 1 h |
| 1409 | Protocolo de evaluación y evaluar.py | Juan | 7 | 8 | +14 % | Yeison 1,5 h (coautor) |
| 1410 | Pruebas del pipeline con datos sintéticos | Fernando | 8 | 9 | +12 % | — |
| 1411 | Verificación de la división y evaluación en los 5 casos de prueba | Fernando | 4 | 4 | 0 % | Juan 2 h (análisis del informe) |
| 1412 | Ajuste fino preparado (no ejecutado) y decisión del modelo | Yeison | 8 | 9 | +12 % | — |
| 1413 | Revisión en 3D Slicer de las máscaras predichas | Sergio | 4 | 4,5 | +12 % | Juan 1,5 h |
| 1414 | Matriz de trazabilidad, LOGD/LOGT y cierre (v0.3-ciclo3) | Yimis | 4 | 4,5 | +12 % | Juan 1 h (LOGD) |
| | **Total** | | **76** | **87,5** | **+15 %** | 11,5 h de ayuda en total |

Por persona:

| Persona | Plan h | Real h | Desviación | Ayuda dada h | Total trabajado h | h/día (días con tarea) |
|---|---:|---:|---:|---:|---:|---:|
| Yimis | 4 | 4,5 | +12 % | 1 | 5,5 | 2,8 |
| Juan | 13 | 15 | +15 % | 5,5 | 20,5 | 3,4 |
| Sergio | 8 | 9,5 | +19 % | 0 | 9,5 | 2,4 |
| Yeison | 31 | 36,5 | +18 % | 2,5 | 39 | 4,9 |
| Fernando | 20 | 22 | +10 % | 2,5 | 24,5 | 3,5 |
| **Equipo** | 76 | 87,5 | +15 % | 11,5 | 99 | |

Mayores desviaciones: 1407 (+37,5 %, incluye D-007 y 2,5 h de depuración en pareja), 1403 y 1408 (+25 %).

## 3. Fechas

| Hito | Plan replanificado | Real | Plan original |
|---|---|---|---|
| Inicio | 31/10 | 31/10 (PR #25, 13:00) | 31/10 |
| Cierre | 10/11 | 10/11 (PR #39, 20:30) | 13/11 |
| Desviación | **0 días** (a tiempo) | | **3 días antes** del plan original (H005) |

## 4. Defectos del ciclo

| ID | Tarea | Tipo | Inyectado → removido | Corrección | Resumen |
|---|---|---|---|---:|---|
| D-007 | 1407 | 80 | IMP → PU | 2,5 h | Sin `.eval()` el dropout (0,15) y la normalización por lotes seguían en modo entrenamiento: prostate_13 Dice 0,2065 (61 289 vóxeles) y prostate_28 0,1726; con `.eval()` 0,9012 (22 172 vóxeles) y 0,8320 |

Encontró Fernando depurando en pareja con Yeison; quedó una prueba de regresión (`assert not modelo.training`). Rendimiento de revisión del ciclo: 0 de 1: la revisión no lo vio, el síntoma (Dice bajo) apareció al evaluar. D-006 sigue abierto para el ciclo 6.

## 5. Valor ganado

Todas las tareas quedaron terminadas: valor ganado = 76 h plan de 76 (100 %). Valor ganado acumulado del proyecto (Inicio + H002 + ciclos cerrados): **223 h plan**.

## 6. Ayudas

| Quién ayudó | A quién | Horas | Tarea |
|---|---|---:|---|
| Yimis | Fernando | 1 | 1401 Lanzamiento, postmortem C2 y replanificación (aprobación y riesgos) |
| Juan | Yeison | 1 | 1406 Preparación (mismas transformaciones, RF-09) |
| Fernando | Yeison | 2,5 | 1407 Segmentación e inferencia por ventana deslizante (depuración en pareja, D-007) |
| Yeison | Fernando | 1 | 1408 Tiempos de preparación e inferencia y memoria (CPU; GPU pendiente) |
| Yeison | Juan | 1,5 | 1409 Protocolo de evaluación y evaluar.py (coautor) |
| Juan | Fernando | 2 | 1411 Verificación de la división y evaluación en los 5 casos de prueba (análisis del informe) |
| Juan | Sergio | 1,5 | 1413 Revisión en 3D Slicer de las máscaras predichas |
| Juan | Yimis | 1 | 1414 Matriz de trazabilidad, LOGD/LOGT y cierre (v0.3-ciclo3) (LOGD) |

Total de ayuda: 11,5 h, el máximo hasta ahora (ciclo 1: 6,5 h; ciclo 2: 2,5 h). La mayor parte fue la depuración de D-007 y el trabajo de Juan alrededor del protocolo y la evaluación.

## 7. Efecto del adelanto (replanificación)

| Aspecto | Lo que pasó |
|---|---|
| Ritmo | 99 h trabajadas en 11 días calendario (10 sin el festivo del 02/11), con tareas en fines de semana (31/10, 01/11, 07/11, 08/11) |
| Horas por día | En los días con tarea, el promedio del equipo fue 3,4 h/día, frente a 3,1 h/día del ciclo 1 y 2,1 h/día del ciclo 2. Yeison llegó a 4,9 h/día. Contando todos los días calendario del ciclo, el promedio por persona pasó de 0,9 h/día (ciclo 1, 13 días) y 1,5 h/día (ciclo 2, 9 días desde el 22/10) a 2,0 h/día en este ciclo (10 días); el efecto del adelanto se ve más en esa medida que en la de días con tarea |
| Sobrecarga | Yeison puso 36,5 h propias + 2,5 h de ayuda y estuvo en tres tareas a la vez entre el 03/11 y el 05/11. Es el riesgo 6 del Acta en la práctica; se manejó porque Fernando y Juan se repartieron la depuración y el protocolo |
| Trabajo en paralelo | Funcionó: el protocolo (Juan) se escribió antes de tener predicciones, las pruebas con datos sintéticos (Fernando) arrancaron el 02/11 sin esperar al modelo, y Sergio adelantó el diseño del visor |
| Solapamiento | El lanzamiento del ciclo 4 se hizo el 08/11 con este ciclo en cierre. Costo: el postmortem del ciclo 3 no se hizo al iniciar el ciclo 4 como en los ciclos anteriores sino el 11/11 (tarea 1509) |
| Beneficio de margen | Cerramos 3 días antes del plan original y el ciclo 4 cerró 8 días antes (ver su postmortem). Hay margen para los ciclos 5 a 7 sin tocar el hito de entrega final |

## 8. Qué funcionó

- Elegir el preentrenado quitó el mayor riesgo del Acta (1) sin entrenar: el Dice en prueba superó la meta de 0,80.
- Depuración en pareja: D-007 se resolvió entre Yeison y Fernando (2,5 h de ayuda) y quedó prueba de regresión.
- Escribir el protocolo de evaluación antes de ver las predicciones.
- Pruebas con datos sintéticos desde el primer día del pipeline, sin datos reales en el repo.
- Versiones fijadas de MONAI/torch con guía de instalación (1403).

## 9. Qué no funcionó

- Seguimos subestimando: +15 % sobre el plan, aun con la replanificación.
- Yeison cargó 41,7 % de las horas de responsable del ciclo.
- La GPU no estaba disponible: 1408 solo midió en CPU.
- La prueba que habría atrapado `.eval()` no existía antes de la inferencia; la escribimos después.
- Pasó tiempo con el postmortem desplazado por el solapamiento.

## 10. Lecciones

1. Una replanificación sí da margen, pero cuesta horas por día y hay que cuidarlas en el LOGT.
2. La prueba de «el modelo está en modo evaluación» es obligatoria en cualquier inferencia.
3. Las tareas de modelo e inferencia se estiman con margen mayor (la de 1407 fue +37,5 %).

## 11. Acciones para el ciclo 4

| Acción | Responsable |
|---|---|
| Etapa ROI y imagen con aviso, con pruebas desde el principio | Yeison y Fernando |
| Repartir mejor la carga: Sergio y Juan toman más tareas del ciclo | Yimis |
| Escribir este postmortem y no dejar el del ciclo 4 para el último momento | Fernando |
| Dejar la medición en GPU (1408) para el ciclo 5 | Fernando |


*Las horas son las del registro de tiempos (`LOGT_registro_tiempos.md`), reconstruidas a partir de la bitácora del equipo (simuladas para este registro).*
