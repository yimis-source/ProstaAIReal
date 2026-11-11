"""Medición de tiempo y memoria de la inferencia (tarea 1408, riesgo 1 del Acta, RR-01).

Con un estudio representativo mide, por separado, cuánto tarda cada paso de la
ruta de inferencia y cuánta memoria usa el proceso:

1. lectura del NIfTI y control de calidad,
2. preparación (orientación, remuestreo a 0,5 mm, intensidad),
3. inferencia por ventana deslizante (incluye el posproceso de componentes),
4. paso de la máscara a la rejilla de la imagen original.

La primera repetición incluye la carga de los pesos (arranque en frío); las
siguientes reutilizan el modelo ya cargado, como hará la aplicación.

Uso (desde la raíz del repositorio):
    python scripts/medir_rendimiento.py --caso prostate_13 --repeticiones 3 [--dispositivo cpu]

Escribe `reports/rendimiento/rendimiento_1408_<fecha>.md`.
"""
from __future__ import annotations

import argparse
import platform
import resource
import statistics
import sys
import time
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
for ruta in (RAIZ / "backend", RAIZ):
    if str(ruta) not in sys.path:
        sys.path.insert(0, str(ruta))

import monai
import numpy as np
import torch

from prosta_ai.pipeline.factory import build_pipeline
from prosta_ai.pipeline.io import load_volume
from prosta_ai.pipeline.preparation import prepare_volume
from prosta_ai.pipeline.roi import mask_to_original_space
from prosta_ai.pipeline.validators import detailed_validation

LIMITE_S = 120.0  # RR-01: un estudio en 2 minutos como máximo
PASOS = ("lectura y control de calidad", "preparación", "inferencia", "rejilla original")


def rss_actual_mb() -> float:
    """Memoria residente actual del proceso (Linux, /proc/self/status)."""
    for linea in Path("/proc/self/status").read_text().splitlines():
        if linea.startswith("VmRSS:"):
            return int(linea.split()[1]) / 1024
    return float("nan")


def rss_pico_mb() -> float:
    """Pico de memoria residente del proceso desde que arrancó (ru_maxrss está en KiB en Linux)."""
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def cpu_nombre() -> str:
    try:
        for linea in Path("/proc/cpuinfo").read_text().splitlines():
            if linea.startswith("model name"):
                return linea.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or platform.machine()


def ram_total_gb() -> float:
    for linea in Path("/proc/meminfo").read_text().splitlines():
        if linea.startswith("MemTotal:"):
            return int(linea.split()[1]) / 1024**2
    return float("nan")


def medir(caso: str, datos: Path, modelos: Path, repeticiones: int, dispositivo: str) -> dict:
    imagen = datos / "imagesTr" / f"{caso}.nii.gz"
    pipeline = build_pipeline("prostate_mri_anatomy", modelos / "prostate_mri_anatomy")
    estrategia = pipeline.strategy
    estrategia._device = torch.device(dispositivo)
    rss_inicio = rss_actual_mb()
    filas = []
    info: dict = {}
    for rep in range(1, repeticiones + 1):
        tiempos = {}
        t = time.perf_counter()
        vol = load_volume([imagen], "NIfTI")
        detailed_validation(vol)
        tiempos[PASOS[0]] = time.perf_counter() - t

        t = time.perf_counter()
        prep = prepare_volume(vol, estrategia.config)
        tiempos[PASOS[1]] = time.perf_counter() - t

        t = time.perf_counter()
        mascara = estrategia.segment(prep)
        tiempos[PASOS[2]] = time.perf_counter() - t

        t = time.perf_counter()
        original = mask_to_original_space(mascara, prep, vol)
        tiempos[PASOS[3]] = time.perf_counter() - t

        tiempos["total"] = sum(tiempos[p] for p in PASOS)
        filas.append({"repeticion": rep, "frio": rep == 1, **tiempos, "rss_pico_mb": rss_pico_mb()})
        if rep == 1:
            info = {
                "forma_original": tuple(int(s) for s in vol.data.shape),
                "espaciado": tuple(round(s, 3) for s in vol.spacing),
                "forma_preparada": tuple(int(s) for s in prep.tensor.shape[1:]),
                "voxeles_mascara": int(original.sum()),
            }
        print(f"repetición {rep}: total {tiempos['total']:.1f} s, pico de memoria {rss_pico_mb():.0f} MB", flush=True)
    return {"filas": filas, "info": info, "rss_inicio_mb": rss_inicio}


def informe(caso: str, res: dict, dispositivo: str, hilos: int) -> str:
    filas = res["filas"]
    calientes = [f for f in filas if not f["frio"]] or filas
    lineas = [
        f"# Tiempo y memoria de la inferencia (tarea 1408) — {date.today().isoformat()}",
        "",
        "Uso académico y experimental. Mide la ruta de inferencia del ciclo 3 con un estudio representativo.",
        "",
        "## Condiciones",
        "",
        f"- Estudio: `{caso}` de MSD Task05 (canal T2), forma {res['info']['forma_original']}, "
        f"espaciado {res['info']['espaciado']} mm; volumen preparado a 0,5 mm: {res['info']['forma_preparada']}.",
        "- Modelo: `prostate_mri_anatomy` 0.3.6, ventana deslizante 96³, lote 4, solape 0,5.",
        f"- Dispositivo: {dispositivo}. CPU: {cpu_nombre()}; {hilos} hilos de torch; RAM {ram_total_gb():.1f} GB; "
        f"{platform.system()} {platform.release()}.",
        f"- Software: Python {platform.python_version()}, torch {torch.__version__}, MONAI {monai.__version__}.",
        f"- Repeticiones: {len(filas)}. La primera incluye la carga de los pesos (arranque en frío).",
        "- Memoria: pico de memoria residente (RSS) del proceso medido con `resource.getrusage`.",
        "",
        "## Resultados por repetición (segundos)",
        "",
        "| Rep. | " + " | ".join(PASOS) + " | Total | Pico RSS (MB) |",
        "|---|" + "---:|" * (len(PASOS) + 2),
    ]
    for f in filas:
        marca = f"{f['repeticion']} (en frío)" if f["frio"] else str(f["repeticion"])
        lineas.append(f"| {marca} | " + " | ".join(f"{f[p]:.2f}" for p in PASOS)
                      + f" | **{f['total']:.2f}** | {f['rss_pico_mb']:.0f} |")
    media = statistics.mean(f["total"] for f in calientes)
    peor = max(f["total"] for f in filas)
    inferencia = statistics.mean(f[PASOS[2]] for f in calientes)
    lineas += [
        "",
        "## Resumen",
        "",
        f"- Memoria del proceso tras importar librerías y construir el pipeline: {res['rss_inicio_mb']:.0f} MB; "
        f"pico durante la medición: {max(f['rss_pico_mb'] for f in filas):.0f} MB.",
        f"- Tiempo medio por estudio con el modelo ya cargado: {media:.1f} s (inferencia: {inferencia:.1f} s).",
        f"- Repetición más lenta (de todas, incluida la de arranque en frío): {peor:.1f} s.",
        f"- RR-01 (≤ {LIMITE_S:.0f} s por estudio): **{'se cumple' if peor <= LIMITE_S else 'NO se cumple'}** "
        f"con margen de {LIMITE_S - peor:.0f} s sobre la repetición más lenta.",
        "",
        "## GPU",
        "",
        "No disponible en este equipo (no hay GPU NVIDIA con CUDA). Queda pendiente medir en Google Colab "
        "(ciclo 5) con `--dispositivo cuda`; los tiempos de CPU y GPU no son comparables entre sí.",
        "",
        "## Limitaciones",
        "",
        "- Un solo estudio y un solo equipo; los tiempos cambian con el tamaño del volumen y el hardware.",
        "- No incluye la carga del archivo por la web ni guardar resultados (eso se mide en el ciclo 6).",
        "",
    ]
    return "\n".join(lineas)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--caso", default="prostate_13")
    ap.add_argument("--repeticiones", type=int, default=3)
    ap.add_argument("--dispositivo", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--datos", type=Path, default=RAIZ / "datos" / "Task05_Prostate")
    ap.add_argument("--modelos", type=Path, default=RAIZ / "modelos")
    ap.add_argument("--salida", type=Path, default=RAIZ / "reports" / "rendimiento")
    args = ap.parse_args()
    if args.dispositivo.startswith("cuda") and not torch.cuda.is_available():
        sys.exit("No hay GPU con CUDA en este equipo; use --dispositivo cpu o ejecútelo en Colab.")
    res = medir(args.caso, args.datos, args.modelos, args.repeticiones, args.dispositivo)
    args.salida.mkdir(parents=True, exist_ok=True)
    destino = args.salida / f"rendimiento_1408_{date.today().isoformat()}.md"
    destino.write_text(informe(args.caso, res, args.dispositivo, torch.get_num_threads()), encoding="utf-8")
    print(f"Informe escrito en {destino}")


if __name__ == "__main__":
    main()
