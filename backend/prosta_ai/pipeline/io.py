"""Lectura y escritura de volúmenes (patrón Adapter sobre nibabel).

Convención interna: `Volume.data` se indexa como en nibabel (x, y, z) y
`Volume.affine` lleva coordenadas RAS+ (mm).

En esta versión solo se lee NIfTI (los conjuntos del proyecto son NIfTI tras la
unificación de formato del ciclo 2). La lectura de DICOM, su desidentificación y
los archivos .zip llegan con la carga de estudios de la aplicación (ciclo 6).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import nibabel as nib
import numpy as np

from .errors import StageError
from .stages import CONTROL_CALIDAD


@dataclass
class Volume:
    """Volumen 3D en float32 con su geometría."""

    data: np.ndarray
    affine: np.ndarray
    spacing: tuple[float, float, float]


def _leer_nifti(path: Path) -> Volume:
    """Lee un NIfTI. Si es 4D (p. ej. MSD Task05: canal 0 = T2, canal 1 = ADC) usa el canal 0."""
    try:
        img = nib.load(str(path))
        shape = img.shape
        if len(shape) == 4:
            data = np.asarray(img.dataobj[..., 0], dtype=np.float32)
        elif len(shape) == 3:
            data = np.asarray(img.dataobj, dtype=np.float32)
        else:
            raise StageError(CONTROL_CALIDAD, f"El volumen tiene {len(shape)} dimensiones; se esperaba 3D.")
        affine = np.array(img.affine, dtype=np.float64)
    except StageError:
        raise
    except Exception as exc:  # incluye .nii.gz truncados (EOFError de gzip)
        raise StageError(CONTROL_CALIDAD, f"El archivo {path.name} está dañado o no se puede leer.") from exc
    zooms = np.linalg.norm(affine[:3, :3], axis=0)
    return Volume(data=data, affine=affine, spacing=(float(zooms[0]), float(zooms[1]), float(zooms[2])))


def load_volume(files: list[Path], fmt: str) -> Volume:
    """Lee el estudio como un Volume. Lanza StageError("control de calidad", ...) si falla."""
    if not files:
        raise StageError(CONTROL_CALIDAD, "No hay archivos para leer.")
    if fmt == "NIfTI":
        if len(files) != 1:
            raise StageError(CONTROL_CALIDAD, "Un estudio NIfTI debe ser un único archivo.")
        return _leer_nifti(Path(files[0]))
    if fmt == "DICOM":
        raise StageError(CONTROL_CALIDAD, "La lectura de DICOM se habilita en el ciclo 6 (carga de estudios).")
    raise StageError(CONTROL_CALIDAD, f"Formato desconocido: {fmt}")


def save_nifti(data: np.ndarray, affine: np.ndarray, path: Path) -> None:
    """Guarda un NIfTI sin descripción ni metadatos de persona."""
    arr = np.asarray(data)
    if arr.dtype == np.float64:
        arr = arr.astype(np.float32)
    img = nib.Nifti1Image(arr, np.asarray(affine))
    img.header["descrip"] = b""
    img.header["db_name"] = b""
    img.header["aux_file"] = b""
    img.header.set_qform(img.affine, code=1)
    img.header.set_sform(img.affine, code=1)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    nib.save(img, str(path))
