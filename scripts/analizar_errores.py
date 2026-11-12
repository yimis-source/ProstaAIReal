"""Análisis de errores de la ROI por caso (tarea 1508).

Para cada caso indicado ejecuta el pipeline y descompone el error de la máscara
(P = predicción en la rejilla original, G = referencia, etiquetas > 0):

- verdaderos positivos, falsos positivos y falsos negativos (en vóxeles y ml);
- componentes conexas de P y de los falsos positivos, con la mayor región falsa y su
  distancia al borde del campo de visión;
- cortes axiales con próstata en G y en P (cobertura de base y ápex).

Uso (desde la raíz del repositorio):
    python scripts/analizar_errores.py --casos prostate_07 prostate_28 prostate_46
    python scripts/analizar_errores.py --peores reports/evaluacion/<informe>_32casos.csv --n 4

Escribe `reports/evaluacion/analisis_errores_<fecha>.md`. Solo cifras: no guarda imágenes.
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
import SimpleITK as sitk

from entrenamiento.division import DIVISION_POR_DEFECTO, cargar_division, rutas_caso
from prosta_ai.pipeline.base import PipelineInput
from prosta_ai.pipeline.evaluation import dice
from prosta_ai.pipeline.factory import build_pipeline
from prosta_ai.pipeline.progress import PipelineProgress

DATOS = RAIZ / "datos" / "Task05_Prostate"


def componentes(binaria: np.ndarray) -> list[tuple[int, np.ndarray]]:
    """(tamaño, centroide en vóxeles) de cada componente conexa, de mayor a menor."""
    if not binaria.any():
        return []
    img = sitk.GetImageFromArray(binaria.astype(np.uint8))
    etiquetas = sitk.GetArrayFromImage(sitk.RelabelComponent(sitk.ConnectedComponent(img), sortByObjectSize=True))
    salida = []
    for k in range(1, int(etiquetas.max()) + 1):
        # GetImageFromArray/GetArrayFromImage conservan el orden de ejes del arreglo de numpy,
        # así que los índices quedan en (x, y, z) como en nibabel
        idx = np.argwhere(etiquetas == k)
        salida.append((len(idx), idx.mean(axis=0)))
    return salida


def analizar(pipeline, caso: str, datos: Path, conjunto: str) -> dict:
    imagen, etiqueta = rutas_caso(datos, caso)
    with tempfile.TemporaryDirectory() as tmp:
        res = pipeline.run(PipelineInput([imagen], "NIfTI", [etiqueta], Path(tmp)), PipelineProgress())
        msk = nib.load(str(res.mask_path))
        p = np.asarray(msk.dataobj) > 0
        zooms = msk.header.get_zooms()[:3]
    g = np.asarray(nib.load(str(etiqueta)).dataobj) > 0
    ml = float(np.prod(zooms)) / 1000
    fp, fn = p & ~g, g & ~p
    comp_p, comp_fp = componentes(p), componentes(fp)
    forma = np.array(p.shape)
    mayor_fp, borde_mm = 0, float("nan")
    if comp_fp:
        mayor_fp, centro = comp_fp[0]
        # distancia en el plano axial del centroide al borde más cercano del campo de visión
        borde_vox = min(centro[0], forma[0] - 1 - centro[0], centro[1], forma[1] - 1 - centro[1])
        borde_mm = float(borde_vox * zooms[0])
    cortes_g = np.flatnonzero(g.any(axis=(0, 1)))
    cortes_p = np.flatnonzero(p.any(axis=(0, 1)))
    return {
        "caso": caso, "conjunto": conjunto, "dice": dice(p, g),
        "g_ml": g.sum() * ml, "p_ml": p.sum() * ml, "vp": int((p & g).sum()), "fp": int(fp.sum()),
        "fn": int(fn.sum()), "g": int(g.sum()), "p": int(p.sum()),
        "componentes_p": len(comp_p), "mayor_fp": mayor_fp, "borde_mm": borde_mm,
        "cortes_g": f"{cortes_g.min()}–{cortes_g.max()}" if cortes_g.size else "–",
        "cortes_p": f"{cortes_p.min()}–{cortes_p.max()}" if cortes_p.size else "–",
        "forma": "×".join(str(int(s)) for s in p.shape),
        "espaciado": "×".join(f"{float(z):.2f}" for z in zooms),
    }


def peores(csv_ruta: Path, n: int) -> list[str]:
    with open(csv_ruta, encoding="utf-8") as f:
        filas = sorted(csv.DictReader(f), key=lambda r: float(r["dice"]))
    return [r["caso"] for r in filas[:n]]


def informe(filas: list[dict], origen: str) -> str:
    md = [
        f"# Análisis de errores de la ROI por caso ({date.today().isoformat()})",
        "",
        "Uso académico y experimental; no es una evaluación clínica ni diagnóstica.",
        "",
        f"Generado con `scripts/analizar_errores.py` ({origen}). Máscaras en la rejilla original; "
        "VP/FP/FN en vóxeles; volúmenes en ml.",
        "",
        "| Caso | Conjunto | Dice | Forma | Espaciado (mm) | Ref. (ml) | Pred. (ml) | VP | FP | FN | "
        "Componentes pred. | Mayor región falsa (vóx.) | Distancia al borde del FOV (mm) | Cortes ref. | Cortes pred. |",
        "|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for f in filas:
        md.append(
            f"| {f['caso']} | {f['conjunto']} | {f['dice']:.4f} | {f['forma']} | {f['espaciado']} | {f['g_ml']:.1f} | "
            f"{f['p_ml']:.1f} | {f['vp']} | {f['fp']} | {f['fn']} | {f['componentes_p']} | {f['mayor_fp']} | "
            f"{f['borde_mm']:.1f} | {f['cortes_g']} | {f['cortes_p']} |"
        )
    md.append("")
    return "\n".join(md)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--casos", nargs="+")
    grupo.add_argument("--peores", type=Path, help="CSV de evaluación: analiza los N casos con menor Dice.")
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--datos", type=Path, default=DATOS)
    ap.add_argument("--modelos", type=Path, default=RAIZ / "modelos")
    ap.add_argument("--salida", type=Path, default=RAIZ / "reports" / "evaluacion")
    args = ap.parse_args()
    casos = args.casos or peores(args.peores, args.n)
    origen = f"los {len(casos)} casos de menor Dice de `{args.peores.name}`" if args.peores else "casos indicados"
    conj = {c: k for k, v in cargar_division(DIVISION_POR_DEFECTO)["conjuntos"].items() for c in v}
    pipeline = build_pipeline("prostate_mri_anatomy", args.modelos / "prostate_mri_anatomy")
    filas = []
    for caso in casos:
        filas.append(analizar(pipeline, caso, args.datos, conj.get(caso, "–")))
        print(f"{caso}: Dice {filas[-1]['dice']:.4f}, FP {filas[-1]['fp']}, mayor FP {filas[-1]['mayor_fp']}", flush=True)
    args.salida.mkdir(parents=True, exist_ok=True)
    destino = args.salida / f"analisis_errores_{date.today().isoformat()}.md"
    destino.write_text(informe(filas, origen), encoding="utf-8")
    print(f"Informe escrito en {destino}")


if __name__ == "__main__":
    main()
