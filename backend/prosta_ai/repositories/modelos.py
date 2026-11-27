"""Modelo de segmentación activo: se registra una sola vez por nombre y versión."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from prosta_ai.models import Modelo


class RepositorioModelos:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    def por_nombre_version(self, nombre: str, version: str) -> Modelo | None:
        return self.sesion.scalar(
            select(Modelo).where(Modelo.nombre == nombre, Modelo.version == version)
        )

    def registrar(self, info: dict) -> Modelo:
        """Recibe el dict de `model_info`; si ya existe, devuelve el registrado."""
        modelo = self.por_nombre_version(info["nombre"], info["version"])
        if modelo is not None:
            return modelo
        modelo = Modelo(
            nombre=info["nombre"], version=info["version"],
            ruta_pesos=info.get("ruta_pesos"), hash_pesos=info.get("hash_pesos"),
            ruta_configuracion=info.get("ruta_configuracion"),
        )
        self.sesion.add(modelo)
        self.sesion.flush()
        return modelo
