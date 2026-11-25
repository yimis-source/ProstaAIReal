"""Almacenamiento privado: rutas sin nombre original, SHA-256 y limpieza."""
import hashlib
import io

import pytest

from prosta_ai.storage import AlmacenamientoPrivado, extension_segura, rol_de_ruta

DATOS = b"\x5c\x01\x00\x00" + b"volumen de prueba" * 1000


@pytest.fixture
def almacen(tmp_path):
    return AlmacenamientoPrivado(tmp_path / "almacenamiento")


def test_guarda_con_ruta_relativa_y_sha256(almacen):
    g = almacen.guardar("EST-0001", "imagen", io.BytesIO(DATOS), "Perez_Juan_T2.nii.gz")
    assert g.ruta == "estudios/EST-0001/imagen.nii.gz"
    assert g.tamano_bytes == len(DATOS)
    assert g.sha256 == hashlib.sha256(DATOS).hexdigest()
    assert almacen.absoluta(g.ruta).read_bytes() == DATOS
    assert almacen.sha256(g.ruta) == g.sha256


def test_nunca_usa_el_nombre_original(almacen):
    g = almacen.guardar("EST-0002", "referencia", DATOS, "Maria Lopez mascara.nii")
    assert "Maria" not in g.ruta and "Lopez" not in g.ruta
    assert rol_de_ruta(g.ruta) == "referencia"
    archivos = [p.name for p in almacen.raiz.rglob("*") if p.is_file()]
    assert archivos == ["referencia.nii"]


def test_extension_desconocida_queda_bin():
    assert extension_segura("datos.NII.GZ") == ".nii.gz"
    assert extension_segura("../../etc/passwd") == ".bin"
    assert extension_segura(None) == ".bin"


def test_rechaza_codigo_rol_y_rutas_fuera(almacen):
    with pytest.raises(ValueError):
        almacen.guardar("../fuera", "imagen", DATOS)
    with pytest.raises(ValueError):
        almacen.guardar("EST-0001", "otro", DATOS)
    with pytest.raises(ValueError):
        almacen.absoluta("../fuera.nii")


class _Falla(io.BytesIO):
    def read(self, n=-1):
        if self.tell() > 0:
            raise OSError("disco lleno")
        return super().read(10)


def test_borra_lo_guardado_a_medias(almacen):
    with pytest.raises(OSError):
        almacen.guardar("EST-0003", "imagen", _Falla(DATOS), "x.nii")
    assert not (almacen.raiz / "estudios" / "EST-0003" / "imagen.nii").exists()


def test_borrar_estudio(almacen):
    almacen.guardar("EST-0004", "imagen", DATOS, "x.nii")
    almacen.guardar("EST-0004", "referencia", DATOS, "y.nii")
    almacen.borrar_estudio("EST-0004")
    assert not (almacen.raiz / "estudios" / "EST-0004").exists()
