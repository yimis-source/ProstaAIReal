# Matriz de trazabilidad de implementación · Prosta-AI

**Versión:** T2 · **Fecha:** 30/10/2026 · **Autor:** Yimis Buenaventura (rol de Trazabilidad) · Cierre del ciclo 2 (`v0.2-ciclo2`)

Relaciona cada requisito de la SRS (`docs/ejecucion/fuentes/1.3.1.1_SRS_requisitos_ISO29148.md`) y su número en la matriz de requisitos (`1.3.1.2_matriz_trazabilidad.md`) con la tarea que lo implementa, la evidencia en el repositorio, la prueba y el estado. Solo se listan evidencias que existen en esa fecha.

Se agregan el control de calidad, la división por paciente y el preprocesamiento. Ya hay pruebas unitarias en `tests/`.

| Requisito (SRS) | Matriz | Tarea | Evidencia en el repositorio | Prueba | Estado |
|---|---|---|---|---|---|
| **RC-03** División por paciente en entrenamiento, validación y prueba, sin repetidos; se verifica antes de entrenar | 3.3 | 1303, 1304 | `entrenamiento/division.py`, `entrenamiento/division_task05.json`, `scripts/verificar_fuga.py`, `reports/division/verificacion_division.md` | `tests/test_division.py`; informe del Tester: 22 / 5 / 5 sin pacientes repetidos y 12 casos compartidos con PROMISE12 (D-005 corregido) | Verificado |
| **RN-01** Solo datos públicos y anónimos; sin datos personales (Ley 1581/2012, Decreto 1377/2013) | 2.1, 2.2 | 1205, 1203 | `scripts/verificar_anonimizacion.py`, `reports/datos/verificacion_anonimizacion.md`, `docs/datos/fichas/` | `tests/test_anonimizacion.py`; revisado en el cierre del ciclo 2 | Verificado para los datos (aplicación en el ciclo 6) |
| **RF-10** Excluir y registrar con motivo toda imagen que no pase el control de calidad | 3.2 | 1301 | `scripts/control_calidad.py`, `reports/calidad/control_calidad.md`, `reports/calidad/control_calidad.csv` | `tests/test_control_calidad.py` (incluye `test_archivo_truncado_se_excluye`, D-004); 128 casos revisados, 0 excluidos | Verificado |
| **RF-09** Mismas transformaciones de preparación en el entrenamiento y en la inferencia | 3.2, 4.2 | 1302, 1305 | `scripts/convertir_nifti.py`, `scripts/preprocesar.py`, `reports/calidad/conversion_nifti.md`, `reports/calidad/preprocesamiento.md` | Informes de los scripts; todavía no hay inferencia que reutilice la preparación | Parcial (preparación de datos hecha; inferencia en el ciclo 3) |
| **RC-04** Sin cuentas, roles ni permisos más allá del acceso básico | 4.7 | — | Sin código de cuentas ni permisos (aún no hay aplicación) | Revisión por ausencia | Sin implementar; se verifica en el ciclo 6 |
| **RF-11** Segmentar la próstata con un modelo 3D (tipo U-Net) y entregar la máscara | 3.4 | — | — | — | Planificado (ciclo 3) |
| **RF-12** Generar la ROI y dejarla alineada con la imagen original | 4.3 | — | — | — | Planificado (ciclo 4) |
| **RF-13** Mostrar la ROI superpuesta y alineada sobre la imagen | 4.3 | — | — | — | Planificado (ciclos 4 y 6) |
| **RF-14** Comparar la imagen con y sin la máscara | 4.3 | — | — | — | Planificado (ciclos 4 y 6) |
| **RF-15** Aviso de salida experimental en toda salida de resultados | 2.3 | — | — | — | Planificado (ciclos 4 y 6) |
| **RF-16** Sin lenguaje clínico en ningún texto | 2.3 | — | — | — | Planificado (ciclos 4 y 6) |
| **RF-17** Explicación junto a cada resultado: qué muestra, métricas y limitaciones | 4.4 | — | — | — | Planificado (ciclos 4 y 6) |
| **RF-23** Dice e IoU por caso y promedio en el conjunto de prueba, con condiciones y limitaciones | 3.5 | — | — | — | Planificado (ciclos 3 y 5) |
| **RF-24** Dice medio ≥ 0,80 en el conjunto de prueba; si no, documentar la brecha | 3.5 | — | — | — | Planificado (ciclos 3 y 5) |
| **RR-01** Procesar un estudio en 2 minutos o menos | 5.1 | — | — | — | Planificado (ciclo 3, tarea 1408) |
| **RA-02** Cada requisito vinculado a necesidad, entregable, prueba e interesado | 6.4 | H003, 1310 | `docs/gestion/trazabilidad.md` | Revisión cruzada de los documentos de diseño (1310) | En curso |

## Resumen de estados

| Estado | Requisitos |
|---|---:|
| Verificado | 3 |
| Parcial | 1 |
| En curso / sin implementar | 2 |
| Planificado | 10 |

## Notas

- D-004 (archivo truncado) y D-005 (comparación de flotantes en `verificar_fuga.py`) se encontraron con pruebas y ya están corregidos.
- Hallazgo de la división: 12 casos de MSD Task05 son el mismo estudio que uno de PROMISE12 (2 en prueba); PROMISE12 no se usa para entrenar ni evaluar.
