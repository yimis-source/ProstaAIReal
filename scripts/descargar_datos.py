"""Descarga del conjunto MSD Task05_Prostate (tarea 1204).

Autor: Yeison Bolaños Ruiz (Desarrollador).

Descarga el .tar de MSD Task05_Prostate (copia usada por MONAI), lo extrae de forma
segura y escribe `datos/FUENTE.md` con fuente, licencia y cita (requisito RC-03).
Prostate158 y PROMISE12 NO se descargan aquí: requieren registro y aceptar
condiciones de uso, así que solo se imprimen las instrucciones manuales.

Uso (desde la raíz del repositorio):
    python scripts/descargar_datos.py
    python scripts/descargar_datos.py --destino datos --forzar
"""
from __future__ import annotations

import argparse
import sys
import tarfile
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
URL_MSD = "https://msd-for-monai.s3-us-west-2.amazonaws.com/Task05_Prostate.tar"
CARPETA_MSD = "Task05_Prostate"

FUENTE_MD = """# Datos de ejemplo: Medical Segmentation Decathlon, Task05_Prostate

- Fuente: http://medicaldecathlon.com/ (copia usada por MONAI: {url}).
- Licencia: CC-BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/).
- Contenido: 32 casos de entrenamiento con MRI multimodal (canal 0 = T2, canal 1 = ADC)
  y etiquetas de zona periférica (1) y zona de transición (2).
- Uso en Prosta-AI: solo ejemplos y pruebas manuales; el canal 0 (T2) se usa como imagen
  y la unión de etiquetas > 0 como referencia.

## Cita

Antonelli, M., Reinke, A., Bakas, S. et al. The Medical Segmentation Decathlon.
Nat Commun 13, 4128 (2022). https://doi.org/10.1038/s41467-022-30695-9

## Aviso

Uso académico y experimental. No se usa para diagnóstico.
"""

INSTRUCCIONES_MANUALES = """
Conjuntos de descarga MANUAL (no se descargan con este script):

1. Prostate158 (respaldo, solo referencia)
   - Zenodo: https://doi.org/10.5281/zenodo.6481141
   - Reto: https://prostate158.grand-challenge.org/ (acuerdo de uso de investigación
     no comercial y sin redistribución; léelo antes de descargar).
   - Ubicación: datos/externos/prostate158_train/
   - No se redistribuye ni se sube al repositorio.

2. PROMISE12 (comparación)
   - Reto: https://promise12.grand-challenge.org/ (requiere registro y aceptar las condiciones).
   - Ubicación: datos/externos/promise12/training_data y datos/externos/promise12/test_data
   - Si la descarga trae un archivo a.py, NO lo ejecutes ni lo importes: bórralo o ignóralo.

Ver docs/datos/procedimiento_descarga.md.
"""


def _progreso(bloques: int, tam_bloque: int, total: int) -> None:
    hecho = bloques * tam_bloque
    if total > 0:
        pct = min(100.0, hecho * 100.0 / total)
        sys.stdout.write(f"\r  {hecho / 1e6:8.1f} / {total / 1e6:.1f} MB ({pct:5.1f} %)")
    else:
        sys.stdout.write(f"\r  {hecho / 1e6:8.1f} MB")
    sys.stdout.flush()


def descargar(url: str, archivo: Path) -> None:
    archivo.parent.mkdir(parents=True, exist_ok=True)
    print(f"Descargando {url}")
    urllib.request.urlretrieve(url, archivo, reporthook=_progreso)
    sys.stdout.write("\n")


def extraer_seguro(archivo_tar: Path, destino: Path) -> None:
    """Extrae el tar rechazando rutas fuera de `destino`, enlaces y archivos especiales."""
    destino = destino.resolve()
    with tarfile.open(archivo_tar) as tar:
        miembros = tar.getmembers()
        for m in miembros:
            objetivo = (destino / m.name).resolve()
            if objetivo != destino and destino not in objetivo.parents:
                raise RuntimeError(f"Ruta insegura en el tar: {m.name}")
            if not (m.isfile() or m.isdir()):
                raise RuntimeError(f"Tipo de miembro no permitido en el tar: {m.name}")
        for m in miembros:
            tar.extract(m, destino)  # sin 'filter' para compatibilidad; ya validamos arriba


def main() -> int:
    ap = argparse.ArgumentParser(description="Descarga MSD Task05_Prostate.")
    ap.add_argument("--destino", type=Path, default=RAIZ / "datos",
                    help="carpeta de datos (por defecto datos/)")
    ap.add_argument("--forzar", action="store_true",
                    help="volver a descargar aunque Task05_Prostate ya exista")
    args = ap.parse_args()

    destino: Path = args.destino
    carpeta = destino / CARPETA_MSD
    if carpeta.exists() and not args.forzar:
        print(f"{carpeta} ya existe; usa --forzar para descargar de nuevo.")
    else:
        destino.mkdir(parents=True, exist_ok=True)
        tar_local = destino / "Task05_Prostate.tar"
        try:
            descargar(URL_MSD, tar_local)
            print("Extrayendo...")
            extraer_seguro(tar_local, destino)
        finally:
            if tar_local.exists():
                tar_local.unlink()
        print(f"Listo: {carpeta}")

    (destino / "FUENTE.md").write_text(FUENTE_MD.format(url=URL_MSD), encoding="utf-8")
    print(f"Escrito {destino / 'FUENTE.md'}")
    print(INSTRUCCIONES_MANUALES)
    return 0


if __name__ == "__main__":
    sys.exit(main())
