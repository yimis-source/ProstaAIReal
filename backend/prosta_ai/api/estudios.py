"""CU02: carga de un estudio NIfTI y su detalle."""
import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from prosta_ai.api.admision import (
    MSG_SIN_ARCHIVO, ArchivoRechazado, NiftiAdmitido, comprobar_nifti, leer_limitado,
    limpiar_cabecera,
)
from prosta_ai.api.deps import ajustes, almacenamiento, sesion, usuario_actual
from prosta_ai.config import Settings
from prosta_ai.models import Estudio, Usuario
from prosta_ai.repositories import RepositorioArchivos, RepositorioEstudios
from prosta_ai.storage import AlmacenamientoPrivado

log = logging.getLogger(__name__)
router = APIRouter(prefix="/estudios", tags=["estudios"])

MSG_NO_GUARDADO = "No se pudo guardar el estudio. Intente de nuevo."


def estado_visible(estudio: Estudio) -> str:
    """Estado que ve la interfaz (contrato, sección 3); no se guarda."""
    if estudio.estado_admision == "no compatible":
        return "no compatible"
    if estudio.trabajos:
        return estudio.trabajos[-1].estado
    return "listo para procesar"


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
            limpiar_cabecera(admitido.imagen)
            # Solo la extensión: el nombre original no se guarda (RB-02)
            guardado = almacen.guardar(codigo, rol, admitido.contenido, f"x{admitido.extension}")
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
