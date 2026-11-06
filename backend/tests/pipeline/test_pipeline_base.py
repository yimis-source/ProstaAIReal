import nibabel as nib
import numpy as np
import pytest

from prosta_ai.pipeline import stages
from prosta_ai.pipeline.base import PipelineInput, Segmentation3DPipeline
from prosta_ai.pipeline.errors import StageError
from prosta_ai.pipeline.progress import PipelineProgress, TimingRecorder
from datos_sinteticos import EstrategiaUmbral


class Registro:
    def __init__(self):
        self.eventos = []

    def on_stage_start(self, stage):
        self.eventos.append(("inicio", stage))

    def on_stage_end(self, stage, duration_s):
        assert duration_s >= 0
        self.eventos.append(("fin", stage))

    def on_stage_failed(self, stage, message):
        self.eventos.append(("fallo", stage, message))


def pipeline(config_prep, umbral=1.0):
    return Segmentation3DPipeline(EstrategiaUmbral(umbral), config=config_prep)


def test_punta_a_punta_nifti(tmp_path, nifti_path, referencia_path, config_prep):
    reg, tiempos = Registro(), TimingRecorder()
    prog = PipelineProgress()
    prog.attach(reg)
    prog.attach(tiempos)
    res = pipeline(config_prep).run(PipelineInput([nifti_path], "NIfTI", [referencia_path]), prog)

    # orden de etapas y notificaciones
    esperado = []
    for s in stages.STAGES:
        esperado += [("inicio", s), ("fin", s)]
    assert reg.eventos == esperado
    assert list(tiempos.durations) == stages.STAGES
    assert list(res.durations) == stages.STAGES

    # la máscara vuelve a la geometría de la imagen original
    orig = nib.load(str(nifti_path))
    assert res.mask.shape == orig.shape and res.mask.dtype == np.uint8
    assert np.allclose(res.affine, orig.affine)
    assert set(np.unique(res.mask)) <= {0, 1}
    assert res.dice > 0.8 and 0 < res.iou <= res.dice


def test_sin_referencia_deja_metricas_vacias(tmp_path, nifti_path, config_prep):
    res = pipeline(config_prep).run(PipelineInput([nifti_path], "NIfTI", []), PipelineProgress())
    assert res.dice is None and res.iou is None
    assert "evaluación" in res.durations


def test_dicom_aun_no_disponible(tmp_path, nifti_path, config_prep):
    with pytest.raises(StageError) as e:
        pipeline(config_prep).run(PipelineInput([nifti_path], "DICOM", []), PipelineProgress())
    assert e.value.stage == "control de calidad" and "ciclo 6" in e.value.message


def test_fallo_en_control_de_calidad(tmp_path, affine_demo, config_prep):
    pequeno = tmp_path / "chico.nii.gz"
    nib.save(nib.Nifti1Image(np.random.rand(40, 40, 4).astype(np.float32), affine_demo), str(pequeno))
    reg = Registro()
    prog = PipelineProgress()
    prog.attach(reg)
    estrategia = EstrategiaUmbral()
    p = Segmentation3DPipeline(estrategia, config=config_prep)
    with pytest.raises(StageError) as e:
        p.run(PipelineInput([pequeno], "NIfTI", []), prog)
    assert e.value.stage == "control de calidad" and "cortes" in e.value.message
    assert reg.eventos[0] == ("inicio", "control de calidad")
    assert reg.eventos[1][:2] == ("fallo", "control de calidad")
    assert len(reg.eventos) == 2  # no se ejecutan las etapas siguientes
    assert estrategia.llamadas == 0


@pytest.mark.parametrize("caso", ["constante", "nan", "ref_distinta"])
def test_otros_fallos_de_calidad(tmp_path, affine_demo, referencia_path, config_prep, caso):
    datos = np.random.rand(48, 48, 16).astype(np.float32)
    if caso == "constante":
        datos[:] = 3
    if caso == "nan":
        datos[0, 0, 0] = np.nan
    p = tmp_path / "v.nii.gz"
    nib.save(nib.Nifti1Image(datos, affine_demo), str(p))
    refs = [referencia_path]
    if caso == "ref_distinta":
        r = tmp_path / "r.nii.gz"
        nib.save(nib.Nifti1Image(np.zeros((48, 48, 10), np.uint8), affine_demo), str(r))
        refs = [r]
    with pytest.raises(StageError) as e:
        pipeline(config_prep).run(PipelineInput([p], "NIfTI", refs), PipelineProgress())
    assert e.value.stage == "control de calidad"


def test_error_inesperado_se_convierte_en_stage_error(tmp_path, nifti_path, config_prep):
    class Mala(EstrategiaUmbral):
        def segment(self, prepared):
            raise RuntimeError("boom")

    reg = Registro()
    prog = PipelineProgress()
    prog.attach(reg)
    with pytest.raises(StageError) as e:
        Segmentation3DPipeline(Mala(), config=config_prep).run(
            PipelineInput([nifti_path], "NIfTI", []), prog
        )
    assert e.value.stage == "segmentación"
    assert reg.eventos[-1][:2] == ("fallo", "segmentación")
