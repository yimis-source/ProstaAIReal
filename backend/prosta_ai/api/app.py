"""Fábrica de la aplicación FastAPI.

Arranque (desde backend/): uvicorn prosta_ai.api.app:create_app --factory
"""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from prosta_ai import __version__
from sqlalchemy import Engine

from prosta_ai.api import acceso, salud
from prosta_ai.config import Settings, get_settings
from prosta_ai.db import crear_fabrica_sesiones, crear_motor
from prosta_ai.storage import AlmacenamientoPrivado


def _error(status_code: int, detalle, headers=None) -> JSONResponse:
    # Formato común de error: {"detalle": ...}
    return JSONResponse(status_code=status_code, content={"detalle": detalle}, headers=headers)


def create_app(
    settings: Settings | None = None,
    *,
    motor: Engine | None = None,
    almacenamiento: AlmacenamientoPrivado | None = None,
) -> FastAPI:
    """El motor y el almacenamiento salen de settings; las pruebas pueden pasar los suyos."""
    settings = settings or get_settings()
    motor = motor or crear_motor(settings.database_url)

    app = FastAPI(title="Prosta-AI", version=__version__)
    app.state.settings = settings
    app.state.motor = motor
    app.state.fabrica_sesiones = crear_fabrica_sesiones(motor)
    app.state.almacenamiento = almacenamiento or AlmacenamientoPrivado(settings.storage_dir)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_lista,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Base de Starlette: el 404/405 del enrutador no pasa por fastapi.HTTPException
    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, exc: StarletteHTTPException):
        detalle = exc.detail
        if exc.status_code == 404 and detalle == "Not Found":
            detalle = "Recurso no encontrado."
        elif exc.status_code == 405 and detalle == "Method Not Allowed":
            detalle = "Método no permitido."
        return _error(exc.status_code, detalle, getattr(exc, "headers", None))

    @app.exception_handler(RequestValidationError)
    async def _validacion(_: Request, exc: RequestValidationError):
        campos = [".".join(str(p) for p in e.get("loc", ())[1:]) for e in exc.errors()]
        return JSONResponse(
            status_code=422,
            content={"detalle": "Datos no válidos.", "campos": [c for c in campos if c]},
        )

    for router in (salud.router, acceso.router):
        app.include_router(router, prefix="/api")
    return app
