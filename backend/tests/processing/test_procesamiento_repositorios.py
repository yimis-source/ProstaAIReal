"""Repositorio de trabajos: creación con etapas, transiciones y consultas."""
import pytest

from prosta_ai.pipeline.stages import STAGES
from prosta_ai.repositories import RepositorioTrabajos, TransicionNoValida


def test_crear_pendiente_con_cinco_etapas(fabrica, crear_trabajo):
    id_trabajo = crear_trabajo()
    with fabrica() as s:
        trabajo = RepositorioTrabajos(s).obtener(id_trabajo)
        assert trabajo.estado == "pendiente"
        assert [(e.nombre, e.estado, e.duracion_s) for e in trabajo.etapas] == [
            (n, "pendiente", None) for n in STAGES
        ]


def test_transiciones(fabrica, crear_trabajo):
    id_trabajo = crear_trabajo()
    with fabrica() as s:
        repo = RepositorioTrabajos(s)
        trabajo = repo.obtener(id_trabajo)
        with pytest.raises(TransicionNoValida):
            repo.completar(trabajo)
        repo.iniciar(trabajo)
        repo.fallar(trabajo, None, "x")
        with pytest.raises(TransicionNoValida):
            repo.iniciar(trabajo)


def test_activo_y_ultimo_del_estudio(fabrica, crear_trabajo):
    id_trabajo = crear_trabajo()
    with fabrica() as s:
        repo = RepositorioTrabajos(s)
        trabajo = repo.obtener(id_trabajo)
        assert repo.activo_del_estudio(trabajo.id_estudio) is trabajo
        repo.iniciar(trabajo)
        repo.fallar(trabajo, None, "x")
        assert repo.activo_del_estudio(trabajo.id_estudio) is None
        nuevo = repo.crear_pendiente(trabajo.id_estudio, trabajo.id_modelo)
        assert repo.ultimo_del_estudio(trabajo.id_estudio) is nuevo


def test_trabajo_ajeno_no_se_obtiene(fabrica, crear_trabajo):
    de_ana = crear_trabajo(alias="ana")
    crear_trabajo(alias="beto")
    with fabrica() as s:
        repo = RepositorioTrabajos(s)
        id_ana = repo.obtener(de_ana).estudio.id_usuario
        assert repo.obtener_de_usuario(de_ana, id_ana) is not None
        assert repo.obtener_de_usuario(de_ana, id_ana + 1) is None
