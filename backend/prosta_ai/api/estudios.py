"""CU02 y CU03: carga de un estudio NIfTI, su detalle y la orden de procesarlo."""
import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from prosta_ai.api.admision import (
    MSG_SIN_ARCHIVO, ArchivoRechazado, NiftiAdmitido, a_bytes, comprobar_nifti, leer_limitado,
    limpiar_cabecera,
)
from prosta_ai.api.deps import ajustes, almacenamiento, servicio, sesion, usuario_actual
from prosta_ai.api.vistas import NO_COMPATIBLE, detalle_estudio, detalle_trabajo, estado_visible
from prosta_ai.config import Settings
from prosta_ai.models import Usuario
from prosta_ai.processing import ServicioProcesamiento
from prosta_ai.repositories import RepositorioArchivos, RepositorioEstudios, RepositorioTrabajos
from prosta_ai.storage import AlmacenamientoPrivado

log = logging.getLogger(__name__)
router = APIRouter(prefix="/estudios", tags=["estudios"])

MSG_NO_GUARDADO = "No se pudo guardar el estudio. Intente de nuevo."
MSG_NO_ENCONTRADO = "Estudio no encontrado."
MSG_NO_COMPATIBLE = "El estudio no es compatible y no se puede procesar."
MSG_EN_CURSO = "El estudio ya tiene un procesamiento pendiente o en curso."


def _con_nombre(archivos: list[UploadFile]) -> list[UploadFile]:
    # El navegador manda el campo vacío cuando no se elige archivo
    return [f for f in archivos if f.filename]


async def _admitir(archivo: UploadFile, settings: Settings) -> NiftiAdmitido:
    contenido = await leer_limitado(archivo, settings.max_upload_bytes)
    return comprobar_nifti(archivo.filename, contenido, settings.max_estudio_bytes)


@router.post("", status_code=201)
async def cargar(
    archivos: list[UploadFile] = File(default=[]),
    referencia: list[UploadFile] = File(default=[]),
    db: Session = Depends(sesion),
    almacen: AlmacenamientoPrivado = Depends(almacenamiento),
    settings: Settings = Depends(ajustes),
    usuario: Usuario = Depends(usuario_actual),
) -> dict:
    archivos, referencia = _con_nombre(archivos), _con_nombre(referencia)
    if not archivos:
        raise HTTPException(422, MSG_SIN_ARCHIVO)
    if len(archivos) > 1 or len(referencia) > 1:
        raise HTTPException(422, "Cargue un solo archivo de imagen y, si quiere, una referencia.")

    # Validación completa antes de guardar o registrar nada
    try:
        admitidos = {"imagen": await _admitir(archivos[0], settings)}
        if referencia:
            admitidos["referencia"] = await _admitir(referencia[0], settings)
    except ArchivoRechazado as exc:
        raise HTTPException(422, exc.mensaje)
    total = sum(len(a.contenido) for a in admitidos.values())
    if total > settings.max_estudio_bytes:
        raise HTTPException(
            422, f"El estudio supera el máximo de {settings.max_estudio_mb} MB."
        )

    estudios, registro = RepositorioEstudios(db), RepositorioArchivos(db)
    codigo = None
    try:
        estudio = estudios.crear(usuario.id_usuario, formato="NIfTI")
        codigo = estudio.codigo_anonimo
        for rol, admitido in admitidos.items():
            # RF-05: se guarda el NIfTI ya limpio, no los bytes que llegaron
            limpiar_cabecera(admitido.imagen)
            limpio = a_bytes(admitido.imagen, admitido.comprimido)
            # Solo la extensión: el nombre original no se guarda (RB-02)
            guardado = almacen.guardar(codigo, rol, limpio, f"x{admitido.extension}")
            registro.registrar(estudio.id_estudio, guardado)
        db.commit()
    except Exception:
        log.exception("No se pudo guardar el estudio %s", codigo)
        db.rollback()
        if codigo:
            almacen.borrar_estudio(codigo)
        raise HTTPException(500, MSG_NO_GUARDADO)
    return {
        "id": estudio.id_estudio,
        "codigo": codigo,
        "formato": estudio.formato,
        "estado": estado_visible(estudio),
    }


@router.get("/{id_estudio}")
def detalle(
    id_estudio: int, db: Session = Depends(sesion), usuario: Usuario = Depends(usuario_actual)
) -> dict:
    estudio = RepositorioEstudios(db).obtener_de_usuario(id_estudio, usuario.id_usuario)
    if estudio is None:
        # Ajeno o inexistente: misma respuesta
        raise HTTPException(404, MSG_NO_ENCONTRADO)
    return detalle_estudio(estudio)


@router.post("/{id_estudio}/procesar", status_code=201)
def procesar(
    id_estudio: int, db: Session = Depends(sesion), usuario: Usuario = Depends(usuario_actual),
    procesamiento: ServicioProcesamiento = Depends(servicio),
) -> dict:
    """Crea un trabajo pendiente y responde de inmediato; lo corre la tarea en segundo plano."""
    estudio = RepositorioEstudios(db).obtener_de_usuario(id_estudio, usuario.id_usuario)
    if estudio is None:
        raise HTTPException(404, MSG_NO_ENCONTRADO)
    if estudio.estado_admision == NO_COMPATIBLE:
        raise HTTPException(409, MSG_NO_COMPATIBLE)
    trabajos = RepositorioTrabajos(db)
    # Pendiente o en proceso: un trabajo pendiente todavía no lo tomó la tarea
    if trabajos.activo_del_estudio(estudio.id_estudio) is not None:
        raise HTTPException(409, MSG_EN_CURSO)
    trabajo = trabajos.crear_pendiente(
        estudio.id_estudio, procesamiento.id_modelo_activo()
    )
    db.commit()
    return detalle_trabajo(trabajo, estudio.codigo_anonimo)
