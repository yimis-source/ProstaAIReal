# Postmortem del ciclo 5 · Evaluación técnica del modelo

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha:** 23/11/2026 · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2

## 1. Resumen

El ciclo 5 se planeó del 16/11 al 25/11 (hito H007), usando el colchón que dejó el adelanto del ciclo 4. Este postmortem se escribe el 23/11, en su propio PR y antes del cierre, como se acordó en el ciclo 4. Las tareas 1601 a 1606 están terminadas; queda la 1607 (trazabilidad, revisión de PR y cierre con `v0.5-ciclo5`), que hace Yimis del 23/11 al 25/11.

Resultados del modelo preentrenado `prostate_mri_anatomy` en los 5 casos de prueba (`reports/evaluacion/informe_metricas_ciclo5.md`):

| Métrica | Media ± desviación típica |
|---|---:|
| Dice | 0,8925 ± 0,0340 |
| IoU | 0,8071 ± 0,0534 |
| HD95 | 4,09 ± 0,92 mm |
| Distancia media de superficie | 1,17 ± 0,49 mm |

- **RF-24 (Dice medio ≥ 0,80):** se cumple.
- **Ajuste fino (1603):** el modelo ajustado en Colab obtuvo un Dice medio de 0,8735 en los mismos 5 casos. No superó el 0,8925 del preentrenado, así que **se conserva el preentrenado**.
- **Rendimiento (1602, RR-01):** en GPU (Tesla T4, Colab) 5,0 s por estudio con el modelo cargado, inferencia 2,3 s; en CPU 14,1 s. RR-01 (≤ 120 s) se cumple en los dos equipos. Las cifras no son comparables entre sí.
- **Pruebas:** 84 en verde (81 al cierre de la 1606 y 3 nuevas del informe de rendimiento).

## 2. Plan frente a real

| ID | Tarea | Responsable | Plan h | Real h | Estado | Evidencia |
|---|---|---|---:|---:|---|---|
| 1601 | Lanzamiento del ciclo 5 | Fernando | 3 | por registrar | Terminada | `docs/gestion/tsp/ciclo5_lanzamiento.md` |
| 1602 | Rendimiento en GPU | Fernando | 5 | por registrar | Terminada; falta la memoria de la GPU (ver sección 9) | `reports/rendimiento/rendimiento_1408_gpu_2026-11-13.md`, `scripts/medir_rendimiento.py` |
| 1603 | Ajuste fino en Google Colab | Yeison | 10 | por registrar | Terminada (PR #75, 21/11) | `docs-tecnicos/modelo-y-licencias.md`, informes del 21/11 |
| 1604 | HD95 y distancia media de superficie | Juan (ayuda: Yeison) | 5 | por registrar | Terminada (PR #72, 19/11) | `backend/prosta_ai/pipeline/evaluation.py` y sus pruebas |
| 1605 | Informe de métricas y límites | Juan | 6 | por registrar | Terminada (PR #72, 19/11; comparación en el PR #77, 21/11) | `reports/evaluacion/informe_metricas_ciclo5.md` |
| 1606 | Revisión visual en 3D Slicer y textos | Sergio | 5 | por registrar | Terminada (PR #74 y #78, 21/11) | `docs/datos/revision_slicer_predicciones.md`, `docs/diseno/texto_roi.md` |
| 1607 | Trazabilidad, revisión de PR y cierre | Yimis | 5 | por registrar | En curso (23/11–25/11) | `docs/gestion/trazabilidad.md` |
| 1608 | Postmortem del ciclo 5 | Fernando | 2 | por registrar | Este documento | `docs/gestion/tsp/ciclo5_postmortem.md` |
| | **Total** | | **41** | | | |

**Horas reales:** cada integrante debe registrar las suyas en el LOGT (sección «Ciclo 5»), como se hizo con la corrección de horas del 21/11. Cuando estén, se completan aquí la desviación por tarea y por persona, las horas por día y las ayudas (por ejemplo, la de Yeison a Juan en la 1604).

## 3. Fechas

| Tarea | Plan | Real | Desviación |
|---|---|---|---|
| Inicio del ciclo | 16/11 | 16/11, con la guía de tareas del 13/11; el documento de lanzamiento se versionó el 23/11 | 0 días en el trabajo; 7 días en el registro |
| 1602 | 16/11–18/11 | Medición en Colab el 13/11; corrección del script e informe el 23/11 | 5 días tarde |
| 1603 | 16/11–21/11 | 21/11 | a tiempo |
| 1604 | 17/11–20/11 | 19/11 | 1 día antes |
| 1605 | 21/11–24/11 | 19/11 (informe) y 21/11 (comparación) | 3 días antes |
| 1606 | 18/11–23/11 | 21/11 | 2 días antes |
| Cierre (H007) | 25/11 | pendiente (1607) | — |

## 4. Defectos del ciclo

| ID | Tarea | Tipo | Inyectado → removido | Tiempo de corrección | Descripción |
|---|---|---:|---|---:|---|
| D-009 | 1604 | 80 | IMP → PU | 0,2 h | HD95 y distancia media devolvían `nan` en vez de `inf` con una sola máscara vacía; lo encontró una prueba |
| D-010 | 1602 | 80 | IMP → EJE | dentro de 1602 | El informe de rendimiento decía «GPU no disponible» aunque se midiera en GPU, y no medía la memoria de la GPU; se vio al correrlo en Colab |

Los dos son de función e inyectados en implementación. Ninguno lo encontró la revisión del PR (rendimiento de revisión del ciclo: 0 de 2). D-010 viene del ciclo 3 (tarea 1408): el script se probó solo en CPU, porque ningún equipo del grupo tiene GPU.

## 5. Valor ganado

Con las tareas terminadas al 23/11 (1601 a 1606 y este postmortem): 36 h plan de 41 (87,8 %). Falta la 1607 (5 h, 12,2 %), que se gana con el cierre del 25/11.

## 6. Decisiones del ciclo

| Decisión | Con qué evidencia | Resultado |
|---|---|---|
| Usar el colchón del 13/11 al 20/11 y empezar el 16/11 | Postmortem del ciclo 4, sección 7 | Ciclo de 10 días en vez de 5 |
| Conservar el modelo preentrenado | Mismos 5 casos de prueba, misma ruta de evaluación, regla de adopción escrita antes de ver los resultados | Dice 0,8925 frente a 0,8735 del ajustado |
| Medir en GPU en Colab y no en un equipo propio | Ningún equipo del grupo tiene GPU NVIDIA | Cifras reales de una Tesla T4 |

## 7. Qué funcionó

- La regla de adopción del ajuste fino se escribió antes de entrenar: la decisión se tomó con datos y no por preferencia.
- Las métricas de borde (HD95) mostraron lo que el Dice no muestra: `prostate_28` tiene el Dice más bajo (0,8320) y también el HD95 más alto (5,69 mm).
- La prueba de máscaras vacías encontró D-009 antes de integrar.
- El colchón del ciclo 4 dio margen: 1604, 1605 y 1606 terminaron antes de lo planeado.
- La revisión visual en 3D Slicer se hizo en pareja (Sergio con Juan) y con las cifras del informe al lado.

## 8. Qué no funcionó

- El lanzamiento se acordó con la guía del ciclo, pero el documento se versionó una semana después; el LOGT del ciclo no tuvo el plan desde el principio.
- La 1602 terminó 5 días tarde y sin la memoria de la GPU, porque la medición en Colab se hizo antes de corregir el script.
- Las horas reales del ciclo no se registraron al terminar cada tarea.
- El 21/11 se fusionaron cinco PR (#74 a #78) en el mismo día; otra vez se juntaron las entregas.
- D-006 (Ejecutar/Procesar) sigue abierto desde el ciclo 2; se corrige en la interfaz del ciclo 6.

## 9. Pendientes que pasan al cierre o al ciclo 6

| Pendiente | Responsable | Cuándo |
|---|---|---|
| Repetir la medición en Colab con el script corregido para tener la memoria pico de la GPU | Fernando | Antes del ciclo 6 |
| Registrar las horas reales del ciclo 5 en el LOGT | Cada integrante | Antes del cierre (25/11) |
| Trazabilidad T5, revisión de PR, `desarrollo → main` y etiqueta `v0.5-ciclo5` | Yimis | 25/11 |
| Corregir D-006 en la interfaz | Sergio / Yeison | Ciclo 6 |

## 10. Lecciones

1. Un script que tiene dos modos (CPU y GPU) necesita una prueba de cada modo, aunque el equipo no tenga GPU: el informe se puede probar sin ejecutar el modelo.
2. El documento de lanzamiento y el plan del LOGT se versionan el mismo día del lanzamiento, no después.
3. La regla para adoptar un modelo se escribe antes de entrenarlo y se compara siempre con los mismos casos.
4. Las horas se anotan al terminar cada tarea; reconstruirlas al final las vuelve estimaciones.

## 11. Qué le toca al ciclo 6 (desarrollo web e integración)

| Tema | Detalle |
|---|---|
| Modelo | Se integra el preentrenado `prostate_mri_anatomy` (decisión de la 1603) |
| Rendimiento | Medir el tiempo de punta a punta en la web (carga del archivo y guardado de resultados), que no está en la 1408 ni en la 1602 |
| Interfaz | Corregir D-006 («Procesar» en lugar de «Ejecutar») y mostrar el aviso de uso no diagnóstico en todas las pantallas de resultados |
| Proceso | Escalonar los PR a lo largo del ciclo y registrar las horas al terminar cada tarea |

*Las horas plan son las del lanzamiento (`ciclo5_lanzamiento.md`) y del LOGT; las reales las registra cada integrante.*
