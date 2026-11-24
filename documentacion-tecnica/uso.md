# Uso

Todos los comandos se ejecutan desde la raíz del repositorio con el entorno de `backend/.venv` (ver
[Instalación](instalacion.md)). Los informes publican solo cifras; las imágenes van a `salidas/` (fuera de git).

## Preparación de datos

```bash
python scripts/inventario_datos.py           # reports/datos/inventario_datos.md y .csv
python scripts/verificar_anonimizacion.py    # reports/datos/verificacion_anonimizacion.md
python scripts/analizar_geometria.py         # reports/datos/geometria.md y CSV por conjunto
python scripts/control_calidad.py            # reports/calidad/control_calidad.md y .csv
python scripts/convertir_nifti.py            # datos/convertidos/ + reports/calidad/conversion_nifti.md
python scripts/verificar_fuga.py             # reports/division/verificacion_division.md
python scripts/preprocesar.py ENTRADA SALIDA [--espaciado 0.5] [--sin-normalizar]
```

Resultados registrados: control de calidad con 32/32 casos MSD con máscara, 16/16 sin máscara, 50/50 y 30/30 de
PROMISE12 aprobados (0 excluidos). División 22/5/5 sin intersecciones; 12 casos de MSD son el mismo estudio que
uno de PROMISE12 (2 de ellos en prueba), por lo que PROMISE12 no se usa para entrenar ni evaluar.

## ROI de un caso

```bash
python scripts/generar_roi.py --caso prostate_13
python scripts/generar_roi.py --imagen ruta/estudio.nii.gz [--referencia ruta/mascara.nii.gz] [--corte N]
```

Deja en `salidas/roi/<caso>/` los archivos `imagen.nii.gz`, `mascara.nii.gz` y `roi_<caso>.png`, e imprime la
ruta de la ROI, el corte usado, Dice/IoU (si hay referencia) y los tiempos por etapa.

## Evaluación

```bash
python -m entrenamiento.evaluar --modelo prostate_mri_anatomy            # 5 casos de prueba
python -m entrenamiento.evaluar --modelo prostate_mri_anatomy --todos    # + 32 casos como dato adicional
```

Salida: `reports/evaluacion/evaluacion_<modelo>_<fecha>.md` y `.csv`. Cifras de
`evaluacion_prostate_mri_anatomy_2026-11-11_32casos.md` (CPU AMD Ryzen 5 5600G):

| Caso (prueba) | Dice | IoU |
|---|---:|---:|
| prostate_13 | 0,9012 | 0,8201 |
| prostate_17 | 0,9097 | 0,8344 |
| prostate_28 | 0,8320 | 0,7123 |
| prostate_34 | 0,9105 | 0,8356 |
| prostate_44 | 0,9090 | 0,8332 |
| **Media ± desv.** | **0,8925 ± 0,0340** | **0,8071 ± 0,0534** |

Meta RF-24 (Dice medio ≥ 0,80) cumplida. Dato adicional en los 32 casos: Dice 0,8736 ± 0,1222, IoU
0,7892 ± 0,1304.

## Rendimiento, verificación de la ROI y errores

```bash
python scripts/medir_rendimiento.py --caso prostate_13 --repeticiones 3 [--dispositivo cpu|cuda]
python scripts/verificar_roi.py [--evaluacion reports/evaluacion/<informe>.csv]
python scripts/analizar_errores.py --peores reports/evaluacion/<informe>_32casos.csv --n 4
```

- `reports/rendimiento/rendimiento_1408_2026-11-07.md`: 13,1–16,0 s por estudio (media 14,1 s con el modelo
  cargado), pico de memoria 2048 MB; RR-01 (≤ 120 s) cumplido.
- `reports/rendimiento/rendimiento_1408_gpu_2026-11-13.md`: en GPU (Tesla T4, Colab) 4,9–6,9 s por estudio
  (media 5,0 s, inferencia 2,3 s). Con `--dispositivo cuda` el script escribe `rendimiento_1408_gpu_<fecha>.md`.
- `reports/roi/verificacion_roi_2026-11-11.md`: en los 5 casos de prueba la máscara tiene la misma forma y afín
  que la imagen, es binaria, la cabecera no tiene texto libre y el Dice recalculado coincide con el del informe.
- `reports/evaluacion/analisis_errores_2026-11-11.md`: análisis de prostate_07, prostate_10, prostate_28 y
  prostate_46 (ver [Limitaciones](limitaciones.md)).

## API web

Desde `backend/`, con las dependencias de `pyproject.toml` instaladas:

```bash
cd backend
uvicorn prosta_ai.api.app:create_app --factory --reload --port 8000
curl http://localhost:8000/api/salud          # {"estado":"ok","version":"0.6.0"}
```

Todas las rutas van bajo `/api`; los errores responden `{"detalle": "..."}` (el 422 añade `campos`). Los
orígenes permitidos por CORS se leen de `PROSTA_CORS_ORIGINS` (separados por comas; por defecto
`http://localhost:5173`). La documentación interactiva queda en `http://localhost:8000/docs`. Uso académico,
no diagnóstico.
