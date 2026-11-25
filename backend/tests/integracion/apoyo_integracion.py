"""Apoyo de las pruebas de integración: PostgreSQL migrado con Alembic y almacenamiento temporal.

Los NIfTI se generan en cada prueba con nibabel; nunca se usan datos reales.
"""
import gzip
from pathlib import Path

import nibabel as nib
import numpy as np
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import func, inspect, select, text

from prosta_ai.api.app import create_app
from prosta_ai.config import Settings
from prosta_ai.models import Archivo, Estudio, Usuario

BACKEND = Path(__file__).resolve().parents[2]
CONTRASENA = "clave-segura-1"
# Texto que imita lo que un equipo de resonancia podría dejar en la cabecera
TEXTO_CABECERA = b"ficticio prueba 1708"


def config_alembic(url: str) -> Config:
    cfg = Config(str(BACKEND / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND / "migrations"))
    cfg.set_main_option("sqlalchemy.url", url)
    cfg.attributes["configurar_logs"] = False
    return cfg


def nifti(forma=(16, 16, 8), semilla=0, texto: bytes = TEXTO_CABECERA, comprimido=True,
          mascara=False) -> bytes:
    """Volumen sintético con texto libre en la cabecera (para comprobar RF-05)."""
    rng = np.random.default_rng(semilla)
    if mascara:
        datos = (rng.random(forma) > 0.7).astype(np.uint8)
    else:
        datos = rng.normal(100, 10, forma).astype(np.float32)
    imagen = nib.Nifti1Image(datos, np.eye(4))
    if texto:
        imagen.header["descrip"] = texto
        imagen.header["aux_file"] = texto[:23]
        imagen.header["intent_name"] = texto[:15]
        imagen.header["db_name"] = texto[:17]
    crudo = imagen.to_bytes()
    return gzip.compress(crudo) if comprimido else crudo


def leer_nifti(ruta: Path):
    datos = ruta.read_bytes()
    if ruta.name.endswith(".gz"):
        datos = gzip.decompress(datos)
    return nib.Nifti1Image.from_bytes(datos)


def leer_nifti_bytes(contenido: bytes):
    return nib.Nifti1Image.from_bytes(gzip.decompress(contenido))


class EntornoPostgres:
    """Base de pruebas migrada a head, API real y carpeta de almacenamiento temporal."""

    def __init__(self, url: str, tmp_path: Path):
        self.url = url
        self.cfg = config_alembic(url)
        # Por si una ejecución anterior se cortó sin limpiar
        command.downgrade(self.cfg, "base")
        command.upgrade(self.cfg, "head")
        self.settings = Settings(
            _env_file=None,
            database_url=url,
            storage_dir=tmp_path / "almacen",
            secret_key="clave-de-pruebas-integracion",
        )
        self.app = create_app(self.settings)
        self.motor = self.app.state.motor
        self.client = TestClient(self.app, raise_server_exceptions=False)
        self.almacen = self.app.state.almacenamiento

    # --- API ---

    def verificar(self, alias: str):
        return self.client.post("/api/acceso/verificar", json={"alias": alias})

    def acceder(self, alias: str, contrasena=CONTRASENA, confirmacion=None):
        cuerpo = {"alias": alias, "contrasena": contrasena}
        if confirmacion is not None:
            cuerpo["confirmacion"] = confirmacion
        return self.client.post("/api/acceso", json=cuerpo)

    def cabeceras(self, alias: str) -> dict:
        """Crea la cuenta si no existe e ingresa."""
        r = self.acceder(alias, confirmacion=CONTRASENA)
        assert r.status_code == 200, r.text
        return {"Authorization": f"Bearer {r.json()['token']}"}

    def cargar(self, cab, contenido=None, nombre="estudio.nii.gz", referencia=None,
               nombre_referencia="referencia.nii.gz"):
        archivos = [("archivos", (nombre, nifti() if contenido is None else contenido))]
        if referencia is not None:
            archivos.append(("referencia", (nombre_referencia, referencia)))
        return self.client.post("/api/estudios", files=archivos, headers=cab)

    def detalle(self, cab, id_estudio: int):
        return self.client.get(f"/api/estudios/{id_estudio}", headers=cab)

    # --- Base y disco ---

    def sesion(self):
        return self.app.state.fabrica_sesiones()

    def contar(self, modelo) -> int:
        with self.sesion() as s:
            return s.scalar(select(func.count()).select_from(modelo))

    def conteos(self) -> dict:
        return {m.__tablename__: self.contar(m) for m in (Usuario, Estudio, Archivo)}

    def estudio(self, id_estudio: int) -> Estudio:
        with self.sesion() as s:
            return s.get(Estudio, id_estudio)

    def archivos(self, id_estudio: int) -> list[Archivo]:
        with self.sesion() as s:
            return list(s.scalars(
                select(Archivo).where(Archivo.id_estudio == id_estudio)
                .order_by(Archivo.id_archivo)
            ))

    def texto_de_la_base(self) -> str:
        """Todo el contenido de las tablas de la aplicación como texto, para buscar fugas."""
        partes = []
        with self.motor.connect() as c:
            for tabla in inspect(c).get_table_names():
                for fila in c.execute(text(f'SELECT * FROM "{tabla}"')):
                    partes.append(" ".join(str(v) for v in fila))
        return "\n".join(partes)

    def version_alembic(self) -> str:
        with self.motor.connect() as c:
            return c.scalar(text("SELECT version_num FROM alembic_version"))

    def carpetas_de_estudios(self) -> set[str]:
        raiz = self.almacen.raiz / "estudios"
        return {p.name for p in raiz.iterdir()} if raiz.exists() else set()

    def archivos_en_disco(self) -> list[Path]:
        return sorted(p for p in self.almacen.raiz.rglob("*") if p.is_file())

    def cerrar(self):
        self.client.close()
        self.motor.dispose()
        command.downgrade(self.cfg, "base")
