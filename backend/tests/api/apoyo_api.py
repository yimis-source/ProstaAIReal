"""Apoyo de las pruebas de la API: SQLite y almacenamiento en carpetas temporales.

Los NIfTI se generan en cada prueba con nibabel; nunca se usan datos reales.
"""
import gzip
import sys
from pathlib import Path

import nibabel as nib
import numpy as np
from fastapi.testclient import TestClient
from sqlalchemy import func, select

from prosta_ai.api.app import create_app
from prosta_ai.config import Settings
from prosta_ai.db import Base
from prosta_ai.models import Archivo, Estudio

# El pipeline falso de las pruebas del servicio (tests/processing)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "processing"))
from apoyo_procesamiento import ProveedorFalso  # noqa: E402

CONTRASENA = "clave-segura-1"


def nifti(forma=(16, 16, 8), texto: bytes = b"", comprimido=True, nifti2=False) -> bytes:
    """Volumen sintético; `texto` va en los campos de texto libre de la cabecera."""
    datos = np.random.default_rng(0).normal(100, 10, forma).astype(np.float32)
    clase = nib.Nifti2Image if nifti2 else nib.Nifti1Image
    imagen = clase(datos, np.eye(4))
    if texto:
        imagen.header["descrip"] = texto
        imagen.header["aux_file"] = texto[:23]
        imagen.header["intent_name"] = texto[:15]
        if "db_name" in imagen.header:
            imagen.header["db_name"] = texto[:17]
    crudo = imagen.to_bytes()
    return gzip.compress(crudo) if comprimido else crudo


class Entorno:
    def __init__(self, tmp_path, proveedor=None, **ajustes):
        # Sin hilo: las pruebas llaman al servicio a mano
        ajustes.setdefault("worker_activo", False)
        self.settings = Settings(
            _env_file=None,
            database_url=f"sqlite:///{tmp_path / 'prueba.db'}",
            storage_dir=tmp_path / "almacen",
            secret_key="clave-de-pruebas",
            **ajustes,
        )
        self.proveedor = proveedor or ProveedorFalso()
        self.app = create_app(self.settings, proveedor_pipeline=self.proveedor)
        Base.metadata.create_all(self.app.state.motor)
        self.client = TestClient(self.app, raise_server_exceptions=False)
        self.almacen = self.app.state.almacenamiento
        self.servicio = self.app.state.servicio

    def acceder(self, alias="ana", contrasena=CONTRASENA, confirmacion=CONTRASENA):
        cuerpo = {"alias": alias, "contrasena": contrasena}
        if confirmacion is not None:
            cuerpo["confirmacion"] = confirmacion
        return self.client.post("/api/acceso", json=cuerpo)

    def cabeceras(self, alias="ana") -> dict:
        r = self.acceder(alias)
        assert r.status_code == 200, r.text
        return {"Authorization": f"Bearer {r.json()['token']}"}

    def cargar(self, cab, contenido=None, nombre="estudio.nii.gz", referencia=None):
        archivos = [("archivos", (nombre, nifti() if contenido is None else contenido))]
        if referencia is not None:
            archivos.append(("referencia", ("referencia.nii.gz", referencia)))
        return self.client.post("/api/estudios", files=archivos, headers=cab)

    def contar(self, modelo) -> int:
        with self.app.state.fabrica_sesiones() as s:
            return s.scalar(select(func.count()).select_from(modelo))

    def archivos(self) -> list[Archivo]:
        with self.app.state.fabrica_sesiones() as s:
            return list(s.scalars(select(Archivo).order_by(Archivo.id_archivo)))

    def nada_registrado(self) -> bool:
        guardados = [p for p in self.almacen.raiz.rglob("*") if p.is_file()]
        return self.contar(Estudio) == 0 and self.contar(Archivo) == 0 and not guardados

    def cerrar(self):
        self.client.close()
        self.app.state.motor.dispose()
