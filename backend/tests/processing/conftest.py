"""Fixtures del servicio de procesamiento: SQLite en archivo y almacenamiento temporal."""
import pytest

from apoyo_procesamiento import ProveedorFalso, referencia_nifti, volumen_nifti
from prosta_ai.db import Base, crear_fabrica_sesiones, crear_motor
import prosta_ai.models  # noqa: F401  (registra las tablas)
from prosta_ai.processing import ServicioProcesamiento
from prosta_ai.repositories import (
    RepositorioArchivos, RepositorioEstudios, RepositorioTrabajos, RepositorioUsuarios,
)
from prosta_ai.storage import AlmacenamientoPrivado


@pytest.fixture
def fabrica(tmp_path):
    motor = crear_motor(f"sqlite:///{tmp_path / 'prosta.db'}")
    Base.metadata.create_all(motor)
    yield crear_fabrica_sesiones(motor)
    motor.dispose()


@pytest.fixture
def almacen(tmp_path):
    return AlmacenamientoPrivado(tmp_path / "almacenamiento")


@pytest.fixture
def proveedor():
    return ProveedorFalso()


@pytest.fixture
def servicio(fabrica, almacen, proveedor):
    return ServicioProcesamiento(fabrica, almacen, proveedor)


@pytest.fixture
def crear_trabajo(fabrica, almacen, servicio):
    """Crea usuario, estudio con sus archivos y un trabajo pendiente; devuelve su id."""

    def _crear(con_referencia: bool = True, alias: str = "estudiante01",
               imagen: bytes | None = None, referencia: bytes | None = None) -> int:
        id_modelo = servicio.id_modelo_activo()
        with fabrica() as s:
            usuario = RepositorioUsuarios(s).por_alias(alias) or \
                RepositorioUsuarios(s).crear(alias, "$2b$12$" + "x" * 53)
            estudio = RepositorioEstudios(s).crear(usuario.id_usuario)
            archivos = RepositorioArchivos(s)
            archivos.registrar(estudio.id_estudio, almacen.guardar(
                estudio.codigo_anonimo, "imagen", imagen or volumen_nifti(), "caso.nii.gz"))
            if con_referencia:
                archivos.registrar(estudio.id_estudio, almacen.guardar(
                    estudio.codigo_anonimo, "referencia", referencia or referencia_nifti(), "ref.nii.gz"))
            trabajo = RepositorioTrabajos(s).crear_pendiente(estudio.id_estudio, id_modelo)
            s.commit()
            return trabajo.id_trabajo

    return _crear
