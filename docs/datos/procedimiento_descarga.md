# Procedimiento de descarga de los conjuntos

| Campo | Valor |
|---|---|
| Tarea | 1204 |
| Responsable | Yeison Bolaños Ruiz (Desarrollador) |
| Fecha | 18/10/2026 |
| Versión | 1.0 |

## 1. Dónde van los datos

Todos van dentro de `datos/`, que está en `.gitignore`: **no se suben al repositorio**.

| Conjunto | Ubicación | Cómo se obtiene |
|---|---|---|
| MSD Task05_Prostate | `datos/Task05_Prostate/` | Automático |
| Prostate158 | `datos/externos/prostate158_train/` | Manual |
| PROMISE12 | `datos/externos/promise12/training_data/` y `datos/externos/promise12/test_data/` | Manual |

## 2. MSD Task05_Prostate (automático)

Desde la raíz del repositorio:

```bash
python scripts/descargar_datos.py
```

Opciones:

- `--destino RUTA`: carpeta de datos (por defecto `datos/`).
- `--forzar`: vuelve a descargar aunque `Task05_Prostate/` ya exista.

El script descarga `https://msd-for-monai.s3-us-west-2.amazonaws.com/Task05_Prostate.tar` con `urllib`, muestra el progreso, extrae el tar rechazando rutas fuera del destino, borra el `.tar` y escribe `datos/FUENTE.md` con fuente, licencia y cita (RC-03). Para los otros dos conjuntos solo imprime las instrucciones manuales.

Comprobación: debe haber `imagesTr/` (32), `labelsTr/` (32), `imagesTs/` (16) y `dataset.json`.

## 3. Prostate158 (manual)

1. Leer el acuerdo de uso del reto (https://prostate158.grand-challenge.org/): investigación no comercial y sin redistribución.
2. Descargar desde Zenodo (doi 10.5281/zenodo.6481141) los datos de entrenamiento.
3. Colocar el contenido en `datos/externos/prostate158_train/` (con `train/`, `valid/` y los csv `train.csv` y `valid.csv`).
4. No compartirlo ni subirlo. Es solo referencia (ver `eleccion_dataset.md`).

## 4. PROMISE12 (manual)

1. Registrarse en https://promise12.grand-challenge.org/ y aceptar las condiciones.
2. Descargar los datos de entrenamiento y de prueba.
3. Colocarlos en `datos/externos/promise12/training_data/` y `datos/externos/promise12/test_data/`.

**Archivo `a.py`:** las descargas de PROMISE12 traían un `a.py` que no esperábamos (uno por carpeta). **No se ejecuta ni se importa.** Se borra o se ignora. El inventario lo lista como «no esperado» y no lo abre.

## 5. Generar el inventario con SHA-256

Después de descargar:

```bash
python scripts/inventario_datos.py
```

Escribe en `reports/datos/` el archivo `inventario_datos.csv` (un archivo por fila, con su SHA-256) y `inventario_datos.md` (resumen por conjunto). Sirve para comprobar que todo el equipo trabaja con los mismos archivos. Resultado del ciclo 1:

| Conjunto | Casos | Archivos de imagen | No esperados | Tamaño (MB) |
|---|---|---:|---:|---:|
| MSD Task05_Prostate | 32 con máscara + 16 sin máscara | 80 | 0 | 239,8 |
| Prostate158 (entrenamiento) | 139 | 844 | 0 | 2784,6 |
| PROMISE12 (entrenamiento) | 50 | 200 | 1 | 786,5 |
| PROMISE12 (prueba) | 30 | 120 | 1 | 466,6 |

Después se comprueba la anonimización con `python scripts/verificar_anonimizacion.py` (resultado: sin hallazgos).
