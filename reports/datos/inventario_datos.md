# Inventario de datos descargados

Generado con `scripts/inventario_datos.py`. El detalle por archivo (con SHA-256) está en
`inventario_datos.csv`. Los datos no se versionan (`datos/` está en `.gitignore`).

| Conjunto | Casos | Archivos de imagen | Metadatos | No esperados | Tamaño (MB) |
|---|---|---:|---:|---:|---:|
| MSD Task05_Prostate | 32 con máscara (imagesTr/labelsTr) + 16 sin máscara (imagesTs) | 80 | 1 | 0 | 239.8 |
| Prostate158 (entrenamiento) | 139 | 844 | 2 | 0 | 2784.6 |
| PROMISE12 (entrenamiento) | 50 | 200 | 0 | 1 | 786.5 |
| PROMISE12 (prueba) | 30 | 120 | 0 | 1 | 466.6 |

## Archivos no esperados

- PROMISE12 (entrenamiento): `a.py` (no se abre ni se ejecuta; no forma parte de los datos)
- PROMISE12 (prueba): `a.py` (no se abre ni se ejecuta; no forma parte de los datos)
