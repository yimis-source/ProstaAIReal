# Postmortem del ciclo 4 · Generación de la ROI

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha:** 12/11/2026 · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2


## 1. Resumen

El ciclo 4 se cerró el 12/11 (PR #49, `v0.4-ciclo4`) con las **fechas replanificadas** (08/11–12/11; plan original 14/11–20/11). Plan 42 h, real 47 h, desviación +12 %. Salió la etapa ROI del pipeline (imagen y máscara NIfTI en la rejilla original), la imagen del corte con la ROI superpuesta y el aviso experimental, el texto explicativo y el diseño del visor.

Resultados (informes `reports/roi/` y `reports/evaluacion/`):

| Caso (conjunto de prueba) | Forma | Vóxeles ROI | Volumen (ml) | Dice (= informe) |
|---|---|---:|---:|---:|
| prostate_13 | 320×320×20 | 22 172 | 31,2 | 0,9012 |
| prostate_17 | 320×320×20 | 25 485 | 35,8 | 0,9097 |
| prostate_28 | 384×384×11 | 27 858 | 40,7 | 0,8320 |
| prostate_34 | 320×320×15 | 44 562 | 64,2 | 0,9105 |
| prostate_44 | 320×320×20 | 30 938 | 43,5 | 0,9090 |

En los 5 casos la forma y la afín son iguales a la imagen, la máscara es binaria y las cabeceras no traen texto. El Dice de la máscara guardada coincide con el del informe. Dato adicional sobre los 32 casos con máscara: Dice 0,8736 ± 0,1222, IoU 0,7892 ± 0,1304, 13,5 ± 2,4 s por caso; en el conjunto de prueba sigue 0,8925 ± 0,0340. Pruebas: 58 en `backend/tests` + 20 en la raíz.

## 2. Plan frente a real

| ID | Tarea | Responsable | Plan h | Real h | Desviación | Ayuda recibida |
|---|---|---|---:|---:|---:|---|
| 1501 | Lanzamiento del ciclo 4 (con el ciclo 3 en cierre) | Fernando | 3 | 3 | 0 % | — |
| 1502 | Diseño del visor y de la superposición de la ROI | Sergio | 6 | 7 | +17 % | — |
| 1503 | Etapa ROI (rejilla original, NIfTI de salida) | Yeison | 6 | 6,5 | +8 % | — |
| 1504 | Imagen de la ROI con aviso no clínico | Yeison | 6 | 7,5 | +25 % | Sergio 1,5 h (coautor) |
| 1505 | Texto explicativo de la ROI y revisión de lenguaje no clínico | Sergio | 3 | 3 | 0 % | — |
| 1506 | Pruebas de la ROI y de la imagen con aviso | Fernando | 5 | 6 | +20 % | Juan 1 h |
| 1507 | Verificación de alineación (3D Slicer + script) | Juan | 4 | 4,5 | +12 % | Sergio 1 h |
| 1508 | Análisis de errores por caso (incluye prostate_07, 32 casos) | Juan | 3 | 3,5 | +17 % | — |
| 1509 | Postmortem del ciclo 3 | Fernando | 2 | 2 | 0 % | — |
| 1510 | Postmortem C4, matriz y cierre (v0.4-ciclo4) | Fernando / Yimis | 4 | 4 | 0 % | — |
| | **Total** | | **42** | **47** | **+12 %** | 3,5 h de ayuda en total |

Por persona:

| Persona | Plan h | Real h | Desviación | Ayuda dada h | Total trabajado h | h/día (días con tarea) |
|---|---:|---:|---:|---:|---:|---:|
| Yimis | 2 | 2 | 0 % | 0 | 2 | 2,0 |
| Juan | 7 | 8 | +14 % | 1 | 9 | 9,0 |
| Sergio | 9 | 10 | +11 % | 2,5 | 12,5 | 3,1 |
| Yeison | 12 | 14 | +17 % | 0 | 14 | 4,7 |
| Fernando | 12 | 13 | +8 % | 0 | 13 | 3,2 |
| **Equipo** | 42 | 47 | +12 % | 3,5 | 50,5 | |

Mayores desviaciones: 1504 (+25 %), 1506 (+20 %) y 1502 (+17 %). Es la menor desviación de los ciclos 1 a 4 (+12 %); puede que ayudara aplicar el margen que se pidió en los postmortems anteriores.

## 3. Fechas

| Hito | Plan replanificado | Real | Plan original |
|---|---|---|---|
| Inicio | 08/11 (1502 desde el 07/11) | 08/11 (PR #35, 18:00) | 14/11 |
| Cierre | 12/11 | 12/11 (PR #49, 17:30) | 20/11 |
| Desviación | **0 días** (a tiempo) | | **8 días antes** del plan original (H006) |

## 4. Defectos del ciclo

| ID | Tarea | Tipo | Inyectado → removido | Corrección | Resumen |
|---|---|---|---|---:|---|
| D-008 | 1503 | 50 | IMP → PU | 0,5 h | La etapa ROI hizo que `PipelineInput` exija `output_dir` y `entrenamiento/evaluar.py` dejó de funcionar; ahora escribe en una carpeta temporal |

Encontró y corrigió Yeison al correr la evaluación. Rendimiento de revisión del ciclo: 0 de 1. D-006 sigue abierto y se corrige en el ciclo 6.

## 5. Valor ganado

Todas las tareas quedaron terminadas: valor ganado = 42 h plan de 42 (100 %). Valor ganado acumulado del proyecto (Inicio + H002 + ciclos cerrados): **265 h plan**.

## 6. Ayudas

| Quién ayudó | A quién | Horas | Tarea |
|---|---|---:|---|
| Sergio | Yeison | 1,5 | 1504 Imagen de la ROI con aviso no clínico (coautor) |
| Juan | Fernando | 1 | 1506 Pruebas de la ROI y de la imagen con aviso |
| Sergio | Juan | 1 | 1507 Verificación de alineación (3D Slicer + script) |

Total de ayuda: 3,5 h.

## 7. Efecto del adelanto (replanificación)

| Aspecto | Lo que pasó |
|---|---|
| Ritmo | 50,5 h trabajadas entre el 07/11 y el 12/11. En la semana se juntaron el cierre del ciclo 3 (PR #38 y #39), el 4 y dos postmortems |
| Horas por día | En los días con tarea el promedio por persona fue 4,4 h/día (en días calendario del 07 al 12/11, 1,7 h/día); sin el pico de Juan (9 h el 11/11 entre 1507 y 1508) queda en 3,3 h/día. Yeison 4,7 h/día |
| Sobrecarga | El 11/11 hubo cuatro PR (42 a 45) y el 12/11 otros cuatro (46 a 49, incluyendo el cierre). Juan en un solo día hizo la verificación de alineación y el análisis de errores. Es aceptable por una vez, no como ritmo |
| Solapamiento | El 10/11 se cerró el ciclo 3 (PR #39) y esa misma noche entraron 1502 y 1503 del ciclo 4. |
| Beneficio de margen | El ciclo 4 cerró 8 días antes de lo planificado en el Acta (20/11). El ciclo 5 empieza en el plan el 21/11, así que quedan del 13/11 al 20/11 como colchón para la medición en GPU y para decidir el ajuste fino sin presionar al ciclo 6 |

## 8. Qué funcionó

- Pruebas de la ROI antes de integrar: forma, afín, máscara binaria y cabecera sin texto.
- Verificación de alineación con un script y con 3D Slicer (Juan con Sergio): evidencia doble.
- Aviso experimental centralizado en `constantes.py` y probado en la imagen (riesgo 5).
- El análisis de errores por caso ubicó el problema de prostate_07 (Dice 0,2255): región falsa de 24 225 vóxeles a 13,1 mm del borde del campo de visión; los otros bajos son prostate_10 (0,8080), prostate_28 (0,8320, de prueba) y prostate_46 (0,8322).
- Margen de estimación aplicado: la desviación bajó a +12 %.

## 9. Qué no funcionó

- D-008: cambiamos la API del pipeline sin correr la evaluación completa antes de integrar.
- Dos PR el mismo día con dependencia (visualización antes de sus pruebas) obligaron a sincronizar ramas.
- La medición en GPU sigue sin hacerse.
- El cierre del 12/11 concentró cuatro PR; el postmortem y la matriz se hicieron con prisa.
- D-006 (Ejecutar/Procesar) sigue abierto desde el ciclo 2.

## 10. Lecciones

1. Cuando se cambia la API de un módulo hay que correr todos los consumidores (pruebas y `evaluar.py`) en el mismo PR.
2. Un Dice promedio bueno no muestra casos como prostate_07; el análisis por caso es parte de la evaluación.
3. Vale la pena el adelanto, pero hay que escalonar los PR de cierre en vez de dejarlos para el último día.

## 11. Qué le toca al ciclo 5 (evaluación técnica)

| Tema | Detalle |
|---|---|
| Métricas por caso | Dice e IoU por caso y por conjunto, con las condiciones y limitaciones (RF-23, RF-24); seguir el caso prostate_07 y los más bajos |
| Medición en GPU | Pendiente de la tarea 1408: correr `scripts/medir_rendimiento.py` en Colab y comparar con los 16,0 s de CPU |
| Ajuste fino | Decidir si se ejecuta `entrenamiento/entrenar.py` en Colab; solo se adopta si mejora el Dice del preentrenado sobre el mismo conjunto de prueba |
| Fuera del ciclo 5 | La integración web (API, base de datos, interfaz) es del ciclo 6; D-006 se corrige ahí |

## 12. Acciones para el ciclo 5

| Acción | Responsable |
|---|---|
| Lanzamiento del ciclo 5 con la decisión de usar o no el colchón del 13/11 al 20/11 | Fernando, aprobación de Yimis |
| Preparar el cuaderno de Colab para medir GPU y, si se decide, ajustar | Yeison |
| Informe de métricas por caso y protocolo ya definido | Juan |
| Mantener el margen de 15 % y repartir las tareas para no repetir el pico del 11/11 | Fernando |


*Las horas son las del registro de tiempos (`LOGT_registro_tiempos.md`), reconstruidas a partir de la bitácora del equipo (simuladas para este registro).*
