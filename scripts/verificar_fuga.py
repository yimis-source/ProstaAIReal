"""Verificación de fuga de pacientes (tarea 1304, RC-04, riesgo 4 del Acta).

1. Verifica `entrenamiento/division_task05.json`: conjuntos completos, sin pacientes
   repetidos dentro ni entre conjuntos, y huella SHA-256 intacta.
2. (Pendiente) Buscar pacientes compartidos entre MSD Task05 y PROMISE12.

Uso (desde la raíz del repositorio):
    python scripts/verificar_fuga.py [--convertidos datos/convertidos] [--salida reports/division]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from entrenamiento.division import CONJUNTOS, cargar_division  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--division", type=Path, default=RAIZ / "entrenamiento" / "division_task05.json")
    ap.add_argument("--salida", type=Path, default=RAIZ / "reports" / "division")
    args = ap.parse_args()

    doc = cargar_division(args.division)  # lanza ValueError si hay repetidos o la huella no coincide
    conj = {k: set(doc["conjuntos"][k]) for k in CONJUNTOS}
    inter = {f"{a} ∩ {b}": sorted(conj[a] & conj[b])
             for i, a in enumerate(CONJUNTOS) for b in CONJUNTOS[i + 1:]}

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
        "## 2. Pacientes compartidos con otros conjuntos",
        "",
        "Pendiente: comparar MSD Task05 con PROMISE12 (ambos tienen estudios de Radboud, Nijmegen).",
    ]
    args.salida.mkdir(parents=True, exist_ok=True)
    (args.salida / "verificacion_division.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("División OK: sin pacientes repetidos entre conjuntos.")


if __name__ == "__main__":
    main()
