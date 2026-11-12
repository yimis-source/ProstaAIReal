"""Verificación de la ROI sobre el conjunto de prueba (tarea 1507, RF-12).

Para cada caso de prueba de la división genera la ROI con el pipeline y comprueba:
1. `mascara.nii.gz` tiene la misma forma y la misma afín que `imagen.nii.gz` y que el
   estudio original (alineación vóxel a vóxel);
2. la máscara es binaria (solo 0 y 1) y no está vacía;
3. las cabeceras no tienen texto libre (descrip, db_name, aux_file);
4. el Dice recalculado leyendo la máscara GUARDADA coincide con el que da el pipeline
   y, si se indica, con el del informe de evaluación (CSV).

Uso (desde la raíz del repositorio):
    python scripts/verificar_roi.py [--evaluacion reports/evaluacion/<informe>.csv]

Escribe `reports/roi/verificacion_roi_<fecha>.md`. Las imágenes se generan en una
carpeta temporal que se borra al terminar (no se guardan imágenes de los datos).
"""
from __future__ import annotations

import argparse
import csv
import sys
import tempfile
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
for ruta in (RAIZ / "backend", RAIZ):
    if str(ruta) not in sys.path:
        sys.path.insert(0, str(ruta))

import nibabel as nib
import numpy as np

from entrenamiento.division import DIVISION_POR_DEFECTO, cargar_division, rutas_caso
from prosta_ai.pipeline.base import PipelineInput
from prosta_ai.pipeline.evaluation import dice, iou
from prosta_ai.pipeline.factory import build_pipeline
from prosta_ai.pipeline.progress import PipelineProgress
from prosta_ai.pipeline.visualizacion import guardar_imagen_roi

DATOS = RAIZ / "datos" / "Task05_Prostate"
TOLERANCIA_DICE = 1e-4  # el CSV del informe guarda 6 decimales


def _texto_libre(ruta: Path) -> list[str]:
    h = nib.load(str(ruta)).header
    return [c for c in ("descrip", "db_name", "aux_file") if bytes(h[c]).strip(b"\0")]


def verificar_caso(pipeline, caso: str, datos: Path) -> dict:
    imagen, etiqueta = rutas_caso(datos, caso)
    original = nib.load(str(imagen))
    with tempfile.TemporaryDirectory() as tmp:
        res = pipeline.run(PipelineInput([imagen], "NIfTI", [etiqueta], Path(tmp)), PipelineProgress())
        img, msk = nib.load(str(res.image_path)), nib.load(str(res.mask_path))
        datos_msk = np.asarray(msk.dataobj)
        ref = np.asarray(nib.load(str(etiqueta)).dataobj) > 0
        k = guardar_imagen_roi(res.image_path, res.mask_path, Path(tmp) / f"roi_{caso}.png")
        return {
            "caso": caso,
            "forma": tuple(int(s) for s in msk.shape),
            "misma_forma": msk.shape == img.shape == original.shape[:3],
            "misma_afin": bool(np.allclose(msk.affine, img.affine) and np.allclose(msk.affine, original.affine)),
            "binaria": set(np.unique(datos_msk).tolist()) <= {0, 1},
            "voxeles_roi": int(datos_msk.sum()),
            "volumen_ml": float(datos_msk.sum() * np.prod(msk.header.get_zooms()[:3]) / 1000),
            "sin_texto": not (_texto_libre(res.image_path) or _texto_libre(res.mask_path)),
            "dice_pipeline": res.dice,
            "dice_guardada": dice(datos_msk, ref),
            "iou_guardada": iou(datos_msk, ref),
            "corte_png": k,
            "tiempo_roi_s": res.durations.get("ROI", float("nan")),
        }


def leer_csv(ruta: Path | None) -> dict[str, float]:
    if ruta is None:
        return {}
    with open(ruta, encoding="utf-8") as f:
        return {fila["caso"]: float(fila["dice"]) for fila in csv.DictReader(f)}


def informe(filas: list[dict], ref_csv: dict[str, float], fuente_csv: Path | None) -> tuple[str, bool]:
    ok_total = True
    md = [
        f"# Verificación de la ROI en el conjunto de prueba ({date.today().isoformat()})",
        "",
        "Uso académico y experimental; no es una evaluación clínica ni diagnóstica.",
        "",
        "Generado con `scripts/verificar_roi.py`. Las imágenes y máscaras se crearon en una carpeta temporal "
        "y se borraron al terminar; aquí solo se publican cifras.",
        "",
        "| Caso | Forma | Forma igual | Afín igual | Binaria | Vóxeles ROI | Volumen (ml) | Cabecera sin texto | "
        "Dice (pipeline) | Dice (máscara guardada) | Dice (informe) | Coincide | Corte PNG | Etapa ROI (s) |",
        "|---|---|:-:|:-:|:-:|---:|---:|:-:|---:|---:|---:|:-:|---:|---:|",
    ]
    for f in filas:
        d_inf = ref_csv.get(f["caso"])
        coincide = abs(f["dice_guardada"] - f["dice_pipeline"]) < 1e-9 and (
            d_inf is None or abs(f["dice_guardada"] - d_inf) < TOLERANCIA_DICE)
        ok = all((f["misma_forma"], f["misma_afin"], f["binaria"], f["sin_texto"], f["voxeles_roi"] > 0, coincide))
        ok_total &= ok
        si = lambda v: "sí" if v else "**no**"  # noqa: E731
        md.append(
            f"| {f['caso']} | {f['forma'][0]}×{f['forma'][1]}×{f['forma'][2]} | {si(f['misma_forma'])} | "
            f"{si(f['misma_afin'])} | {si(f['binaria'])} | {f['voxeles_roi']} | {f['volumen_ml']:.1f} | "
            f"{si(f['sin_texto'])} | {f['dice_pipeline']:.4f} | {f['dice_guardada']:.4f} | "
            f"{'–' if d_inf is None else f'{d_inf:.4f}'} | {si(coincide)} | {f['corte_png']} | {f['tiempo_roi_s']:.2f} |"
        )
    md += [
        "",
        f"Informe de evaluación usado para comparar: `{fuente_csv.as_posix()}`." if fuente_csv else
        "No se indicó informe de evaluación para comparar.",
        "",
        f"**Resultado:** {'todas las comprobaciones se cumplen' if ok_total else 'HAY comprobaciones que fallan'} "
        f"({len(filas)} casos).",
        "",
        "La alineación visual (ROI sobre la imagen en 3D Slicer) se revisa aparte y se documenta en "
        "`docs/datos/` por el Analista y el Diseñador.",
        "",
    ]
    return "\n".join(md), ok_total


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datos", type=Path, default=DATOS)
    ap.add_argument("--division", type=Path, default=DIVISION_POR_DEFECTO)
    ap.add_argument("--modelos", type=Path, default=RAIZ / "modelos")
    ap.add_argument("--evaluacion", type=Path, default=None, help="CSV del informe de evaluación para comparar el Dice.")
    ap.add_argument("--salida", type=Path, default=RAIZ / "reports" / "roi")
    args = ap.parse_args()
    casos = cargar_division(args.division)["conjuntos"]["prueba"]
    pipeline = build_pipeline("prostate_mri_anatomy", args.modelos / "prostate_mri_anatomy")
    filas = []
    for caso in casos:
        filas.append(verificar_caso(pipeline, caso, args.datos))
        print(f"{caso}: Dice {filas[-1]['dice_guardada']:.4f}", flush=True)
    fuente = None
    if args.evaluacion is not None:
        try:
            fuente = args.evaluacion.resolve().relative_to(RAIZ)
        except ValueError:
            fuente = args.evaluacion
    texto, ok = informe(filas, leer_csv(args.evaluacion), fuente)
    args.salida.mkdir(parents=True, exist_ok=True)
    destino = args.salida / f"verificacion_roi_{date.today().isoformat()}.md"
    destino.write_text(texto, encoding="utf-8")
    print(f"{'OK' if ok else 'FALLAN COMPROBACIONES'}: {destino}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
