"""Dependencias compartidas por las rutas: sesión, ajustes, almacenamiento y usuario."""
from collections.abc import Iterator

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from prosta_ai.config import Settings
from prosta_ai.models import Usuario
from prosta_ai.repositories import RepositorioUsuarios
from prosta_ai.seguridad import TokenNoValido, leer_token
from prosta_ai.storage import AlmacenamientoPrivado

_bearer = HTTPBearer(auto_error=False)

SESION_NO_VALIDA = "Sesión no válida o vencida. Ingrese de nuevo."


def sesion(request: Request) -> Iterator[Session]:
    """Sesión por petición, de la fábrica que armó create_app."""
    with request.app.state.fabrica_sesiones() as s:
        yield s


def ajustes(request: Request) -> Settings:
    return request.app.state.settings


def almacenamiento(request: Request) -> AlmacenamientoPrivado:
    return request.app.state.almacenamiento


def usuario_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(sesion),
    settings: Settings = Depends(ajustes),
) -> Usuario:
    """Usuario del token Bearer; sin token, token alterado o vencido → 401."""
    error = HTTPException(401, SESION_NO_VALIDA, headers={"WWW-Authenticate": "Bearer"})
    if credenciales is None:
        raise error
    try:
        datos = leer_token(credenciales.credentials, settings.secret_key)
        usuario = RepositorioUsuarios(db).obtener(int(datos["sub"]))
    except (TokenNoValido, KeyError, ValueError):
        raise error
    if usuario is None:
        raise error
    return usuario
