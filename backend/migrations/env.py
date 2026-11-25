"""Entorno de Alembic: la URL sale de la configuración de la aplicación."""
from logging.config import fileConfig

from alembic import context

from prosta_ai.config import get_settings
from prosta_ai.db import Base, crear_motor
import prosta_ai.models  # noqa: F401  (registra las tablas)

config = context.config
if config.config_file_name and config.attributes.get("configurar_logs", True):
    fileConfig(config.config_file_name, disable_existing_loggers=False)

target_metadata = Base.metadata


def _url() -> str:
    # Orden: -x url=..., sqlalchemy.url (pruebas) y por último PROSTA_DATABASE_URL
    return (
        context.get_x_argument(as_dictionary=True).get("url")
        or config.get_main_option("sqlalchemy.url")
        or get_settings().database_url
    )


def run_migrations_offline() -> None:
    context.configure(url=_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    motor = crear_motor(_url())
    with motor.connect() as conexion:
        context.configure(connection=conexion, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    motor.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
