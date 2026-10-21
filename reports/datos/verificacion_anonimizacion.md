# Verificación de anonimización de los datos descargados

Generado con `scripts/verificar_anonimizacion.py` (solo lectura; no modifica los datos).

| Conjunto | NIfTI revisados | MetaImage revisados | DICOM | Texto libre en cabeceras | Claves no estándar (.mhd) | Nombres no neutros | Fechas en nombres |
|---|---:|---:|---:|---|---|---:|---:|
| MSD Task05_Prostate | 80 | 0 | 0 | descrip = «5.0.10» (80) | ninguna | 0 | 0 |
| Prostate158 (entrenamiento) | 844 | 0 | 0 | ninguno | ninguna | 0 | 0 |
| PROMISE12 (entrenamiento) | 0 | 100 | 0 | ninguno | ninguna | 0 | 0 |
| PROMISE12 (prueba) | 0 | 60 | 0 | ninguno | ninguna | 0 | 0 |


**Resultado:** SIN HALLAZGOS.
