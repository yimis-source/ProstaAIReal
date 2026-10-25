"""Verificación de anonimización de los conjuntos descargados (tarea 1205).

Revisa, sin modificar nada, que los archivos no contengan datos que identifiquen
a una persona:

- NIfTI (.nii/.nii.gz): campos de texto libre de la cabecera (`descrip`,
  `db_name`, `aux_file`, `intent_name`).
- MetaImage (.mhd): todas las claves de la cabecera; se marcan las que no
  pertenecen al formato estándar.
- Nombres de archivo y carpeta: deben ser códigos neutros (sin nombres ni fechas).
- Ausencia de archivos DICOM (que sí podrían traer datos de paciente).

Uso (desde la raíz del repositorio):
    python scripts/verificar_anonimizacion.py [--datos datos] [--salida reports/datos]
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

import nibabel as nib

RAIZ = Path(__file__).resolve().parents[1]
CONJUNTOS = {
    "MSD Task05_Prostate": "Task05_Prostate",
    "Prostate158 (entrenamiento)": "externos/prostate158_train",
    "PROMISE12 (entrenamiento)": "externos/promise12/training_data",
    "PROMISE12 (prueba)": "externos/promise12/test_data",
}
CAMPOS_NIFTI = ("descrip", "db_name", "aux_file", "intent_name")
CLAVES_MHD_ESTANDAR = {
    "ObjectType", "NDims", "BinaryData", "BinaryDataByteOrderMSB", "CompressedData",
    "CompressedDataSize", "TransformMatrix", "Offset", "CenterOfRotation",
    "AnatomicalOrientation", "ElementSpacing", "DimSize", "ElementType",
    "ElementDataFile", "ElementNumberOfChannels", "Position", "Orientation",
}
# Nombres esperados: códigos de caso o nombres de secuencia, sin nombres propios ni fechas.
PATRON_NOMBRE_NEUTRO = re.compile(
    r"^(prostate_\d{2}|Case\d{2}(_segmentation)?|\d{3}|"
    r"(t2|adc|dwi|empty)(_(anatomy|tumor)_reader\d)?)$"
)
PATRON_FECHA = re.compile(r"(19|20)\d{2}[-_]?(0[1-9]|1[0-2])[-_]?([0-2]\d|3[01])")


def _base(nombre: str) -> str:
    for ext in (".nii.gz", ".nii", ".mhd", ".raw"):
        if nombre.endswith(ext):
            return nombre[: -len(ext)]
    return nombre


def _es_dicom(ruta: Path) -> bool:
    if ruta.suffix.lower() == ".dcm":
        return True
    try:
        with open(ruta, "rb") as f:
            f.seek(128)
            return f.read(4) == b"DICM"
    except OSError:
        return False


def _texto(valor) -> str:
    v = valor.tobytes() if hasattr(valor, "tobytes") else bytes(valor)
    return v.split(b"\x00")[0].decode("latin-1").strip()


def revisar(datos: Path) -> dict:
    res: dict = {}
    for conjunto, carpeta in CONJUNTOS.items():
        base = datos / carpeta
        r = {
            "presente": base.exists(), "nifti": 0, "mhd": 0, "dicom": [],
            "campos_nifti": Counter(), "claves_mhd_extra": Counter(),
            "nombres_no_neutros": [], "fechas_en_nombres": [],
        }
        res[conjunto] = r
        if not base.exists():
            continue
        for ruta in sorted(p for p in base.rglob("*") if p.is_file()):
            rel = ruta.relative_to(base)
            if rel.name.startswith("._") or "convertidas" in rel.parts or rel.suffix in (".py", ".csv", ".json"):
                continue
            for parte in list(rel.parts[:-1]) + [_base(rel.name)]:
                if parte in ("imagesTr", "labelsTr", "imagesTs", "train"):
                    continue
                if not PATRON_NOMBRE_NEUTRO.match(parte):
                    r["nombres_no_neutros"].append(str(rel))
                if PATRON_FECHA.search(parte):
                    r["fechas_en_nombres"].append(str(rel))
            if _es_dicom(ruta):
                r["dicom"].append(str(rel))
            nombre = rel.name.lower()
            if nombre.endswith((".nii", ".nii.gz")):
                r["nifti"] += 1
                h = nib.load(str(ruta)).header
                for campo in CAMPOS_NIFTI:
                    valor = _texto(h[campo])
                    if valor:
                        r["campos_nifti"][f"{campo} = «{valor}»"] += 1
            elif nombre.endswith(".mhd"):
                r["mhd"] += 1
                for linea in ruta.read_text(encoding="latin-1").splitlines():
                    if "=" not in linea:
                        continue
                    clave, valor = (t.strip() for t in linea.split("=", 1))
                    if clave not in CLAVES_MHD_ESTANDAR:
                        r["claves_mhd_extra"][f"{clave} = «{valor}»"] += 1
    return res


def informe(res: dict) -> tuple[str, bool]:
    aprobado = True
    lineas = [
        "# Verificación de anonimización de los datos descargados",
        "",
        "Generado con `scripts/verificar_anonimizacion.py` (solo lectura; no modifica los datos).",
        "",
        "| Conjunto | NIfTI revisados | MetaImage revisados | DICOM | Texto libre en cabeceras | Claves no estándar (.mhd) | Nombres no neutros | Fechas en nombres |",
        "|---|---:|---:|---:|---|---|---:|---:|",
    ]
    for conjunto, r in res.items():
        if not r["presente"]:
            lineas.append(f"| {conjunto} | no descargado | | | | | | |")
            continue
        campos = "; ".join(f"{k} ({n})" for k, n in r["campos_nifti"].items()) or "ninguno"
        extra = "; ".join(f"{k} ({n})" for k, n in r["claves_mhd_extra"].items()) or "ninguna"
        lineas.append(
            f"| {conjunto} | {r['nifti']} | {r['mhd']} | {len(r['dicom'])} | {campos} | {extra} | "
            f"{len(r['nombres_no_neutros'])} | {len(r['fechas_en_nombres'])} |"
        )
        if r["dicom"] or r["nombres_no_neutros"] or r["fechas_en_nombres"] or r["claves_mhd_extra"]:
            aprobado = False
    lineas += [""]
    for conjunto, r in res.items():
        for etiqueta, clave in (("nombre no neutro", "nombres_no_neutros"), ("fecha en el nombre", "fechas_en_nombres"),
                                ("archivo DICOM", "dicom")):
            for n in r.get(clave, [])[:20]:
                lineas.append(f"- {conjunto}: {etiqueta}: `{n}`")
    return "\n".join(lineas) + "\n", aprobado


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datos", type=Path, default=RAIZ / "datos")
    ap.add_argument("--salida", type=Path, default=RAIZ / "reports" / "datos")
    args = ap.parse_args()
    texto, aprobado = informe(revisar(args.datos))
    args.salida.mkdir(parents=True, exist_ok=True)
    destino = args.salida / "verificacion_anonimizacion.md"
    veredicto = "SIN HALLAZGOS" if aprobado else "CON HALLAZGOS (revisar la lista)"
    destino.write_text(texto + f"\n**Resultado:** {veredicto}.\n", encoding="utf-8")
    print(f"Resultado: {veredicto}. Informe en {destino}")


if __name__ == "__main__":
    main()
