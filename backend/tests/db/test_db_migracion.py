"""La migración escrita a mano debe crear el mismo esquema que models.py."""
import os
from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext

from prosta_ai.db import Base, crear_motor
import prosta_ai.models  # noqa: F401

BACKEND = Path(__file__).resolve().parents[2]
TABLAS = {"usuario", "estudio", "archivo", "modelo", "trabajo", "etapa_trabajo", "resultado"}


def _config(url: str) -> Config:
    cfg = Config(str(BACKEND / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND / "migrations"))
    cfg.set_main_option("sqlalchemy.url", url)
    cfg.attributes["configurar_logs"] = False
    return cfg


def _esquema(motor) -> dict:
    """Tabla -> {columna: (tipo, nullable)} e índices, sin la tabla de Alembic."""
    insp = sa.inspect(motor)
    esquema = {}
    for tabla in insp.get_table_names():
        if tabla == "alembic_version":
            continue
        columnas = {c["name"]: (str(c["type"]), c["nullable"]) for c in insp.get_columns(tabla)}
        indices = sorted(i["name"] for i in insp.get_indexes(tabla))
        fks = sorted((f["referred_table"], tuple(f["constrained_columns"]),
                      (f.get("options") or {}).get("ondelete")) for f in insp.get_foreign_keys(tabla))
        esquema[tabla] = {"columnas": columnas, "indices": indices, "fks": fks}
    return esquema


def _diferencias(url: str) -> list:
    motor = crear_motor(url)
    with motor.connect() as conexion:
        diffs = compare_metadata(MigrationContext.configure(conexion), Base.metadata)
    motor.dispose()
    return diffs


def test_migracion_igual_a_modelos_sqlite(tmp_path):
    url_migrada = f"sqlite:///{tmp_path / 'migrada.db'}"
    command.upgrade(_config(url_migrada), "head")
    modelos = crear_motor(f"sqlite:///{tmp_path / 'modelos.db'}")
    Base.metadata.create_all(modelos)

    migrada = crear_motor(url_migrada)
    esquema_migrado, esquema_modelos = _esquema(migrada), _esquema(modelos)
    assert set(esquema_migrado) == TABLAS
    for tabla in sorted(TABLAS):
        assert esquema_migrado[tabla] == esquema_modelos[tabla], tabla
    migrada.dispose()
    modelos.dispose()
    assert _diferencias(url_migrada) == []


def test_downgrade_deja_la_base_vacia(tmp_path):
    url = f"sqlite:///{tmp_path / 'm.db'}"
    cfg = _config(url)
    command.upgrade(cfg, "head")
    command.downgrade(cfg, "base")
    motor = crear_motor(url)
    assert set(sa.inspect(motor).get_table_names()) <= {"alembic_version"}
    motor.dispose()


@pytest.mark.skipif(not os.environ.get("PROSTA_TEST_DATABASE_URL"),
                    reason="sin PROSTA_TEST_DATABASE_URL (PostgreSQL de pruebas)")
def test_migracion_igual_a_modelos_postgresql():
    url = os.environ["PROSTA_TEST_DATABASE_URL"]
    cfg = _config(url)
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    try:
        assert _diferencias(url) == []
    finally:
        command.downgrade(cfg, "base")
