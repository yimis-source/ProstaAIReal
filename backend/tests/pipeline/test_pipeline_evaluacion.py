import numpy as np
import pytest

from prosta_ai.pipeline.evaluation import (
    dice, distancia_media_superficie, hd95, iou,
)


def test_identicas():
    m = np.zeros((4, 4, 4), np.uint8)
    m[1:3, 1:3, 1:3] = 1
    assert dice(m, m) == 1.0 and iou(m, m) == 1.0


def test_disjuntas():
    a = np.zeros((4, 4, 4), np.uint8)
    b = a.copy()
    a[0] = 1
    b[3] = 1
    assert dice(a, b) == 0.0 and iou(a, b) == 0.0


def test_solape_parcial():
    a = np.zeros(10, np.uint8)
    b = np.zeros(10, np.uint8)
    a[:4] = 1  # 4 vóxeles
    b[2:6] = 1  # 4 vóxeles, 2 en común
    assert dice(a, b) == pytest.approx(2 * 2 / 8)
    assert iou(a, b) == pytest.approx(2 / 6)


def test_ambos_vacios():
    z = np.zeros((3, 3, 3))
    assert dice(z, z) == 1.0 and iou(z, z) == 1.0


def test_uno_vacio():
    a = np.ones((3, 3, 3))
    assert dice(a, np.zeros_like(a)) == 0.0


def test_formas_distintas():
    with pytest.raises(ValueError):
        dice(np.zeros((2, 2)), np.zeros((3, 3)))


def test_metricas_superficie_identicas_y_spacing():
    a = np.zeros(10, np.uint8)
    b = np.zeros(10, np.uint8)
    a[1] = 1
    b[4] = 1
    assert hd95(a, a) == 0.0
    assert distancia_media_superficie(a, a) == 0.0
    assert hd95(a, b, spacing=(2.0,)) == pytest.approx(6.0)
    assert distancia_media_superficie(a, b, spacing=(2.0,)) == pytest.approx(6.0)


def test_metricas_superficie_mascaras_vacias():
    vacia = np.zeros((3, 3), dtype=np.uint8)
    llena = vacia.copy()
    llena[1, 1] = 1
    assert hd95(vacia, vacia) == 0.0
    assert distancia_media_superficie(vacia, vacia) == 0.0
    assert np.isinf(hd95(vacia, llena))
    assert np.isinf(distancia_media_superficie(vacia, llena))


def test_spacing_invalido():
    m = np.ones((3, 3), dtype=np.uint8)
    with pytest.raises(ValueError):
        hd95(m, m, spacing=(1.0,))
