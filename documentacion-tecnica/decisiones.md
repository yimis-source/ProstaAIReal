# Decisiones técnicas

| Decisión | Por qué | Dónde consta |
|---|---|---|
| **MONAI 1.4.0 + PyTorch 2.5.1** | MONAI aporta transformaciones médicas, `UNet` 3D y `SlidingWindowInferer`; es el marco con el que se publicó el modelo usado. | `backend/pyproject.toml`, `backend/prosta_ai/pipeline/preparation.py`, `segmentation.py` |
| **Modelo preentrenado `prostate_mri_anatomy` v0.3.6 sin ajuste** | Desde el 04/11/2026: delimita bien la glándula, corre en CPU en < 20 s y responde al riesgo 1 del Acta. Pesos Apache 2.0 (autores de Prostate158); MSD Task05 CC BY-SA 4.0. Prostate158 no se usa para evaluar porque con él se entrenó el modelo. | `docs-tecnicos/modelo-y-licencias.md`, `scripts/descargar_modelo.py` |
| **Formato NIfTI** | Los conjuntos usados se unificaron a NIfTI en el ciclo 2; nibabel conserva la afín RAS. DICOM se deja para la carga de estudios. | `backend/prosta_ai/pipeline/io.py`, `scripts/convertir_nifti.py` |
| **División por paciente 70/15/15, semilla 2026** | Evitar fuga de pacientes (RC-04). En Task05 un caso = un paciente. Huella SHA-256 versionada. | `entrenamiento/division.py`, `entrenamiento/division_task05.json`, `reports/division/verificacion_division.md` |
| **Misma preparación en entrenamiento e inferencia (RF-09)** | Un único `preparacion.json` derivado de `configs/inference.json` del bundle; `entrenar.py` importa la misma `PreparationConfig`. | `backend/prosta_ai/pipeline/preparation.py`, `entrenamiento/entrenar.py` |
| **Vecino más cercano para devolver la ROI** | Mantiene la máscara binaria y en la rejilla exacta (forma y afín) de la imagen original, donde se mide Dice/IoU (RF-12). | `backend/prosta_ai/pipeline/roi.py`, `docs/datos/protocolo_evaluacion.md` |
| **Evaluación con la misma ruta de la aplicación** | `evaluar.py` usa `build_pipeline`; el conjunto de prueba no se usa para elegir modelo ni posproceso. | `docs/datos/protocolo_evaluacion.md`, `entrenamiento/evaluar.py` |
| **CPU; GPU solo en Colab** | Ningún equipo del grupo tiene GPU NVIDIA; torch se instala desde el índice CPU. El ajuste fino se prevé en Colab. | `backend/pyproject.toml` (`pytorch-cpu`), `docs/entorno_desarrollo.md`, `entrenamiento/Prosta_AI_entrenamiento.ipynb` |
| **Aviso impreso en toda imagen exportada** | RF-15: `AvisoDecorator` envuelve el renderizador de exportación; el texto vive en una sola constante. | `backend/prosta_ai/constantes.py`, `backend/prosta_ai/pipeline/visualizacion.py` |
| **Límites de 50 MB por archivo y 150 MB por estudio (previstos)** | Requisito RF-03 de la carga de archivos; se implementará con los validadores de carga de la aplicación (ciclo 6). | `docs/ejecucion/01_requisitos.md`, docstring de `validators.py` |
| **Datos y pesos fuera de git** | Ley 1581 de 2012 y licencias de los conjuntos. | `.gitignore` |
