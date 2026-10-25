# Matriz de trazabilidad de implementación · Prosta-AI

**Versión:** T1 · **Fecha:** 25/10/2026 · **Autor:** Yimis Buenaventura (rol de Trazabilidad) · Cierre del ciclo 1 (`v0.1-ciclo1`)

Relaciona cada requisito de la SRS (`docs/ejecucion/fuentes/1.3.1.1_SRS_requisitos_ISO29148.md`) y su número en la matriz de requisitos (`1.3.1.2_matriz_trazabilidad.md`) con la tarea que lo implementa, la evidencia en el repositorio, la prueba y el estado. Solo se listan evidencias que existen en esa fecha.

Solo hay evidencia del ciclo 1 (datos) y de la matriz. Los demás requisitos aparecen como planificados con su ciclo.

| Requisito (SRS) | Matriz | Tarea | Evidencia en el repositorio | Prueba | Estado |
|---|---|---|---|---|---|
| **RC-03** División por paciente en entrenamiento, validación y prueba, sin repetidos; se verifica antes de entrenar | 3.3 | — | — | — | Planificado (ciclo 2, tareas 1303 y 1304) |
| **RN-01** Solo datos públicos y anónimos; sin datos personales (Ley 1581/2012, Decreto 1377/2013) | 2.1, 2.2 | 1205 (y 1203) | `scripts/verificar_anonimizacion.py`, `reports/datos/verificacion_anonimizacion.md`, `docs/datos/fichas/` | `tests/test_anonimizacion.py`; verificación sin hallazgos en 844 + 80 NIfTI y 160 MetaImage | Verificado para los datos (la parte de la aplicación entra en el ciclo 6) |
| **RF-10** Excluir y registrar con motivo toda imagen que no pase el control de calidad | 3.2 | — | — | — | Planificado (ciclo 2, tarea 1301) |
| **RF-09** Mismas transformaciones de preparación en el entrenamiento y en la inferencia | 3.2, 4.2 | — | — | — | Planificado (ciclo 2 (preprocesamiento) y ciclo 3 (inferencia)) |
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
| **RA-02** Cada requisito vinculado a necesidad, entregable, prueba e interesado | 6.4 | H003, 1209 | `docs/ejecucion/fuentes/1.3.1.2_matriz_trazabilidad.md`, `docs/gestion/trazabilidad.md` | Revisión de la matriz en el cierre del ciclo | En curso (matriz v1.0 y esta tabla; se actualiza cada ciclo) |

## Resumen de estados

| Estado | Requisitos |
|---|---:|
| Planificado | 13 |
| Verificado | 1 |
| En curso / sin implementar | 2 |

## Notas

- RC-04 no tiene código porque aún no hay aplicación; se verifica en el ciclo 6.
