# Verificación visual de la alineación en 3D Slicer

| Campo | Valor |
|---|---|
| Tarea | 1507 |
| Responsable | Juan David Riascos Erazo (Analista) con Sergio Gabriel Meneses Silva (Diseñador) |
| Fecha | 11/11/2026 |
| Versión | 1.0 |

> **Esto es una revisión visual, sin métricas nuevas.** Complementa las comprobaciones automáticas de `reports/roi/verificacion_roi_2026-11-11.md`. Uso académico y experimental; no es una evaluación clínica ni diagnóstica.

## 1. Qué se verifica

Que `imagen.nii.gz` y `mascara.nii.gz`, generadas con `scripts/generar_roi.py` para cada caso, coinciden en el espacio: la ROI cae sobre la próstata en los tres planos, sin desplazamientos, giros ni inversiones. Casos: prostate_13, prostate_17, prostate_28, prostate_34 y prostate_44 (conjunto de prueba). Los archivos se generan en `salidas/` (ignorada por git) y no se versionan.

## 2. Procedimiento

1. Generar los archivos: `python -I scripts/generar_roi.py --caso prostate_13` (y los demás casos).
2. En 3D Slicer: *File → Add Data* y cargar `imagen.nii.gz` como volumen.
3. Cargar `mascara.nii.gz` como **Segmentation**.
4. Disposición de tres planos (axial, sagital, coronal); con el ratón en un plano, comprobar que el cursor cruzado cae en la misma estructura en los otros dos.
5. Recorrer los cortes y revisar que el contorno de la ROI sigue la glándula y no queda desplazado, girado ni espejado (izquierda/derecha, arriba/abajo).
6. Mirar los extremos (primer y último corte con ROI) y que la ROI no salga del volumen.
7. Cerrar la escena sin guardarla en el repositorio.

## 3. Comprobaciones automáticas citadas (informe 2026-11-11)

| Caso | Forma | Forma y afín iguales a la imagen | Binaria | Vóxeles ROI | Volumen (ml) | Dice máscara guardada = informe |
|---|---|:-:|:-:|---:|---:|---|
| prostate_13 | 320×320×20 | sí | sí | 22 172 | 31,2 | 0,9012 |
| prostate_17 | 320×320×20 | sí | sí | 25 485 | 35,8 | 0,9097 |
| prostate_28 | 384×384×11 | sí | sí | 27 858 | 40,7 | 0,8320 |
| prostate_34 | 320×320×15 | sí | sí | 44 562 | 64,2 | 0,9105 |
| prostate_44 | 320×320×20 | sí | sí | 30 938 | 43,5 | 0,9090 |

Resultado del informe: todas las comprobaciones se cumplen en los 5 casos, y las cabeceras no contienen texto.

## 4. Observaciones visuales

- En los 5 casos la ROI cae sobre la próstata en los tres planos, y el cursor cruzado señala la misma estructura en axial, sagital y coronal. No se vieron desplazamientos, giros ni espejos.
- Los contornos siguen la glándula con los escalones propios de los cortes gruesos al verlos en sagital y coronal; no es un error de alineación.
- En prostate_28 (11 cortes, el caso con menor Dice, 0,8320) la alineación es correcta; la diferencia con la referencia es de forma, no de posición, y ya la recoge el informe de evaluación.
- La ROI no sale del volumen en ningún caso.

## 5. Límites

Revisión visual de 5 casos, por dos personas que no son profesionales de la salud. No añade métricas: la prueba objetiva de la alineación son las comprobaciones automáticas de la sección 3.
