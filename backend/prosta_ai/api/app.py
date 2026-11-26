"""Fábrica de la aplicación FastAPI.

Arranque (desde backend/): uvicorn prosta_ai.api.app:create_app --factory
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from prosta_ai import __version__
from sqlalchemy import Engine

from prosta_ai.api import acceso, estudios, historial, salud, trabajos
from prosta_ai.api.segundo_plano import TareaProcesamiento
from prosta_ai.config import Settings, get_settings
from prosta_ai.db import crear_fabrica_sesiones, crear_motor
from prosta_ai.processing import ProveedorPipeline, ServicioProcesamiento
from prosta_ai.storage import AlmacenamientoPrivado

log = logging.getLogger(__name__)

MSG_ERROR_INTERNO = "Ocurrió un error inesperado. Intente de nuevo más tarde."


def _error(status_code: int, detalle, headers=None) -> JSONResponse:
    # Formato común de error: {"detalle": ...}
    return JSONResponse(status_code=status_code, content={"detalle": detalle}, headers=headers)


def create_app(
    settings: Settings | None = None,
    *,
    motor: Engine | None = None,
    almacenamiento: AlmacenamientoPrivado | None = None,
    proveedor_pipeline=None,
) -> FastAPI:
    """Motor, almacenamiento y pipeline salen de settings; las pruebas pueden pasar los suyos."""
    settings = settings or get_settings()
    motor = motor or crear_motor(settings.database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Los «en proceso» de un cierre anterior no los va a terminar nadie
        try:
            n = app.state.servicio.recuperar_interrumpidos()
            if n:
                log.warning("%d trabajo(s) interrumpido(s) quedaron fallidos", n)
        except Exception:
            log.exception("No se pudieron recuperar los trabajos interrumpidos")
        if settings.worker_activo:
            app.state.tarea.iniciar()
        yield
        app.state.tarea.detener()

    app = FastAPI(title="Prosta-AI", version=__version__, lifespan=lifespan)
    app.state.settings = settings
    app.state.motor = motor
    app.state.fabrica_sesiones = crear_fabrica_sesiones(motor)
    app.state.almacenamiento = almacenamiento or AlmacenamientoPrivado(settings.storage_dir)
    # El pipeline real se construye al primer trabajo, no al arrancar
    app.state.servicio = ServicioProcesamiento(
        app.state.fabrica_sesiones, app.state.almacenamiento,
        proveedor_pipeline or ProveedorPipeline.desde_ajustes(settings),
    )
    app.state.tarea = TareaProcesamiento(app.state.servicio, settings.worker_intervalo_s)

    # Sin allow_credentials: el token va en la cabecera Authorization, no en cookies
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_lista,
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
        # Solo nombres: en un JSON mal formado loc trae la posición del error (un número)
        campos = []
        for e in exc.errors():
            campo = ".".join(p for p in e.get("loc", ())[1:] if isinstance(p, str))
            if campo and campo not in campos:
                campos.append(campo)
        return JSONResponse(
            status_code=422, content={"detalle": "Datos no válidos.", "campos": campos}
        )

    @app.exception_handler(Exception)
    async def _inesperado(request: Request, exc: Exception):
        # El detalle va al registro del servidor, nunca a la respuesta
        log.error("Error no controlado en %s %s", request.method, request.url.path, exc_info=exc)
        return _error(500, MSG_ERROR_INTERNO)

    routers = (salud.router, acceso.router, estudios.router, historial.router, trabajos.router)
    for router in routers:
        app.include_router(router, prefix="/api")
    return app
