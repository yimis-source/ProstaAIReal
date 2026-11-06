import gzip

import nibabel as nib
import numpy as np
import pytest

from prosta_ai.pipeline.errors import StageError
from prosta_ai.pipeline.io import load_volume, save_nifti


def test_cargar_nifti_3d(nifti_path, affine_demo):
    v = load_volume([nifti_path], "NIfTI")
    assert v.data.shape == (48, 48, 16) and v.data.dtype == np.float32
    assert np.allclose(v.affine, affine_demo)
    assert v.spacing == pytest.approx((1.5, 1.5, 3.0))


def test_nifti_4d_usa_canal_0(tmp_path, affine_demo):
    t2 = np.full((40, 40, 10), 7, np.float32)
    t2[5:10] = 9
    adc = np.full((40, 40, 10), 100, np.float32)
    p = tmp_path / "msd.nii.gz"
    nib.save(nib.Nifti1Image(np.stack([t2, adc], -1), affine_demo), str(p))
    v = load_volume([p], "NIfTI")
    assert v.data.shape == (40, 40, 10)
    assert np.array_equal(v.data, t2)


def test_nifti_corrupto(tmp_path):
    p = tmp_path / "malo.nii.gz"
    p.write_bytes(b"\x1f\x8b" + b"basura" * 20)
    with pytest.raises(StageError) as e:
        load_volume([p], "NIfTI")
    assert e.value.stage == "control de calidad"


def test_nifti_truncado_se_rechaza(tmp_path, nifti_path):
    """Defecto del ciclo 2: un .nii.gz cortado no debe pasar como volumen relleno de ceros."""
    datos = nifti_path.read_bytes()
    p = tmp_path / "truncado.nii.gz"
    p.write_bytes(datos[: len(datos) * 6 // 10])
    with pytest.raises(StageError) as e:
        load_volume([p], "NIfTI")
    assert "dañado" in e.value.message


def test_nifti_sin_comprimir(tmp_path, nifti_path):
    p = tmp_path / "plano.nii"
    p.write_bytes(gzip.decompress(nifti_path.read_bytes()))
    assert load_volume([p], "NIfTI").data.shape == (48, 48, 16)


@pytest.mark.parametrize("fmt, mensaje", [("DICOM", "ciclo 6"), ("PNG", "desconocido")])
def test_formatos_no_disponibles(nifti_path, fmt, mensaje):
    with pytest.raises(StageError) as e:
        load_volume([nifti_path], fmt)
    assert mensaje in e.value.message


def test_varios_archivos_nifti(nifti_path):
    with pytest.raises(StageError, match="único archivo"):
        load_volume([nifti_path, nifti_path], "NIfTI")


def test_save_nifti_sin_metadatos(tmp_path, affine_demo):
    p = tmp_path / "o" / "x.nii.gz"
    save_nifti(np.ones((4, 4, 4), np.float64), affine_demo, p)
    img = nib.load(str(p))
    assert bytes(img.header["descrip"]).strip(b"\0") == b""
    assert np.allclose(img.affine, affine_demo)
    assert img.get_data_dtype() == np.float32
