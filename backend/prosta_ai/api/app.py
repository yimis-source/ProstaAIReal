"""Fábrica de la aplicación FastAPI.

Arranque (desde backend/): uvicorn prosta_ai.api.app:create_app --factory
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from prosta_ai import __version__
from prosta_ai.api import salud
from prosta_ai.config import Settings, get_settings


def _error(status_code: int, detalle, headers=None) -> JSONResponse:
    # Formato común de error: {"detalle": ...}
    return JSONResponse(status_code=status_code, content={"detalle": detalle}, headers=headers)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    app = FastAPI(title="Prosta-AI", version=__version__)
    app.state.settings = settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_lista,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(HTTPException)
    async def _http(_: Request, exc: HTTPException):
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

    app.include_router(salud.router, prefix="/api")
    return app
