import numpy as np
import pytest

from prosta_ai.pipeline.errors import StageError
from prosta_ai.pipeline.io import Volume
from prosta_ai.pipeline.validators import MIN_SIDE, MIN_SLICES, detailed_validation


def vol(shape=(48, 48, 16), spacing=(1.0, 1.0, 3.0), datos=None) -> Volume:
    d = np.random.default_rng(1).random(shape).astype(np.float32) if datos is None else datos
    return Volume(data=d, affine=np.diag([*spacing, 1.0]), spacing=spacing)


def test_volumen_valido_pasa():
    detailed_validation(vol(), vol())


@pytest.mark.parametrize("datos, texto", [
    (np.full((48, 48, 16), 5, np.float32), "constante"),
    (np.full((48, 48, 16), np.nan, np.float32), "no numéricos"),
    (np.zeros((48, 48), np.float32), "3D"),
])
def test_integridad(datos, texto):
    with pytest.raises(StageError) as e:
        detailed_validation(vol(datos=datos))
    assert e.value.stage == "control de calidad" and texto in e.value.message


def test_pocos_cortes():
    with pytest.raises(StageError, match=f"al menos {MIN_SLICES}"):
        detailed_validation(vol(shape=(48, 48, MIN_SLICES - 1)))


def test_cortes_pequenos():
    with pytest.raises(StageError, match=f"{MIN_SIDE}x{MIN_SIDE}"):
        detailed_validation(vol(shape=(MIN_SIDE - 1, 48, 16)))


def test_espaciado_no_positivo():
    with pytest.raises(StageError, match="espaciado"):
        detailed_validation(vol(spacing=(1.0, 0.0, 3.0)))


def test_referencia_con_otra_forma():
    with pytest.raises(StageError, match="misma forma"):
        detailed_validation(vol(), vol(shape=(48, 48, 10)))
