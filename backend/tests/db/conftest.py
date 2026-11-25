"""Fixtures de las pruebas de base de datos (SQLite en memoria)."""
import pytest

from prosta_ai.db import Base, crear_fabrica_sesiones, crear_motor
import prosta_ai.models  # noqa: F401  (registra las tablas)


@pytest.fixture
def sesion():
    motor = crear_motor("sqlite://")
    Base.metadata.create_all(motor)
    with crear_fabrica_sesiones(motor)() as s:
        yield s
    motor.dispose()
