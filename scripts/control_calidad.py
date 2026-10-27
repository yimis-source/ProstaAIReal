"""Control de calidad de las imágenes y máscaras (tarea 1301, RF-10).

Para cada caso comprueba que el archivo se puede leer completo, que el volumen es
3D (o 4D con canales), que no tiene valores no numéricos ni intensidad constante,
que tiene al menos 8 cortes y 32x32 vóxeles por corte, espaciado positivo y, si
hay máscara, que tiene la misma forma que la imagen y solo etiquetas esperadas.

Toda imagen que no supere el control se EXCLUYE y se registra con su motivo.

Uso (desde la raíz del repositorio):
    python scripts/control_calidad.py [--datos datos] [--salida reports/calidad]
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import SimpleITK as sitk

RAIZ = Path(__file__).resolve().parents[1]
MIN_CORTES = 8
MIN_LADO = 32
ETIQUETAS_VALIDAS = {0, 1, 2}


@dataclass
class Resultado:
    conjunto: str
    caso: str
    aprobado: bool = True
    motivos: list[str] = field(default_factory=list)

    def excluir(self, motivo: str) -> None:
        self.aprobado = False
        self.motivos.append(motivo)


def leer(ruta: Path) -> sitk.Image:
    return sitk.ReadImage(str(ruta))


def _volumen(img: sitk.Image) -> np.ndarray:
    arr = sitk.GetArrayFromImage(img)  # (z, y, x) o (t, z, y, x) / (z, y, x, c)
    return arr


def revisar_caso(conjunto: str, caso: str, imagen: Path, mascara: Path | None) -> Resultado:
    r = Resultado(conjunto, caso)
    try:
        img = leer(imagen)
    except Exception as exc:
        r.excluir(f"imagen ilegible: {exc}")
        return r
    dim = img.GetDimension()
    if dim not in (3, 4):
        r.excluir(f"la imagen tiene {dim} dimensiones")
        return r
    tam = img.GetSize()[:3]
    esp = img.GetSpacing()[:3]
    arr = _volumen(img).astype(np.float32)
    if not np.isfinite(arr).all():
        r.excluir("valores no numéricos (NaN o infinitos)")
    if float(arr.max()) == float(arr.min()):
        r.excluir("intensidad constante")
    if tam[2] < MIN_CORTES:
        r.excluir(f"{tam[2]} cortes (mínimo {MIN_CORTES})")
    if tam[0] < MIN_LADO or tam[1] < MIN_LADO:
        r.excluir(f"cortes de {tam[0]}x{tam[1]} vóxeles (mínimo {MIN_LADO})")
    if not all(np.isfinite(e) and e > 0 for e in esp):
        r.excluir("espaciado no positivo")
    if mascara is None:
        return r
    try:
        m = leer(mascara)
    except Exception as exc:
        r.excluir(f"máscara ilegible: {exc}")
        return r
    if m.GetSize()[:3] != tam:
        r.excluir(f"máscara {m.GetSize()} con forma distinta a la imagen {tam}")
        return r
    valores = set(np.unique(sitk.GetArrayFromImage(m)).astype(int).tolist())
    if not valores <= ETIQUETAS_VALIDAS:
        r.excluir(f"etiquetas inesperadas en la máscara: {sorted(valores - ETIQUETAS_VALIDAS)}")
    if valores <= {0}:
        r.excluir("máscara vacía")
    return r


def casos(datos: Path) -> list[tuple[str, str, Path, Path | None]]:
    lista = []
    msd = datos / "Task05_Prostate"
    for p in sorted((msd / "imagesTr").glob("prostate_*.nii.gz")):
        lista.append(("MSD Task05 (con máscara)", p.name[:-7], p, msd / "labelsTr" / p.name))
    for p in sorted((msd / "imagesTs").glob("prostate_*.nii.gz")):
        lista.append(("MSD Task05 (sin máscara)", p.name[:-7], p, None))
    for carpeta, nombre in (("training_data", "PROMISE12 (entrenamiento)"), ("test_data", "PROMISE12 (prueba)")):
        base = datos / "externos" / "promise12" / carpeta
        for p in sorted(base.glob("Case??.mhd")):
            seg = base / f"{p.stem}_segmentation.mhd"
            lista.append((nombre, p.stem, p, seg if seg.exists() else None))
    return lista


def escribir(resultados: list[Resultado], salida: Path) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    with open(salida / "control_calidad.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["conjunto", "caso", "resultado", "motivo"])
        for r in resultados:
            w.writerow([r.conjunto, r.caso, "aprobado" if r.aprobado else "excluido", "; ".join(r.motivos)])
    lineas = [
        "# Control de calidad de imágenes y máscaras (RF-10)",
        "",
        "Generado con `scripts/control_calidad.py`. Detalle por caso en `control_calidad.csv`.",
        f"Reglas: lectura, 3D/4D, valores finitos, "
        f"intensidad no constante, ≥ {MIN_CORTES} cortes, ≥ {MIN_LADO}x{MIN_LADO} vóxeles por corte, "
        "espaciado positivo; máscara con la misma forma, etiquetas en {0, 1, 2} y no vacía.",
        "",
        "| Conjunto | Casos revisados | Aprobados | Excluidos |",
        "|---|---:|---:|---:|",
    ]
    conjuntos: dict[str, list[Resultado]] = {}
    for r in resultados:
        conjuntos.setdefault(r.conjunto, []).append(r)
    for nombre, lista in conjuntos.items():
        ok = sum(r.aprobado for r in lista)
        lineas.append(f"| {nombre} | {len(lista)} | {ok} | {len(lista) - ok} |")
    excluidos = [r for r in resultados if not r.aprobado]
    lineas += ["", "## Casos excluidos", ""]
    lineas += [f"- {r.conjunto} / {r.caso}: {'; '.join(r.motivos)}" for r in excluidos] or ["Ninguno."]
    (salida / "control_calidad.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datos", type=Path, default=RAIZ / "datos")
    ap.add_argument("--salida", type=Path, default=RAIZ / "reports" / "calidad")
    args = ap.parse_args()
    resultados = [revisar_caso(*c) for c in casos(args.datos)]
    escribir(resultados, args.salida)
    excl = sum(not r.aprobado for r in resultados)
    print(f"{len(resultados)} casos revisados, {excl} excluidos. Informe en {args.salida / 'control_calidad.md'}")


if __name__ == "__main__":
    main()
