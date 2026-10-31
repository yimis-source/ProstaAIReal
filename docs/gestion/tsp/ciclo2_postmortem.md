# Postmortem del ciclo 2 · Preprocesamiento, división por paciente y diseño

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha:** 31/10/2026 · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2


## 1. Resumen

El ciclo 2 se cerró a tiempo el 30/10 (PR #24, `v0.2-ciclo2`). Plan 56 h, real 65 h, desviación +16 %. Resultados: control de calidad sobre 128 casos (32 + 16 de MSD, 50 + 30 de PROMISE12) con 0 excluidos; división de MSD Task05 en 22 / 5 / 5 con semilla 2026; y el hallazgo del Tester de que **12 casos con máscara de MSD son el mismo estudio que un caso de PROMISE12** (2 en el conjunto de prueba: prostate_13 y prostate_17). Por eso PROMISE12 no se usa para entrenar ni evaluar.

## 2. Plan frente a real

| ID | Tarea | Responsable | Plan h | Real h | Desviación | Ayuda recibida |
|---|---|---|---:|---:|---:|---|
| 1300 | Postmortem ciclo 1 y lanzamiento ciclo 2 | Fernando | 3 | 3 | 0 % | — |
| 1301 | Control de calidad (RF-10) | Yeison | 5 | 7 | +40 % | — |
| 1302 | Formato unificado NIfTI | Yeison | 4 | 4 | 0 % | — |
| 1303 | División por paciente 70/15/15 (semilla 2026) | Juan | 4 | 3,5 | -12 % | — |
| 1304 | Informe del Tester: sin pacientes repetidos + fuga entre conjuntos | Fernando | 4 | 7 | +75 % | Juan 1,5 h (comparación de vóxeles) |
| 1305 | Script de preprocesamiento | Yeison | 4 | 4,5 | +12 % | — |
| 1306 | Diseño de arquitectura (sistema y software) | Yimis | 8 | 9 | +12 % | Yeison 1 h |
| 1307 | Diseño de pantallas | Sergio | 10 | 12 | +20 % | — |
| 1308 | Diseño del módulo de IA (componentes y patrones) | Yeison | 5 | 5,5 | +10 % | — |
| 1309 | Diseño de base de datos | Juan | 5 | 5 | 0 % | — |
| 1310 | Revisión cruzada de documentos, cierre y etiqueta | Yimis / Juan | 4 | 4,5 | +12 % | — |
| | **Total** | | **56** | **65** | **+16 %** | 2,5 h de ayuda en total |

Por persona:

| Persona | Plan h | Real h | Desviación | Ayuda dada h | Total trabajado h | h/día (días con tarea) |
|---|---:|---:|---:|---:|---:|---:|
| Yimis | 10 | 11,2 | +12 % | 0 | 11,2 | 1,2 |
| Juan | 11 | 10,8 | -2 % | 1,5 | 12,2 | 1,4 |
| Sergio | 10 | 12 | +20 % | 0 | 12 | 1,7 |
| Yeison | 18 | 21 | +17 % | 1 | 22 | 2,8 |
| Fernando | 7 | 10 | +43 % | 0 | 10 | 3,3 |
| **Equipo** | 56 | 65 | +16 % | 2,5 | 67,5 | |

Las tareas 1306–1309 se trabajaron desde el 22/10, por eso en la columna de «h/día» salen pocas horas por día en esos días. Mayores desviaciones: 1304 (+75 %), 1301 (+40 %, de los cuales 1,5 h son la corrección de D-004) y 1307 (+20 %). La única tarea que bajó fue 1303 (−12,5 %).

## 3. Fechas

| Hito | Plan | Real |
|---|---|---|
| Inicio del ciclo | 26/10 | 26/10 (PR #14, 20:30) |
| Cierre | 30/10 | 30/10 (PR #24, 18:00) |
| Diseño (1306–1309) | desde el 22/10 | desde el 22/10, versionado en el ciclo 2 |
| Desviación de fecha | | 0 días |

## 4. Defectos del ciclo

| ID | Tarea | Tipo | Inyectado → removido | Corrección | Resumen |
|---|---|---|---|---:|---|
| D-004 | 1301 | 60 | IMP → PU | 1,5 h | Un `.nii.gz` truncado pasaba el control de calidad (SimpleITK rellena con ceros) |
| D-005 | 1304 | 80 | IMP → PU | 0,2 h | Comparación del Dice con `== 1.0` en `verificar_fuga.py`; no marcaba prostate_16 ≡ Case23 |
| D-006 | 1307 | 50 | DIS → REV | abierto | Pantalla y navegación dicen «Ejecutar» y debe decir «Procesar»; se corrige en el ciclo 6 |

Rendimiento de revisión del ciclo: 1 de 3 (33 %). D-004 pasó la revisión del PR #15 y solo apareció con la prueba del Tester. Tiempo total de corrección: 1,7 h (D-006 sigue abierto).

## 5. Valor ganado

Todas las tareas quedaron terminadas: valor ganado = 56 h plan de 56 (100 %). Valor ganado acumulado del proyecto (Inicio + H002 + ciclos cerrados): **147 h plan**.

## 6. Ayudas

| Quién ayudó | A quién | Horas | Tarea |
|---|---|---:|---|
| Juan | Fernando | 1,5 | 1304 Informe del Tester: sin pacientes repetidos + fuga entre conjuntos (comparación de vóxeles) |
| Yeison | Yimis | 1 | 1306 Diseño de arquitectura (sistema y software) |

Total de ayuda: 2,5 h (Juan ayudó a Fernando con la comparación de vóxeles; Yeison a Yimis en la arquitectura).

## 7. Qué funcionó

- La prueba con un archivo truncado (`test_archivo_truncado_se_excluye`) encontró un defecto real que la revisión del PR no vio.
- La verificación de fuga entre conjuntos encontró algo que no estaba en el plan (estudios repetidos entre MSD y PROMISE12) y permitió decidir con evidencia.
- Adelantar el diseño al 22/10 hizo que un ciclo de 5 días alcanzara.
- La revisión cruzada de los diseños encontró el defecto D-006.

## 8. Qué no funcionó

- 1304 costó 75 % más: la comparación de vóxeles entre conjuntos no estaba en la estimación.
- Ciclo corto con 65 h reales: Yeison puso 21 h de las 65.
- La revisión de PR no ve archivos dañados si no hay prueba con casos límite: D-004 tuvo que esperar a PU.
- D-006 quedó abierto porque la corrección depende de la interfaz, que todavía no existe.

## 9. Lecciones

1. Las pruebas con datos dañados o raros hay que escribirlas junto con el código de control de calidad.
2. El margen de estimación del 15 % no alcanzó para tareas nuevas del Tester; en tareas de exploración hay que pedir más.
3. El trabajo de diseño adelantado ayuda, pero hay que anotarlo en el plan para que las horas por día sean comparables.

## 10. Acciones para el ciclo 3

| Acción | Responsable |
|---|---|
| Replanificar el ciclo 3 y el 4 aprovechando el modelo preentrenado (decisión en el lanzamiento del 31/10) | Fernando, aprobación de Yimis |
| Escribir pruebas de casos límite junto con el código del pipeline | Yeison y Fernando |
| Verificar la división (1411) antes de evaluar | Fernando |
| Dejar D-006 registrado como abierto hasta el ciclo 6 | Juan |
| Vigilar horas por día por la replanificación | Fernando |


*Las horas son las del registro de tiempos (`LOGT_registro_tiempos.md`), reconstruidas a partir de la bitácora del equipo (simuladas para este registro).*
