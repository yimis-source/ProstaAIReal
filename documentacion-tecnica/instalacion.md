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

## Aplicación web (ciclo 6)

La aplicación web usa PostgreSQL para los datos estructurados (usuarios, estudios, trabajos, etapas, modelos
y resultados) y guarda los archivos en disco, en `almacenamiento/`; la base solo conserva la ruta y la huella
SHA-256 de cada archivo (RB-01, RB-02). Uso académico, no diagnóstico.

### Dependencias

Las de la aplicación web (FastAPI, SQLAlchemy 2.0, psycopg 3, Alembic, pydantic-settings) están en
`backend/pyproject.toml`; se instalan con el mismo comando del entorno:

```bash
cd backend && uv sync --extra dev && cd ..
```

### PostgreSQL local

`scripts/postgres_local.sh` crea y arranca un clúster propio en `.pgdata/` (ignorado por git), sin permisos de
administrador ni Docker. Necesita `initdb`, `pg_ctl`, `createdb` y `psql` en el `PATH`.

```bash
scripts/postgres_local.sh iniciar   # initdb la primera vez, arranca y crea la base prosta_ai
scripts/postgres_local.sh estado
scripts/postgres_local.sh detener
```

- Puerto 5433 (cambiar con `PROSTA_PG_PUERTO`), usuario `prosta`, base `prosta_ai`, autenticación `trust`
  solo para desarrollo.
- Escucha solo por TCP en `localhost`; no crea socket Unix, porque una ruta de repositorio larga supera el
  límite de 107 bytes del socket. Por eso `psql` necesita `-h localhost -p 5433 -U prosta`.
- El registro del servidor queda en `.pgdata/servidor.log`.

### Variables PROSTA_*

`backend/prosta_ai/config.py` lee las variables con prefijo `PROSTA_` del entorno o de `backend/.env`
(copiar `backend/.env.example`; `.env` no se sube):

| Variable | Valor por defecto | Uso |
|---|---|---|
| `PROSTA_DATABASE_URL` | `postgresql+psycopg://prosta@localhost:5433/prosta_ai` | Conexión a la base |
| `PROSTA_STORAGE_DIR` | `../almacenamiento` | Archivos subidos y resultados |
| `PROSTA_MAX_UPLOAD_MB` | `50` | Tamaño máximo por archivo (RF-03) |
| `PROSTA_MAX_ESTUDIO_MB` | `150` | Tamaño máximo por estudio (RF-03) |
| `PROSTA_MODELO_NOMBRE` | `prostate_mri_anatomy` | Modelo de segmentación |
| `PROSTA_MODELO_DIR` | `../modelos` | Carpeta de pesos |
| `PROSTA_CORS_ORIGINS` | `http://localhost:5173` | Orígenes del frontend, separados por coma |

### Migraciones

El esquema se crea con Alembic (`backend/migrations/versions/0001_esquema_inicial.py`), desde `backend/`:

```bash
cd backend
.venv/bin/alembic upgrade head      # crea las tablas
.venv/bin/alembic current           # debe mostrar 0001 (head)
.venv/bin/alembic downgrade base    # borra las tablas
```

La URL sale de `PROSTA_DATABASE_URL`; para otra base sin tocar `.env`: `alembic -x url=postgresql+psycopg://... upgrade head`.
Cualquier cambio en `prosta_ai/models.py` necesita una migración nueva.

### Pruebas de base de datos

`backend/tests/db/` usa SQLite (en memoria para los modelos y un archivo temporal para la migración), así que
no necesita PostgreSQL. `test_db_migracion.py` aplica la migración y la compara con `models.py` (columnas,
nulos, índices, llaves foráneas y `compare_metadata` de Alembic). Para repetir la comparación en PostgreSQL,
con una base aparte que la prueba vacía:

```bash
createdb -h localhost -p 5433 -U prosta prosta_ai_pruebas
PROSTA_TEST_DATABASE_URL=postgresql+psycopg://prosta@localhost:5433/prosta_ai_pruebas \
  backend/.venv/bin/python -m pytest -q backend/tests/db
```
