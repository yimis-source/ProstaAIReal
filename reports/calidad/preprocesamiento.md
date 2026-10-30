# Preprocesamiento de las imágenes

| Campo | Valor |
|---|---|
| Tarea | 1305 |
| Responsable | Yeison Bolaños Ruiz (Desarrollador) |
| Fecha | 29/10/2026 |
| Versión | 1.0 |

## Qué hace `scripts/preprocesar.py`

Prepara un volumen NIfTI (canal 0 = T2 si es 4D) con MONAI, en este orden:

1. Orientación **RAS**.
2. Remuestreo a vóxeles isotrópicos de **0,5 mm**, interpolación bilineal.
3. Escala de intensidad a **[0, 1]**.
4. Normalización: resta de la media y división por la desviación típica.

Los parámetros son los de la configuración de inferencia del modelo preentrenado candidato `prostate_mri_anatomy` (MONAI Model Zoo). La misma preparación debe usarse en entrenamiento e inferencia; en el ciclo 3 pasa al paquete del pipeline.

Uso: `python scripts/preprocesar.py datos/convertidos/msd_task05/prostate_00_t2.nii.gz salida.nii.gz` (opciones `--espaciado`, `--sin-normalizar`).

## Prueba (CPU, sin GPU)

Equipo: AMD Ryzen 5 5600G, sin GPU. Tres casos del NIfTI convertido:

| Caso | Forma preparada | Tiempo (s) | Tamaño comprimido (MB) | Media | Desv. |
|---|---|---:|---:|---:|---:|
| prostate_00 | (384, 384, 113) | 3,9 | 60,2 | 0,000 | 1,000 |
| prostate_07 | (400, 400, 138) | 3,5 | 79,0 | 0,000 | 1,000 |
| prostate_16 | (400, 400, 138) | 3,4 | 79,0 | 0,000 | 1,000 |

Tras normalizar, la media es 0,000 y la desviación 1,000 en los tres casos.

## Conclusión

- El remuestreo a 0,5 mm multiplica el número de vóxeles: los cortes de 3,6–4 mm pasan a 0,5 mm, y cada volumen pasa a más de 100 cortes de 384x384 o 400x400.
- Un volumen así no cabe cómodamente en memoria para inferir de una vez, por lo que en el ciclo 3 se hará la inferencia por **ventana deslizante**.
- El tiempo por caso es de unos 3–4 s en CPU, aceptable.
- Los volúmenes preparados **no se guardan en el repo** (pesan 60–79 MB cada uno y los datos no se versionan).
