"""ServicioProcesamiento con un pipeline falso inyectado (no carga el modelo)."""
import pytest
from sqlalchemy import func, select

from apoyo_procesamiento import INFO_FALSA, PipelineFalso, ProveedorFalso
from prosta_ai.constantes import (
    MENSAJE_ERROR_GENERICO, MENSAJE_INTERRUMPIDO, MENSAJE_MODELO,
)
from prosta_ai.models import Modelo, Resultado, Trabajo
from prosta_ai.pipeline import stages
from prosta_ai.pipeline.errors import StageError
from prosta_ai.pipeline.stages import STAGES
from prosta_ai.processing import ServicioProcesamiento
from prosta_ai.repositories import RepositorioTrabajos, TransicionNoValida


def _trabajo(fabrica, id_trabajo) -> Trabajo:
    with fabrica() as s:
        trabajo = s.get(Trabajo, id_trabajo)
        trabajo.etapas, trabajo.resultado, trabajo.estudio  # cargar antes de cerrar
        return trabajo


def _estados(trabajo) -> dict:
    return {e.nombre: e.estado for e in trabajo.etapas}


def _carpeta(almacen, trabajo):
    return almacen.carpeta_trabajo(trabajo.estudio.codigo_anonimo, trabajo.id_trabajo)


def test_caso_completo(fabrica, almacen, servicio, crear_trabajo):
    id_trabajo = crear_trabajo()
    servicio.procesar(id_trabajo)

    trabajo = _trabajo(fabrica, id_trabajo)
    assert trabajo.estado == "completado", (trabajo.etapa_fallida, trabajo.mensaje_error)
    assert trabajo.fecha_inicio is not None and trabajo.fecha_fin is not None
    assert trabajo.etapa_fallida is None and trabajo.mensaje_error is None
    assert [e.nombre for e in trabajo.etapas] == STAGES
    for etapa in trabajo.etapas:
        assert etapa.estado == "completado"
        assert etapa.fecha_inicio is not None and etapa.fecha_fin is not None
        assert etapa.duracion_s is not None and 0 <= etapa.duracion_s < 60  # segundos

    r = trabajo.resultado
    assert float(r.dice) == 1.0 and float(r.iou) == 1.0
    assert r.tiempo_total_s is not None
    base = f"estudios/EST-0001/trabajo-{id_trabajo}"
    assert (r.ruta_imagen, r.ruta_mascara, r.ruta_roi) == (
        f"{base}/volumen.nii.gz", f"{base}/mascara.nii.gz", f"{base}/roi.png"
    )
    for ruta in (r.ruta_imagen, r.ruta_mascara, r.ruta_roi):
        assert almacen.absoluta(ruta).is_file()
    # La carpeta temporal del pipeline no queda
    assert not any((almacen.raiz / "tmp").iterdir())


def test_sin_referencia_dice_e_iou_nulos(fabrica, servicio, crear_trabajo):
    id_trabajo = crear_trabajo(con_referencia=False)
    servicio.procesar(id_trabajo)
    trabajo = _trabajo(fabrica, id_trabajo)
    assert trabajo.estado == "completado", (trabajo.etapa_fallida, trabajo.mensaje_error)
    assert trabajo.resultado.dice is None and trabajo.resultado.iou is None


def test_fallo_en_una_etapa(fabrica, almacen, crear_trabajo):
    error = StageError(stages.PREPARACION, "El volumen no tiene el espaciado esperado.")
    servicio = ServicioProcesamiento(
        fabrica, almacen, ProveedorFalso(PipelineFalso(stages.PREPARACION, error))
    )
    id_trabajo = crear_trabajo()
    servicio.procesar(id_trabajo)

    trabajo = _trabajo(fabrica, id_trabajo)
    assert trabajo.estado == "fallido"
    assert trabajo.etapa_fallida == stages.PREPARACION
    assert trabajo.mensaje_error == "El volumen no tiene el espaciado esperado."
    assert _estados(trabajo) == {
        stages.CONTROL_CALIDAD: "completado", stages.PREPARACION: "fallido",
        stages.SEGMENTACION: "pendiente", stages.ROI: "pendiente", stages.EVALUACION: "pendiente",
    }
    assert trabajo.resultado is None
    assert not _carpeta(almacen, trabajo).exists()


def _admision(fabrica, id_trabajo) -> str:
    with fabrica() as s:
        return s.get(Trabajo, id_trabajo).estudio.estado_admision


def test_fallo_en_control_de_calidad_deja_el_estudio_no_compatible(fabrica, almacen, crear_trabajo):
    error = StageError(stages.CONTROL_CALIDAD, "El volumen no es tridimensional.")
    servicio = ServicioProcesamiento(
        fabrica, almacen, ProveedorFalso(PipelineFalso(stages.CONTROL_CALIDAD, error))
    )
    id_trabajo = crear_trabajo()
    servicio.procesar(id_trabajo)

    trabajo = _trabajo(fabrica, id_trabajo)
    assert trabajo.estado == "fallido"
    assert trabajo.etapa_fallida == stages.CONTROL_CALIDAD
    assert trabajo.mensaje_error == "El volumen no es tridimensional."
    assert _admision(fabrica, id_trabajo) == "no compatible", (
        "el control de calidad falló y el estudio sigue admitido"
    )


@pytest.mark.parametrize("etapa", [stages.PREPARACION, stages.SEGMENTACION, stages.ROI,
                                   stages.EVALUACION])
def test_fallo_en_otra_etapa_no_cambia_la_admision(fabrica, almacen, crear_trabajo, etapa):
    servicio = ServicioProcesamiento(fabrica, almacen, ProveedorFalso(PipelineFalso(etapa)))
    id_trabajo = crear_trabajo()
    servicio.procesar(id_trabajo)
    assert _trabajo(fabrica, id_trabajo).estado == "fallido"
    assert _admision(fabrica, id_trabajo) == "admitido"


def test_modelo_que_no_carga_no_cambia_la_admision(fabrica, almacen, crear_trabajo):
    servicio = ServicioProcesamiento(
        fabrica, almacen, ProveedorFalso(error_al_construir=OSError("sin pesos"))
    )
    id_trabajo = crear_trabajo()
    servicio.procesar(id_trabajo)
    assert _trabajo(fabrica, id_trabajo).estado == "fallido"
    assert _admision(fabrica, id_trabajo) == "admitido"


def test_fallo_inesperado_no_muestra_datos_internos(fabrica, almacen, crear_trabajo):
    error = RuntimeError("CUDA out of memory en /home/servidor/modelos/model.pt")
    servicio = ServicioProcesamiento(
        fabrica, almacen, ProveedorFalso(PipelineFalso(stages.SEGMENTACION, error))
    )
    id_trabajo = crear_trabajo()
    servicio.procesar(id_trabajo)

    trabajo = _trabajo(fabrica, id_trabajo)
    assert trabajo.estado == "fallido"
    assert trabajo.etapa_fallida == stages.SEGMENTACION
    assert "CUDA" not in trabajo.mensaje_error and "/home" not in trabajo.mensaje_error
    assert trabajo.mensaje_error == "Ocurrió un error inesperado durante esta etapa."
    assert _estados(trabajo)[stages.SEGMENTACION] == "fallido"
    assert _estados(trabajo)[stages.ROI] == "pendiente"


def test_fallo_al_guardar_no_deja_salidas_a_medias(fabrica, almacen, servicio, crear_trabajo,
                                                    monkeypatch):
    original = almacen.guardar_salida
    llamadas = []

    def guardar_y_fallar(codigo, id_trabajo, rol, origen):
        llamadas.append(rol)
        if len(llamadas) == 2:
            raise OSError("disco lleno en /var/almacenamiento")
        return original(codigo, id_trabajo, rol, origen)

    monkeypatch.setattr(almacen, "guardar_salida", guardar_y_fallar)
    id_trabajo = crear_trabajo()
    servicio.procesar(id_trabajo)

    trabajo = _trabajo(fabrica, id_trabajo)
    assert trabajo.estado == "fallido"
    assert trabajo.mensaje_error == MENSAJE_ERROR_GENERICO
    assert trabajo.resultado is None
    assert not _carpeta(almacen, trabajo).exists()


def test_modelo_que_no_carga(fabrica, almacen, crear_trabajo):
    proveedor = ProveedorFalso(error_al_construir=FileNotFoundError("/ruta/model.pt"))
    servicio = ServicioProcesamiento(fabrica, almacen, proveedor)
    id_trabajo = crear_trabajo()
    servicio.procesar(id_trabajo)
    trabajo = _trabajo(fabrica, id_trabajo)
    assert trabajo.estado == "fallido"
    assert trabajo.etapa_fallida == stages.SEGMENTACION
    assert trabajo.mensaje_error == MENSAJE_MODELO


def test_recuperar_interrumpidos(fabrica, almacen, servicio, crear_trabajo):
    interrumpido, pendiente = crear_trabajo(), crear_trabajo()
    with fabrica() as s:
        repo = RepositorioTrabajos(s)
        repo.iniciar(repo.obtener(interrumpido))
        repo.etapa(interrumpido, stages.CONTROL_CALIDAD).estado = "completado"
        repo.etapa(interrumpido, stages.PREPARACION).estado = "en proceso"
        s.commit()
    trabajo = _trabajo(fabrica, interrumpido)
    parcial = _carpeta(almacen, trabajo) / "volumen.nii.gz"
    parcial.parent.mkdir(parents=True)
    parcial.write_bytes(b"a medias")

    assert servicio.recuperar_interrumpidos() == 1

    trabajo = _trabajo(fabrica, interrumpido)
    assert trabajo.estado == "fallido"
    assert trabajo.mensaje_error == MENSAJE_INTERRUMPIDO
    assert trabajo.etapa_fallida == stages.PREPARACION
    assert _estados(trabajo)[stages.PREPARACION] == "fallido"
    assert not parcial.parent.exists()
    assert _trabajo(fabrica, pendiente).estado == "pendiente"
    assert servicio.recuperar_interrumpidos() == 0


def test_modelo_se_registra_una_sola_vez(fabrica, almacen, proveedor, servicio, crear_trabajo):
    a, b = crear_trabajo(), crear_trabajo()
    assert servicio.id_modelo_activo() == servicio.id_modelo_activo()
    assert proveedor.llamadas_info == 1
    # Otro arranque del backend con el mismo modelo reutiliza la fila
    otro = ServicioProcesamiento(fabrica, almacen, ProveedorFalso())
    assert otro.id_modelo_activo() == servicio.id_modelo_activo()
    with fabrica() as s:
        assert s.scalar(select(func.count()).select_from(Modelo)) == 1
        modelo = s.scalar(select(Modelo))
        assert (modelo.nombre, modelo.version, modelo.hash_pesos) == (
            INFO_FALSA["nombre"], INFO_FALSA["version"], INFO_FALSA["hash_pesos"]
        )
    assert _trabajo(fabrica, a).id_modelo == _trabajo(fabrica, b).id_modelo == modelo.id_modelo


def test_procesar_siguiente_en_orden(fabrica, servicio, crear_trabajo):
    primero, segundo = crear_trabajo(), crear_trabajo()
    assert servicio.procesar_siguiente() is True
    assert _trabajo(fabrica, primero).estado == "completado"
    assert _trabajo(fabrica, segundo).estado == "pendiente"
    assert servicio.procesar_siguiente() is True
    assert servicio.procesar_siguiente() is False
    with fabrica() as s:
        assert s.scalar(select(func.count()).select_from(Resultado)) == 2


def test_no_procesa_dos_veces(fabrica, servicio, crear_trabajo):
    id_trabajo = crear_trabajo()
    servicio.procesar(id_trabajo)
    with pytest.raises(TransicionNoValida):
        servicio.procesar(id_trabajo)
    with pytest.raises(LookupError):
        servicio.procesar(999)
