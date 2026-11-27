"""Pruebas del script de RR-01 por la API (tarea 1715), sin el modelo.

Usan la API real con TestClient, SQLite y el pipeline falso de `backend/tests/processing`.
La tarea en segundo plano va apagada: la espera entre consultas del script procesa el
siguiente trabajo a mano. Los NIfTI son sintéticos; nunca se usan datos reales.
"""
import json
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
for carpeta in ("api", "processing"):
    ruta = str(RAIZ / "backend" / "tests" / carpeta)
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

from apoyo_api import Entorno  # noqa: E402
from apoyo_procesamiento import (  # noqa: E402
    PipelineFalso, ProveedorFalso, referencia_nifti, volumen_nifti,
)
from prosta_ai import seguridad  # noqa: E402
from prosta_ai.pipeline import stages  # noqa: E402
from scripts.medir_rr01_api import (  # noqa: E402
    DIVISION, ErrorMedicion, ResultadoCaso, casos_de_prueba, condiciones_equipo, crear_cuenta,
    informe, medir, medir_caso, resumen, rutas_caso,
)

CASOS = ["prostate_13", "prostate_17"]


@pytest.fixture(autouse=True)
def _bcrypt_rapido(monkeypatch):
    monkeypatch.setattr(seguridad, "ROUNDS", 4)


@pytest.fixture
def datos(tmp_path):
    """Carpetas imagesTr y labelsTr con volúmenes sintéticos bajo los ids del conjunto."""
    imagenes, etiquetas = tmp_path / "imagesTr", tmp_path / "labelsTr"
    imagenes.mkdir()
    etiquetas.mkdir()
    for caso in CASOS:
        (imagenes / f"{caso}.nii.gz").write_bytes(volumen_nifti())
        (etiquetas / f"{caso}.nii.gz").write_bytes(referencia_nifti())
    return imagenes, etiquetas


def _entorno(tmp_path, pipeline=None):
    return Entorno(tmp_path / "api", proveedor=ProveedorFalso(pipeline) if pipeline else None)


@pytest.fixture
def entorno(tmp_path):
    (tmp_path / "api").mkdir()
    e = _entorno(tmp_path)
    yield e
    e.cerrar()


def _procesar_al_esperar(entorno):
    """En lugar de dormir, la «tarea en segundo plano» toma el siguiente trabajo."""
    return lambda _s: entorno.servicio.procesar_siguiente()


def _condiciones():
    return condiciones_equipo("http://localhost:8000", "cpu", 0.5, "abc1234")


# --- Casos y archivos ---

def test_casos_de_prueba_son_los_cinco_de_la_division():
    casos = casos_de_prueba(DIVISION)
    assert casos == ["prostate_13", "prostate_17", "prostate_28", "prostate_34", "prostate_44"]
    datos = json.loads(DIVISION.read_text(encoding="utf-8"))
    assert not set(casos) & set(datos["conjuntos"]["entrenamiento"])


def test_rutas_caso_exige_imagen_y_mascara(datos):
    imagenes, etiquetas = datos
    imagen, mascara = rutas_caso("prostate_13", imagenes, etiquetas)
    assert imagen.parent == imagenes and mascara.parent == etiquetas
    (etiquetas / "prostate_17.nii.gz").unlink()
    with pytest.raises(FileNotFoundError, match="prostate_17"):
        rutas_caso("prostate_17", imagenes, etiquetas)


# --- Flujo por la API ---

def test_crear_cuenta_da_token_que_sirve(entorno):
    cab = crear_cuenta(entorno.client)
    assert entorno.client.get("/api/estudios", headers=cab).status_code == 200


def test_medir_recorre_los_casos_y_toma_tiempos_y_metricas(entorno, datos):
    imagenes, etiquetas = datos
    res = medir(entorno.client, CASOS, imagenes, etiquetas, intervalo_s=0,
                dormir=_procesar_al_esperar(entorno))
    assert res["version_api"]
    assert res["modelo"]["nombre"] == "modelo_falso"
    assert [f.caso for f in res["filas"]] == CASOS
    for f in res["filas"]:
        assert f.estado == "completado" and f.error is None
        assert f.carga_s > 0 and f.procesar_s > 0
        assert f.total_s == pytest.approx(f.carga_s + f.procesar_s, abs=1e-6)
        # el pipeline falso segmenta exactamente la referencia
        assert f.dice == pytest.approx(1.0) and f.iou == pytest.approx(1.0)
        assert f.consultas >= 1
        assert f.proceso_api_s is not None and f.proceso_api_s >= 0
        assert len(f.etapas) == 5 and all(v is not None for v in f.etapas.values())
    rs = resumen(res["filas"])
    assert rs["medidos"] == 2 and rs["cumple"] and rs["cumple_total"]


def test_trabajo_fallido_queda_con_su_etapa_y_mensaje(tmp_path, datos):
    (tmp_path / "api").mkdir()
    e = _entorno(tmp_path, PipelineFalso(falla_en=stages.SEGMENTACION))
    try:
        imagenes, etiquetas = datos
        imagen, mascara = rutas_caso("prostate_13", imagenes, etiquetas)
        f = medir_caso(e.client, crear_cuenta(e.client), "prostate_13", imagen, mascara,
                       intervalo_s=0, dormir=_procesar_al_esperar(e))
    finally:
        e.cerrar()
    assert f.estado == "fallido"
    assert f.procesar_s is None and f.total_s is None and f.dice is None
    assert stages.SEGMENTACION in f.error and "Falla de prueba." in f.error
    rs = resumen([f])
    assert not rs["cumple"]


def test_espera_maxima_corta_el_caso_sin_colgarse(entorno, datos):
    imagenes, etiquetas = datos
    imagen, mascara = rutas_caso("prostate_13", imagenes, etiquetas)
    reloj = iter(range(0, 10_000, 100))  # cada lectura avanza 100 s; nadie procesa el trabajo
    f = medir_caso(entorno.client, crear_cuenta(entorno.client), "prostate_13", imagen, mascara,
                   espera_max_s=250, reloj=lambda: float(next(reloj)), dormir=lambda _s: None)
    assert f.estado == "error"
    assert "no terminó en 250 s" in f.error and "pendiente" in f.error


def test_carga_rechazada_se_reporta_con_el_mensaje_de_la_api(entorno, tmp_path):
    malo = tmp_path / "malo.nii.gz"
    malo.write_bytes(b"no es un nifti")
    f = medir_caso(entorno.client, crear_cuenta(entorno.client), "prostate_13", malo, malo)
    assert f.estado == "error"
    assert f.error.startswith("Carga: HTTP 422")


def test_error_de_acceso_se_explica():
    class ClienteFalso:
        def post(self, *a, **k):
            class R:
                status_code = 500
                text = "x"

                def json(self):
                    return {"detalle": "No disponible."}
            return R()
    with pytest.raises(ErrorMedicion, match="Acceso: HTTP 500: No disponible."):
        crear_cuenta(ClienteFalso())


# --- Resumen e informe ---

def _fila(caso, carga, procesar, dice=0.9):
    return ResultadoCaso(caso, "completado", carga_s=carga, procesar_s=procesar,
                         total_s=carga + procesar, cola_api_s=1.0, proceso_api_s=procesar - 2,
                         etapas={"control de calidad": 0.1, "segmentación": procesar - 3},
                         dice=dice, iou=dice - 0.1)


def test_resumen_media_maximo_y_limite_de_120_s():
    filas = [_fila("prostate_13", 1.0, 30.0), _fila("prostate_17", 2.0, 20.0)]
    rs = resumen(filas)
    assert rs["procesar_s"]["media"] == pytest.approx(25.0)
    assert rs["procesar_s"]["max"] == pytest.approx(30.0)
    assert rs["total_s"]["max"] == pytest.approx(31.0)
    assert rs["procesar_caliente_media"] == pytest.approx(20.0)  # sin el primero (en frío)
    assert rs["cumple"]
    assert not resumen(filas + [_fila("prostate_28", 1.0, 121.0)])["cumple"]
    # 119 s procesando cumple RR-01, aunque con la carga pase de 120 s de punta a punta
    rs = resumen([_fila("prostate_13", 5.0, 119.0)])
    assert rs["cumple"] and not rs["cumple_total"]


def test_resumen_sin_casos_completados_no_cumple():
    rs = resumen([ResultadoCaso("prostate_13", "error", error="x")])
    assert rs["medidos"] == 0 and not rs["cumple"]


def test_informe_tabla_resumen_y_sin_datos_personales(entorno, datos):
    imagenes, etiquetas = datos
    res = medir(entorno.client, CASOS, imagenes, etiquetas, intervalo_s=0,
                dormir=_procesar_al_esperar(entorno))
    texto = informe(res, _condiciones(), "2026-11-27")
    assert texto.startswith("# RR-01 por la API con los casos de prueba (tarea 1715) — 2026-11-27")
    assert "no son un diagnóstico" in texto
    assert "`prostate_13` (en frío)" in texto and "`prostate_17`" in texto
    assert "| **Media** |" in texto and "| **Máximo** |" in texto
    assert "**se cumple**" in texto
    assert "No se compara con GPU" in texto
    assert "`abc1234`" in texto
    # ni el alias de la cuenta, ni rutas locales, ni nombres de archivo de los datos
    assert "rr01_" not in texto
    assert str(imagenes) not in texto and str(etiquetas.parent) not in texto
    assert ".nii" not in texto
    # todas las filas de cada tabla tienen las mismas columnas que su encabezado
    for bloque in re.split(r"\n\n", texto):
        lineas = [x for x in bloque.splitlines() if x.startswith("|")]
        if lineas:
            assert len({x.count("|") for x in lineas}) == 1, bloque


def test_informe_con_errores_dice_que_no_se_cumple():
    filas = [_fila("prostate_13", 1.0, 30.0),
             ResultadoCaso("prostate_17", "fallido", error="Trabajo fallido en «ROI»: x")]
    texto = informe({"filas": filas, "version_api": "0.6.0", "modelo": None}, _condiciones(),
                    "2026-11-27")
    assert "**no se cumple**" in texto
    assert "- `prostate_17`: Trabajo fallido en «ROI»: x" in texto
    assert "Casos completados: 1 de 2." in texto


def test_informe_sin_ningun_caso_completado():
    filas = [ResultadoCaso("prostate_13", "error", error="Carga: HTTP 422: x")]
    texto = informe({"filas": filas, "version_api": "0.6.0", "modelo": None}, _condiciones(),
                    "2026-11-27")
    assert "RR-01 no se puede comprobar" in texto
