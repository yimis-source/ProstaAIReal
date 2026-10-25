# Tamaños, espaciado y casos de los conjuntos

Generado con `scripts/analizar_geometria.py`. Detalle por caso en `geometria_<conjunto>.csv`.
Volumen de próstata = vóxeles con etiqueta > 0 × volumen del vóxel (máscara del lector 1 en Prostate158).

| Conjunto | Casos | Formas (más frecuente) | Canales | Espaciado en plano (mm) | Grosor de corte (mm) | Cortes | Orientaciones | Volumen próstata (mL) |
|---|---:|---|---|---|---|---|---|---|
| msd_task05 | 32 | 320x320x20 (8 formas distintas) | 2 | 0.600–0.750 (mediana 0.625) | 3.00–4.00 (mediana 3.60) | 11–24 (mediana 20) | RAS (32) | 16.0–315.4 (mediana 62.0) |
| prostate158 | 139 | 270x270x24 (15 formas distintas) | 1 | 0.272–0.469 (mediana 0.402) | 3.00–3.00 (mediana 3.00) | 24–40 (mediana 25) | LPS (139) | 14.8–197.4 (mediana 52.4) |
| promise12_entrenamiento | 50 | 320x320x24 (19 formas distintas) | 1 | 0.273–0.750 (mediana 0.613) | 2.20–4.00 (mediana 3.60) | 15–54 (mediana 24) | LPS (50) | 14.9–315.4 (mediana 43.2) |
| promise12_prueba | 30 | 320x320x24 (11 formas distintas) | 1 | 0.273–0.625 (mediana 0.503) | 2.20–3.60 (mediana 3.45) | 19–52 (mediana 24) | LPS (30) | 23.6–114.0 (mediana 39.0) |

## Observaciones sobre MSD Task05 (conjunto principal)

- Próstata más pequeña: prostate_07 (16.0 mL); más grande: prostate_16 (315.4 mL).
- Etiquetas presentes: ['0', '1', '2'] (0 fondo, 1 zona periférica, 2 zona de transición).
- Las imágenes son 4D (canal 0 = T2, canal 1 = ADC); el análisis de forma usa las tres primeras dimensiones.
