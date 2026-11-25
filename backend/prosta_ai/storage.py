"""Almacenamiento privado de archivos en disco, fuera de la base de datos (RB-02).

Estructura: <storage_dir>/estudios/<EST-0001>/<rol>.<ext>. El nombre original del
archivo nunca se usa en la ruta: solo se toma su extensión conocida.
"""
import hashlib
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

ROLES = ("imagen", "referencia")
# Extensiones que se conservan; cualquier otra queda como .bin
_EXTENSIONES = (".nii.gz", ".nii")
_BLOQUE = 1024 * 1024
_CODIGO = re.compile(r"^EST-\d{4,}$")


@dataclass(frozen=True)
class ArchivoGuardado:
    ruta: str  # relativa a storage_dir, con «/»
    tamano_bytes: int
    sha256: str


def extension_segura(nombre: str | None) -> str:
    bajo = (nombre or "").lower()
    for ext in _EXTENSIONES:
        if bajo.endswith(ext):
            return ext
    return ".bin"


def rol_de_ruta(ruta: str) -> str:
    """Rol (imagen o referencia) a partir de la ruta guardada."""
    nombre = Path(ruta).name.split(".")[0]
    if nombre not in ROLES:
        raise ValueError("Ruta sin rol conocido")
    return nombre


class AlmacenamientoPrivado:
    def __init__(self, raiz: Path):
        self.raiz = Path(raiz).resolve()
        self.raiz.mkdir(parents=True, exist_ok=True)

    def carpeta_estudio(self, codigo: str) -> Path:
        if not _CODIGO.match(codigo):
            raise ValueError("Código de estudio no válido")
        return self.raiz / "estudios" / codigo

    def absoluta(self, ruta_relativa: str) -> Path:
        """Ruta en disco; rechaza las que salen del almacenamiento."""
        ruta = (self.raiz / ruta_relativa).resolve()
        if self.raiz not in ruta.parents:
            raise ValueError("Ruta fuera del almacenamiento")
        return ruta

    def guardar(
        self, codigo: str, rol: str, origen: BinaryIO | bytes, nombre_original: str | None = None
    ) -> ArchivoGuardado:
        """Guarda los bytes bajo el código y calcula su SHA-256 al escribir."""
        if rol not in ROLES:
            raise ValueError("Rol de archivo no válido")
        carpeta = self.carpeta_estudio(codigo)
        carpeta.mkdir(parents=True, exist_ok=True)
        destino = carpeta / f"{rol}{extension_segura(nombre_original)}"
        sha = hashlib.sha256()
        tamano = 0
        try:
            with open(destino, "wb") as f:
                if isinstance(origen, (bytes, bytearray)):
                    f.write(origen)
                    sha.update(origen)
                    tamano = len(origen)
                else:
                    while bloque := origen.read(_BLOQUE):
                        f.write(bloque)
                        sha.update(bloque)
                        tamano += len(bloque)
        except BaseException:
            # No dejar un archivo a medias
            destino.unlink(missing_ok=True)
            raise
        return ArchivoGuardado(str(destino), tamano, sha.hexdigest())

    def sha256(self, ruta_relativa: str) -> str:
        """Recalcula la huella de un archivo guardado."""
        sha = hashlib.sha256()
        with open(self.absoluta(ruta_relativa), "rb") as f:
            while bloque := f.read(_BLOQUE):
                sha.update(bloque)
        return sha.hexdigest()

    def borrar_estudio(self, codigo: str) -> None:
        """Borra todo lo guardado de un estudio (p. ej. si falló el registro)."""
        shutil.rmtree(self.carpeta_estudio(codigo), ignore_errors=True)
