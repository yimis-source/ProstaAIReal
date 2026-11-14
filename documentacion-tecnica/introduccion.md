# Introducción

## Propósito

Construir y documentar, con fines académicos, una ruta reproducible de segmentación 3D de la próstata en MRI
(secuencia T2) usando datos públicos y anónimos, y medir su calidad técnica con Dice e IoU.

## Alcance actual (ciclos 1–4)

Lo que existe hoy en el repositorio:

- **Datos:** descarga de MSD Task05_Prostate (CC BY-SA 4.0), inventario con SHA-256, verificación de
  anonimización, análisis de geometría, control de calidad (RF-10), conversión a NIfTI 3D y verificación de fuga
  de pacientes (`scripts/`).
- **División por paciente** 22/5/5 con semilla 2026 (`entrenamiento/division_task05.json`).
- **Pipeline** en el paquete `prosta_ai` (`backend/prosta_ai/pipeline/`): control de calidad, preparación,
  segmentación con la U-Net 3D preentrenada `prostate_mri_anatomy`, ROI en la rejilla original y evaluación.
- **Imagen de la ROI** (PNG) con el aviso experimental impreso (`pipeline/visualizacion.py`).
- **Evaluación y verificación:** Dice/IoU sobre el conjunto de prueba, medición de tiempo y memoria,
  verificación de la ROI y análisis de errores (`reports/`).
- **Ajuste fino** preparado (`entrenamiento/entrenar.py`, cuaderno de Colab), no ejecutado.

Fuera del alcance actual: no hay API web, base de datos, interfaz web (frontend) ni asistente. Son trabajo del
ciclo 6 y posteriores; ver [Limitaciones](limitaciones.md). Todo se usa hoy desde la línea de comandos.
