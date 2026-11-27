"""Cuerpos JSON de estudios y trabajos (contrato, secciones 3, 4.5 y 4.7)."""
from datetime import datetime, timezone

from prosta_ai.models import Estudio, Trabajo

NO_COMPATIBLE = "no compatible"
LISTO = "listo para procesar"


def fecha(valor: datetime | None) -> str | None:
    if valor is None:
        return None
    # SQLite devuelve la fecha sin zona; se guardó en UTC
    if valor.tzinfo is None:
        valor = valor.replace(tzinfo=timezone.utc)
    return valor.isoformat()


def num(valor) -> float | None:
    return None if valor is None else float(valor)


def ultimo_trabajo(estudio: Estudio) -> Trabajo | None:
    # La relación viene ordenada por id_trabajo: el último es el más reciente
    return estudio.trabajos[-1] if estudio.trabajos else None


def estado_visible(estudio: Estudio) -> str:
    """Estado que ve la interfaz; se calcula, no se guarda.

    no compatible > estado del último trabajo (pendiente, en proceso, completado, fallido)
    > listo para procesar.
    """
    if estudio.estado_admision == NO_COMPATIBLE:
        return NO_COMPATIBLE
    ultimo = ultimo_trabajo(estudio)
    return ultimo.estado if ultimo is not None else LISTO


def detalle_trabajo(trabajo: Trabajo, codigo: str) -> dict:
    """Cuerpo de GET /api/trabajos/{id_trabajo}; las etapas en el orden del pipeline."""
    return {
        "id": trabajo.id_trabajo,
        "id_estudio": trabajo.id_estudio,
        "codigo": codigo,
        "estado": trabajo.estado,
        "etapa_fallida": trabajo.etapa_fallida,
        "mensaje_error": trabajo.mensaje_error,
        "fecha_creacion": fecha(trabajo.fecha_creacion),
        "fecha_inicio": fecha(trabajo.fecha_inicio),
        "fecha_fin": fecha(trabajo.fecha_fin),
        "etapas": [
            {"nombre": e.nombre, "estado": e.estado, "duracion_s": num(e.duracion_s)}
            for e in trabajo.etapas
        ],
    }


def detalle_estudio(estudio: Estudio) -> dict:
    """Cuerpo de GET /api/estudios/{id_estudio}: Dice e IoU del último trabajo, si terminó."""
    ultimo = ultimo_trabajo(estudio)
    resultado = ultimo.resultado if ultimo is not None else None
    return {
        "id": estudio.id_estudio,
        "codigo": estudio.codigo_anonimo,
        "formato": estudio.formato,
        "fecha_carga": fecha(estudio.fecha_carga),
        "estado": estado_visible(estudio),
        "estado_admision": estudio.estado_admision,
        "id_ultimo_trabajo": ultimo.id_trabajo if ultimo is not None else None,
        "dice": num(resultado.dice) if resultado is not None else None,
        "iou": num(resultado.iou) if resultado is not None else None,
        "trabajos": [detalle_trabajo(t, estudio.codigo_anonimo) for t in estudio.trabajos],
    }
