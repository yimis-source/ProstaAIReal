"""Modelos: relaciones, restricciones y borrado en cascada."""
from decimal import Decimal

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from prosta_ai.models import (
    Archivo, Estudio, EtapaTrabajo, Modelo, Resultado, Trabajo, Usuario,
)
from prosta_ai.pipeline.stages import STAGES


def _estudio(sesion, codigo="EST-0001", alias="ana"):
    usuario = sesion.scalar(select(Usuario).where(Usuario.alias == alias))
    if usuario is None:
        usuario = Usuario(alias=alias, hash_contrasena="x" * 60)
    estudio = Estudio(codigo_anonimo=codigo, usuario=usuario, formato="NIfTI",
                      estado_admision="admitido")
    sesion.add(estudio)
    sesion.flush()
    return estudio


def _trabajo(sesion, estudio):
    modelo = sesion.scalar(select(Modelo)) or Modelo(nombre="prostate_mri_anatomy", version="0.3.1")
    trabajo = Trabajo(estudio=estudio, modelo=modelo)
    trabajo.etapas = [EtapaTrabajo(nombre=n) for n in STAGES]
    sesion.add(trabajo)
    sesion.flush()
    return trabajo


def test_valores_por_defecto(sesion):
    estudio = _estudio(sesion)
    trabajo = _trabajo(sesion, estudio)
    sesion.commit()
    assert estudio.fecha_carga is not None
    assert trabajo.estado == "pendiente"
    assert [e.nombre for e in trabajo.etapas] == STAGES
    assert {e.estado for e in trabajo.etapas} == {"pendiente"}


def test_alias_unico(sesion):
    sesion.add_all([Usuario(alias="ana", hash_contrasena="h"), Usuario(alias="ana", hash_contrasena="h")])
    with pytest.raises(IntegrityError):
        sesion.flush()


def test_codigo_anonimo_unico(sesion):
    _estudio(sesion, "EST-0001")
    with pytest.raises(IntegrityError):
        _estudio(sesion, "EST-0001")


@pytest.mark.parametrize("campo,valor", [
    ("formato", "PNG"), ("estado_admision", "dudoso"),
])
def test_listas_cerradas_del_estudio(sesion, campo, valor):
    estudio = _estudio(sesion)
    setattr(estudio, campo, valor)
    with pytest.raises(IntegrityError):
        sesion.flush()


def test_estado_y_etapa_fuera_de_lista(sesion):
    trabajo = _trabajo(sesion, _estudio(sesion))
    trabajo.estado = "terminado"
    with pytest.raises(IntegrityError):
        sesion.flush()
    sesion.rollback()
    trabajo = _trabajo(sesion, _estudio(sesion))
    sesion.add(EtapaTrabajo(trabajo=trabajo, nombre="visor 3D"))
    with pytest.raises(IntegrityError):
        sesion.flush()


def test_modelo_nombre_version_unicos(sesion):
    sesion.add_all([Modelo(nombre="m", version="1"), Modelo(nombre="m", version="1")])
    with pytest.raises(IntegrityError):
        sesion.flush()


def test_resultado_sin_mascara_de_referencia(sesion):
    trabajo = _trabajo(sesion, _estudio(sesion))
    trabajo.resultado = Resultado(ruta_mascara="estudios/EST-0001/mascara.nii.gz")
    sesion.commit()
    assert trabajo.resultado.dice is None and trabajo.resultado.iou is None


def test_dice_fuera_de_rango(sesion):
    trabajo = _trabajo(sesion, _estudio(sesion))
    trabajo.resultado = Resultado(ruta_mascara="m", dice=Decimal("1.200"))
    with pytest.raises(IntegrityError):
        sesion.flush()


def test_un_resultado_por_trabajo(sesion):
    trabajo = _trabajo(sesion, _estudio(sesion))
    sesion.add_all([Resultado(trabajo=trabajo, ruta_mascara="a"),
                    Resultado(id_trabajo=trabajo.id_trabajo, ruta_mascara="b")])
    with pytest.raises(IntegrityError):
        sesion.flush()


def test_borrar_estudio_borra_en_cascada(sesion):
    estudio = _estudio(sesion)
    estudio.archivos.append(Archivo(ruta="estudios/EST-0001/t2.nii.gz", tamano_bytes=10,
                                    hash_sha256="0" * 64))
    trabajo = _trabajo(sesion, estudio)
    trabajo.resultado = Resultado(ruta_mascara="m")
    sesion.commit()
    sesion.delete(estudio)
    sesion.commit()
    for tabla in (Archivo, Trabajo, EtapaTrabajo, Resultado):
        assert sesion.scalar(select(func.count()).select_from(tabla)) == 0
    assert sesion.scalar(select(func.count()).select_from(Modelo)) == 1
    assert sesion.scalar(select(func.count()).select_from(Usuario)) == 1


def test_llave_foranea_activa_en_sqlite(sesion):
    sesion.add(Archivo(id_estudio=999, ruta="r", tamano_bytes=1, hash_sha256="0" * 64))
    with pytest.raises(IntegrityError):
        sesion.flush()
