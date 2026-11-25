"""Admisión de archivos NIfTI antes de guardar nada (RF-03, RF-04) y limpieza de la
cabecera (RF-05).

Se comprueba la extensión y también la cabecera del archivo: un .nii con otro
contenido se rechaza igual que un .zip.
"""
import gzip
import io
import struct
import zlib
from dataclasses import dataclass

import nibabel as nib
import numpy as np
from fastapi import UploadFile

_BLOQUE = 1024 * 1024
_GZIP = b"\x1f\x8b"
# Campos de texto libre de la cabecera que pueden traer datos de la persona (RF-05)
CAMPOS_TEXTO = ("descrip", "aux_file", "intent_name", "db_name")

MSG_SIN_ARCHIVO = "Seleccione al menos un archivo de imagen."
MSG_FORMATO = (
    "Formato no admitido. En esta versión solo se aceptan archivos NIfTI (.nii o .nii.gz)."
)
MSG_DANADO = "El archivo está dañado o no es un NIfTI válido."
MSG_VACIO = "El archivo está vacío."


class ArchivoRechazado(Exception):
    """El archivo no pasa la admisión; el mensaje va tal cual al usuario (422)."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje


@dataclass
class NiftiAdmitido:
    extension: str  # ".nii" o ".nii.gz"
    contenido: bytes  # bytes tal como llegaron
    imagen: nib.Nifti1Image | nib.Nifti2Image

    @property
    def comprimido(self) -> bool:
        return self.extension == ".nii.gz"


def extension_nifti(nombre: str | None) -> str:
    bajo = (nombre or "").lower().strip()
    for ext in (".nii.gz", ".nii"):
        if bajo.endswith(ext):
            return ext
    raise ArchivoRechazado(MSG_FORMATO)


def _mb(n_bytes: int) -> int:
    return n_bytes // (1024 * 1024)


async def leer_limitado(archivo: UploadFile, maximo: int) -> bytes:
    """Lee el archivo sin pasar del máximo permitido."""
    partes, total = [], 0
    while bloque := await archivo.read(_BLOQUE):
        total += len(bloque)
        if total > maximo:
            raise ArchivoRechazado(f"El archivo supera el máximo de {_mb(maximo)} MB.")
        partes.append(bloque)
    return b"".join(partes)


def _descomprimir(contenido: bytes, maximo: int) -> bytes:
    if not contenido.startswith(_GZIP):
        raise ArchivoRechazado(MSG_DANADO)
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(contenido)) as gz:
            datos = gz.read(maximo + 1)
    except (OSError, EOFError, zlib.error):
        raise ArchivoRechazado(MSG_DANADO)
    if len(datos) > maximo:
        raise ArchivoRechazado("El archivo descomprimido es demasiado grande.")
    return datos


def _clase_por_cabecera(datos: bytes):
    """Clase de nibabel según sizeof_hdr y la marca mágica (NIfTI-1 o NIfTI-2 en un solo archivo)."""
    if len(datos) < 348:
        raise ArchivoRechazado(MSG_DANADO)
    for orden in ("<", ">"):
        (tamano,) = struct.unpack(orden + "i", datos[:4])
        if tamano == 348 and datos[344:348] == b"n+1\x00":
            return nib.Nifti1Image
        if tamano == 540 and datos[4:8] == b"n+2\x00":
            return nib.Nifti2Image
    raise ArchivoRechazado(MSG_DANADO)


def comprobar_nifti(nombre: str | None, contenido: bytes, max_descomprimido: int) -> NiftiAdmitido:
    """Extensión, cabecera y datos legibles; lanza ArchivoRechazado si algo falla."""
    extension = extension_nifti(nombre)
    if not contenido:
        raise ArchivoRechazado(MSG_VACIO)
    datos = _descomprimir(contenido, max_descomprimido) if extension == ".nii.gz" else contenido
    clase = _clase_por_cabecera(datos)
    try:
        imagen = clase.from_bytes(datos)
        # Fuerza la lectura de los vóxeles: un archivo truncado falla aquí
        np.asanyarray(imagen.dataobj)
    except Exception:
        raise ArchivoRechazado(MSG_DANADO)
    return NiftiAdmitido(extension, contenido, imagen)


def limpiar_cabecera(imagen) -> None:
    """RF-05: vacía los campos de texto libre y quita las extensiones de la cabecera."""
    cabecera = imagen.header
    for campo in CAMPOS_TEXTO:
        if campo in cabecera:
            cabecera[campo] = b""
    cabecera.extensions.clear()


def a_bytes(imagen, comprimido: bool) -> bytes:
    """Serializa el NIfTI; mtime=0 para que el mismo volumen dé el mismo SHA-256."""
    datos = imagen.to_bytes()
    return gzip.compress(datos, mtime=0) if comprimido else datos
