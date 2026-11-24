"""Ruta de salud de la API."""
from fastapi import APIRouter

from prosta_ai import __version__

router = APIRouter(tags=["salud"])


@router.get("/salud")
def salud() -> dict:
    return {"estado": "ok", "version": __version__}
