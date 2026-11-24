# Código

## Pipeline (`backend/prosta_ai/pipeline/`)

| Módulo | Elementos principales | Lógica |
|---|---|---|
| `stages.py` | `CONTROL_CALIDAD`, `PREPARACION`, `SEGMENTACION`, `ROI`, `EVALUACION`, `STAGES` | Nombres de las etapas en su orden fijo. |
| `errors.py` | `StageError(stage: str, message: str)` | Error controlado con la etapa que falló. |
| `io.py` | `Volume(data, affine, spacing)`; `load_volume(files: list[Path], fmt: str) -> Volume`; `save_nifti(data, affine, path) -> None` | Lee un único NIfTI con nibabel; si es 4D usa el canal 0 (T2). Archivo dañado → `StageError`. `fmt="DICOM"` falla con aviso de ciclo 6. `save_nifti` borra `descrip`, `db_name` y `aux_file`. |
| `validators.py` | `Validator.set_next/handle/check`; `IntegrityValidator`; `MetadataValidator`; `detailed_validation(volume, reference=None)` | Cadena: 3D, valores finitos, intensidad no constante; luego ≥ 8 cortes (`MIN_SLICES`), cortes ≥ 32×32 (`MIN_SIDE`), espaciado positivo y referencia con la misma forma. |
| `progress.py` | `PipelineObserver` (Protocol); `PipelineProgress.attach/notify_start/notify_end/notify_failed`; `TimingRecorder.durations` | Reparte eventos de avance; `TimingRecorder` guarda segundos por etapa. |
| `preparation.py` | `PreparationConfig` (+ `from_json(path)`); `PreparedVolume`; `build_transforms(config) -> Compose`; `prepare_volume(volume, config) -> PreparedVolume` | Lee `preparacion.json` y aplica en MONAI `Orientationd` (RAS) → `Spacingd` (0,5 mm, bilineal) → `ScaleIntensityd` [0, 1] → `NormalizeIntensityd`. Guarda forma y afín originales para revertir. |
| `segmentation.py` | `SegmentationStrategy.segment(prepared) -> np.ndarray`; `PretrainedUNetStrategy(weights_dir, device=None)`; `NnUNetStrategy`; `create_strategy(name, weights_dir)`; `resolve_model_dir(name, weights_dir)` | Carga `UNet(**cfg.red)` una sola vez (`weights_only=True`, `.eval()`), infiere con `SlidingWindowInferer` (96³, lote 4, solape 0,5), hace `argmax`, conserva la mayor componente conexa de cada etiqueta (SimpleITK) y une las etiquetas 1 y 2. `NnUNetStrategy` solo informa que no está disponible. |
| `roi.py` | `mask_to_original_space(mask, prepared, original, stage=ROI) -> np.ndarray` | Para cada vóxel original calcula su índice en el espacio preparado con `inv(prepared.affine) @ original.affine` y toma el vecino más cercano, corte a corte. Resultado uint8 con la forma de la imagen original. |
| `evaluation.py` | `dice(pred, ref) -> float`; `iou(pred, ref) -> float` | Binariza (> 0); formas distintas → `ValueError`; ambas vacías → 1.0. |
| `base.py` | `PipelineInput(files, fmt, reference_files, output_dir)`; `PipelineOutput(image_path, mask_path, dice, iou, durations)`; `PipelineContext`; `BasePipeline.run(inp, progress)`; `Segmentation3DPipeline(strategy, config=None)` | `run` ejecuta las cinco etapas, notifica avance y convierte cualquier excepción no prevista en `StageError`. `build_roi` escribe `imagen.nii.gz` y `mascara.nii.gz` con la misma afín; `evaluate` solo calcula Dice/IoU si hay referencia. |
| `visualizacion.py` | `cargar_volumen(ruta_imagen, ruta_mascara=None)`; `corte_representativo(vol)`; `ImageSliceRenderer`, `MaskSliceRenderer`, `OverlaySliceRenderer`; `AvisoDecorator(renderer, aviso=AVISO_EXPERIMENTAL)`; `renderizador_exportacion()`; `guardar_imagen_roi(ruta_imagen, ruta_mascara, destino, indice=None) -> int` | Normaliza intensidad (percentiles 1–99), elige el corte axial con más ROI, superpone la ROI (#2dd4bf, alfa 0,45) y añade debajo una banda con el aviso (ancho mínimo 512 px). Todo lo exportado pasa por `AvisoDecorator`. |
| `factory.py` | `build_pipeline(model_name, model_dir) -> Segmentation3DPipeline`; `model_info(model_name, model_dir) -> dict` | Crea el pipeline con la estrategia; `model_info` devuelve nombre, versión, rutas y SHA-256 de los pesos para los informes. |

## Scripts (`scripts/`)

| Script | Función |
|---|---|
| `descargar_datos.py` | Descarga y extrae (de forma segura) MSD Task05 en `datos/`; escribe `datos/FUENTE.md`. Opciones `--destino`, `--forzar`. |
| `inventario_datos.py` | Cuenta casos y calcula SHA-256 por archivo → `reports/datos/inventario_datos.{md,csv}`. |
| `verificar_anonimizacion.py` | Revisa texto libre de cabeceras NIfTI/MHD, nombres y ausencia de DICOM → `reports/datos/`. |
| `analizar_geometria.py` | Forma, espaciado, orientación, volumen y etiquetas por caso → `reports/datos/geometria*.{md,csv}`. |
| `control_calidad.py` | Reglas RF-10 (gzip completo, finito, ≥ 8 cortes, ≥ 32×32, etiquetas {0,1,2}); excluye y registra motivo. |
| `convertir_nifti.py` | MSD 4D → NIfTI 3D (canal T2); PROMISE12 MHD → NIfTI; salida en `datos/convertidos/`. |
| `verificar_fuga.py` | Verifica la división (intersecciones y huella) y busca estudios idénticos entre MSD y PROMISE12. |
| `preprocesar.py` | Preparación independiente (RAS, 0,5 mm, escala, normalización) de un volumen: `ENTRADA SALIDA [--espaciado] [--sin-normalizar]`. |
| `descargar_modelo.py` | Descarga el bundle `prostate_mri_anatomy` de Hugging Face (revisión fijada) y genera `preparacion.json` desde `configs/inference.json` con `construir_preparacion(inference, version)`. |
| `generar_roi.py` | Ejecuta el pipeline sobre `--caso` o `--imagen [--referencia]` y guarda imagen, máscara y PNG con aviso. |
| `medir_rendimiento.py` | Tiempo por paso y pico de RSS con `medir(caso, datos, modelos, repeticiones, dispositivo)`; en GPU también el nombre de la GPU y su memoria pico (`torch.cuda.max_memory_allocated`). |
| `verificar_roi.py` | Comprueba forma/afín, binariedad, cabeceras limpias y Dice recalculado desde la máscara guardada. |
| `analizar_errores.py` | VP/FP/FN, componentes conexas y cobertura de cortes por caso (`--casos` o `--peores CSV --n N`). |

## Entrenamiento (`entrenamiento/`)

- **`division.py`**: `SEMILLA = 2026`, `PROPORCIONES` 70/15/15. `dividir(casos, semilla=SEMILLA)` mezcla los
  casos ordenados con la semilla; `verificar_division(conjuntos, esperados=None)` exige conjuntos disjuntos y
  completos; `huella(conjuntos)` calcula el SHA-256; `cargar_division(ruta)` lee y verifica
  `division_task05.json`; `crear_division(datos, salida, semilla)` lo regenera.
- **`evaluar.py`**: `evaluar_casos(modelo, carpeta, datos, ids, dispositivo)` ejecuta `build_pipeline` por caso
  en una carpeta temporal y devuelve Dice, IoU y tiempo; `construir_informe(...)` escribe el Markdown con
  condiciones, tabla, veredicto frente a `META_DICE = 0.80` (RF-24) y limitaciones.
- **`entrenar.py`**: ajuste fino (o `--desde-cero`) con la misma `PreparationConfig` de la inferencia.
  `preparar_etiqueta(ruta, cfg)` intercambia las etiquetas de Task05 (1 = periférica, 2 = transición) a las del
  modelo base; `crear_red(cfg, pesos_base, dispositivo)`, `validar(...)` (Dice de validación) y
  `escribir_salida(...)` deja `modelos/<nombre>/` con pesos, `preparacion.json`, `metadatos.json`,
  `division.json`, `historial.json` y `FICHA.md`. `--prueba-rapida` hace una comprobación en CPU.
