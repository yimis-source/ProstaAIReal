"""Pruebas del control de calidad (tarea 1301) escritas por el Tester."""
import gzip

import nibabel as nib
import numpy as np
import pytest

from scripts.control_calidad import revisar_caso


def _volumen(forma=(64, 64, 16), constante=False):
    if constante:
        return np.full(forma, 7, dtype=np.int16)
    rng = np.random.default_rng(0)
    return rng.integers(0, 1000, size=forma, dtype=np.int16)


def _mascara(forma=(64, 64, 16)):
    m = np.zeros(forma, dtype=np.uint8)
    m[20:40, 20:40, 4:12] = 1
    m[25:35, 25:35, 6:10] = 2
    return m


def _guardar(tmp_path, nombre, datos, espaciado=(0.6, 0.6, 3.6)):
    ruta = tmp_path / nombre
    nib.save(nib.Nifti1Image(datos, np.diag([*espaciado, 1.0])), str(ruta))
    return ruta


def test_caso_valido_se_aprueba(tmp_path):
    img = _guardar(tmp_path, "img.nii.gz", _volumen())
    ref = _guardar(tmp_path, "ref.nii.gz", _mascara())
    r = revisar_caso("prueba", "caso", img, ref)
    assert r.aprobado, r.motivos


@pytest.mark.parametrize(
    "datos, motivo",
    [
        (_volumen(constante=True), "intensidad constante"),
        (_volumen((64, 64, 5)), "cortes"),
        (_volumen((20, 64, 16)), "vóxeles"),
    ],
)
def test_imagenes_invalidas_se_excluyen_con_motivo(tmp_path, datos, motivo):
    img = _guardar(tmp_path, "img.nii.gz", datos)
    r = revisar_caso("prueba", "caso", img, None)
    assert not r.aprobado
    assert any(motivo in m for m in r.motivos)


def test_mascara_con_forma_distinta(tmp_path):
    img = _guardar(tmp_path, "img.nii.gz", _volumen())
    ref = _guardar(tmp_path, "ref.nii.gz", _mascara((64, 64, 12)))
    r = revisar_caso("prueba", "caso", img, ref)
    assert not r.aprobado and "forma distinta" in r.motivos[0]


def test_mascara_vacia_o_con_etiquetas_raras(tmp_path):
    img = _guardar(tmp_path, "img.nii.gz", _volumen())
    vacia = _guardar(tmp_path, "vacia.nii.gz", np.zeros((64, 64, 16), np.uint8))
    rara = _mascara()
    rara[0, 0, 0] = 5
    rara = _guardar(tmp_path, "rara.nii.gz", rara)
    assert "máscara vacía" in revisar_caso("p", "c", img, vacia).motivos
    assert any("etiquetas inesperadas" in m for m in revisar_caso("p", "c", img, rara).motivos)


def test_archivo_truncado_se_excluye(tmp_path):
    """Un .nii.gz cortado a la mitad (descarga interrumpida) no debe pasar el control.

    SimpleITK lo abre sin error y rellena con ceros los cortes que faltan.
    """
    completo = _guardar(tmp_path, "completo.nii.gz", _volumen())
    contenido = completo.read_bytes()
    truncado = tmp_path / "truncado.nii.gz"
    truncado.write_bytes(contenido[: len(contenido) // 2])
    with pytest.raises(EOFError):  # el archivo de verdad está incompleto
        with gzip.open(truncado) as f:
            f.read()
    r = revisar_caso("prueba", "truncado", truncado, None)
    assert not r.aprobado
