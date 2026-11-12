# Matriz de trazabilidad de implementación · Prosta-AI

**Versión:** T4 · **Fecha:** 12/11/2026 · **Autor:** Yimis Buenaventura (rol de Trazabilidad) · Cierre del ciclo 4 (`v0.4-ciclo4`)

Relaciona cada requisito de la SRS (`docs/ejecucion/fuentes/1.3.1.1_SRS_requisitos_ISO29148.md`) y su número en la matriz de requisitos (`1.3.1.2_matriz_trazabilidad.md`) con la tarea que lo implementa, la evidencia en el repositorio, la prueba y el estado. Solo se listan evidencias que existen en esa fecha.

Se agregan la etapa ROI, la imagen con aviso, los textos y el análisis de errores. Pruebas: 58 en `backend/tests` + 20 en la raíz.

| Requisito (SRS) | Matriz | Tarea | Evidencia en el repositorio | Prueba | Estado |
|---|---|---|---|---|---|
| **RC-03** División por paciente en entrenamiento, validación y prueba, sin repetidos; se verifica antes de entrenar | 3.3 | 1303, 1304 | `entrenamiento/division.py`, `entrenamiento/division_task05.json`, `scripts/verificar_fuga.py`, `reports/division/verificacion_division.md` | `tests/test_division.py`; informe del Tester: 22 / 5 / 5 sin pacientes repetidos y 12 casos compartidos con PROMISE12 (D-005 corregido) | Verificado |
| **RN-01** Solo datos públicos y anónimos; sin datos personales (Ley 1581/2012, Decreto 1377/2013) | 2.1, 2.2 | 1205, 1203; 1404; 1503 | `reports/datos/verificacion_anonimizacion.md`, `docs/datos/fichas/`, `backend/prosta_ai/pipeline/io.py` | `tests/test_anonimizacion.py`; `test_pipeline_io.py`; `test_pipeline_roi.py` (`test_roi_sin_descripcion_en_cabecera`) | Verificado para datos y salidas del pipeline (aplicación en el ciclo 6) |
| **RF-10** Excluir y registrar con motivo toda imagen que no pase el control de calidad | 3.2 | 1301; 1404 | `scripts/control_calidad.py`, `reports/calidad/control_calidad.md`, `backend/prosta_ai/pipeline/validators.py` | `tests/test_control_calidad.py`; `backend/tests/pipeline/test_pipeline_validadores.py` y `test_pipeline_io.py` (`test_nifti_truncado_se_rechaza`) | Verificado (scripts y pipeline) |
| **RF-09** Mismas transformaciones de preparación en el entrenamiento y en la inferencia | 3.2, 4.2 | 1302, 1305; 1406 | `scripts/preprocesar.py`, `backend/prosta_ai/pipeline/preparation.py`, `entrenamiento/entrenar.py`, `docs-tecnicos/modelo-y-licencias.md` | `backend/tests/entrenamiento/test_entrenar.py` (`preparacion.json` releíble); `backend/tests/pipeline/test_pipeline_roi_modelo.py` | Verificado (inferencia y ajuste fino usan la misma preparación) |
| **RC-04** Sin cuentas, roles ni permisos más allá del acceso básico | 4.7 | — | Sin código de cuentas ni permisos (aún no hay aplicación) | Revisión por ausencia | Sin implementar; se verifica en el ciclo 6 |
| **RF-11** Segmentar la próstata con un modelo 3D (tipo U-Net) y entregar la máscara | 3.4 | 1402, 1405, 1407, 1412 | `backend/prosta_ai/pipeline/segmentation.py`, `backend/prosta_ai/pipeline/factory.py`, `scripts/descargar_modelo.py`, `docs-tecnicos/modelo-y-licencias.md` | `backend/tests/pipeline/test_pipeline_roi_modelo.py` (incluye `assert not modelo.training`, D-007); revisión de máscaras en 3D Slicer (`docs/datos/revision_slicer_predicciones.md`) | Verificado (CPU, modelo preentrenado `prostate_mri_anatomy`) |
| **RF-12** Generar la ROI y dejarla alineada con la imagen original | 4.3 | 1407, 1503 | `backend/prosta_ai/pipeline/roi.py`, `backend/prosta_ai/pipeline/base.py` (etapa ROI), `scripts/verificar_roi.py`, `reports/roi/verificacion_roi_2026-11-11.md` | `backend/tests/pipeline/test_pipeline_roi.py`; en 5 casos: forma y afín iguales, máscara binaria, Dice de la máscara guardada igual al del informe; revisión en 3D Slicer (`docs/datos/verificacion_alineacion_slicer.md`) | Verificado |
| **RF-13** Mostrar la ROI superpuesta y alineada sobre la imagen | 4.3 | 1502, 1504 | `backend/prosta_ai/pipeline/visualizacion.py`, `scripts/generar_roi.py`, `docs/diseno/visor_roi.md` | `backend/tests/pipeline/test_pipeline_visualizacion.py` (superposición con el color de la ROI) | Parcial (imagen con superposición; el visor web es del ciclo 6) |
| **RF-14** Comparar la imagen con y sin la máscara | 4.3 | 1502, 1503 | `docs/diseno/visor_roi.md`, `backend/prosta_ai/pipeline/base.py` (guarda `imagen.nii.gz` y `mascara.nii.gz` por separado), `docs/ejecucion/assets/pantallas/cu04_roi.png` | `test_pipeline_visualizacion.py` (`test_corte_sin_roi_en_gris`, `test_imagen_sin_mascara_tambien_lleva_aviso`) | Parcial (la comparación interactiva es del ciclo 6) |
| **RF-15** Aviso de salida experimental en toda salida de resultados | 2.3 | 1504 | `backend/prosta_ai/constantes.py` (`AVISO_EXPERIMENTAL`), `backend/prosta_ai/pipeline/visualizacion.py` | `test_pipeline_visualizacion.py` (`test_aviso_en_banda_inferior_y_ancho_minimo`, `test_aviso_es_el_texto_unico`) | Parcial (imagen de la ROI con aviso; las pantallas son del ciclo 6) |
| **RF-16** Sin lenguaje clínico en ningún texto | 2.3 | 1505 | `docs/diseno/texto_roi.md`, `backend/prosta_ai/constantes.py` | Revisión de lenguaje no clínico en 1505 | Verificado en los textos del ciclo 4 (las pantallas, en el ciclo 6) |
| **RF-17** Explicación junto a cada resultado: qué muestra, métricas y limitaciones | 4.4 | 1505 | `docs/diseno/texto_roi.md` | Revisión del texto en 1505; no hay panel todavía | Parcial (texto en el ciclo 4; panel en el ciclo 6) |
| **RF-23** Dice e IoU por caso y promedio en el conjunto de prueba, con condiciones y limitaciones | 3.5 | 1409, 1411, 1508 | `docs/datos/protocolo_evaluacion.md`, `reports/evaluacion/evaluacion_prostate_mri_anatomy_2026-11-06.md`, `reports/evaluacion/evaluacion_prostate_mri_anatomy_2026-11-11_32casos.md`, `reports/evaluacion/analisis_errores_2026-11-11.md`, `scripts/analizar_errores.py` | Prueba: Dice 0,8925 ± 0,0340. Dato adicional con 32 casos: Dice 0,8736 ± 0,1222; prostate_07 con 0,2255 | Parcial (evaluación preliminar y análisis por caso; la formal es del ciclo 5) |
| **RF-24** Dice medio ≥ 0,80 en el conjunto de prueba; si no, documentar la brecha | 3.5 | 1411, 1508 | `reports/evaluacion/evaluacion_prostate_mri_anatomy_2026-11-06.md`, `reports/evaluacion/analisis_errores_2026-11-11.md` | Dice medio 0,8925 en prueba frente a la meta de 0,80 | Parcial (cumple en la evaluación preliminar; formal en el ciclo 5) |
| **RR-01** Procesar un estudio en 2 minutos o menos | 5.1 | 1408 | `scripts/medir_rendimiento.py`, `reports/rendimiento/rendimiento_1408_2026-11-07.md` | Medición en CPU (prostate_13, 3 repeticiones): 16,0 s en frío, 13,1 s y 15,1 s; pico RSS 2 048 MB | Cumple en CPU; medición en GPU pendiente (Colab, ciclo 5) |
| **RA-02** Cada requisito vinculado a necesidad, entregable, prueba e interesado | 6.4 | H003, 1310, 1414, 1510 | `docs/gestion/trazabilidad.md`, `docs/ejecucion/fuentes/1.3.1.2_matriz_trazabilidad.md` | Revisión en el cierre del ciclo 4 | En curso |

## Resumen de estados

| Estado | Requisitos |
|---|---:|
| Verificado | 8 |
| En curso / sin implementar | 2 |
| Parcial | 6 |

## Notas

- D-006 (rótulo «Ejecutar» en lugar de «Procesar») sigue abierto y se corrige en el ciclo 6.
- Lo que falta para cerrar RF-13 a RF-17 es el visor y las pantallas del ciclo 6.
- La evaluación formal (RF-23 y RF-24), la medición en GPU y la decisión del ajuste fino son del ciclo 5.
