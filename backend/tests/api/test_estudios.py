"""CU02: carga de NIfTI, validación, RF-05, detalle y errores 500."""
import gzip
import hashlib
import logging
import re

import nibabel as nib
import numpy as np
import pytest

from prosta_ai.api.admision import CAMPOS_TEXTO, MSG_DANADO, MSG_FORMATO, MSG_SIN_ARCHIVO
from prosta_ai.models import Archivo, Estudio

from apoyo_api import nifti

TEXTO = b"texto libre de prueba"


def _leer(ruta):
    datos = ruta.read_bytes()
    if ruta.name.endswith(".gz"):
        datos = gzip.decompress(datos)
    return nib.Nifti1Image.from_bytes(datos)


def _leer_bytes(contenido: bytes, comprimido: bool):
    return nib.Nifti1Image.from_bytes(gzip.decompress(contenido) if comprimido else contenido)


# --- Carga válida ---------------------------------------------------------------------------

def test_carga_valida_201(entorno):
    cab = entorno.cabeceras()
    r = entorno.cargar(cab, nombre="paciente_nombre_apellido.nii.gz")
    assert r.status_code == 201, r.text
    cuerpo = r.json()
    assert set(cuerpo) == {"id", "codigo", "formato", "estado"}
    assert re.fullmatch(r"EST-\d{4}", cuerpo["codigo"])
    assert cuerpo["formato"] == "NIfTI"
    assert cuerpo["estado"] == "listo para procesar"


def test_carga_guarda_ruta_relativa_y_sha256(entorno):
    cab = entorno.cabeceras()
    codigo = entorno.cargar(cab, nombre="paciente_nombre.nii.gz").json()["codigo"]
    (archivo,) = entorno.archivos()
    assert archivo.ruta == f"estudios/{codigo}/imagen.nii.gz"
    assert "paciente" not in archivo.ruta
    en_disco = entorno.almacen.absoluta(archivo.ruta)
    assert archivo.hash_sha256 == hashlib.sha256(en_disco.read_bytes()).hexdigest()
    assert archivo.tamano_bytes == en_disco.stat().st_size


def test_carga_con_referencia(entorno):
    cab = entorno.cabeceras()
    r = entorno.cargar(cab, referencia=nifti(forma=(16, 16, 8)))
    assert r.status_code == 201
    rutas = [a.ruta for a in entorno.archivos()]
    assert [ruta.rsplit("/", 1)[1] for ruta in rutas] == ["imagen.nii.gz", "referencia.nii.gz"]


@pytest.mark.parametrize("comprimido", [True, False])
def test_rf05_cabecera_guardada_sin_texto_libre(entorno, comprimido):
    cab = entorno.cabeceras()
    nombre = "estudio.nii.gz" if comprimido else "estudio.nii"
    r = entorno.cargar(cab, contenido=nifti(texto=TEXTO, comprimido=comprimido), nombre=nombre)
    assert r.status_code == 201
    (archivo,) = entorno.archivos()
    guardado = _leer(entorno.almacen.absoluta(archivo.ruta))
    for campo in CAMPOS_TEXTO:
        assert guardado.header[campo].tobytes().strip(b"\x00") == b"", campo
    # La limpieza no toca los vóxeles ni la geometría
    original = _leer_bytes(nifti(texto=TEXTO, comprimido=comprimido), comprimido)
    assert np.array_equal(guardado.get_fdata(), original.get_fdata())
    assert np.allclose(guardado.affine, original.affine)


def test_carga_nifti2_admitido(entorno):
    cab = entorno.cabeceras()
    r = entorno.cargar(cab, contenido=nifti(nifti2=True))
    assert r.status_code == 201


# --- Rechazos: 422 y nada registrado --------------------------------------------------------

@pytest.mark.parametrize("nombre", ["estudio.zip", "corte.dcm", "imagen.png", "sin_extension"])
def test_rechaza_extension(entorno, nombre):
    r = entorno.cargar(entorno.cabeceras(), nombre=nombre)
    assert r.status_code == 422
    assert r.json() == {"detalle": MSG_FORMATO}
    assert entorno.nada_registrado()


@pytest.mark.parametrize(
    "contenido, nombre",
    [
        (b"esto no es un nifti" * 50, "falso.nii"),
        (b"esto no es un nifti" * 50, "falso.nii.gz"),
        (gzip.compress(b"x" * 1000), "gzip_sin_nifti.nii.gz"),
        (nifti(comprimido=False)[:600], "truncado.nii"),
        (nifti()[:200], "truncado.nii.gz"),
    ],
)
def test_rechaza_archivo_danado(entorno, contenido, nombre):
    r = entorno.cargar(entorno.cabeceras(), contenido=contenido, nombre=nombre)
    assert r.status_code == 422
    assert r.json() == {"detalle": MSG_DANADO}
    assert entorno.nada_registrado()


def test_rechaza_archivo_vacio(entorno):
    r = entorno.cargar(entorno.cabeceras(), contenido=b"")
    assert r.status_code == 422
    assert r.json() == {"detalle": "El archivo está vacío."}
    assert entorno.nada_registrado()


def test_rechaza_sin_archivo(entorno):
    cab = entorno.cabeceras()
    r = entorno.client.post("/api/estudios", headers=cab)
    assert r.status_code == 422 and r.json() == {"detalle": MSG_SIN_ARCHIVO}
    # Campo sin archivo elegido, como lo manda el navegador (filename=""); httpx omitiría
    # el filename vacío, por eso el cuerpo se arma a mano
    cuerpo = (
        b'--limite\r\nContent-Disposition: form-data; name="archivos"; filename=""\r\n'
        b"Content-Type: application/octet-stream\r\n\r\n\r\n--limite--\r\n"
    )
    r = entorno.client.post(
        "/api/estudios", content=cuerpo,
        headers={**cab, "Content-Type": "multipart/form-data; boundary=limite"},
    )
    assert r.status_code == 422 and r.json() == {"detalle": MSG_SIN_ARCHIVO}
    assert entorno.nada_registrado()


def test_rechaza_archivo_demasiado_grande(entorno_limitado):
    e = entorno_limitado
    grande = nifti(forma=(64, 64, 80), comprimido=False)  # ~1,3 MB
    r = e.cargar(e.cabeceras(), contenido=grande, nombre="grande.nii")
    assert r.status_code == 422
    assert r.json() == {"detalle": "El archivo supera el máximo de 1 MB."}
    assert e.nada_registrado()


def test_rechaza_estudio_demasiado_grande(entorno_limitado):
    e = entorno_limitado
    medio = nifti(forma=(64, 64, 40), comprimido=False)  # ~0,65 MB cada uno
    archivos = [("archivos", ("imagen.nii", medio)), ("referencia", ("ref.nii", medio))]
    r = e.client.post("/api/estudios", files=archivos, headers=e.cabeceras())
    assert r.status_code == 422
    assert r.json() == {"detalle": "El estudio supera el máximo de 1 MB."}
    assert e.nada_registrado()


def test_referencia_danada_no_registra_la_imagen(entorno):
    r = entorno.cargar(entorno.cabeceras(), referencia=b"no es nifti")
    assert r.status_code == 422
    assert entorno.nada_registrado()


# --- Detalle y propiedad --------------------------------------------------------------------

def test_detalle_del_estudio(entorno):
    cab = entorno.cabeceras()
    id_estudio = entorno.cargar(cab).json()["id"]
    r = entorno.client.get(f"/api/estudios/{id_estudio}", headers=cab)
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["id"] == id_estudio
    assert cuerpo["estado"] == "listo para procesar"
    assert cuerpo["estado_admision"] == "admitido"
    assert cuerpo["trabajos"] == [] and cuerpo["id_ultimo_trabajo"] is None
    assert cuerpo["dice"] is None and cuerpo["iou"] is None
    assert re.search(r"[+-]\d{2}:\d{2}$", cuerpo["fecha_carga"])


def test_estudio_ajeno_da_404(entorno):
    id_estudio = entorno.cargar(entorno.cabeceras("ana")).json()["id"]
    otro = entorno.cabeceras("beto")
    r = entorno.client.get(f"/api/estudios/{id_estudio}", headers=otro)
    assert r.status_code == 404
    assert r.json() == {"detalle": "Estudio no encontrado."}
    assert entorno.client.get("/api/estudios/999", headers=otro).status_code == 404


# --- Errores 500 ----------------------------------------------------------------------------

def test_fallo_al_guardar_da_500_y_no_deja_nada(entorno, monkeypatch):
    cab = entorno.cabeceras()
    original = entorno.almacen.guardar
    llamadas = []

    def guardar_que_falla(codigo, rol, origen, nombre=None):
        llamadas.append(rol)
        if rol == "referencia":
            raise OSError("disco lleno /ruta/interna")
        return original(codigo, rol, origen, nombre)

    monkeypatch.setattr(entorno.almacen, "guardar", guardar_que_falla)
    r = entorno.cargar(cab, referencia=nifti())
    assert llamadas == ["imagen", "referencia"]
    assert r.status_code == 500
    assert r.json() == {"detalle": "No se pudo guardar el estudio. Intente de nuevo."}
    assert entorno.contar(Estudio) == 0 and entorno.contar(Archivo) == 0
    assert not any(p.is_file() for p in entorno.almacen.raiz.rglob("*"))


def test_error_inesperado_da_500_generico_y_queda_en_el_log(entorno, caplog):
    @entorno.app.get("/api/explota")
    def explota():
        raise RuntimeError("detalle interno /home/secreto")

    with caplog.at_level(logging.ERROR, logger="prosta_ai.api.app"):
        r = entorno.client.get("/api/explota")
    assert r.status_code == 500
    assert set(r.json()) == {"detalle"}
    assert "secreto" not in r.text and "Traceback" not in r.text
    assert "detalle interno /home/secreto" in caplog.text
