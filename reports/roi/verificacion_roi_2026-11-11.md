# Verificación de la ROI en el conjunto de prueba (2026-11-11)

Uso académico y experimental; no es una evaluación clínica ni diagnóstica.

Generado con `scripts/verificar_roi.py`. Las imágenes y máscaras se crearon en una carpeta temporal y se borraron al terminar; aquí solo se publican cifras.

| Caso | Forma | Forma igual | Afín igual | Binaria | Vóxeles ROI | Volumen (ml) | Cabecera sin texto | Dice (pipeline) | Dice (máscara guardada) | Dice (informe) | Coincide | Corte PNG | Etapa ROI (s) |
|---|---|:-:|:-:|:-:|---:|---:|:-:|---:|---:|---:|:-:|---:|---:|
| prostate_13 | 320×320×20 | sí | sí | sí | 22172 | 31.2 | sí | 0.9012 | 0.9012 | 0.9012 | sí | 12 | 0.18 |
| prostate_17 | 320×320×20 | sí | sí | sí | 25485 | 35.8 | sí | 0.9097 | 0.9097 | 0.9097 | sí | 11 | 0.18 |
| prostate_28 | 384×384×11 | sí | sí | sí | 27858 | 40.7 | sí | 0.8320 | 0.8320 | 0.8320 | sí | 6 | 0.13 |
| prostate_34 | 320×320×15 | sí | sí | sí | 44562 | 64.2 | sí | 0.9105 | 0.9105 | 0.9105 | sí | 8 | 0.12 |
| prostate_44 | 320×320×20 | sí | sí | sí | 30938 | 43.5 | sí | 0.9090 | 0.9090 | 0.9090 | sí | 12 | 0.18 |

Informe de evaluación usado para comparar: `reports/evaluacion/evaluacion_prostate_mri_anatomy_2026-11-06.csv`.

**Resultado:** todas las comprobaciones se cumplen (5 casos).

La alineación visual (ROI sobre la imagen en 3D Slicer) se revisa aparte y se documenta en `docs/datos/` por el Analista y el Diseñador.
