"""Imagen de la ROI con el aviso no diagnóstico (RF-13, RF-15)."""
import nibabel as nib
import numpy as np
import pytest
from PIL import Image

from prosta_ai.constantes import AVISO_EXPERIMENTAL
from prosta_ai.pipeline.visualizacion import (
    ANCHO_MINIMO_EXPORTAR,
    COLOR_BANDA_AVISO,
    COLOR_ROI,
    AvisoDecorator,
    ImageSliceRenderer,
    MaskSliceRenderer,
    OverlaySliceRenderer,
    cargar_volumen,
    corte_representativo,
    guardar_imagen_roi,
)
from datos_sinteticos import esfera


@pytest.fixture
def rutas(tmp_path, affine_demo):
    img = tmp_path / "imagen.nii.gz"
    msk = tmp_path / "mascara.nii.gz"
    datos = esfera()
    nib.save(nib.Nifti1Image(datos, affine_demo), str(img))
    nib.save(nib.Nifti1Image((datos > 300).astype(np.uint8), affine_demo), str(msk))
    return img, msk


def test_corte_sin_roi_en_gris(rutas):
    vol = cargar_volumen(*rutas)
    im = ImageSliceRenderer().render(vol, 8)
    assert im.mode == "L" and im.size == (48, 48)


def test_mascara_rgba_con_color_de_la_roi(rutas):
    vol = cargar_volumen(*rutas)
    rgba = np.asarray(MaskSliceRenderer().render(vol, 8))
    visibles = rgba[rgba[..., 3] > 0]
    assert len(visibles) > 0 and (visibles[:, :3] == COLOR_ROI).all()
    assert (rgba[..., 3] == 0).any()  # fuera de la ROI es transparente


def test_superposicion_tine_solo_la_roi(rutas):
    vol = cargar_volumen(*rutas)
    gris = np.asarray(ImageSliceRenderer().render(vol, 8).convert("RGB")).astype(int)
    mezcla = np.asarray(OverlaySliceRenderer().render(vol, 8)).astype(int)
    roi = np.rot90(vol.mascara[:, :, 8])
    assert (mezcla[~roi] == gris[~roi]).all()
    assert (mezcla[roi] != gris[roi]).any(axis=-1).all()


def test_aviso_en_banda_inferior_y_ancho_minimo(rutas):
    vol = cargar_volumen(*rutas)
    im = AvisoDecorator(OverlaySliceRenderer()).render(vol, 8)
    assert im.width >= ANCHO_MINIMO_EXPORTAR
    # la imagen 48x48 se amplía 11 veces (528 px) y debajo va la banda del aviso
    assert im.height > im.width
    banda = np.asarray(im)[im.width + 2 :, :, :]
    assert (banda == COLOR_BANDA_AVISO).all(axis=-1).mean() > 0.5  # fondo de la banda
    assert (banda > 200).all(axis=-1).any()  # texto blanco


def test_imagen_sin_mascara_tambien_lleva_aviso(tmp_path, rutas):
    vol = cargar_volumen(rutas[0], tmp_path / "no_existe.nii.gz")
    assert vol.mascara is None and corte_representativo(vol) == vol.cortes // 2
    im = AvisoDecorator(OverlaySliceRenderer()).render(vol, 8)
    assert im.height > ANCHO_MINIMO_EXPORTAR


def test_mascara_vacia(tmp_path, rutas, affine_demo):
    vacia = tmp_path / "vacia.nii.gz"
    nib.save(nib.Nifti1Image(np.zeros((48, 48, 16), np.uint8), affine_demo), str(vacia))
    vol = cargar_volumen(rutas[0], vacia)
    rgba = np.asarray(MaskSliceRenderer().render(vol, 8))
    assert (rgba[..., 3] == 0).all()
    assert corte_representativo(vol) == 8


def test_corte_representativo_es_el_de_mayor_roi(rutas):
    vol = cargar_volumen(*rutas)
    assert corte_representativo(vol) == 8  # centro de la elipsoide


def test_guardar_png(tmp_path, rutas):
    destino = tmp_path / "salida" / "roi_demo.png"
    k = guardar_imagen_roi(*rutas, destino)
    assert k == 8 and destino.exists()
    with Image.open(destino) as im:
        assert im.format == "PNG" and im.width >= ANCHO_MINIMO_EXPORTAR
    with pytest.raises(IndexError):
        guardar_imagen_roi(*rutas, tmp_path / "x.png", indice=99)


def test_mascara_de_otra_forma(tmp_path, rutas, affine_demo):
    otra = tmp_path / "otra.nii.gz"
    nib.save(nib.Nifti1Image(np.zeros((10, 10, 10), np.uint8), affine_demo), str(otra))
    with pytest.raises(ValueError):
        cargar_volumen(rutas[0], otra)


def test_aviso_es_el_texto_unico():
    assert "No es un diagnóstico" in AVISO_EXPERIMENTAL
