"""Pruebas del esqueleto de la API: salud, 404, validación y CORS."""
import pytest
from fastapi.testclient import TestClient

from prosta_ai import __version__
from prosta_ai.api.app import create_app
from prosta_ai.config import Settings

ORIGEN_OK = "http://localhost:5173"


@pytest.fixture
def cliente():
    settings = Settings(_env_file=None, cors_origins=f"{ORIGEN_OK}, http://127.0.0.1:5173")
    app = create_app(settings)

    # Ruta solo de prueba para comprobar el formato del 422
    @app.get("/api/eco")
    def eco(n: int):
        return {"n": n}

    return TestClient(app)


def test_salud_responde_ok(cliente):
    r = cliente.get("/api/salud")
    assert r.status_code == 200
    assert r.json() == {"estado": "ok", "version": "0.6.0"}
    assert __version__ == "0.6.0"


def test_salud_fuera_de_prefijo_no_existe(cliente):
    assert cliente.get("/salud").status_code == 404


def test_ruta_inexistente_devuelve_404_con_detalle(cliente):
    r = cliente.get("/api/no-existe")
    assert r.status_code == 404
    cuerpo = r.json()
    assert "detalle" in cuerpo
    assert "detail" not in cuerpo


def test_validacion_devuelve_422_con_detalle_y_campos(cliente):
    r = cliente.get("/api/eco", params={"n": "abc"})
    assert r.status_code == 422
    cuerpo = r.json()
    assert cuerpo["detalle"]
    assert "n" in cuerpo["campos"]


def test_cors_permite_origen_configurado(cliente):
    r = cliente.get("/api/salud", headers={"Origin": ORIGEN_OK})
    assert r.headers.get("access-control-allow-origin") == ORIGEN_OK


def test_cors_preflight_origen_configurado(cliente):
    r = cliente.options(
        "/api/salud",
        headers={"Origin": ORIGEN_OK, "Access-Control-Request-Method": "GET"},
    )
    assert r.status_code == 200
    assert r.headers.get("access-control-allow-origin") == ORIGEN_OK


def test_cors_rechaza_otro_origen(cliente):
    r = cliente.get("/api/salud", headers={"Origin": "http://otro.ejemplo"})
    assert "access-control-allow-origin" not in r.headers
