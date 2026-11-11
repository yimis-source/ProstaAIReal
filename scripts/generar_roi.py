"""Genera la ROI de un estudio NIfTI (tarea 1503/1504).

Ejecuta el pipeline completo y deja en la carpeta de salida:
- `imagen.nii.gz`: el volumen original (canal T2 si el NIfTI es 4D), sin metadatos;
- `mascara.nii.gz`: la ROI en la misma rejilla (forma y afín) que la imagen;
- `roi_<caso>.png`: corte axial con la ROI superpuesta y el aviso no diagnóstico impreso.

La salida contiene imágenes derivadas de los datos: guárdela FUERA del repositorio
(por defecto `salidas/`, que está en `.gitignore`). Si se comparte, MSD Task05 exige
atribución y la misma licencia (CC BY-SA 4.0).

Uso (desde la raíz del repositorio):
    python scripts/generar_roi.py --caso prostate_13
    python scripts/generar_roi.py --imagen ruta/estudio.nii.gz [--referencia ruta/mascara.nii.gz]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
for ruta in (RAIZ / "backend", RAIZ):
    if str(ruta) not in sys.path:
        sys.path.insert(0, str(ruta))

from prosta_ai.pipeline.base import PipelineInput
from prosta_ai.pipeline.factory import build_pipeline
from prosta_ai.pipeline.progress import PipelineProgress
from prosta_ai.pipeline.visualizacion import guardar_imagen_roi

DATOS = RAIZ / "datos" / "Task05_Prostate"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--caso", help="Caso de MSD Task05 (p. ej. prostate_13); usa su etiqueta como referencia.")
    grupo.add_argument("--imagen", type=Path, help="Estudio NIfTI cualquiera.")
    ap.add_argument("--referencia", type=Path, default=None, help="Máscara de referencia NIfTI (opcional).")
    ap.add_argument("--modelos", type=Path, default=RAIZ / "modelos")
    ap.add_argument("--salida", type=Path, default=RAIZ / "salidas" / "roi")
    ap.add_argument("--corte", type=int, default=None, help="Corte axial del PNG (por defecto, el de mayor ROI).")
    args = ap.parse_args()

    if args.caso:
        imagen = DATOS / "imagesTr" / f"{args.caso}.nii.gz"
        referencia = DATOS / "labelsTr" / f"{args.caso}.nii.gz"
        nombre = args.caso
    else:
        imagen, referencia = args.imagen, args.referencia
        nombre = imagen.name.split(".")[0]
    carpeta = args.salida / nombre
    pipeline = build_pipeline("prostate_mri_anatomy", args.modelos / "prostate_mri_anatomy")
    refs = [referencia] if referencia is not None else []
    res = pipeline.run(PipelineInput([imagen], "NIfTI", refs, carpeta), PipelineProgress())
    png = carpeta / f"roi_{nombre}.png"
    k = guardar_imagen_roi(res.image_path, res.mask_path, png, args.corte)
    print(f"ROI de {nombre}: {res.mask_path}")
    print(f"Imagen con aviso (corte {k}): {png}")
    if res.dice is not None:
        print(f"Dice {res.dice:.4f}  IoU {res.iou:.4f}")
    print("Tiempos por etapa: " + ", ".join(f"{e} {s:.1f} s" for e, s in res.durations.items()))


if __name__ == "__main__":
    main()
