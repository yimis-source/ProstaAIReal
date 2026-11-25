"""CU01: verificar si el alias existe e ingresar (crea la cuenta en el primer acceso)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from prosta_ai.api.deps import ajustes, sesion
from prosta_ai.api.esquemas import AccesoEntrada, AliasEntrada
from prosta_ai.config import Settings
from prosta_ai.repositories import RepositorioUsuarios
from prosta_ai.seguridad import crear_token, hash_contrasena, verificar_contrasena

router = APIRouter(prefix="/acceso", tags=["acceso"])

MIN_CONTRASENA = 8


@router.post("/verificar")
def verificar(datos: AliasEntrada, db: Session = Depends(sesion)) -> dict:
    return {"existe": RepositorioUsuarios(db).por_alias(datos.alias) is not None}


@router.post("")
def acceder(
    datos: AccesoEntrada, db: Session = Depends(sesion), settings: Settings = Depends(ajustes)
) -> dict:
    repo = RepositorioUsuarios(db)
    usuario = repo.por_alias(datos.alias)
    primer_acceso = usuario is None
    if primer_acceso:
        if len(datos.contrasena) < MIN_CONTRASENA:
            raise HTTPException(
                422, f"La contraseña debe tener al menos {MIN_CONTRASENA} caracteres."
            )
        if datos.confirmacion != datos.contrasena:
            raise HTTPException(422, "La confirmación no coincide con la contraseña.")
        try:
            usuario = repo.crear(datos.alias, hash_contrasena(datos.contrasena))
            db.commit()
        except IntegrityError:
            # Otra persona creó el mismo alias al mismo tiempo
            db.rollback()
            raise HTTPException(409, "El alias ya fue registrado. Intente ingresar de nuevo.")
    elif not verificar_contrasena(datos.contrasena, usuario.hash_contrasena):
        raise HTTPException(401, "Alias o contraseña incorrectos.")
    token = crear_token(usuario.id_usuario, usuario.alias, settings.secret_key, settings.token_horas)
    return {"token": token, "alias": usuario.alias, "primer_acceso": primer_acceso}
