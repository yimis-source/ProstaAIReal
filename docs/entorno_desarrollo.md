# Entorno de desarrollo del módulo de IA (tarea 1403)

Responsable: Sergio Gabriel Meneses Silva (Gerente de soporte). Ciclo 3.

Objetivo: que los cinco integrantes y Google Colab ejecuten el pipeline con **las mismas versiones** (RA-01).
Las versiones quedan fijadas en `backend/pyproject.toml`; no instale otras sin pasar por control de cambios.

## Versiones fijadas

| Paquete | Versión | Para qué |
|---|---|---|
| Python | 3.11 o 3.12 | Intérprete (el equipo usa 3.12) |
| numpy | 1.26.4 | Arreglos de vóxeles (torch 2.5.1 y MONAI 1.4.0 no admiten numpy 2) |
| nibabel | 5.3.2 | Leer y escribir NIfTI |
| SimpleITK | 2.4.0 | Componentes conexos en el posproceso de la máscara |
| monai | 1.4.0 | Transformaciones de preparación, U-Net y ventana deslizante |
| torch | 2.5.1 (CPU) | Red neuronal; en Colab se usa la versión con CUDA |
| pytest | 8.3.4 | Pruebas (dependencia de desarrollo) |

PyTorch se instala desde el índice de CPU (`download.pytorch.org/whl/cpu`) para no descargar ~2 GB de CUDA en
equipos sin GPU NVIDIA. Ninguno de nuestros portátiles tiene GPU NVIDIA; la GPU se usa solo en Colab.

## Instalación (Linux, macOS o WSL)

```bash
# 1. uv (gestor de entornos); alternativa: python -m venv + pip
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Entorno del backend con las versiones exactas
cd backend
uv sync --extra dev          # crea backend/.venv e instala prosta_ai en modo editable
cd ..

# 3. Comprobar
backend/.venv/bin/python -c "import torch, monai; print(torch.__version__, monai.__version__)"
backend/.venv/bin/python -m pytest -q
```

En Windows sin WSL: `py -3.12 -m venv backend\.venv`, luego
`backend\.venv\Scripts\pip install -e backend[dev] --extra-index-url https://download.pytorch.org/whl/cpu`.

## Datos y modelo (no se suben a git)

```bash
backend/.venv/bin/python scripts/descargar_datos.py      # MSD Task05 en datos/
backend/.venv/bin/python scripts/descargar_modelo.py     # bundle prostate_mri_anatomy en modelos/
```

`datos/`, `modelos/` y los pesos (`*.pt`, `*.pth`) están en `.gitignore`. Antes de cada commit revise
`git status`: no debe aparecer ningún archivo de imagen médica ni de pesos.

## Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `numpy.core.multiarray failed to import` | Se instaló numpy 2.x | `uv sync` de nuevo (vuelve a 1.26.4) |
| `ModuleNotFoundError: prosta_ai` | Se ejecutó fuera del entorno o sin instalar el backend | Usar `backend/.venv/bin/python` desde la raíz del repositorio |
| La descarga de torch pesa 2 GB | Se tomó el índice con CUDA | Revisar que `[tool.uv.sources]` apunte a `pytorch-cpu` |
| En Colab pide reiniciar tras instalar | Colab ya trae otras versiones cargadas | Reiniciar el entorno y seguir desde la celda de clonado |
