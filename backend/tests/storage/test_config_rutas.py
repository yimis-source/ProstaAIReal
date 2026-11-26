"""Configuración: rutas resueltas desde backend/ y datos del token."""
from pathlib import Path

from prosta_ai.config import BACKEND_DIR, Settings


def test_rutas_relativas_desde_backend(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # arrancar desde otra carpeta no cambia nada
    s = Settings(_env_file=None)
    assert s.storage_dir == (BACKEND_DIR.parent / "almacenamiento").resolve()
    assert s.modelo_dir == (BACKEND_DIR.parent / "modelos").resolve()
    assert Path(s.model_config["env_file"]) == BACKEND_DIR / ".env"


def test_ruta_absoluta_se_respeta(tmp_path):
    s = Settings(_env_file=None, storage_dir=tmp_path)
    assert s.storage_dir == tmp_path.resolve()


def test_token_por_defecto_y_por_entorno(monkeypatch):
    s = Settings(_env_file=None)
    assert s.token_horas == 8 and s.secret_key
    monkeypatch.setenv("PROSTA_SECRET_KEY", "otra-clave")
    monkeypatch.setenv("PROSTA_TOKEN_HORAS", "2")
    s = Settings(_env_file=None)
    assert (s.secret_key, s.token_horas) == ("otra-clave", 2)
