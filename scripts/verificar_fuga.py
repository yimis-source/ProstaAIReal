"""Verificación de fuga de pacientes (tarea 1304, RC-04, riesgo 4 del Acta).

1. Verifica `entrenamiento/division_task05.json`: conjuntos completos, sin pacientes
   repetidos dentro ni entre conjuntos, y huella SHA-256 intacta.
2. Busca pacientes compartidos entre MSD Task05 y PROMISE12 (ambos incluyen estudios
   de Radboud, Nijmegen): para cada par con la misma forma compara los vóxeles de la
   imagen T2, admitiendo inversión de los ejes x/y (cada formato guarda la orientación
   a su manera). Si los vóxeles son idénticos es el mismo estudio. Para esos pares
   también compara las máscaras (Dice) para saber si la anotación es la misma.

Necesita los NIfTI de `scripts/convertir_nifti.py` (datos/convertidos/).

Uso (desde la raíz del repositorio):
    python scripts/verificar_fuga.py [--convertidos datos/convertidos] [--salida reports/division]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import nibabel as nib
import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from entrenamiento.division import CONJUNTOS, cargar_division  # noqa: E402


def _cargar(ruta: Path) -> np.ndarray:
    return np.asarray(nib.load(str(ruta)).dataobj, dtype=np.float32)


def _variantes(arr: np.ndarray):
    """El arreglo con los ejes x e y invertidos o no (4 combinaciones)."""
    for fx in (False, True):
        for fy in (False, True):
            a = arr[::-1] if fx else arr
            a = a[:, ::-1] if fy else a
            yield (fx, fy), a


def _dice(a: np.ndarray, b: np.ndarray) -> float:
    a, b = a > 0, b > 0
    total = a.sum() + b.sum()
    return 1.0 if total == 0 else float(2 * (a & b).sum() / total)


def buscar_compartidos(convertidos: Path) -> list[dict]:
    msd = sorted((convertidos / "msd_task05").glob("*_t2.nii.gz"))
    promise = []
    for sub in ("promise12_entrenamiento", "promise12_prueba"):
        promise += sorted((convertidos / sub).glob("*_t2.nii.gz"))
    formas = {p: nib.load(str(p)).shape[:3] for p in msd + promise}
    pares = []
    for a in msd:
        for b in promise:
            if formas[a] != formas[b]:
                continue
            x, y = _cargar(a), _cargar(b)
            for (fx, fy), yv in _variantes(y):
                if np.array_equal(x, yv):
                    caso_a = a.name.replace("_t2.nii.gz", "")
                    caso_b = b.name.replace("_t2.nii.gz", "")
                    ma = _cargar(a.with_name(f"{caso_a}_mascara.nii.gz"))
                    mb_ruta = b.with_name(f"{caso_b}_mascara.nii.gz")
                    dice_m = None
                    if mb_ruta.exists():
                        _, mb = list(_variantes(_cargar(mb_ruta)))[2 * fx + fy]
                        dice_m = _dice(ma, mb)
                    pares.append({"msd": caso_a, "promise12": f"{b.parent.name.replace('promise12_', '')}/{caso_b}",
                                  "dice_mascaras": dice_m})
                    break
    return pares


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--division", type=Path, default=RAIZ / "entrenamiento" / "division_task05.json")
    ap.add_argument("--convertidos", type=Path, default=RAIZ / "datos" / "convertidos")
    ap.add_argument("--salida", type=Path, default=RAIZ / "reports" / "division")
    args = ap.parse_args()

    doc = cargar_division(args.division)  # lanza ValueError si hay repetidos o la huella no coincide
    conj = {k: set(doc["conjuntos"][k]) for k in CONJUNTOS}
    inter = {f"{a} ∩ {b}": sorted(conj[a] & conj[b])
             for i, a in enumerate(CONJUNTOS) for b in CONJUNTOS[i + 1:]}
    pares = buscar_compartidos(args.convertidos)
    en = {c: k for k in CONJUNTOS for c in conj[k]}

    lineas = [
        "# Verificación de la división por paciente y de fuga entre conjuntos",
        "",
        "Generado con `scripts/verificar_fuga.py`.",
        "",
        "## 1. División de MSD Task05 (RC-04)",
        "",
        f"- Archivo: `entrenamiento/division_task05.json`, semilla {doc['semilla']}, huella `{doc['huella_sha256'][:16]}…` (verificada).",
        f"- Cantidades: " + ", ".join(f"{k} {len(conj[k])}" for k in CONJUNTOS) + f" (total {sum(len(v) for v in conj.values())}).",
        "- En Task05 cada caso es un paciente distinto (no hay identificador de paciente aparte).",
        "",
        "| Intersección | Casos |",
        "|---|---|",
    ]
    lineas += [f"| {k} | {', '.join(v) if v else 'vacía'} |" for k, v in inter.items()]
    lineas += [
        "",
        "**Resultado:** " + ("sin pacientes repetidos entre conjuntos." if not any(inter.values())
                             else "HAY PACIENTES REPETIDOS: corregir antes de continuar."),
        "",
        "## 2. Pacientes compartidos entre MSD Task05 y PROMISE12",
        "",
        "Se comparan los vóxeles de la imagen T2 de cada par con la misma forma (admitiendo inversión de ejes x/y).",
        "",
        "| Caso MSD | Conjunto en la división | Caso PROMISE12 | Imagen | Dice entre máscaras |",
        "|---|---|---|---|---:|",
    ]
    for p in pares:
        d = "–" if p["dice_mascaras"] is None else f"{p['dice_mascaras']:.4f}"
        lineas.append(f"| {p['msd']} | {en.get(p['msd'], 'fuera de la división')} | {p['promise12']} | idéntica | {d} |")
    n_prueba = sum(en.get(p["msd"]) == "prueba" for p in pares)
    misma_mascara = [p for p in pares if p["dice_mascaras"] is not None and p["dice_mascaras"] > 0.9999]
    lineas += [
        "",
        f"**Resultado:** {len(pares)} casos de MSD Task05 (con máscara) son exactamente el mismo estudio que un caso de "
        f"PROMISE12; {len(misma_mascara)} de ellos con la misma máscara "
        f"({', '.join(p['msd'] + ' ≡ ' + p['promise12'] for p in misma_mascara) or 'ninguno'}) y el resto con otra anotación. "
        f"{n_prueba} están en el conjunto de prueba.",
        "",
        "**Decisión:** PROMISE12 no se usa para entrenar ni para evaluar: mezclarlo con MSD metería los mismos pacientes "
        "en entrenamiento y prueba. Se conserva solo como referencia.",
    ]
    args.salida.mkdir(parents=True, exist_ok=True)
    (args.salida / "verificacion_division.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"División OK; {len(pares)} casos compartidos con PROMISE12 ({n_prueba} en prueba).")


if __name__ == "__main__":
    main()
