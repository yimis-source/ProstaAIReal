"""Base declarativa, motor y fábrica de sesiones."""
from datetime import datetime, timezone

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


def ahora() -> datetime:
    """Fecha y hora actual con zona UTC."""
    return datetime.now(timezone.utc)


def crear_motor(url: str) -> Engine:
    """Crea el motor; en SQLite (pruebas) activa las llaves foráneas."""
    if not url.startswith("sqlite"):
        return create_engine(url, pool_pre_ping=True)
    opciones: dict = {"connect_args": {"check_same_thread": False}}
    if ":memory:" in url or url in ("sqlite://", "sqlite+pysqlite://"):
        # Una sola conexión para que la base en memoria no se pierda
        opciones["poolclass"] = StaticPool
    motor = create_engine(url, **opciones)

    @event.listens_for(motor, "connect")
    def _activar_fk(conexion_dbapi, _registro):
        conexion_dbapi.execute("PRAGMA foreign_keys=ON")

    return motor


def crear_fabrica_sesiones(motor: Engine) -> sessionmaker[Session]:
    """La fábrica se arma en create_app y se inyecta (api/deps.sesion, servicio de procesamiento)."""
    return sessionmaker(bind=motor, expire_on_commit=False)
