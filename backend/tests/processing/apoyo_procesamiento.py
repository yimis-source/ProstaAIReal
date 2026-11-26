"""Pipeline falso y datos pequeños para probar el servicio sin cargar el modelo."""
from __future__ import annotations

import gzip

import nibabel as nib
import numpy as np

from prosta_ai.pipeline import stages
from prosta_ai.pipeline.base import BasePipeline
from prosta_ai.pipeline.errors import StageError
from prosta_ai.pipeline.evaluation import dice, iou
from prosta_ai.pipeline.io import load_volume, save_nifti

INFO_FALSA = {
    "nombre": "modelo_falso", "version": "0.0.1", "ruta_pesos": None,
    "hash_pesos": "a" * 64, "ruta_configuracion": None,
}


def volumen_nifti(forma=(16, 16, 8)) -> bytes:
    """Esfera de intensidad en un NIfTI en memoria."""
    x, y, z = np.indices(forma)
    c = np.array(forma) / 2
    dist = np.sqrt((x - c[0]) ** 2 + (y - c[1]) ** 2 + ((z - c[2]) * 2) ** 2)
    datos = np.clip(400 - 60 * dist, 0, None).astype(np.float32)
    return _a_bytes(datos)


def referencia_nifti(forma=(16, 16, 8)) -> bytes:
    datos = nib.Nifti1Image.from_bytes(gzip.decompress(volumen_nifti(forma))).get_fdata() > 200
    return _a_bytes(datos.astype(np.uint8))


def _a_bytes(datos: np.ndarray) -> bytes:
    img = nib.Nifti1Image(datos, np.diag([1.5, 1.5, 3.0, 1.0]))
    return gzip.compress(img.to_bytes())  # se guarda como .nii.gz


class PipelineFalso(BasePipeline):
    """Usa el `run` real (orden y avisos de etapas); cada etapa es trivial.

    `falla_en` = nombre de etapa; `error` = excepción que lanza esa etapa.
    """

    def __init__(self, falla_en: str | None = None, error: Exception | None = None):
        self.falla_en = falla_en
        self.error = error
        self.corridas = 0

    def _quizas_fallar(self, etapa: str) -> None:
        if etapa == self.falla_en:
            raise self.error or StageError(etapa, "Falla de prueba.")

    def quality_control(self, inp, ctx):
        self.corridas += 1
        self._quizas_fallar(stages.CONTROL_CALIDAD)
        ctx.volume = load_volume(inp.files, inp.fmt)
        if inp.reference_files:
            ref = load_volume(inp.reference_files, "NIfTI")
            ctx.reference = (ref.data > 0).astype(np.uint8)

    def prepare(self, inp, ctx):
        self._quizas_fallar(stages.PREPARACION)

    def segment(self, inp, ctx):
        self._quizas_fallar(stages.SEGMENTACION)
        ctx.mask = (ctx.volume.data > 200).astype(np.uint8)

    def build_roi(self, inp, ctx):
        self._quizas_fallar(stages.ROI)
        ctx.mask_original = ctx.mask
        ctx.image_path = inp.output_dir / "imagen.nii.gz"
        ctx.mask_path = inp.output_dir / "mascara.nii.gz"
        save_nifti(ctx.volume.data, ctx.volume.affine, ctx.image_path)
        save_nifti(ctx.mask_original, ctx.volume.affine, ctx.mask_path)

    def evaluate(self, inp, ctx):
        self._quizas_fallar(stages.EVALUACION)
        if ctx.reference is not None:
            ctx.dice = dice(ctx.mask_original, ctx.reference)
            ctx.iou = iou(ctx.mask_original, ctx.reference)


class ProveedorFalso:
    def __init__(self, pipeline=None, info=None, error_al_construir: Exception | None = None):
        self._pipeline = pipeline or PipelineFalso()
        self._info = info or dict(INFO_FALSA)
        self._error = error_al_construir
        self.llamadas_info = 0

    def pipeline(self):
        if self._error is not None:
            raise self._error
        return self._pipeline

    def info(self) -> dict:
        self.llamadas_info += 1
        return self._info
