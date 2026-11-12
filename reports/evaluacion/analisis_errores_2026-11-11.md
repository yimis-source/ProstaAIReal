# Análisis de errores de la ROI por caso (2026-11-11)

Uso académico y experimental; no es una evaluación clínica ni diagnóstica.

Generado con `scripts/analizar_errores.py` (los 4 casos de menor Dice de `evaluacion_prostate_mri_anatomy_2026-11-11_32casos.csv`). Máscaras en la rejilla original; VP/FP/FN en vóxeles; volúmenes en ml.

| Caso | Conjunto | Dice | Forma | Espaciado (mm) | Ref. (ml) | Pred. (ml) | VP | FP | FN | Componentes pred. | Mayor región falsa (vóx.) | Distancia al borde del FOV (mm) | Cortes ref. | Cortes pred. |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| prostate_07 | entrenamiento | 0.2255 | 320×320×20 | 0.62×0.62×3.60 | 16.0 | 43.7 | 4792 | 26301 | 6607 | 9 | 24225 | 13.1 | 9–17 | 1–19 |
| prostate_10 | entrenamiento | 0.8080 | 320×320×20 | 0.62×0.62×3.60 | 38.6 | 50.7 | 25675 | 10410 | 1795 | 1 | 9240 | 74.8 | 4–14 | 0–16 |
| prostate_28 | prueba | 0.8320 | 384×384×11 | 0.60×0.60×4.00 | 47.3 | 40.7 | 25051 | 2807 | 7312 | 1 | 2761 | 109.6 | 0–9 | 0–9 |
| prostate_46 | entrenamiento | 0.8322 | 320×320×20 | 0.62×0.62×3.60 | 35.1 | 45.8 | 23919 | 8634 | 1015 | 1 | 7262 | 82.6 | 5–15 | 4–17 |
## Lectura de los resultados (Juan Riascos, Analista)

- **prostate_07 (Dice 0,2255, conjunto de entrenamiento).** La próstata es pequeña (16,0 ml) y el modelo sí la
  encuentra (4 792 vóxeles coinciden con la referencia), pero además predice una región falsa de **24 225 vóxeles**
  cuyo centro está a 13,1 mm del borde del campo de visión, es decir, fuera de la glándula, en tejido periférico.
  La predicción ocupa los cortes 1–19, frente a 9–17 de la referencia. Como el posproceso conserva la componente
  más grande de cada etiqueta, esa región falsa desplaza a la glándula en una de las zonas y el Dice se desploma.
  Es una limitación del modelo preentrenado ante el cambio de dominio (Prostate158 → Task05), no un error de la
  ruta de inferencia ni de la ROI: la verificación de la ROI (`reports/roi/`) confirma forma, afín y Dice.
- **prostate_10 y prostate_46 (Dice ≈ 0,81–0,83, entrenamiento).** Sobresegmentación: los falsos positivos
  (10 410 y 8 634 vóxeles) forman una sola región pegada a la glándula y la predicción se extiende más cortes que
  la referencia hacia la base y el ápex (0–16 frente a 4–14; 4–17 frente a 5–15). Coincide con la diferencia de
  criterio de anotación en los extremos que ya anotamos como limitación.
- **prostate_28 (Dice 0,8320, prueba).** Subsegmentación: más falsos negativos (7 312) que falsos positivos
  (2 807); el volumen predicho (40,7 ml) es menor que el de referencia (47,3 ml). Es el único de los cuatro que
  está en el conjunto de prueba y tiene cortes de 4 mm con solo 11 cortes.
- **Conclusión:** de los 32 casos, solo prostate_07 queda muy por debajo de 0,80, y está en entrenamiento, no en
  prueba; el Dice de prueba (0,8925) no cambia. Mejoras posibles, a evaluar con el conjunto de **validación** y
  aplicando lo mismo en entrenamiento, evaluación e inferencia: ajuste fino con Task05 (ya preparado en
  `entrenamiento/`) o un posproceso que prefiera la componente más cercana al centro del campo de visión. Se
  propone como solicitud de cambio para el ciclo 5 (evaluación técnica).
