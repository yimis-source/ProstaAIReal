"""CU03: estado de un trabajo de procesamiento y de sus etapas (contrato 4.7)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from prosta_ai.api.deps import sesion, usuario_actual
from prosta_ai.api.vistas import detalle_trabajo
from prosta_ai.models import Usuario
from prosta_ai.repositories import RepositorioTrabajos

router = APIRouter(prefix="/trabajos", tags=["trabajos"])


@router.get("/{id_trabajo}")
def estado(
    id_trabajo: int, db: Session = Depends(sesion), usuario: Usuario = Depends(usuario_actual)
) -> dict:
    trabajo = RepositorioTrabajos(db).obtener_de_usuario(id_trabajo, usuario.id_usuario)
    if trabajo is None:
        # Ajeno o inexistente: misma respuesta
        raise HTTPException(404, "Trabajo no encontrado.")
    return detalle_trabajo(trabajo, trabajo.estudio.codigo_anonimo)
