"""Estudios (CU02, RB-01): código anónimo correlativo, sin datos de la persona."""
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from prosta_ai.models import Estudio


def formato_codigo(numero: int) -> str:
    return f"EST-{numero:04d}"


class RepositorioEstudios:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    def crear(
        self, id_usuario: int, formato: str = "NIfTI", estado_admision: str = "admitido"
    ) -> Estudio:
        """Crea el estudio; el código sale del id para no repetirse ni chocar."""
        estudio = Estudio(
            codigo_anonimo=f"TMP-{uuid4().hex[:8]}", id_usuario=id_usuario,
            formato=formato, estado_admision=estado_admision,
        )
        self.sesion.add(estudio)
        self.sesion.flush()
        estudio.codigo_anonimo = formato_codigo(estudio.id_estudio)
        self.sesion.flush()
        return estudio

    def obtener_de_usuario(self, id_estudio: int, id_usuario: int) -> Estudio | None:
        """Solo si es del usuario; uno ajeno se trata como inexistente (404)."""
        return self.sesion.scalar(
            select(Estudio).where(
                Estudio.id_estudio == id_estudio, Estudio.id_usuario == id_usuario
            )
        )
