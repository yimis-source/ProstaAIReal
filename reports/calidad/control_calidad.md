# Control de calidad de imágenes y máscaras (RF-10)

Generado con `scripts/control_calidad.py`. Detalle por caso en `control_calidad.csv`.
Reglas: lectura completa (incluye comprobar que el .gz no esté truncado), 3D/4D, valores finitos, intensidad no constante, ≥ 8 cortes, ≥ 32x32 vóxeles por corte, espaciado positivo; máscara con la misma forma, etiquetas en {0, 1, 2} y no vacía.

| Conjunto | Casos revisados | Aprobados | Excluidos |
|---|---:|---:|---:|
| MSD Task05 (con máscara) | 32 | 32 | 0 |
| MSD Task05 (sin máscara) | 16 | 16 | 0 |
| PROMISE12 (entrenamiento) | 50 | 50 | 0 |
| PROMISE12 (prueba) | 30 | 30 | 0 |

## Casos excluidos

Ninguno.
