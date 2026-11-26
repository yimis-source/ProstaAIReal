"""CU05 (RF-19): historial de los estudios del usuario (contrato, sección 4.10)."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from prosta_ai.api.deps import sesion, usuario_actual
from prosta_ai.api.vistas import detalle_estudio
from prosta_ai.models import Estudio, Trabajo, Usuario

router = APIRouter(prefix="/estudios", tags=["historial"])

# Lo que el detalle trae y la lista no (contrato 4.5 frente a 4.10)
_SOLO_DETALLE = ("estado_admision", "trabajos")


def resumen_estudio(estudio: Estudio) -> dict:
    """Fila del historial: el detalle del estudio sin sus trabajos."""
    cuerpo = detalle_estudio(estudio)
    for campo in _SOLO_DETALLE:
        cuerpo.pop(campo)
    return cuerpo


@router.get("")
def listar(db: Session = Depends(sesion), usuario: Usuario = Depends(usuario_actual)) -> list:
    """Solo los estudios del usuario, del más reciente al más antiguo."""
    estudios = db.scalars(
        select(Estudio)
        .where(Estudio.id_usuario == usuario.id_usuario)
        # A igual fecha de carga decide el id, que es correlativo
        .order_by(Estudio.fecha_carga.desc(), Estudio.id_estudio.desc())
        .options(
            selectinload(Estudio.trabajos).selectinload(Trabajo.etapas),
            selectinload(Estudio.trabajos).selectinload(Trabajo.resultado),
        )
    )
    return [resumen_estudio(e) for e in estudios]
