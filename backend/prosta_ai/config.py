"""Configuración de la aplicación web (variables PROSTA_* o archivo .env)."""
from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Carpeta backend/: las rutas relativas se resuelven desde aquí, no desde donde se arranque
BACKEND_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PROSTA_", env_file=BACKEND_DIR / ".env", extra="ignore"
    )

    database_url: str = "postgresql+psycopg://prosta@localhost:5433/prosta_ai"
    storage_dir: Path = Path("../almacenamiento")
    # Firma del token de acceso (1705); cambiarla fuera de desarrollo
    secret_key: str = "cambiar-esta-clave-en-desarrollo"
    token_horas: int = 8
    # RF-03: máximo 50 MB por archivo y 150 MB por estudio
    max_upload_mb: int = 50
    max_estudio_mb: int = 150
    modelo_nombre: str = "prostate_mri_anatomy"
    modelo_dir: Path = Path("../modelos")
    cors_origins: str = "http://localhost:5173"

    @field_validator("storage_dir", "modelo_dir")
    @classmethod
    def _desde_backend(cls, ruta: Path) -> Path:
        """Ruta relativa → absoluta respecto a backend/."""
        ruta = Path(ruta).expanduser()
        if not ruta.is_absolute():
            ruta = BACKEND_DIR / ruta
        return ruta.resolve()

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024

    @property
    def max_estudio_bytes(self) -> int:
        return self.max_estudio_mb * 1024 * 1024

    @property
    def cors_lista(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
