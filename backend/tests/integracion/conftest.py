"""Pruebas de integración (1708): API real contra PostgreSQL con el esquema de Alembic.

Necesitan PROSTA_TEST_DATABASE_URL apuntando a una base de pruebas aparte (por ejemplo
prosta_ai_pruebas). Cada prueba hace `alembic upgrade head` al empezar y `downgrade base`
al terminar, así que la base queda vacía. Los archivos van a una carpeta temporal.
"""
import os

import pytest
from sqlalchemy.engine import make_url

from prosta_ai import seguridad

from apoyo_integracion import EntornoPostgres

VARIABLE = "PROSTA_TEST_DATABASE_URL"
MOTIVO_OMISION = (
    f"sin {VARIABLE}: las pruebas de integración necesitan PostgreSQL "
    "(ver backend/tests/integracion/README.md)"
)


def pytest_collection_modifyitems(config, items):
    if os.environ.get(VARIABLE):
        return
    omitir = pytest.mark.skip(reason=MOTIVO_OMISION)
    for item in items:
        if "integracion" in item.nodeid.split("/"):
            item.add_marker(omitir)


@pytest.fixture(scope="session")
def url_pruebas() -> str:
    url = os.environ.get(VARIABLE)
    if not url:
        pytest.skip(MOTIVO_OMISION)
    base = make_url(url).database or ""
    # downgrade base borra todas las tablas: nunca sobre la base de desarrollo
    if "prueba" not in base:
        pytest.fail(
            f"{VARIABLE} apunta a la base «{base}»; use una base aparte cuyo nombre "
            "contenga «prueba» (p. ej. prosta_ai_pruebas)."
        )
    return url


@pytest.fixture(autouse=True)
def _bcrypt_rapido(monkeypatch):
    monkeypatch.setattr(seguridad, "ROUNDS", 4)


@pytest.fixture
def entorno(url_pruebas, tmp_path):
    e = EntornoPostgres(url_pruebas, tmp_path)
    try:
        yield e
    finally:
        e.cerrar()
