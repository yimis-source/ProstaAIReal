# Limitaciones y mejoras

## Limitaciones actuales

- **Pocos casos de prueba.** La métrica oficial sale de 5 casos (Dice 0,8925 ± 0,0340); un caso malo mueve mucho
  la media.
- **Cambio de dominio.** El modelo se entrenó con Prostate158 (T2, 3 T, otro hospital); Task05 tiene cortes de
  3,6–4 mm y otro protocolo. El remuestreo a 0,5 mm interpola y no añade detalle. Tampoco puede descartarse
  que el preentrenamiento haya visto datos parecidos a Task05 (posible sobreestimación).
- **Caso prostate_07.** Dice 0,2255 (conjunto de entrenamiento): el modelo predice una región falsa de 24 225
  vóxeles fuera de la glándula que el posproceso de mayor componente conserva. No afecta al Dice de prueba.
- **Errores en base y ápex.** prostate_10 y prostate_46 sobresegmentan; prostate_28 (prueba, 11 cortes de
  4 mm) subsegmenta. Diferencias de criterio de anotación entre conjuntos.
- **Solo Dice e IoU**; sin métricas de superficie ni variabilidad entre observadores.
- **Sin aplicación web.** No existen todavía API (FastAPI), base de datos (PostgreSQL), interfaz web (React) ni
  asistente; el uso es solo por línea de comandos.
- **DICOM pendiente.** `load_volume(..., "DICOM")` falla con un mensaje controlado; tampoco hay carga de `.zip`
  ni validación de tamaño (50/150 MB).
- **Ajuste fino no ejecutado.** `entrenamiento/entrenar.py` está preparado (incluye `--prueba-rapida`), pero no se
  ha ejecutado y no hay modelo propio; `NnUNetStrategy` es un marcador sin implementación.
- **Rendimiento medido solo en CPU** (un estudio, un equipo); la medición en GPU está pendiente.
- **Uso no clínico.** Sin validación clínica ni externa; los resultados no son diagnósticos.

## Mejoras previstas (plan TSP)

| Ciclo | Mejora |
|---|---|
| 5 — Evaluación técnica | Medir en GPU (Colab, `--dispositivo cuda`); evaluar con el conjunto de validación un ajuste fino con Task05 o un posproceso que prefiera la componente más cercana al centro del campo de visión; adoptarlo solo si supera el Dice del preentrenado en los mismos 5 casos de prueba. |
| 6 — Aplicación web | API y almacenamiento, base de datos, visor web que reutilice `visualizacion.py`, lectura y desidentificación de DICOM y `.zip`, validadores de formato y tamaño (RF-03), aviso en todas las pantallas de resultados. |
| 7 — Cierre | Documentación final, lecciones aprendidas y acta de aceptación. |
