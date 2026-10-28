"""Formato unificado NIfTI (tarea 1302).

Deja todos los casos en un mismo formato para el resto del flujo:

- MSD Task05: extrae el canal 0 (T2) del NIfTI 4D a un NIfTI 3D; la máscara se copia
  como NIfTI 3D (uint8).
- PROMISE12: convierte MetaImage (.mhd/.raw) a NIfTI 3D con SimpleITK, que conserva
  origen, espaciado y dirección (la cabecera NIfTI queda en RAS).

Salida (ignorada por git): datos/convertidos/<conjunto>/<caso>_t2.nii.gz y <caso>_mascara.nii.gz.
Al final comprueba que cada archivo convertido conserva la forma y el espaciado del original.

Uso (desde la raíz del repositorio):
    python scripts/convertir_nifti.py [--datos datos] [--salida datos/convertidos] [--informe reports/calidad]
"""
from __future__ import annotations

import argparse
from pathlib import Path

import nibabel as nib
import numpy as np
import SimpleITK as sitk

RAIZ = Path(__file__).resolve().parents[1]


def _limpiar_cabecera(img: nib.Nifti1Image) -> nib.Nifti1Image:
    for campo in ("descrip", "db_name", "aux_file"):
        img.header[campo] = b""
    return img


def convertir_msd(datos: Path, salida: Path) -> list[dict]:
    filas = []
    base = datos / "Task05_Prostate"
    destino = salida / "msd_task05"
    destino.mkdir(parents=True, exist_ok=True)
    for p in sorted((base / "imagesTr").glob("prostate_*.nii.gz")):
        caso = p.name[:-7]
        img = nib.load(str(p))
        t2 = np.asarray(img.dataobj[..., 0], dtype=np.float32)
        nib.save(_limpiar_cabecera(nib.Nifti1Image(t2, img.affine)), str(destino / f"{caso}_t2.nii.gz"))
        lab = nib.load(str(base / "labelsTr" / p.name))
        m = np.asarray(lab.dataobj).astype(np.uint8)
        nib.save(_limpiar_cabecera(nib.Nifti1Image(m, lab.affine)), str(destino / f"{caso}_mascara.nii.gz"))
        filas.append({"conjunto": "msd_task05", "caso": caso, "forma": img.shape[:3],
                      "espaciado": tuple(float(z) for z in img.header.get_zooms()[:3])})
    return filas


def convertir_promise12(datos: Path, salida: Path) -> list[dict]:
    filas = []
    for carpeta, nombre in (("training_data", "promise12_entrenamiento"), ("test_data", "promise12_prueba")):
        base = datos / "externos" / "promise12" / carpeta
        destino = salida / nombre
        destino.mkdir(parents=True, exist_ok=True)
        for p in sorted(base.glob("Case??.mhd")):
            img = sitk.ReadImage(str(p))
            sitk.WriteImage(sitk.Cast(img, sitk.sitkFloat32), str(destino / f"{p.stem}_t2.nii.gz"))
            seg = base / f"{p.stem}_segmentation.mhd"
            if seg.exists():
                sitk.WriteImage(sitk.Cast(sitk.ReadImage(str(seg)), sitk.sitkUInt8),
                                str(destino / f"{p.stem}_mascara.nii.gz"))
            filas.append({"conjunto": nombre, "caso": p.stem, "forma": img.GetSize(),
                          "espaciado": img.GetSpacing()})
    return filas


def comprobar(filas: list[dict], salida: Path) -> list[str]:
    """Devuelve la lista de casos cuya conversión no conserva forma o espaciado."""
    errores = []
    for f in filas:
        conv = nib.load(str(salida / f["conjunto"] / f"{f['caso']}_t2.nii.gz"))
        forma_ok = tuple(conv.shape) == tuple(f["forma"])
        esp_ok = np.allclose(conv.header.get_zooms()[:3], f["espaciado"], atol=1e-4)
        if not (forma_ok and esp_ok):
            errores.append(f"{f['conjunto']}/{f['caso']}")
    return errores


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datos", type=Path, default=RAIZ / "datos")
    ap.add_argument("--salida", type=Path, default=RAIZ / "datos" / "convertidos")
    ap.add_argument("--informe", type=Path, default=RAIZ / "reports" / "calidad")
    args = ap.parse_args()
    filas = convertir_msd(args.datos, args.salida) + convertir_promise12(args.datos, args.salida)
    errores = comprobar(filas, args.salida)
    conteo: dict[str, int] = {}
    for f in filas:
        conteo[f["conjunto"]] = conteo.get(f["conjunto"], 0) + 1
    lineas = [
        "# Conversión a formato unificado NIfTI",
        "",
        "Generado con `scripts/convertir_nifti.py`. Los archivos convertidos quedan en `datos/convertidos/` (no se versionan).",
        "",
        "| Conjunto | Casos convertidos | Origen |",
        "|---|---:|---|",
    ]
    origen = {"msd_task05": "NIfTI 4D (canal 0 = T2)", "promise12_entrenamiento": "MetaImage (.mhd/.raw)",
              "promise12_prueba": "MetaImage (.mhd/.raw)"}
    lineas += [f"| {k} | {v} | {origen.get(k, '')} |" for k, v in conteo.items()]
    lineas += ["", f"Comprobación de forma y espaciado tras convertir: {len(filas) - len(errores)} de {len(filas)} correctos."]
    if errores:
        lineas += ["", "Casos con diferencias: " + ", ".join(errores)]
    args.informe.mkdir(parents=True, exist_ok=True)
    (args.informe / "conversion_nifti.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"{len(filas)} casos convertidos, {len(errores)} con diferencias.")


if __name__ == "__main__":
    main()
