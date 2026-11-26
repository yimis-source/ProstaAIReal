"""Repositorios de usuarios, estudios y archivos (RB-01, RB-02) con SQLite."""
import pytest
from sqlalchemy.orm import Session

from prosta_ai import db as modulo_db
from prosta_ai.db import crear_fabrica_sesiones, crear_motor, obtener_sesion
from prosta_ai.models import Estudio
from prosta_ai.repositories import (
    RepositorioArchivos, RepositorioEstudios, RepositorioUsuarios,
)
from prosta_ai.storage import AlmacenamientoPrivado, ArchivoGuardado

HASH = "$2b$12$" + "x" * 53


def _usuario(sesion, alias="estudiante01"):
    return RepositorioUsuarios(sesion).crear(alias, HASH)


def test_usuario_crear_y_buscar_por_alias(sesion):
    usuario = _usuario(sesion)
    repo = RepositorioUsuarios(sesion)
    assert repo.por_alias("estudiante01").id_usuario == usuario.id_usuario
    assert repo.obtener(usuario.id_usuario) is usuario
    assert repo.por_alias("nadie") is None


def test_codigos_correlativos_y_sin_repetir(sesion):
    usuario = _usuario(sesion)
    repo = RepositorioEstudios(sesion)
    e1, e2 = repo.crear(usuario.id_usuario), repo.crear(usuario.id_usuario)
    sesion.commit()
    assert (e1.codigo_anonimo, e2.codigo_anonimo) == ("EST-0001", "EST-0002")
    assert e1.formato == "NIfTI" and e1.estado_admision == "admitido"
    sesion.delete(e1)
    sesion.commit()
    e3 = repo.crear(usuario.id_usuario)
    sesion.commit()
    assert e3.codigo_anonimo == "EST-0003"


def test_estudio_ajeno_no_se_obtiene(sesion):
    ana, beto = _usuario(sesion, "ana"), _usuario(sesion, "beto")
    repo = RepositorioEstudios(sesion)
    estudio = repo.crear(ana.id_usuario)
    assert repo.obtener_de_usuario(estudio.id_estudio, ana.id_usuario) is estudio
    assert repo.obtener_de_usuario(estudio.id_estudio, beto.id_usuario) is None
    assert repo.obtener_de_usuario(999, ana.id_usuario) is None


def test_carga_completa_guarda_ruta_relativa(sesion, tmp_path):
    """Flujo de la 1705: estudio, archivos en disco y registro en la base."""
    almacen = AlmacenamientoPrivado(tmp_path)
    usuario = _usuario(sesion)
    estudio = RepositorioEstudios(sesion).crear(usuario.id_usuario)
    repo = RepositorioArchivos(sesion)
    for rol, nombre in (("imagen", "Paciente_T2.nii.gz"), ("referencia", "mask.nii")):
        guardado = almacen.guardar(estudio.codigo_anonimo, rol, b"datos " + rol.encode(), nombre)
        repo.registrar(estudio.id_estudio, guardado)
    sesion.commit()

    imagen, = repo.del_estudio(estudio.id_estudio, "imagen")
    assert imagen.ruta == "estudios/EST-0001/imagen.nii.gz"
    assert almacen.sha256(imagen.ruta) == imagen.hash_sha256
    assert imagen.tamano_bytes == len(b"datos imagen")
    assert [a.ruta for a in repo.del_estudio(estudio.id_estudio, "referencia")] == [
        "estudios/EST-0001/referencia.nii"
    ]
    assert len(repo.del_estudio(estudio.id_estudio)) == 2


def test_registrar_rechaza_ruta_absoluta_o_sin_rol(sesion):
    usuario = _usuario(sesion)
    estudio = RepositorioEstudios(sesion).crear(usuario.id_usuario)
    repo = RepositorioArchivos(sesion)
    with pytest.raises(ValueError):
        repo.registrar(estudio.id_estudio, ArchivoGuardado("/tmp/imagen.nii", 1, "0" * 64))
    with pytest.raises(ValueError):
        repo.registrar(estudio.id_estudio, ArchivoGuardado("estudios/EST-0001/x.nii", 1, "0" * 64))


def test_revertir_no_deja_nada(sesion, tmp_path):
    """Si algo falla después de guardar, la API revierte y borra el disco."""
    almacen = AlmacenamientoPrivado(tmp_path)
    usuario = _usuario(sesion)
    sesion.commit()
    estudio = RepositorioEstudios(sesion).crear(usuario.id_usuario)
    guardado = almacen.guardar(estudio.codigo_anonimo, "imagen", b"datos", "a.nii")
    RepositorioArchivos(sesion).registrar(estudio.id_estudio, guardado)
    sesion.rollback()
    almacen.borrar_estudio(estudio.codigo_anonimo)
    assert sesion.query(Estudio).count() == 0
    assert not any(tmp_path.rglob("*.nii"))


def test_obtener_sesion_como_dependencia(monkeypatch):
    fabrica = crear_fabrica_sesiones(crear_motor("sqlite://"))
    monkeypatch.setattr(modulo_db, "_fabrica", fabrica)
    generador = obtener_sesion()
    sesion = next(generador)
    assert isinstance(sesion, Session)
    with pytest.raises(StopIteration):
        next(generador)
