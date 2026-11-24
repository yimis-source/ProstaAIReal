"""Configuración de la aplicación web (variables PROSTA_* o archivo .env)."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PROSTA_", env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://prosta@localhost:5433/prosta_ai"
    storage_dir: Path = Path("../almacenamiento")
    # RF-03: máximo 50 MB por archivo y 150 MB por estudio
    max_upload_mb: int = 50
    max_estudio_mb: int = 150
    modelo_nombre: str = "prostate_mri_anatomy"
    modelo_dir: Path = Path("../modelos")
    cors_origins: str = "http://localhost:5173"

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
