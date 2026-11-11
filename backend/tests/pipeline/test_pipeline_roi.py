"""Etapa ROI (ciclo 4): máscara alineada con la imagen original y guardada sin metadatos."""
import nibabel as nib
import numpy as np
import pytest

from prosta_ai.pipeline import stages
from prosta_ai.pipeline.base import PipelineInput, Segmentation3DPipeline
from prosta_ai.pipeline.errors import StageError
from prosta_ai.pipeline.io import load_volume
from prosta_ai.pipeline.preparation import prepare_volume
from prosta_ai.pipeline.progress import PipelineProgress
from prosta_ai.pipeline.roi import mask_to_original_space
from datos_sinteticos import EstrategiaUmbral


def correr(nifti, ref, config, salida):
    p = Segmentation3DPipeline(EstrategiaUmbral(1.0), config=config)
    return p.run(PipelineInput([nifti], "NIfTI", [ref] if ref else [], salida), PipelineProgress())


def test_roi_es_etapa_entre_segmentacion_y_evaluacion():
    i = stages.STAGES.index(stages.ROI)
    assert stages.STAGES[i - 1] == stages.SEGMENTACION and stages.STAGES[i + 1] == stages.EVALUACION


def test_roi_misma_forma_y_afin_que_la_imagen(tmp_path, nifti_path, referencia_path, config_prep):
    res = correr(nifti_path, referencia_path, config_prep, tmp_path / "out")
    orig = nib.load(str(nifti_path))
    msk = nib.load(str(res.mask_path))
    img = nib.load(str(res.image_path))
    assert msk.shape == img.shape == orig.shape
    assert np.allclose(msk.affine, orig.affine) and np.allclose(img.affine, orig.affine)


def test_roi_es_binaria_y_no_vacia(tmp_path, nifti_path, config_prep):
    res = correr(nifti_path, None, config_prep, tmp_path / "out")
    datos = np.asarray(nib.load(str(res.mask_path)).dataobj)
    assert set(np.unique(datos)) == {0, 1}
    assert datos.dtype == np.uint8


def test_roi_sin_descripcion_en_cabecera(tmp_path, nifti_path, config_prep):
    res = correr(nifti_path, None, config_prep, tmp_path / "out")
    for ruta in (res.image_path, res.mask_path):
        h = nib.load(str(ruta)).header
        for campo in ("descrip", "db_name", "aux_file"):
            assert bytes(h[campo]).strip(b"\0") == b"", (ruta.name, campo)


def test_dice_desde_la_mascara_guardada_coincide(tmp_path, nifti_path, referencia_path, config_prep):
    from prosta_ai.pipeline.evaluation import dice
    res = correr(nifti_path, referencia_path, config_prep, tmp_path / "out")
    guardada = np.asarray(nib.load(str(res.mask_path)).dataobj)
    ref = np.asarray(nib.load(str(referencia_path)).dataobj)
    assert dice(guardada, ref) == pytest.approx(res.dice)


def test_mascara_con_otra_forma_falla_en_roi(nifti_path, config_prep):
    vol = load_volume([nifti_path], "NIfTI")
    prep = prepare_volume(vol, config_prep)
    with pytest.raises(StageError) as e:
        mask_to_original_space(np.zeros((3, 3, 3), np.uint8), prep, vol)
    assert e.value.stage == stages.ROI
