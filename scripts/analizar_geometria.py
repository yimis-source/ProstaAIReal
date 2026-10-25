"""Análisis de tamaños, espaciado y casos de los conjuntos descargados (tarea 1206).

Para cada caso lee solo la cabecera y la máscara (si la hay) y registra:
forma, número de canales, espaciado (mm), orientación, volumen de la
próstata (mL) y etiquetas presentes. Escribe un CSV por conjunto y un resumen.

Uso (desde la raíz del repositorio):
    python scripts/analizar_geometria.py [--datos datos] [--salida reports/datos]
"""
from __future__ import annotations

import argparse
import csv
import statistics as st
from pathlib import Path

import nibabel as nib
import numpy as np
import SimpleITK as sitk

RAIZ = Path(__file__).resolve().parents[1]


def _fila_nifti(caso: str, imagen: Path, mascara: Path | None) -> dict:
    img = nib.load(str(imagen))
    forma = img.shape
    zooms = img.header.get_zooms()[:3]
    fila = {
        "caso": caso,
        "forma": "x".join(str(d) for d in forma[:3]),
        "canales": forma[3] if len(forma) == 4 else 1,
        "esp_x": round(float(zooms[0]), 4), "esp_y": round(float(zooms[1]), 4), "esp_z": round(float(zooms[2]), 4),
        "orientacion": "".join(nib.aff2axcodes(img.affine)),
        "cortes": forma[2],
        "volumen_ml": "", "etiquetas": "",
    }
    if mascara is not None and mascara.exists():
        m = np.asarray(nib.load(str(mascara)).dataobj)
        voxel_ml = float(np.prod(zooms)) / 1000.0
        fila["volumen_ml"] = round(float((m > 0).sum()) * voxel_ml, 1)
        fila["etiquetas"] = " ".join(str(int(v)) for v in np.unique(m))
    return fila


def _fila_mhd(caso: str, imagen: Path, mascara: Path | None) -> dict:
    lector = sitk.ImageFileReader()
    lector.SetFileName(str(imagen))
    lector.ReadImageInformation()
    forma = lector.GetSize()
    esp = lector.GetSpacing()
    direccion = np.array(lector.GetDirection()).reshape(3, 3)
    # SimpleITK usa LPS; se pasa a RAS para comparar con NIfTI
    afin = np.eye(4)
    afin[:3, :3] = np.diag([-1, -1, 1]) @ direccion @ np.diag(esp)
    fila = {
        "caso": caso,
        "forma": "x".join(str(d) for d in forma),
        "canales": lector.GetNumberOfComponents(),
        "esp_x": round(esp[0], 4), "esp_y": round(esp[1], 4), "esp_z": round(esp[2], 4),
        "orientacion": "".join(nib.aff2axcodes(afin)),
        "cortes": forma[2],
        "volumen_ml": "", "etiquetas": "",
    }
    if mascara is not None and mascara.exists():
        m = sitk.GetArrayFromImage(sitk.ReadImage(str(mascara)))
        fila["volumen_ml"] = round(float((m > 0).sum()) * float(np.prod(esp)) / 1000.0, 1)
        fila["etiquetas"] = " ".join(str(int(v)) for v in np.unique(m))
    return fila


def analizar(datos: Path) -> dict[str, list[dict]]:
    res: dict[str, list[dict]] = {}
    msd = datos / "Task05_Prostate"
    if msd.exists():
        res["msd_task05"] = [
            _fila_nifti(p.name[:-7], p, msd / "labelsTr" / p.name)
            for p in sorted((msd / "imagesTr").glob("prostate_*.nii.gz"))
        ]
    p158 = datos / "externos" / "prostate158_train" / "train"
    if p158.exists():
        res["prostate158"] = [
            _fila_nifti(d.name, d / "t2.nii.gz", d / "t2_anatomy_reader1.nii.gz")
            for d in sorted(p for p in p158.iterdir() if p.is_dir())
        ]
    for nombre, carpeta in (("promise12_entrenamiento", "training_data"), ("promise12_prueba", "test_data")):
        base = datos / "externos" / "promise12" / carpeta
        if base.exists():
            res[nombre] = [
                _fila_mhd(p.stem, p, base / f"{p.stem}_segmentation.mhd")
                for p in sorted(base.glob("Case??.mhd"))
            ]
    return res


def _rango(valores: list[float], dec: int = 2) -> str:
    return f"{min(valores):.{dec}f}–{max(valores):.{dec}f} (mediana {st.median(valores):.{dec}f})"


def escribir(res: dict[str, list[dict]], salida: Path) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    campos = ["caso", "forma", "canales", "esp_x", "esp_y", "esp_z", "orientacion", "cortes", "volumen_ml", "etiquetas"]
    lineas = [
        "# Tamaños, espaciado y casos de los conjuntos",
        "",
        "Generado con `scripts/analizar_geometria.py`. Detalle por caso en `geometria_<conjunto>.csv`.",
        "Volumen de próstata = vóxeles con etiqueta > 0 × volumen del vóxel (máscara del lector 1 en Prostate158).",
        "",
        "| Conjunto | Casos | Formas (más frecuente) | Canales | Espaciado en plano (mm) | Grosor de corte (mm) | Cortes | Orientaciones | Volumen próstata (mL) |",
        "|---|---:|---|---|---|---|---|---|---|",
    ]
    for nombre, filas in res.items():
        with open(salida / f"geometria_{nombre}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            w.writerows(filas)
        formas = st.mode([r["forma"] for r in filas])
        n_formas = len({r["forma"] for r in filas})
        canales = sorted({int(r["canales"]) for r in filas})
        vols = [float(r["volumen_ml"]) for r in filas if r["volumen_ml"] != ""]
        orient = {}
        for r in filas:
            orient[r["orientacion"]] = orient.get(r["orientacion"], 0) + 1
        lineas.append(
            f"| {nombre} | {len(filas)} | {formas} ({n_formas} formas distintas) | {', '.join(map(str, canales))} | "
            f"{_rango([r['esp_x'] for r in filas], 3)} | {_rango([r['esp_z'] for r in filas])} | "
            f"{_rango([r['cortes'] for r in filas], 0)} | "
            f"{', '.join(f'{k} ({v})' for k, v in sorted(orient.items()))} | "
            f"{_rango(vols, 1) if vols else 'sin máscara'} |"
        )
    msd = res.get("msd_task05", [])
    if msd:
        chico = min(msd, key=lambda r: float(r["volumen_ml"]))
        grande = max(msd, key=lambda r: float(r["volumen_ml"]))
        lineas += [
            "",
            "## Observaciones sobre MSD Task05 (conjunto principal)",
            "",
            f"- Próstata más pequeña: {chico['caso']} ({chico['volumen_ml']} mL); más grande: {grande['caso']} ({grande['volumen_ml']} mL).",
            f"- Etiquetas presentes: {sorted({e for r in msd for e in r['etiquetas'].split()})} (0 fondo, 1 zona periférica, 2 zona de transición).",
            "- Las imágenes son 4D (canal 0 = T2, canal 1 = ADC); el análisis de forma usa las tres primeras dimensiones.",
        ]
    (salida / "geometria.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datos", type=Path, default=RAIZ / "datos")
    ap.add_argument("--salida", type=Path, default=RAIZ / "reports" / "datos")
    args = ap.parse_args()
    res = analizar(args.datos)
    escribir(res, args.salida)
    print("Casos analizados: " + ", ".join(f"{k}={len(v)}" for k, v in res.items()))


if __name__ == "__main__":
    main()
