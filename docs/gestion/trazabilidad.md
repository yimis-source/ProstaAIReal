# Matriz de trazabilidad de implementación · Prosta-AI

**Versión:** T3 · **Fecha:** 10/11/2026 · **Autor:** Yimis Buenaventura (rol de Trazabilidad) · Cierre del ciclo 3 (`v0.3-ciclo3`)

Relaciona cada requisito de la SRS (`docs/ejecucion/fuentes/1.3.1.1_SRS_requisitos_ISO29148.md`) y su número en la matriz de requisitos (`1.3.1.2_matriz_trazabilidad.md`) con la tarea que lo implementa, la evidencia en el repositorio, la prueba y el estado. Solo se listan evidencias que existen en esa fecha.

Se agregan el pipeline, el modelo y la evaluación preliminar en el conjunto de prueba (5 casos). Pruebas: 42 en `backend/tests` + 20 en la raíz.

| Requisito (SRS) | Matriz | Tarea | Evidencia en el repositorio | Prueba | Estado |
|---|---|---|---|---|---|
| **RC-03** División por paciente en entrenamiento, validación y prueba, sin repetidos; se verifica antes de entrenar | 3.3 | 1303, 1304 | `entrenamiento/division.py`, `entrenamiento/division_task05.json`, `scripts/verificar_fuga.py`, `reports/division/verificacion_division.md` | `tests/test_division.py`; informe del Tester: 22 / 5 / 5 sin pacientes repetidos y 12 casos compartidos con PROMISE12 (D-005 corregido) | Verificado |
| **RN-01** Solo datos públicos y anónimos; sin datos personales (Ley 1581/2012, Decreto 1377/2013) | 2.1, 2.2 | 1205, 1203; 1404 | `reports/datos/verificacion_anonimizacion.md`, `docs/datos/fichas/`, `backend/prosta_ai/pipeline/io.py` (`save_nifti` sin metadatos) | `tests/test_anonimizacion.py`; `backend/tests/pipeline/test_pipeline_io.py` (guardado sin metadatos); datos sintéticos en las pruebas | Verificado para datos y pipeline (aplicación en el ciclo 6) |
| **RF-10** Excluir y registrar con motivo toda imagen que no pase el control de calidad | 3.2 | 1301; 1404 | `scripts/control_calidad.py`, `reports/calidad/control_calidad.md`, `backend/prosta_ai/pipeline/validators.py` | `tests/test_control_calidad.py`; `backend/tests/pipeline/test_pipeline_validadores.py` y `test_pipeline_io.py` (`test_nifti_truncado_se_rechaza`) | Verificado (scripts y pipeline) |
| **RF-09** Mismas transformaciones de preparación en el entrenamiento y en la inferencia | 3.2, 4.2 | 1302, 1305; 1406 | `scripts/preprocesar.py`, `backend/prosta_ai/pipeline/preparation.py`, `entrenamiento/entrenar.py`, `docs-tecnicos/modelo-y-licencias.md` | `backend/tests/entrenamiento/test_entrenar.py` (`preparacion.json` releíble); `backend/tests/pipeline/test_pipeline_roi_modelo.py` | Verificado (inferencia y ajuste fino usan la misma preparación) |
| **RC-04** Sin cuentas, roles ni permisos más allá del acceso básico | 4.7 | — | Sin código de cuentas ni permisos (aún no hay aplicación) | Revisión por ausencia | Sin implementar; se verifica en el ciclo 6 |
| **RF-11** Segmentar la próstata con un modelo 3D (tipo U-Net) y entregar la máscara | 3.4 | 1402, 1405, 1407, 1412 | `backend/prosta_ai/pipeline/segmentation.py`, `backend/prosta_ai/pipeline/factory.py`, `scripts/descargar_modelo.py`, `docs-tecnicos/modelo-y-licencias.md` | `backend/tests/pipeline/test_pipeline_roi_modelo.py` (incluye `assert not modelo.training`, D-007); revisión de máscaras en 3D Slicer (`docs/datos/revision_slicer_predicciones.md`) | Verificado (CPU, modelo preentrenado `prostate_mri_anatomy`) |
| **RF-12** Generar la ROI y dejarla alineada con la imagen original | 4.3 | 1407 | `backend/prosta_ai/pipeline/roi.py` (`mask_to_original_space`) | `backend/tests/pipeline/test_pipeline_roi_modelo.py` (rejilla original) | Parcial (máscara en la rejilla original; etapa ROI y NIfTI de salida en el ciclo 4) |
| **RF-13** Mostrar la ROI superpuesta y alineada sobre la imagen | 4.3 | — | — | — | Planificado (ciclos 4 y 6) |
| **RF-14** Comparar la imagen con y sin la máscara | 4.3 | — | — | — | Planificado (ciclos 4 y 6) |
| **RF-15** Aviso de salida experimental en toda salida de resultados | 2.3 | — | — | — | Planificado (ciclos 4 y 6) |
| **RF-16** Sin lenguaje clínico en ningún texto | 2.3 | — | — | — | Planificado (ciclos 4 y 6) |
| **RF-17** Explicación junto a cada resultado: qué muestra, métricas y limitaciones | 4.4 | — | — | — | Planificado (ciclos 4 y 6) |
| **RF-23** Dice e IoU por caso y promedio en el conjunto de prueba, con condiciones y limitaciones | 3.5 | 1409, 1411 | `docs/datos/protocolo_evaluacion.md`, `entrenamiento/evaluar.py`, `reports/evaluacion/evaluacion_prostate_mri_anatomy_2026-11-06.md` y `.csv` | `backend/tests/pipeline/test_pipeline_evaluacion.py`; evaluación de los 5 casos de prueba (Dice 0,8925 ± 0,0340; IoU 0,8071 ± 0,0534) | Parcial (evaluación preliminar; la formal es del ciclo 5) |
| **RF-24** Dice medio ≥ 0,80 en el conjunto de prueba; si no, documentar la brecha | 3.5 | 1411 | `reports/evaluacion/evaluacion_prostate_mri_anatomy_2026-11-06.md`, `docs-tecnicos/modelo-y-licencias.md` | Dice medio 0,8925 frente a la meta de 0,80, en los 5 casos de prueba | Parcial (cumple en la evaluación preliminar; formal en el ciclo 5) |
| **RR-01** Procesar un estudio en 2 minutos o menos | 5.1 | 1408 | `scripts/medir_rendimiento.py`, `reports/rendimiento/rendimiento_1408_2026-11-07.md` | Medición en CPU (prostate_13, 3 repeticiones): 16,0 s en frío, 13,1 s y 15,1 s; pico RSS 2 048 MB | Cumple en CPU; medición en GPU pendiente (Colab, ciclo 5) |
| **RA-02** Cada requisito vinculado a necesidad, entregable, prueba e interesado | 6.4 | H003, 1310, 1414 | `docs/gestion/trazabilidad.md`, `docs/ejecucion/fuentes/1.3.1.2_matriz_trazabilidad.md` | Revisión en el cierre del ciclo 3 | En curso |

## Resumen de estados

| Estado | Requisitos |
|---|---:|
| Verificado | 6 |
| En curso / sin implementar | 2 |
| Parcial | 3 |
| Planificado | 5 |

## Notas

- RR-01 se cumple en CPU (16,0 s en frío frente a 120 s); la medición en GPU queda para Colab en el ciclo 5.
- D-007 (`.eval()`) quedó con prueba de regresión.
