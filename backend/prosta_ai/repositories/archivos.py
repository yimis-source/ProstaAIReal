"""Archivos de un estudio (RB-02): ruta relativa, tamaño y SHA-256."""
from pathlib import PurePosixPath

from sqlalchemy import select
from sqlalchemy.orm import Session

from prosta_ai.models import Archivo
from prosta_ai.storage import ArchivoGuardado, rol_de_ruta


class RepositorioArchivos:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    def registrar(self, id_estudio: int, guardado: ArchivoGuardado) -> Archivo:
        """Registra lo que devolvió el almacenamiento; el rol va en la ruta."""
        if PurePosixPath(guardado.ruta).is_absolute() or ".." in guardado.ruta:
            raise ValueError("La ruta debe ser relativa al almacenamiento")
        rol_de_ruta(guardado.ruta)
        archivo = Archivo(
            id_estudio=id_estudio, ruta=guardado.ruta, tamano_bytes=guardado.tamano_bytes,
            hash_sha256=guardado.sha256, valido=True,
        )
        self.sesion.add(archivo)
        self.sesion.flush()
        return archivo

    def del_estudio(self, id_estudio: int, rol: str | None = None) -> list[Archivo]:
        """Archivos del estudio; con rol, solo los de imagen o de referencia."""
        archivos = self.sesion.scalars(
            select(Archivo).where(Archivo.id_estudio == id_estudio).order_by(Archivo.id_archivo)
        )
        return [a for a in archivos if rol is None or rol_de_ruta(a.ruta) == rol]
