"""Fixtures de las pruebas de la API (ver apoyo_api.py)."""
import pytest

from prosta_ai import seguridad

from apoyo_api import Entorno


@pytest.fixture(autouse=True)
def _bcrypt_rapido(monkeypatch):
    monkeypatch.setattr(seguridad, "ROUNDS", 4)


@pytest.fixture
def entorno(tmp_path):
    e = Entorno(tmp_path)
    yield e
    e.cerrar()


@pytest.fixture
def entorno_limitado(tmp_path):
    """Límites de 1 MB para probar los rechazos por tamaño sin archivos grandes."""
    e = Entorno(tmp_path, max_upload_mb=1, max_estudio_mb=1)
    yield e
    e.cerrar()
