"""Almacenamiento privado de archivos en disco, fuera de la base de datos (RB-02).

Estructura: <storage_dir>/estudios/<EST-0001>/<rol>.<ext>. El nombre original del
archivo nunca se usa en la ruta: solo se toma su extensión conocida. Las salidas de
cada trabajo van en <storage_dir>/estudios/<EST-0001>/trabajo-<id>/<rol>.<ext>.
"""
import hashlib
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

ROLES_ENTRADA = ("imagen", "referencia")
# Salidas del procesamiento (1711): volumen 3D usado, máscara (ROI) y PNG de la ROI con aviso
ROLES_SALIDA = ("volumen", "mascara", "roi")
ROLES = ROLES_ENTRADA + ROLES_SALIDA
_EXT_SALIDA = {"volumen": ".nii.gz", "mascara": ".nii.gz", "roi": ".png"}
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
    """Rol (imagen, referencia o una salida) a partir de la ruta guardada."""
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

    def carpeta_trabajo(self, codigo: str, id_trabajo: int) -> Path:
        return self.carpeta_estudio(codigo) / f"trabajo-{int(id_trabajo)}"

    def guardar(
        self, codigo: str, rol: str, origen: BinaryIO | bytes, nombre_original: str | None = None
    ) -> ArchivoGuardado:
        """Guarda los bytes bajo el código y calcula su SHA-256 al escribir."""
        if rol not in ROLES_ENTRADA:
            raise ValueError("Rol de archivo no válido")
        carpeta = self.carpeta_estudio(codigo)
        return self._escribir(carpeta / f"{rol}{extension_segura(nombre_original)}", origen)

    def guardar_salida(self, codigo: str, id_trabajo: int, rol: str, origen: Path) -> ArchivoGuardado:
        """Copia una salida del pipeline a la carpeta del trabajo."""
        if rol not in ROLES_SALIDA:
            raise ValueError("Rol de salida no válido")
        destino = self.carpeta_trabajo(codigo, id_trabajo) / f"{rol}{_EXT_SALIDA[rol]}"
        with open(origen, "rb") as f:
            return self._escribir(destino, f)

    def _escribir(self, destino: Path, origen: BinaryIO | bytes) -> ArchivoGuardado:
        destino.parent.mkdir(parents=True, exist_ok=True)
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
        ruta = destino.relative_to(self.raiz).as_posix()
        return ArchivoGuardado(ruta, tamano, sha.hexdigest())

    def carpeta_temporal(self) -> tempfile.TemporaryDirectory:
        """Carpeta de trabajo del pipeline dentro del almacenamiento; se borra al salir."""
        base = self.raiz / "tmp"
        base.mkdir(parents=True, exist_ok=True)
        return tempfile.TemporaryDirectory(dir=base)

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

    def borrar_salidas(self, codigo: str, id_trabajo: int) -> None:
        """Borra las salidas de un trabajo (si falló, no quedan a medias)."""
        shutil.rmtree(self.carpeta_trabajo(codigo, id_trabajo), ignore_errors=True)
