"""CU03 y CU04: estado de un trabajo (contrato 4.7) y su resultado (4.8)."""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from prosta_ai.api.deps import almacenamiento, sesion, usuario_actual
from prosta_ai.api.vistas import detalle_trabajo, num
from prosta_ai.api.volumenes import CacheVolumenes
from prosta_ai.constantes import AVISO_EXPERIMENTAL, COMPLETADO
from prosta_ai.models import Resultado, Trabajo, Usuario
from prosta_ai.pipeline.visualizacion import VolumenCortes
from prosta_ai.repositories import RepositorioResultados, RepositorioTrabajos
from prosta_ai.storage import AlmacenamientoPrivado

router = APIRouter(prefix="/trabajos", tags=["trabajos"])

MSG_NO_ENCONTRADO = "Trabajo no encontrado."
MSG_SIN_RESULTADO = "El trabajo no tiene resultado disponible."


def _trabajo_o_404(db: Session, id_trabajo: int, usuario: Usuario) -> Trabajo:
    trabajo = RepositorioTrabajos(db).obtener_de_usuario(id_trabajo, usuario.id_usuario)
    if trabajo is None:
        # Ajeno o inexistente: misma respuesta
        raise HTTPException(404, MSG_NO_ENCONTRADO)
    return trabajo


def _cache(request: Request) -> CacheVolumenes:
    app = request.app
    if not hasattr(app.state, "cache_volumenes"):
        app.state.cache_volumenes = CacheVolumenes()
    return app.state.cache_volumenes


def _volumen(
    db: Session, trabajo: Trabajo, almacen: AlmacenamientoPrivado, cache: CacheVolumenes
) -> tuple[Resultado, VolumenCortes]:
    """Resultado y volumen usado (con su máscara); 404 si el trabajo no está completado."""
    resultado = RepositorioResultados(db).del_trabajo(trabajo.id_trabajo)
    if trabajo.estado != COMPLETADO or resultado is None or not resultado.ruta_imagen:
        raise HTTPException(404, MSG_SIN_RESULTADO)
    ruta_imagen = almacen.absoluta(resultado.ruta_imagen)
    ruta_mascara = almacen.absoluta(resultado.ruta_mascara)
    if not ruta_imagen.exists():
        raise HTTPException(404, MSG_SIN_RESULTADO)
    return resultado, cache.obtener(trabajo.id_trabajo, ruta_imagen, ruta_mascara)


@router.get("/{id_trabajo}")
def estado(
    id_trabajo: int, db: Session = Depends(sesion), usuario: Usuario = Depends(usuario_actual)
) -> dict:
    trabajo = _trabajo_o_404(db, id_trabajo, usuario)
    return detalle_trabajo(trabajo, trabajo.estudio.codigo_anonimo)


@router.get("/{id_trabajo}/resultado")
def resultado(
    id_trabajo: int, request: Request, db: Session = Depends(sesion),
    almacen: AlmacenamientoPrivado = Depends(almacenamiento),
    usuario: Usuario = Depends(usuario_actual),
) -> dict:
    trabajo = _trabajo_o_404(db, id_trabajo, usuario)
    res, vol = _volumen(db, trabajo, almacen, _cache(request))
    return {
        "id_trabajo": trabajo.id_trabajo,
        "codigo": trabajo.estudio.codigo_anonimo,
        "dice": num(res.dice),
        "iou": num(res.iou),
        "tiempo_total_s": num(res.tiempo_total_s),
        "modelo": {"nombre": trabajo.modelo.nombre, "version": trabajo.modelo.version},
        "cortes": vol.cortes,
        "forma": list(vol.forma),
        "aviso": AVISO_EXPERIMENTAL,
    }
