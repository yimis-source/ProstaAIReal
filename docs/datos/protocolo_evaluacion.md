# Protocolo de evaluación del modelo de segmentación (tarea 1409)

Responsable: Juan David Riascos Erazo (Analista). Fecha: 02/11/2026. Ciclo 3.
Se escribe **antes** de tener predicciones, para que la forma de medir no se ajuste a los resultados.

## 1. Qué se mide y contra qué

| Elemento | Decisión |
|---|---|
| Requisitos | RF-23 (Dice e IoU por caso y promedio, con condiciones y limitaciones) y RF-24 (Dice medio ≥ 0,80 o documentar la brecha) |
| Conjunto | Solo los **5 casos de prueba** de MSD Task05 según `entrenamiento/division_task05.json` (semilla 2026, huella `728fae86…`), verificada por el Tester en el ciclo 2 |
| Conjuntos excluidos | Prostate158 (con él se entrenó el modelo base: no es un conjunto «no visto») y PROMISE12 (comparte pacientes con Task05, ver `reports/division/`) |
| Imagen | Canal 0 (T2) del NIfTI 4D de Task05 |
| Referencia | Unión de las etiquetas > 0 (zona periférica + zona de transición) = próstata completa |
| Espacio de medida | La rejilla de la **imagen original**: la máscara del modelo se devuelve a esa rejilla por vecino más cercano antes de medir |
| Métricas | Dice = 2·\|P∩G\| / (\|P\|+\|G\|); IoU = \|P∩G\| / \|P∪G\|; ambos vacíos ⇒ 1 |
| Resumen | Media y desviación típica muestral (n−1); se reporta además el peor caso |
| Tiempo | Segundos por caso de todo el pipeline, incluida la carga de pesos en el primer caso |

## 2. Reglas para que la evaluación sea honesta

1. El conjunto de prueba **no** se usa para elegir modelo, época, umbral ni posproceso. Esas decisiones, si hacen falta, se toman con el conjunto de validación.
2. La evaluación usa la **misma ruta de inferencia** que usará la aplicación (`build_pipeline`), no un script aparte.
3. Antes de evaluar, el Tester verifica la división (sin pacientes repetidos y huella igual a la versionada) y lo deja en el informe.
4. El informe registra: modelo, versión y SHA-256 de los pesos; hardware y versiones de software; huella de la división; tabla por caso; veredicto frente a 0,80; limitaciones (incluido el posible sesgo por los datos de entrenamiento del modelo base).
5. Si se repite la evaluación con otro modelo (p. ej. un ajuste fino), se comparan **por caso** y en el mismo hardware. Regla de adopción: el modelo ajustado solo reemplaza al preentrenado si su Dice medio en estos 5 casos es mayor.
6. Los 32 casos de Task05 se pueden evaluar como **dato adicional** (`--todos`), pero no cuentan para RF-24 porque incluyen casos de entrenamiento y validación.

## 3. Cómo se ejecuta

```bash
backend/.venv/bin/python -m entrenamiento.evaluar --modelo prostate_mri_anatomy
```

Salida: `reports/evaluacion/evaluacion_<modelo>_<fecha>.md` y `.csv`.

## 4. Análisis de errores (después de la evaluación)

- Ordenar los casos por Dice y revisar visualmente los dos más bajos (3D Slicer, máscara sobre T2).
- Clasificar cada error: falso positivo fuera de la glándula, subsegmentación en base o ápex, desplazamiento por remuestreo, diferencia de criterio del anotador.
- Registrar los defectos encontrados en el LOGD y, si cambian la ruta de inferencia, repetir la evaluación completa.
