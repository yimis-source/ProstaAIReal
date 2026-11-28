"""CU04 por la API: resultado del trabajo (4.8) y cortes en PNG (4.9).

Con el pipeline falso (no carga el modelo): esfera de 16x16x8 y su máscara.
"""
from io import BytesIO

import numpy as np
from PIL import Image

from apoyo_procesamiento import INFO_FALSA, referencia_nifti, volumen_nifti
from prosta_ai.constantes import AVISO_EXPERIMENTAL

FORMA = [16, 16, 8]
SIN_RESULTADO = {"detalle": "El trabajo no tiene resultado disponible."}
NO_ENCONTRADO = {"detalle": "Trabajo no encontrado."}


def _trabajo(entorno, cab, referencia=True, procesar=True) -> int:
    r = entorno.cargar(cab, volumen_nifti(), referencia=referencia_nifti() if referencia else None)
    assert r.status_code == 201, r.text
    r = entorno.client.post(f"/api/estudios/{r.json()['id']}/procesar", headers=cab)
    assert r.status_code == 201, r.text
    if procesar:
        assert entorno.servicio.procesar_siguiente() is True
    return r.json()["id"]


def _resultado(entorno, cab, id_trabajo):
    return entorno.client.get(f"/api/trabajos/{id_trabajo}/resultado", headers=cab)


def _corte(entorno, cab, id_trabajo, indice, capa=None):
    params = {} if capa is None else {"capa": capa}
    return entorno.client.get(f"/api/trabajos/{id_trabajo}/corte/{indice}", params=params, headers=cab)


def _png(r) -> Image.Image:
    assert r.status_code == 200, r.text
    assert r.headers["content-type"] == "image/png"
    return Image.open(BytesIO(r.content))


# --- GET /api/trabajos/{id}/resultado ---

def test_resultado_completado_da_cuerpo_del_contrato(entorno):
    cab = entorno.cabeceras()
    id_trabajo = _trabajo(entorno, cab)
    r = _resultado(entorno, cab, id_trabajo)
    assert r.status_code == 200, r.text
    cuerpo = r.json()
    assert set(cuerpo) == {
        "id_trabajo", "codigo", "dice", "iou", "tiempo_total_s", "modelo", "cortes", "forma", "aviso",
    }
    assert cuerpo["id_trabajo"] == id_trabajo and cuerpo["codigo"] == "EST-0001"
    # La máscara falsa coincide con la referencia
    assert cuerpo["dice"] == 1.0 and cuerpo["iou"] == 1.0
    assert cuerpo["tiempo_total_s"] >= 0
    assert cuerpo["modelo"] == {"nombre": INFO_FALSA["nombre"], "version": INFO_FALSA["version"]}
    assert cuerpo["forma"] == FORMA and cuerpo["cortes"] == FORMA[2]
    assert cuerpo["aviso"] == AVISO_EXPERIMENTAL


def test_resultado_sin_referencia_da_dice_e_iou_null(entorno):
    cab = entorno.cabeceras()
    cuerpo = _resultado(entorno, cab, _trabajo(entorno, cab, referencia=False)).json()
    assert cuerpo["dice"] is None and cuerpo["iou"] is None
    assert cuerpo["cortes"] == FORMA[2] and cuerpo["aviso"] == AVISO_EXPERIMENTAL


def test_resultado_de_trabajo_no_completado_da_404(entorno):
    cab = entorno.cabeceras()
    id_trabajo = _trabajo(entorno, cab, procesar=False)
    r = _resultado(entorno, cab, id_trabajo)
    assert r.status_code == 404 and r.json() == SIN_RESULTADO
    r = _corte(entorno, cab, id_trabajo, 0)
    assert r.status_code == 404 and r.json() == SIN_RESULTADO


def test_resultado_ajeno_o_inexistente_da_404(entorno):
    id_trabajo = _trabajo(entorno, entorno.cabeceras("ana"))
    otro = entorno.cabeceras("beto")
    for id_ in (id_trabajo, 999):
        r = _resultado(entorno, otro, id_)
        assert r.status_code == 404 and r.json() == NO_ENCONTRADO
        r = _corte(entorno, otro, id_, 0)
        assert r.status_code == 404 and r.json() == NO_ENCONTRADO


def test_resultado_sin_token_da_401(entorno):
    id_trabajo = _trabajo(entorno, entorno.cabeceras())
    assert entorno.client.get(f"/api/trabajos/{id_trabajo}/resultado").status_code == 401


# --- GET /api/trabajos/{id}/corte/{indice} ---

def test_corte_imagen_en_gris_con_el_tamano_del_volumen(entorno):
    cab = entorno.cabeceras()
    id_trabajo = _trabajo(entorno, cab)
    img = _png(_corte(entorno, cab, id_trabajo, 4))
    assert img.mode == "L"
    # Corte axial: ancho = x, alto = y
    assert img.size == (FORMA[0], FORMA[1])
    # Sin capa, la imagen
    assert _png(_corte(entorno, cab, id_trabajo, 4, "imagen")).tobytes() == img.tobytes()


def test_corte_mascara_rgba_transparente_y_del_mismo_tamano(entorno):
    cab = entorno.cabeceras()
    id_trabajo = _trabajo(entorno, cab)
    imagen = _png(_corte(entorno, cab, id_trabajo, 4, "imagen"))
    mascara = _png(_corte(entorno, cab, id_trabajo, 4, "mascara"))
    assert mascara.mode == "RGBA" and mascara.size == imagen.size
    alfa = np.asarray(mascara)[..., 3]
    # Fondo transparente (las esquinas quedan fuera de la esfera) y ROI visible en el centro
    assert alfa[0, 0] == 0 and alfa[-1, -1] == 0
    assert (alfa > 0).sum() > 0 and alfa[8, 8] > 0
    assert (alfa == 0).sum() > (alfa > 0).sum()


def test_corte_primero_y_ultimo_son_validos(entorno):
    cab = entorno.cabeceras()
    id_trabajo = _trabajo(entorno, cab)
    for indice in (0, FORMA[2] - 1):
        for capa in ("imagen", "mascara"):
            assert _corte(entorno, cab, id_trabajo, indice, capa).status_code == 200


def test_corte_fuera_de_rango_da_422(entorno):
    cab = entorno.cabeceras()
    id_trabajo = _trabajo(entorno, cab)
    for indice in (-1, FORMA[2], 50):
        r = _corte(entorno, cab, id_trabajo, indice)
        assert r.status_code == 422, (indice, r.status_code)
        assert r.json() == {"detalle": "El corte debe estar entre 0 y 7."}


def test_corte_con_capa_no_valida_da_422(entorno):
    cab = entorno.cabeceras()
    id_trabajo = _trabajo(entorno, cab)
    r = _corte(entorno, cab, id_trabajo, 0, "roi")
    assert r.status_code == 422
    assert r.json()["campos"] == ["capa"]


def test_cortes_seguidos_leen_el_volumen_una_vez(entorno, monkeypatch):
    from prosta_ai.api import volumenes

    cab = entorno.cabeceras()
    id_trabajo = _trabajo(entorno, cab)
    lecturas = []
    original = volumenes.cargar_volumen
    monkeypatch.setattr(
        volumenes, "cargar_volumen", lambda *a: lecturas.append(a) or original(*a)
    )
    _resultado(entorno, cab, id_trabajo)
    for indice in range(FORMA[2]):
        _corte(entorno, cab, id_trabajo, indice, "mascara")
    assert len(lecturas) == 1
