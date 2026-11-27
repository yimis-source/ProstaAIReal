"""CU03 por la API: procesar, estado del trabajo, detalle con trabajos y tarea en segundo plano.

El hilo va apagado (Entorno) y el servicio se llama a mano, con el pipeline falso.
"""
import time

import pytest
from fastapi.testclient import TestClient

from apoyo_api import Entorno
from apoyo_procesamiento import PipelineFalso, ProveedorFalso, referencia_nifti, volumen_nifti
from prosta_ai.constantes import MENSAJE_INTERRUMPIDO
from prosta_ai.models import Estudio, Trabajo
from prosta_ai.pipeline import stages
from prosta_ai.repositories import RepositorioTrabajos

EN_CURSO = "El estudio ya tiene un procesamiento pendiente o en curso."
NO_COMPATIBLE = "El estudio no es compatible y no se puede procesar."


def _estudio(entorno, cab, referencia=True) -> int:
    r = entorno.cargar(cab, volumen_nifti(), referencia=referencia_nifti() if referencia else None)
    assert r.status_code == 201, r.text
    return r.json()["id"]


def _procesar(entorno, cab, id_estudio):
    return entorno.client.post(f"/api/estudios/{id_estudio}/procesar", headers=cab)


def _trabajo(entorno, cab, id_trabajo):
    return entorno.client.get(f"/api/trabajos/{id_trabajo}", headers=cab)


def _iniciar(entorno, id_trabajo):
    """Deja el trabajo en proceso, como si la tarea lo hubiera tomado."""
    with entorno.app.state.fabrica_sesiones() as s:
        repo = RepositorioTrabajos(s)
        repo.iniciar(repo.obtener(id_trabajo))
        s.commit()


@pytest.fixture
def entorno_falla(tmp_path):
    e = Entorno(tmp_path, proveedor=ProveedorFalso(PipelineFalso(falla_en=stages.SEGMENTACION)))
    yield e
    e.cerrar()


# --- POST /api/estudios/{id}/procesar ---

def test_procesar_crea_trabajo_pendiente_con_cinco_etapas(entorno):
    cab = entorno.cabeceras()
    id_estudio = _estudio(entorno, cab)
    r = _procesar(entorno, cab, id_estudio)
    assert r.status_code == 201, r.text
    cuerpo = r.json()
    assert cuerpo["id_estudio"] == id_estudio and cuerpo["codigo"] == "EST-0001"
    assert cuerpo["estado"] == "pendiente"
    assert cuerpo["etapa_fallida"] is None and cuerpo["mensaje_error"] is None
    assert cuerpo["fecha_creacion"] and cuerpo["fecha_inicio"] is None
    assert [e["nombre"] for e in cuerpo["etapas"]] == list(stages.STAGES)
    assert {e["estado"] for e in cuerpo["etapas"]} == {"pendiente"}
    # Solo crea el trabajo: la segmentación la corre la tarea en segundo plano
    assert entorno.proveedor._pipeline.corridas == 0
    assert entorno.contar(Trabajo) == 1


def test_procesar_con_trabajo_pendiente_da_409(entorno):
    cab = entorno.cabeceras()
    id_estudio = _estudio(entorno, cab)
    assert _procesar(entorno, cab, id_estudio).status_code == 201
    r = _procesar(entorno, cab, id_estudio)
    assert r.status_code == 409
    assert r.json() == {"detalle": EN_CURSO}
    assert entorno.contar(Trabajo) == 1


def test_procesar_con_trabajo_en_proceso_da_409(entorno):
    cab = entorno.cabeceras()
    id_estudio = _estudio(entorno, cab)
    _iniciar(entorno, _procesar(entorno, cab, id_estudio).json()["id"])
    r = _procesar(entorno, cab, id_estudio)
    assert r.status_code == 409 and r.json()["detalle"] == EN_CURSO
    assert entorno.client.get(f"/api/estudios/{id_estudio}", headers=cab).json()["estado"] == "en proceso"


def test_procesar_estudio_no_compatible_da_409(entorno):
    cab = entorno.cabeceras()
    id_estudio = _estudio(entorno, cab)
    with entorno.app.state.fabrica_sesiones() as s:
        s.get(Estudio, id_estudio).estado_admision = "no compatible"
        s.commit()
    r = _procesar(entorno, cab, id_estudio)
    assert r.status_code == 409 and r.json()["detalle"] == NO_COMPATIBLE
    assert entorno.contar(Trabajo) == 0
    assert entorno.client.get(f"/api/estudios/{id_estudio}", headers=cab).json()["estado"] == "no compatible"


def test_procesar_estudio_ajeno_o_inexistente_da_404(entorno):
    id_estudio = _estudio(entorno, entorno.cabeceras("ana"))
    otro = entorno.cabeceras("beto")
    for id_ in (id_estudio, 999):
        r = _procesar(entorno, otro, id_)
        assert r.status_code == 404 and r.json()["detalle"] == "Estudio no encontrado."
    assert entorno.contar(Trabajo) == 0


def test_procesar_sin_token_da_401(entorno):
    id_estudio = _estudio(entorno, entorno.cabeceras())
    assert entorno.client.post(f"/api/estudios/{id_estudio}/procesar").status_code == 401


def test_reprocesar_tras_fallido_crea_un_trabajo_nuevo(entorno_falla):
    e = entorno_falla
    cab = e.cabeceras()
    id_estudio = _estudio(e, cab)
    primero = _procesar(e, cab, id_estudio).json()["id"]
    assert e.servicio.procesar_siguiente() is True

    fallido = _trabajo(e, cab, primero).json()
    assert fallido["estado"] == "fallido"
    assert fallido["etapa_fallida"] == "segmentación"
    assert fallido["mensaje_error"] == "Falla de prueba."
    assert [x["estado"] for x in fallido["etapas"]] == [
        "completado", "completado", "fallido", "pendiente", "pendiente"]

    r = _procesar(e, cab, id_estudio)
    assert r.status_code == 201 and r.json()["id"] != primero
    assert r.json()["estado"] == "pendiente"


def test_no_se_reprocesa_un_estudio_completado_en_curso(entorno):
    """Tras completar se puede volver a procesar; mientras el nuevo está pendiente, no."""
    cab = entorno.cabeceras()
    id_estudio = _estudio(entorno, cab)
    _procesar(entorno, cab, id_estudio)
    entorno.servicio.procesar_siguiente()
    assert _procesar(entorno, cab, id_estudio).status_code == 201
    assert _procesar(entorno, cab, id_estudio).status_code == 409


# --- GET /api/trabajos/{id} ---

def test_estado_del_trabajo_durante_y_despues(tmp_path):
    vistos = {}

    class PipelineQueMira(PipelineFalso):
        def segment(self, inp, ctx):
            # A mitad del pipeline: lo que vería la pantalla de estado
            vistos["durante"] = _trabajo(e, cab, id_trabajo).json()
            super().segment(inp, ctx)

    e = Entorno(tmp_path, proveedor=ProveedorFalso(PipelineQueMira()))
    try:
        cab = e.cabeceras()
        id_trabajo = _procesar(e, cab, _estudio(e, cab)).json()["id"]
        assert _trabajo(e, cab, id_trabajo).json()["estado"] == "pendiente"
        e.servicio.procesar_siguiente()

        durante = vistos["durante"]
        assert durante["estado"] == "en proceso" and durante["fecha_inicio"]
        assert [x["estado"] for x in durante["etapas"]] == [
            "completado", "completado", "en proceso", "pendiente", "pendiente"]
        assert durante["etapas"][0]["duracion_s"] is not None
        assert durante["etapas"][2]["duracion_s"] is None

        despues = _trabajo(e, cab, id_trabajo).json()
        assert despues["estado"] == "completado" and despues["fecha_fin"]
        assert despues["etapa_fallida"] is None and despues["mensaje_error"] is None
        assert [x["nombre"] for x in despues["etapas"]] == list(stages.STAGES)
        assert all(x["estado"] == "completado" for x in despues["etapas"])
        assert all(isinstance(x["duracion_s"], float) for x in despues["etapas"])
    finally:
        e.cerrar()


def test_trabajo_ajeno_o_inexistente_da_404(entorno):
    cab = entorno.cabeceras("ana")
    id_trabajo = _procesar(entorno, cab, _estudio(entorno, cab)).json()["id"]
    otro = entorno.cabeceras("beto")
    for id_ in (id_trabajo, 999):
        r = _trabajo(entorno, otro, id_)
        assert r.status_code == 404 and r.json() == {"detalle": "Trabajo no encontrado."}
    assert _trabajo(entorno, cab, id_trabajo).status_code == 200


def test_trabajo_sin_token_da_401(entorno):
    assert entorno.client.get("/api/trabajos/1").status_code == 401


# --- GET /api/estudios/{id} con trabajos ---

def test_detalle_del_estudio_con_trabajos_y_estado_visible(entorno_falla):
    e = entorno_falla
    cab = e.cabeceras()
    id_estudio = _estudio(e, cab)
    detalle = lambda: e.client.get(f"/api/estudios/{id_estudio}", headers=cab).json()  # noqa: E731
    assert detalle()["estado"] == "listo para procesar"

    primero = _procesar(e, cab, id_estudio).json()["id"]
    assert detalle()["estado"] == "pendiente"
    e.servicio.procesar(primero)
    assert detalle()["estado"] == "fallido"

    # Segundo intento con un pipeline que no falla
    e.proveedor._pipeline.falla_en = None
    segundo = _procesar(e, cab, id_estudio).json()["id"]
    e.servicio.procesar_siguiente()

    cuerpo = detalle()
    assert cuerpo["estado"] == "completado"
    assert cuerpo["id_ultimo_trabajo"] == segundo
    assert [t["id"] for t in cuerpo["trabajos"]] == [primero, segundo]
    assert [t["estado"] for t in cuerpo["trabajos"]] == ["fallido", "completado"]
    assert cuerpo["trabajos"][0]["etapa_fallida"] == "segmentación"
    assert set(cuerpo["trabajos"][1]) == set(_trabajo(e, cab, segundo).json())
    assert cuerpo["dice"] == pytest.approx(1.0) and cuerpo["iou"] == pytest.approx(1.0)


def test_detalle_sin_referencia_deja_dice_en_null(entorno):
    cab = entorno.cabeceras()
    id_estudio = _estudio(entorno, cab, referencia=False)
    _procesar(entorno, cab, id_estudio)
    entorno.servicio.procesar_siguiente()
    cuerpo = entorno.client.get(f"/api/estudios/{id_estudio}", headers=cab).json()
    assert cuerpo["estado"] == "completado"
    assert cuerpo["dice"] is None and cuerpo["iou"] is None


# --- Arranque de la API (lifespan) ---

def test_al_arrancar_los_interrumpidos_quedan_fallidos(entorno):
    cab = entorno.cabeceras()
    id_trabajo = _procesar(entorno, cab, _estudio(entorno, cab)).json()["id"]
    _iniciar(entorno, id_trabajo)
    with TestClient(entorno.app):
        pass
    cuerpo = _trabajo(entorno, cab, id_trabajo).json()
    assert cuerpo["estado"] == "fallido"
    assert cuerpo["mensaje_error"] == MENSAJE_INTERRUMPIDO
    assert entorno.app.state.tarea.activa is False


def test_tarea_en_segundo_plano_procesa_y_se_detiene_al_apagar(tmp_path):
    e = Entorno(tmp_path, worker_activo=True, worker_intervalo_s=0.05)
    try:
        cab = e.cabeceras()
        id_estudio = _estudio(e, cab)
        with TestClient(e.app) as cliente:
            assert e.app.state.tarea.activa
            id_trabajo = cliente.post(f"/api/estudios/{id_estudio}/procesar", headers=cab).json()["id"]
            limite = time.monotonic() + 10
            estado = "pendiente"
            while estado not in ("completado", "fallido") and time.monotonic() < limite:
                time.sleep(0.05)
                estado = cliente.get(f"/api/trabajos/{id_trabajo}", headers=cab).json()["estado"]
            assert estado == "completado"
        assert e.app.state.tarea.activa is False
    finally:
        e.cerrar()
