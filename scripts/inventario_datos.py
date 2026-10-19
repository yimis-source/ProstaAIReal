"""Inventario de los conjuntos de datos descargados (tarea 1204).

Recorre `datos/`, cuenta los casos de cada conjunto y calcula el SHA-256 de cada
archivo de imagen o máscara. El resultado sirve para comprobar más adelante que
todos trabajamos con los mismos archivos (los datos no se suben al repositorio).

Uso (desde la raíz del repositorio):
    python scripts/inventario_datos.py
    python scripts/inventario_datos.py --datos datos --salida reports/datos

Escribe `inventario_datos.csv` (un archivo por fila) y `inventario_datos.md` (resumen).
Los archivos que no son imágenes (por ejemplo scripts incluidos en una descarga)
se listan como «no esperados» y NO se ejecutan ni se abren.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

# Conjunto -> carpeta relativa a datos/
CONJUNTOS = {
    "MSD Task05_Prostate": "Task05_Prostate",
    "Prostate158 (entrenamiento)": "externos/prostate158_train",
    "PROMISE12 (entrenamiento)": "externos/promise12/training_data",
    "PROMISE12 (prueba)": "externos/promise12/test_data",
}
EXT_IMAGEN = (".nii.gz", ".nii", ".mhd", ".raw")
EXT_TEXTO = (".json", ".csv")


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def tipo_archivo(nombre: str) -> str:
    n = nombre.lower()
    if n.endswith(EXT_IMAGEN):
        return "imagen"
    if n.endswith(EXT_TEXTO):
        return "metadatos"
    return "no esperado"


def caso_de(conjunto: str, rel: Path) -> str | None:
    """Identificador del caso al que pertenece un archivo (None si no aplica)."""
    nombre = rel.name
    if conjunto.startswith("MSD"):
        if rel.parts[0] in ("imagesTr", "labelsTr", "imagesTs") and nombre.endswith(".nii.gz"):
            return f"{rel.parts[0]}:{nombre[: -len('.nii.gz')]}"
        return None
    if conjunto.startswith("Prostate158"):
        return rel.parts[1] if len(rel.parts) >= 3 and rel.parts[0] == "train" else None
    if conjunto.startswith("PROMISE12"):
        if nombre.lower().endswith((".mhd", ".raw")):
            return nombre.split(".")[0].replace("_segmentation", "")
        return None
    return None


def inventariar(datos: Path) -> tuple[list[dict], dict]:
    filas: list[dict] = []
    resumen: dict = {}
    for conjunto, carpeta in CONJUNTOS.items():
        base = datos / carpeta
        if not base.exists():
            resumen[conjunto] = {"presente": False}
            continue
        casos: set[str] = set()
        por_tipo: Counter = Counter()
        bytes_total = 0
        no_esperados: list[str] = []
        for ruta in sorted(p for p in base.rglob("*") if p.is_file()):
            rel = ruta.relative_to(base)
            if rel.name.startswith("._") or "convertidas" in rel.parts:
                continue  # restos de macOS y copias convertidas localmente (no son la descarga)
            tipo = tipo_archivo(rel.name)
            tam = ruta.stat().st_size
            huella = sha256(ruta) if tipo != "no esperado" else ""
            if tipo == "no esperado":
                no_esperados.append(str(rel))
            caso = caso_de(conjunto, rel)
            if caso:
                casos.add(caso)
            por_tipo[tipo] += 1
            bytes_total += tam
            filas.append(
                {"conjunto": conjunto, "archivo": f"{carpeta}/{rel}", "tipo": tipo,
                 "bytes": tam, "sha256": huella, "caso": caso or ""}
            )
        resumen[conjunto] = {
            "presente": True,
            "casos": casos,
            "archivos": dict(por_tipo),
            "bytes": bytes_total,
            "no_esperados": no_esperados,
        }
    return filas, resumen


def contar_casos(conjunto: str, casos: set[str]) -> str:
    if conjunto.startswith("MSD"):
        c = defaultdict(set)
        for k in casos:
            carpeta, nombre = k.split(":")
            c[carpeta].add(nombre)
        con_mascara = len(c["imagesTr"] | c["labelsTr"])
        return f"{con_mascara} con máscara (imagesTr/labelsTr) + {len(c['imagesTs'])} sin máscara (imagesTs)"
    return str(len(casos))


def escribir(filas: list[dict], resumen: dict, salida: Path) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    with open(salida / "inventario_datos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["conjunto", "archivo", "tipo", "bytes", "sha256", "caso"])
        w.writeheader()
        w.writerows(filas)
    lineas = [
        "# Inventario de datos descargados",
        "",
        "Generado con `scripts/inventario_datos.py`. El detalle por archivo (con SHA-256) está en",
        "`inventario_datos.csv`. Los datos no se versionan (`datos/` está en `.gitignore`).",
        "",
        "| Conjunto | Casos | Archivos de imagen | Metadatos | No esperados | Tamaño (MB) |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for conjunto, r in resumen.items():
        if not r["presente"]:
            lineas.append(f"| {conjunto} | no descargado | – | – | – | – |")
            continue
        a = r["archivos"]
        lineas.append(
            f"| {conjunto} | {contar_casos(conjunto, r['casos'])} | {a.get('imagen', 0)} | "
            f"{a.get('metadatos', 0)} | {a.get('no esperado', 0)} | {r['bytes'] / 1e6:.1f} |"
        )
    lineas += ["", "## Archivos no esperados", ""]
    hay = False
    for conjunto, r in resumen.items():
        for n in r.get("no_esperados", []):
            hay = True
            lineas.append(f"- {conjunto}: `{n}` (no se abre ni se ejecuta; no forma parte de los datos)")
    if not hay:
        lineas.append("Ninguno.")
    (salida / "inventario_datos.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datos", type=Path, default=RAIZ / "datos")
    ap.add_argument("--salida", type=Path, default=RAIZ / "reports" / "datos")
    args = ap.parse_args()
    filas, resumen = inventariar(args.datos)
    escribir(filas, resumen, args.salida)
    print(f"{len(filas)} archivos inventariados; resumen en {args.salida / 'inventario_datos.md'}")


if __name__ == "__main__":
    main()
