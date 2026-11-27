"""Trabajos de procesamiento y sus etapas (CU03, RF-06 a RF-08).

Transiciones válidas: pendiente → en proceso → completado | fallido.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from prosta_ai.constantes import COMPLETADO, EN_PROCESO, FALLIDO, PENDIENTE
from prosta_ai.db import ahora
from prosta_ai.models import Estudio, EtapaTrabajo, Trabajo
from prosta_ai.pipeline.stages import STAGES

_TRANSICIONES = {
    PENDIENTE: {EN_PROCESO},
    EN_PROCESO: {COMPLETADO, FALLIDO},
    COMPLETADO: set(),
    FALLIDO: set(),
}


class TransicionNoValida(ValueError):
    """Cambio de estado que no sigue el orden del trabajo."""


def _cambiar(trabajo: Trabajo, destino: str) -> None:
    if destino not in _TRANSICIONES[trabajo.estado]:
        raise TransicionNoValida(f"No se puede pasar de «{trabajo.estado}» a «{destino}»")
    trabajo.estado = destino


class RepositorioTrabajos:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    def crear_pendiente(self, id_estudio: int, id_modelo: int) -> Trabajo:
        """Trabajo pendiente con sus cinco etapas en pendiente."""
        trabajo = Trabajo(id_estudio=id_estudio, id_modelo=id_modelo, estado=PENDIENTE)
        trabajo.etapas = [EtapaTrabajo(nombre=n, estado=PENDIENTE) for n in STAGES]
        self.sesion.add(trabajo)
        self.sesion.flush()
        return trabajo

    def obtener(self, id_trabajo: int) -> Trabajo | None:
        return self.sesion.get(Trabajo, id_trabajo)

    def obtener_de_usuario(self, id_trabajo: int, id_usuario: int) -> Trabajo | None:
        """Solo si el estudio es del usuario; uno ajeno se trata como inexistente."""
        return self.sesion.scalar(
            select(Trabajo).join(Estudio)
            .where(Trabajo.id_trabajo == id_trabajo, Estudio.id_usuario == id_usuario)
        )

    def activo_del_estudio(self, id_estudio: int) -> Trabajo | None:
        """Trabajo pendiente o en proceso del estudio (para el 409 de procesar)."""
        return self.sesion.scalar(
            select(Trabajo).where(
                Trabajo.id_estudio == id_estudio, Trabajo.estado.in_([PENDIENTE, EN_PROCESO])
            ).limit(1)
        )

    def ultimo_del_estudio(self, id_estudio: int) -> Trabajo | None:
        return self.sesion.scalar(
            select(Trabajo).where(Trabajo.id_estudio == id_estudio)
            .order_by(Trabajo.id_trabajo.desc()).limit(1)
        )

    def siguiente_pendiente(self) -> Trabajo | None:
        """El pendiente más antiguo; en PostgreSQL con SKIP LOCKED."""
        consulta = (
            select(Trabajo).where(Trabajo.estado == PENDIENTE)
            .order_by(Trabajo.id_trabajo).limit(1)
        )
        if self.sesion.get_bind().dialect.name == "postgresql":
            consulta = consulta.with_for_update(skip_locked=True)
        return self.sesion.scalar(consulta)

    def en_proceso(self) -> list[Trabajo]:
        return list(self.sesion.scalars(
            select(Trabajo).where(Trabajo.estado == EN_PROCESO).order_by(Trabajo.id_trabajo)
        ))

    def etapa(self, id_trabajo: int, nombre: str) -> EtapaTrabajo | None:
        return self.sesion.scalar(
            select(EtapaTrabajo).where(
                EtapaTrabajo.id_trabajo == id_trabajo, EtapaTrabajo.nombre == nombre
            )
        )

    def iniciar(self, trabajo: Trabajo) -> None:
        _cambiar(trabajo, EN_PROCESO)
        trabajo.fecha_inicio = ahora()
        self.sesion.flush()

    def completar(self, trabajo: Trabajo) -> None:
        _cambiar(trabajo, COMPLETADO)
        trabajo.fecha_fin = ahora()
        self.sesion.flush()

    def fallar(self, trabajo: Trabajo, etapa: str | None, mensaje: str) -> None:
        _cambiar(trabajo, FALLIDO)
        trabajo.fecha_fin = ahora()
        trabajo.etapa_fallida = etapa
        trabajo.mensaje_error = mensaje
        self.sesion.flush()

    def recuperar_interrumpidos(self, mensaje: str) -> list[Trabajo]:
        """Al arrancar: los «en proceso» de una ejecución anterior pasan a fallido."""
        trabajos = self.en_proceso()
        for trabajo in trabajos:
            etapa = None
            for e in trabajo.etapas:
                if e.estado == EN_PROCESO:
                    e.estado, e.fecha_fin = FALLIDO, ahora()
                    etapa = e.nombre
            self.fallar(trabajo, etapa, mensaje)
        return trabajos
