"""Procesa un caso real con el modelo preentrenado (solo si están los pesos y el caso).

PROSTA_TEST_MODELO_DIR=<carpeta de modelos> PROSTA_TEST_CASO=<imagen .nii.gz>
La referencia se busca en PROSTA_TEST_REFERENCIA o, si no, en ../labelsTr/<mismo nombre>.
"""
import os
import time
from pathlib import Path

import pytest

from prosta_ai.models import Trabajo
from prosta_ai.processing import ProveedorPipeline

MODELO_DIR = os.environ.get("PROSTA_TEST_MODELO_DIR")
CASO = os.environ.get("PROSTA_TEST_CASO")

pytestmark = pytest.mark.skipif(
    not (MODELO_DIR and CASO and Path(CASO).is_file() and Path(MODELO_DIR).is_dir()),
    reason="sin PROSTA_TEST_MODELO_DIR y PROSTA_TEST_CASO (pesos y caso reales)",
)


def _referencia(caso: Path) -> Path | None:
    if os.environ.get("PROSTA_TEST_REFERENCIA"):
        return Path(os.environ["PROSTA_TEST_REFERENCIA"])
    candidata = caso.parent.parent / "labelsTr" / caso.name
    return candidata if candidata.is_file() else None


@pytest.fixture
def proveedor():
    # Sustituye al proveedor falso de conftest: aquí se usa el modelo de verdad
    return ProveedorPipeline("prostate_mri_anatomy", Path(MODELO_DIR))


def test_procesa_caso_real(fabrica, servicio, crear_trabajo):
    caso = Path(CASO)
    ref = _referencia(caso)
    id_trabajo = crear_trabajo(
        con_referencia=ref is not None, imagen=caso.read_bytes(),
        referencia=ref.read_bytes() if ref is not None else None,
    )

    inicio = time.perf_counter()
    servicio.procesar(id_trabajo)
    segundos = time.perf_counter() - inicio

    with fabrica() as s:
        trabajo = s.get(Trabajo, id_trabajo)
        assert trabajo.estado == "completado", trabajo.mensaje_error
        r = trabajo.resultado
        print(f"\n{caso.name}: Dice={r.dice} IoU={r.iou} tiempo={segundos:.1f} s "
              f"etapas={[(e.nombre, float(e.duracion_s)) for e in trabajo.etapas]}")
        assert trabajo.modelo.hash_pesos is not None
        if ref is not None:
            assert float(r.dice) > 0.7
