# Informe de métricas y límites — ciclo 5 (tarea 1605)
> Aviso: resultados académicos y experimentales; no son diagnóstico ni tienen uso clínico.

## 1. Condiciones de la evaluación

- Modelo: `prostate_mri_anatomy` del MONAI Model Zoo, versión 0.3.6, sin ajuste fino. SHA-256 de los pesos: `3c18e4c658bb088f551b1d63219ef8340fe6256d016c75fc140d3da49dda696d`.
- Conjunto de prueba: los 5 casos de MSD Task05 de `entrenamiento/division_task05.json`, con división por paciente (semilla 2026, huella `728fae869f02e7c7…`): `prostate_13`, `prostate_17`, `prostate_28`, `prostate_34` y `prostate_44`.
- Equipo: CPU, sin GPU; hardware: AMD64 Family 25 Model 117 Stepping 2, AuthenticAMD; 8 hilos de torch; Windows 11. Software: Python 3.12.16, torch 2.5.1+cpu, MONAI 1.4.0.
- Fecha de la evaluación: 19/11/2026. Ruta de ejecución: `build_pipeline`, la misma de la aplicación. Imagen: canal 0 (T2) del NIfTI 4D; referencia: unión de las etiquetas > 0. Métricas calculadas en la rejilla original y desviación típica muestral (n−1).

## 2. Métricas en los 5 casos de prueba

| Caso | Dice | IoU | HD95 (mm) | Distancia media de superficie (mm) |
|---|---:|---:|---:|---:|
| prostate_13 | 0.9012 | 0.8201 | 3.60 | 1.03 |
| prostate_17 | 0.9097 | 0.8344 | 3.54 | 0.80 |
| prostate_28 | 0.8320 | 0.7123 | 5.69 | 2.01 |
| prostate_34 | 0.9105 | 0.8356 | 4.00 | 1.15 |
| prostate_44 | 0.9090 | 0.8332 | 3.60 | 0.86 |
| **Media ± desviación típica** | **0.8925 ± 0.0340** | **0.8071 ± 0.0534** | **4.09 ± 0.92** | **1.17 ± 0.49** |

## 3. Preentrenado frente a ajustado

La comparación queda pendiente: a la fecha de este informe no hay resultados del modelo ajustado (tarea 1603). Todas las cifras corresponden al modelo preentrenado.

## 4. Análisis de errores

- Caso con el Dice más bajo: `prostate_28` (0.8320). Caso con el HD95 más alto: `prostate_28` (5.69 mm). Coinciden en el mismo caso, que también tiene el IoU más bajo (0.7123).
- El archivo B atribuye los errores en base y ápex a sobresegmentación: en `prostate_10` y `prostate_46` los falsos positivos forman una sola región pegada a la glándula y la predicción se extiende más cortes que la referencia hacia la base y el ápex (0–16 frente a 4–14; 4–17 frente a 5–15). Lo relaciona con la diferencia de criterio de anotación en los extremos, registrada como limitación. En `prostate_07` la predicción ocupa los cortes 1–19 frente a 9–17 de la referencia, y una región falsa de 24 225 vóxeles desplaza a la glándula. En `prostate_28` describe subsegmentación (7 312 falsos negativos frente a 2 807 falsos positivos), con los mismos cortes anotados (0–9).
- Un HD95 alto significa que hay puntos del borde lejos de la referencia aunque el Dice sea bueno: HD95 mide distancias entre superficies (percentil 95), no solapamiento de volúmenes. Por eso puede haber un Dice alto y, aun así, zonas del contorno mal ubicadas.

## 5. Dato adicional: 32 casos

- Media en los 32 casos: Dice 0.8736 ± 0.1222, IoU 0.7892 ± 0.1304, HD95 7.51 ± 18.99 mm y distancia media de superficie 3.01 ± 9.90 mm.
- Caso `prostate_07`: Dice 0.2255, IoU 0.1271, HD95 111.46 mm y distancia media de superficie 57.23 mm.
- **Incluye casos de entrenamiento y validación, así que NO cuenta para la meta.**

## 6. Limitaciones

- Solo 5 casos de prueba: la media y la desviación son sensibles a un solo caso.
- Cambio de dominio: los pesos se entrenaron con Prostate158 (T2, 3 T, otro equipo) y Task05 tiene cortes gruesos (4 mm), otra resolución y otro protocolo; el remuestreo no añade detalle.
- Posible sesgo del preentrenado: no se puede garantizar que los datos de Task05 estén ausentes del preentrenamiento del modelo base, lo que sobreestimaría las cifras.
- Un solo anotador por caso: no hay medida de variabilidad entre observadores, en especial en base y ápex.
- Tiempos medidos en un solo equipo (CPU, Windows 11): no representan otro hardware.

## 7. Veredicto (RF-24)

Dice medio en prueba: 0,8925 ± 0,0340 frente a la meta de 0,80: cumple.

## 8. Archivos de origen

- A: `reports/evaluacion/evaluacion_prostate_mri_anatomy_2026-11-19_32casos.md` y su `.csv` (condiciones, tabla de 5 casos y dato adicional de 32).
- B: `reports/evaluacion/analisis_errores_2026-11-11.md` (análisis por caso, base y ápex).
- C: `docs/datos/protocolo_evaluacion.md` (reglas de evaluación y meta Dice ≥ 0,80).
- D: `docs-tecnicos/modelo-y-licencias.md` (modelo empleado y ausencia de ajuste fino).
