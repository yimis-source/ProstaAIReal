"""Cola de trabajos con dos procesos contra PostgreSQL real (SELECT ... FOR UPDATE SKIP LOCKED).

Necesita PROSTA_TEST_DATABASE_URL con una base de pruebas aparte (su nombre debe contener
«prueba»): se hace `alembic upgrade head` al empezar y `downgrade base` al terminar.
"""
import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import event
from sqlalchemy.engine import make_url

from prosta_ai.db import crear_fabrica_sesiones, crear_motor
from prosta_ai.models import Trabajo
from prosta_ai.processing import ServicioProcesamiento
from prosta_ai.repositories import RepositorioTrabajos

VARIABLE = "PROSTA_TEST_DATABASE_URL"
BACKEND = Path(__file__).resolve().parents[2]

pytestmark = pytest.mark.skipif(
    not os.environ.get(VARIABLE), reason=f"sin {VARIABLE} (PostgreSQL de pruebas)"
)


def _config(url: str) -> Config:
    cfg = Config(str(BACKEND / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND / "migrations"))
    cfg.set_main_option("sqlalchemy.url", url)
    cfg.attributes["configurar_logs"] = False
    return cfg


@pytest.fixture
def fabrica():
    """Reemplaza la fábrica SQLite del conftest por PostgreSQL migrado con Alembic."""
    url = os.environ[VARIABLE]
    if "prueba" not in (make_url(url).database or ""):
        pytest.fail(f"{VARIABLE} debe apuntar a una base de pruebas aparte (con «prueba»)")
    cfg = _config(url)
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    motor = crear_motor(url)
    try:
        yield crear_fabrica_sesiones(motor)
    finally:
        motor.dispose()
        command.downgrade(cfg, "base")


def test_segundo_proceso_no_toma_el_mismo_trabajo(fabrica, almacen, proveedor, crear_trabajo,
                                                   monkeypatch):
    id_trabajo = crear_trabajo()
    proceso_a = ServicioProcesamiento(fabrica, almacen, proveedor)
    proceso_b = ServicioProcesamiento(fabrica, almacen, proveedor)
    tomado_por_b: list[bool] = []
    consultas = []

    original = RepositorioTrabajos.siguiente_pendiente

    def siguiente_y_luego_b(self):
        consultas.append(self.sesion)
        trabajo = original(self)
        if len(consultas) == 1 and trabajo is not None:  # solo la consulta del proceso A
            sesion_a = self.sesion

            # Apenas termina la transacción que tomó el bloqueo, el proceso B pide trabajo
            @event.listens_for(sesion_a, "after_transaction_end")
            def _b_pide(sesion, transaccion):
                if transaccion.parent is None and not tomado_por_b:
                    tomado_por_b.append(proceso_b.procesar_siguiente())
        return trabajo

    monkeypatch.setattr(RepositorioTrabajos, "siguiente_pendiente", siguiente_y_luego_b)

    error_a = None
    try:
        resultado_a = proceso_a.procesar_siguiente()
    except Exception as exc:  # antes de la corrección A choca con el trabajo que tomó B
        error_a, resultado_a = exc, None

    assert tomado_por_b == [False], "el segundo proceso tomó el mismo trabajo que el primero"
    assert error_a is None and resultado_a is True
    with fabrica() as s:
        assert s.get(Trabajo, id_trabajo).estado == "completado"
