# Evaluación del modelo `prostate_task05_ft` (2026-11-21)

Uso académico y experimental; no es una evaluación clínica ni diagnóstica.

## Condiciones

- Modelo: prostate_task05_ft, versión 1.0.0.
- SHA-256 de los pesos: `59676d68a88ead47ece3a04cd996ab4f7ca7a5e009d192bfe420b52e6268dcb7`.
- Ruta de ejecución: `build_pipeline` (la misma que usará la aplicación), imagen = canal 0 (T2) del NIfTI 4D, referencia = etiquetas > 0 (zona periférica + zona de transición).
- Métricas calculadas en la rejilla de la imagen original (máscara devuelta al espacio original).
- Dispositivo: cuda. Hardware: Intel(R) Xeon(R) CPU @ 2.00GHz; 1 hilos de torch; Tesla T4; Linux 6.6.159+.
- Software: Python 3.11.18, torch 2.5.1+cu124, MONAI 1.4.0.
- División: `entrenamiento/division_task05.json`, semilla 2026, {'entrenamiento': 22, 'validacion': 5, 'prueba': 5}, huella `728fae869f02e7c7…`.
- Conjunto evaluado: prueba (5 casos: prostate_13, prostate_17, prostate_28, prostate_34, prostate_44).
- Tiempo por caso: todo el pipeline (lectura, preparación, segmentación, ROI en el espacio original), incluida la carga de los pesos, que se hace una sola vez en el primer caso.
- Desviación: típica muestral (n-1).

## Resultados sobre el conjunto de prueba

| Caso | Dice | IoU | HD95 (mm) | Distancia media (mm) | Tiempo (s) |
|---|---:|---:|---:|---:|---:|
| prostate_13 | 0.8451 | 0.7318 | 4.00 | 1.55 | 7.7 |
| prostate_17 | 0.8846 | 0.7930 | 5.00 | 1.18 | 6.4 |
| prostate_28 | 0.8455 | 0.7324 | 4.43 | 1.84 | 5.5 |
| prostate_34 | 0.9215 | 0.8543 | 4.00 | 0.98 | 4.9 |
| prostate_44 | 0.8706 | 0.7709 | 3.60 | 1.17 | 6.7 |
| **Media ± desv.** | **0.8735 ± 0.0317** | **0.7765 ± 0.0508** | **4.21 ± 0.53** | **1.34 ± 0.35** | **6.2 ± 1.1** |

## Comparación con la meta (RF-24)

Se **cumple** la meta (Dice medio 0.8735 >= 0.80).
El caso más bajo es prostate_13 (Dice 0.8451).

## Limitaciones

- **Posible sesgo (sobreestimación).** Si el modelo se entrenó o ajustó con datos que incluyen casos de prueba, la evaluación está sobreestimada; revise `metadatos.json` y la división del modelo.
- Con solo 5 casos de prueba la media tiene mucha incertidumbre; un caso malo mueve mucho el promedio (ver la desviación típica).
- Cambio de dominio: los pesos se entrenaron con Prostate158 (T2, 3 T, hospital distinto) y Task05 tiene cortes gruesos (4 mm), otra resolución y otro protocolo; el remuestreo a 0,5 mm es por interpolación y no añade detalle.
- Las etiquetas de Task05 son zona periférica y de transición; la próstata completa es su unión, mientras el modelo se entrenó para dos zonas. Los criterios de delimitación de los anotadores pueden diferir (p. ej. en base y ápex).
- Un solo conjunto público y un solo observador por caso (sin variabilidad entre observadores).
- Los tiempos dependen del equipo; no representan el rendimiento en otro hardware.
- No hay validación clínica ni externa a estos datos públicos.
