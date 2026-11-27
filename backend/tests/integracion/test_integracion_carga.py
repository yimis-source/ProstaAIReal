"""1708: flujo de acceso y carga de punta a punta contra PostgreSQL migrado con Alembic.

Complementa las pruebas unitarias de backend/tests/api/ (SQLite con create_all): aquí el
esquema sale de la migración y se revisa lo que queda en PostgreSQL y en disco.
"""
import gzip
import hashlib
import re
from datetime import datetime, timedelta, timezone
from pathlib import PurePosixPath

import pytest

from prosta_ai.api.admision import CAMPOS_TEXTO, MSG_DANADO, MSG_FORMATO
from prosta_ai.models import Archivo, Estudio, Usuario

from apoyo_integracion import CONTRASENA, TEXTO_CABECERA, leer_nifti, leer_nifti_bytes, nifti

# Nombres de archivo ficticios que no deben quedar en ningún lado (RB-02)
NOMBRE_IMAGEN = "Nombre_Ficticio_Apellido_19700101.nii.gz"
NOMBRE_REFERENCIA = "Mascara_Ficticia_Apellido.nii.gz"


def _sha256(ruta) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def _cabecera_limpia(ruta) -> None:
    """RF-05: los campos de texto libre quedan vacíos y sin extensiones."""
    cabecera = leer_nifti(ruta).header
    for campo in CAMPOS_TEXTO:
        assert bytes(cabecera[campo]).strip(b"\x00 ") == b"", campo
    assert len(cabecera.extensions) == 0
    assert TEXTO_CABECERA not in gzip.decompress(ruta.read_bytes())


def _comprobar_archivo(entorno, archivo: Archivo, codigo: str, rol: str) -> None:
    assert archivo.ruta == f"estudios/{codigo}/{rol}.nii.gz"
    assert not PurePosixPath(archivo.ruta).is_absolute()
    assert str(entorno.almacen.raiz) not in archivo.ruta
    en_disco = entorno.almacen.absoluta(archivo.ruta)
    assert en_disco.is_file()
    assert archivo.hash_sha256 == _sha256(en_disco)
    assert archivo.tamano_bytes == en_disco.stat().st_size
    assert archivo.valido is True
    _cabecera_limpia(en_disco)


def test_esquema_creado_por_la_migracion(entorno):
    assert entorno.version_alembic() == "0002"  # 0002: rutas de salida del resultado (1711)
    assert entorno.conteos() == {"usuario": 0, "estudio": 0, "archivo": 0}


def test_flujo_cuenta_ingreso_carga_y_detalle(entorno):
    # Crear cuenta (CU01)
    assert entorno.verificar("tester01").json() == {"existe": False}
    r = entorno.acceder("tester01", confirmacion=CONTRASENA)
    assert r.status_code == 200, r.text
    assert r.json()["primer_acceso"] is True
    assert entorno.verificar("tester01").json() == {"existe": True}

    # Ingresar de nuevo con la cuenta ya creada
    r = entorno.acceder("tester01")
    assert r.status_code == 200, r.text
    assert r.json()["primer_acceso"] is False
    cab = {"Authorization": f"Bearer {r.json()['token']}"}
    assert entorno.acceder("tester01", contrasena="otra-clave-9").status_code == 401

    with entorno.sesion() as s:
        (usuario,) = s.query(Usuario).all()
        assert usuario.alias == "tester01"
        assert usuario.hash_contrasena.startswith("$2b$")
        assert CONTRASENA not in usuario.hash_contrasena

    # Cargar sin referencia (CU02)
    antes = datetime.now(timezone.utc)
    r = entorno.cargar(cab, nombre=NOMBRE_IMAGEN)
    assert r.status_code == 201, r.text
    cuerpo = r.json()
    assert cuerpo == {
        "id": cuerpo["id"], "codigo": f"EST-{cuerpo['id']:04d}", "formato": "NIfTI",
        "estado": "listo para procesar",
    }
    codigo = cuerpo["codigo"]

    # Detalle del estudio
    r = entorno.detalle(cab, cuerpo["id"])
    assert r.status_code == 200, r.text
    det = r.json()
    assert det["codigo"] == codigo
    assert det["formato"] == "NIfTI"
    assert det["estado"] == "listo para procesar"
    assert det["estado_admision"] == "admitido"
    assert det["id_ultimo_trabajo"] is None
    assert det["dice"] is None and det["iou"] is None
    assert det["trabajos"] == []
    fecha = datetime.fromisoformat(det["fecha_carga"])
    assert fecha.tzinfo is not None
    assert antes - timedelta(minutes=1) <= fecha <= datetime.now(timezone.utc) + timedelta(minutes=1)

    # Filas en PostgreSQL
    estudio = entorno.estudio(cuerpo["id"])
    assert estudio.codigo_anonimo == codigo
    assert estudio.id_usuario == usuario.id_usuario
    assert estudio.estado_admision == "admitido"
    assert estudio.fecha_carga.tzinfo is not None
    (archivo,) = entorno.archivos(cuerpo["id"])
    _comprobar_archivo(entorno, archivo, codigo, "imagen")

    # El nombre original no queda en la base ni en disco
    texto = entorno.texto_de_la_base()
    for parte in ("Nombre_Ficticio", "Apellido", "19700101"):
        assert parte not in texto
    assert [p.relative_to(entorno.almacen.raiz).as_posix() for p in entorno.archivos_en_disco()] \
        == [f"estudios/{codigo}/imagen.nii.gz"]


def test_carga_con_referencia(entorno):
    cab = entorno.cabeceras("tester02")
    r = entorno.cargar(cab, contenido=nifti(semilla=1), nombre=NOMBRE_IMAGEN,
                       referencia=nifti(semilla=2, mascara=True),
                       nombre_referencia=NOMBRE_REFERENCIA)
    assert r.status_code == 201, r.text
    id_estudio, codigo = r.json()["id"], r.json()["codigo"]

    imagen, referencia = entorno.archivos(id_estudio)
    _comprobar_archivo(entorno, imagen, codigo, "imagen")
    _comprobar_archivo(entorno, referencia, codigo, "referencia")
    assert imagen.hash_sha256 != referencia.hash_sha256
    assert entorno.conteos() == {"usuario": 1, "estudio": 1, "archivo": 2}

    # Los vóxeles se conservan; solo cambia la cabecera
    en_disco = leer_nifti(entorno.almacen.absoluta(referencia.ruta))
    original = leer_nifti_bytes(nifti(semilla=2, mascara=True))
    assert (en_disco.get_fdata() == original.get_fdata()).all()

    assert entorno.detalle(cab, id_estudio).status_code == 200
    texto = entorno.texto_de_la_base()
    assert "Ficticio" not in texto and "Ficticia" not in texto


@pytest.mark.parametrize(
    ("archivos", "mensaje"),
    [
        ({"nombre": "estudio.zip", "contenido": b"PK\x03\x04no es nifti"}, MSG_FORMATO),
        ({"nombre": "estudio.nii.gz", "contenido": b"\x1f\x8b danado"}, MSG_DANADO),
        ({"nombre": "estudio.nii", "contenido": nifti(comprimido=False)[:200]}, MSG_DANADO),
        ({"referencia": b"no es un nifti"}, MSG_DANADO),
    ],
    ids=["zip", "gzip-danado", "nii-truncado", "referencia-danada"],
)
def test_rechazo_no_registra_nada(entorno, archivos, mensaje):
    cab = entorno.cabeceras("tester03")
    # Un estudio previo, para comprobar que el rechazo no agrega nada encima
    previo = entorno.cargar(cab)
    assert previo.status_code == 201, previo.text
    conteos, carpetas = entorno.conteos(), entorno.carpetas_de_estudios()
    en_disco = entorno.archivos_en_disco()

    r = entorno.cargar(cab, **archivos)
    assert r.status_code == 422, r.text
    assert r.json() == {"detalle": mensaje}
    assert entorno.conteos() == conteos
    assert entorno.carpetas_de_estudios() == carpetas
    assert entorno.archivos_en_disco() == en_disco

    # El rechazo no gasta código: la siguiente carga sigue la numeración
    siguiente = entorno.cargar(cab)
    assert siguiente.status_code == 201, siguiente.text
    assert siguiente.json()["id"] == previo.json()["id"] + 1


def test_estudio_de_otro_usuario_da_404(entorno):
    cab_dueno = entorno.cabeceras("duena01")
    cab_otro = entorno.cabeceras("otro01")
    id_estudio = entorno.cargar(cab_dueno).json()["id"]

    assert entorno.detalle(cab_dueno, id_estudio).status_code == 200
    ajeno = entorno.detalle(cab_otro, id_estudio)
    inexistente = entorno.detalle(cab_otro, id_estudio + 1000)
    assert ajeno.status_code == inexistente.status_code == 404
    assert ajeno.json() == inexistente.json() == {"detalle": "Estudio no encontrado."}
    assert entorno.detalle({}, id_estudio).status_code == 401


def test_dos_cargas_codigos_distintos_y_correlativos(entorno):
    cab = entorno.cabeceras("tester04")
    primera = entorno.cargar(cab, contenido=nifti(semilla=3))
    segunda = entorno.cargar(cab, contenido=nifti(semilla=4))
    assert primera.status_code == segunda.status_code == 201
    uno, dos = primera.json(), segunda.json()

    assert uno["codigo"] != dos["codigo"]
    assert re.fullmatch(r"EST-\d{4,}", uno["codigo"]) and re.fullmatch(r"EST-\d{4,}", dos["codigo"])
    numero = lambda c: int(c.split("-")[1])  # noqa: E731
    assert numero(dos["codigo"]) == numero(uno["codigo"]) + 1
    assert dos["id"] == uno["id"] + 1
    # Base recién migrada: la numeración empieza en EST-0001
    assert uno["codigo"] == "EST-0001"

    with entorno.sesion() as s:
        codigos = [e.codigo_anonimo for e in s.query(Estudio).order_by(Estudio.id_estudio)]
    assert codigos == [uno["codigo"], dos["codigo"]]
    assert entorno.carpetas_de_estudios() == {uno["codigo"], dos["codigo"]}
    rutas = [a.ruta for i in (uno["id"], dos["id"]) for a in entorno.archivos(i)]
    assert rutas == [f"estudios/{uno['codigo']}/imagen.nii.gz",
                     f"estudios/{dos['codigo']}/imagen.nii.gz"]
