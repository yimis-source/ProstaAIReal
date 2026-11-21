# Verificación visual de la alineación en 3D Slicer

| Campo | Valor |
|---|---|
| Tarea | 1507, repetida en 1606 |
| Responsable | Juan David Riascos Erazo (Analista) con Sergio Gabriel Meneses Silva (Diseñador) |
| Fecha | 20/11/2026 |
| Versión | 1.1 |

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

Resultado del informe: todas las comprobaciones se cumplen en los 5 casos, y las cabeceras no contienen texto. En la revisión del ciclo 5 se volvieron a generar las máscaras y el Dice de cada caso coincidió con esta tabla.

## 4. Observaciones visuales (ciclo 5)

- En los 5 casos, la máscara del modelo y la referencia ocupan la misma zona; en los cortes revisados no se vio desplazamiento ni giro entre ellas.
- Los bordes tienen escalones en sagital y coronal por el grosor de los cortes; no se interpretó como error de alineación.
- En prostate_28 (11 cortes, el caso con menor Dice, 0,8320) las dos máscaras ocupan la misma zona; las diferencias que se vieron son de tamaño en algunos cortes (ver `revision_slicer_predicciones.md`).

## 5. Límites

- Revisión visual de 5 casos y algunos cortes por caso, hecha por personas que no son profesionales de la salud.
- Solo se compararon la máscara del modelo y la referencia entre sí.
- No se verificó qué canal (T2 o ADC) se cargó.
- No añade métricas: la prueba objetiva de la alineación son las comprobaciones automáticas de la sección 3.