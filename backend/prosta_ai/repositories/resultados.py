"""Resultado de un trabajo completado (CU04): rutas de salida y métricas."""
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from prosta_ai.models import Resultado


def _decimal(valor: float | None, cifras: int) -> Decimal | None:
    return None if valor is None else Decimal(str(round(float(valor), cifras)))


class RepositorioResultados:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    def crear(
        self, id_trabajo: int, ruta_mascara: str, *, ruta_imagen: str | None = None,
        ruta_roi: str | None = None, dice: float | None = None, iou: float | None = None,
        tiempo_total_s: float | None = None,
    ) -> Resultado:
        """Dice e IoU con 3 decimales; el tiempo en segundos con 2."""
        resultado = Resultado(
            id_trabajo=id_trabajo, ruta_mascara=ruta_mascara, ruta_imagen=ruta_imagen,
            ruta_roi=ruta_roi, dice=_decimal(dice, 3), iou=_decimal(iou, 3),
            tiempo_total_s=_decimal(tiempo_total_s, 2),
        )
        self.sesion.add(resultado)
        self.sesion.flush()
        return resultado

    def del_trabajo(self, id_trabajo: int) -> Resultado | None:
        return self.sesion.scalar(select(Resultado).where(Resultado.id_trabajo == id_trabajo))
