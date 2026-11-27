"""Migración 0002: rutas de salida del resultado (ruta_imagen y ruta_roi)."""
import sqlalchemy as sa
from alembic import command

from prosta_ai.db import crear_motor
from test_db_migracion import _config


def _columnas(url: str) -> set[str]:
    motor = crear_motor(url)
    columnas = {c["name"] for c in sa.inspect(motor).get_columns("resultado")}
    motor.dispose()
    return columnas


def test_0002_agrega_y_quita_columnas(tmp_path):
    url = f"sqlite:///{tmp_path / 'm.db'}"
    cfg = _config(url)
    command.upgrade(cfg, "0001")
    assert not {"ruta_imagen", "ruta_roi"} & _columnas(url)
    command.upgrade(cfg, "0002")
    assert {"ruta_mascara", "ruta_imagen", "ruta_roi"} <= _columnas(url)
    command.downgrade(cfg, "0001")
    assert not {"ruta_imagen", "ruta_roi"} & _columnas(url)
