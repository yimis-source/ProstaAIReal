# Instalación

## Requisitos

- Python 3.12 (`requires-python = ">=3.11,<3.13"` en `backend/pyproject.toml`).
- [uv](https://docs.astral.sh/uv/) o `venv` + `pip`.
- Sin GPU: PyTorch se instala desde el índice de CPU (`[tool.uv.sources]` apunta a `pytorch-cpu`).

Versiones fijadas en `backend/pyproject.toml`:

| Paquete | Versión | Uso |
|---|---|---|
| numpy | 1.26.4 | Arreglos de vóxeles (torch 2.5.1 y MONAI 1.4.0 no admiten numpy 2) |
| nibabel | 5.3.2 | Lectura y escritura de NIfTI |
| SimpleITK | 2.4.0 | Componentes conexos; lectura de MetaImage en scripts |
| monai | 1.4.0 | Transformaciones, U-Net, ventana deslizante |
| torch | 2.5.1 | Red neuronal (CPU; CUDA solo en Colab) |
| pillow | 11.1.0 | Imagen de la ROI con aviso |
| pytest | 8.3.4 | Pruebas (extra `dev`) |

## Entorno

Desde la raíz del repositorio (guía completa en `docs/entorno_desarrollo.md`):

```bash
cd backend && uv sync --extra dev && cd ..      # crea backend/.venv e instala prosta_ai (editable)
backend/.venv/bin/python -c "import torch, monai; print(torch.__version__, monai.__version__)"
```

Windows sin WSL: `py -3.12 -m venv backend\.venv` y
`backend\.venv\Scripts\pip install -e backend[dev] --extra-index-url https://download.pytorch.org/whl/cpu`.

## Datos y modelo

No se versionan (`.gitignore` excluye `datos/`, `modelos/`, `salidas/`, `*.nii*`, `*.dcm`, `*.pt`, etc.).

```bash
backend/.venv/bin/python scripts/descargar_datos.py    # MSD Task05_Prostate en datos/ + datos/FUENTE.md
backend/.venv/bin/python scripts/descargar_modelo.py   # modelos/prostate_mri_anatomy + preparacion.json
```

Prostate158 y PROMISE12 requieren registro y se descargan a mano (`docs/datos/procedimiento_descarga.md`).

## Pruebas

`pytest.ini` define `testpaths = tests backend/tests` y `pythonpath = . backend`:

```bash
backend/.venv/bin/python -m pytest -q
```

- `tests/`: scripts de datos (anonimización, control de calidad, división, inventario).
- `backend/tests/pipeline/`: io, validadores, pipeline base, ROI, evaluación y visualización, con volúmenes
  sintéticos (`datos_sinteticos.py`); no necesitan datos reales ni pesos.
- `backend/tests/entrenamiento/`: comprobaciones de `entrenamiento/entrenar.py`.
