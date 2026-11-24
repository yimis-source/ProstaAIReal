"""Pruebas del informe de rendimiento (tareas 1408 y 1602) sin ejecutar el modelo."""
from scripts.medir_rendimiento import PASOS, informe, nombre_informe


def _resultado(gpu: bool) -> dict:
    filas = []
    for rep, total in ((1, 6.9), (2, 5.1), (3, 4.9)):
        fila = {"repeticion": rep, "frio": rep == 1, **{p: total / len(PASOS) for p in PASOS},
                "total": total, "rss_pico_mb": 3000.0 + rep}
        if gpu:
            fila["gpu_pico_mb"] = 1500.0 + rep
        filas.append(fila)
    res = {"filas": filas, "rss_inicio_mb": 1400.0,
           "info": {"forma_original": (320, 320, 20), "espaciado": (0.625, 0.625, 3.6),
                    "forma_preparada": (400, 400, 138), "voxeles_mascara": 1000}}
    if gpu:
        res["gpu"] = "Tesla T4"
    return res


def test_nombre_del_informe_depende_del_dispositivo():
    assert nombre_informe("cpu", "2026-11-23") == "rendimiento_1408_2026-11-23.md"
    assert nombre_informe("cuda", "2026-11-23") == "rendimiento_1408_gpu_2026-11-23.md"
    assert nombre_informe("cuda:0", "2026-11-23") == "rendimiento_1408_gpu_2026-11-23.md"


def test_informe_cpu_dice_que_no_hay_gpu_y_no_tiene_columna_gpu():
    texto = informe("prostate_13", _resultado(gpu=False), "cpu", 4)
    assert "No disponible en este equipo" in texto
    assert "Pico GPU (MB)" not in texto


def test_informe_gpu_muestra_nombre_y_memoria_de_la_gpu():
    texto = informe("prostate_13", _resultado(gpu=True), "cuda", 1)
    assert "No disponible en este equipo" not in texto
    assert "Tesla T4" in texto
    assert "| Pico GPU (MB) |" in texto
    assert "Memoria pico de la GPU (`torch.cuda.max_memory_allocated`): 1503 MB." in texto
    assert "no son comparables con los de CPU" in texto
    # el encabezado, el separador y las filas tienen el mismo número de columnas
    lineas = texto.splitlines()
    encabezado = next(l for l in lineas if l.startswith("| Rep."))
    separador = next(l for l in lineas if l.startswith("|---"))
    fila = next(l for l in lineas if l.startswith("| 1 (en frío)"))
    assert encabezado.count("|") == separador.count("|") == fila.count("|")
