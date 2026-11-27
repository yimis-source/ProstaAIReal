"""CU05 (RF-19): GET /api/estudios lista solo los estudios del usuario, el más reciente primero."""
from datetime import datetime, timedelta, timezone

from apoyo_procesamiento import referencia_nifti, volumen_nifti
from prosta_ai.models import Estudio

CAMPOS = {"id", "codigo", "formato", "fecha_carga", "estado", "id_ultimo_trabajo", "dice", "iou"}


def _historial(entorno, cab):
    return entorno.client.get("/api/estudios", headers=cab)


def _cargar(entorno, cab, referencia=False) -> int:
    r = entorno.cargar(cab, volumen_nifti(), referencia=referencia_nifti() if referencia else None)
    assert r.status_code == 201, r.text
    return r.json()["id"]


def _fijar_fecha(entorno, id_estudio, fecha):
    with entorno.app.state.fabrica_sesiones() as s:
        s.get(Estudio, id_estudio).fecha_carga = fecha
        s.commit()


def test_sin_estudios_devuelve_lista_vacia(entorno):
    r = _historial(entorno, entorno.cabeceras())
    assert r.status_code == 200
    assert r.json() == []


def test_varios_estudios_del_mas_reciente_al_mas_antiguo(entorno):
    cab = entorno.cabeceras()
    ids = [_cargar(entorno, cab) for _ in range(3)]
    # El segundo es el más reciente y el tercero el más antiguo
    base = datetime(2026, 11, 26, 15, 0, tzinfo=timezone.utc)
    for id_estudio, minutos in zip(ids, (10, 20, 0)):
        _fijar_fecha(entorno, id_estudio, base + timedelta(minutes=minutos))

    r = _historial(entorno, cab)
    assert r.status_code == 200
    filas = r.json()
    assert [f["id"] for f in filas] == [ids[1], ids[0], ids[2]]
    assert all(set(f) == CAMPOS for f in filas)
    assert [f["codigo"] for f in filas] == ["EST-0002", "EST-0001", "EST-0003"]
    assert {f["formato"] for f in filas} == {"NIfTI"}
    assert filas[0]["fecha_carga"].startswith("2026-11-26T15:20:00")
    assert {f["estado"] for f in filas} == {"listo para procesar"}
    assert {f["id_ultimo_trabajo"] for f in filas} == {None}


def test_misma_fecha_de_carga_ordena_por_el_ultimo_cargado(entorno):
    cab = entorno.cabeceras()
    ids = [_cargar(entorno, cab) for _ in range(2)]
    fecha = datetime(2026, 11, 26, 15, 0, tzinfo=timezone.utc)
    for id_estudio in ids:
        _fijar_fecha(entorno, id_estudio, fecha)
    assert [f["id"] for f in _historial(entorno, cab).json()] == ids[::-1]


def test_estado_visible_ultimo_trabajo_y_dice(entorno):
    cab = entorno.cabeceras()
    procesado = _cargar(entorno, cab, referencia=True)
    pendiente = _cargar(entorno, cab)
    sin_procesar = _cargar(entorno, cab)
    r = entorno.client.post(f"/api/estudios/{procesado}/procesar", headers=cab)
    id_trabajo = r.json()["id"]
    assert entorno.servicio.procesar_siguiente() is True
    id_pendiente = entorno.client.post(
        f"/api/estudios/{pendiente}/procesar", headers=cab
    ).json()["id"]

    filas = {f["id"]: f for f in _historial(entorno, cab).json()}
    assert filas[procesado]["estado"] == "completado"
    assert filas[procesado]["id_ultimo_trabajo"] == id_trabajo
    assert 0 <= filas[procesado]["dice"] <= 1 and 0 <= filas[procesado]["iou"] <= 1
    # Coincide con el detalle del estudio (contrato 4.5)
    detalle = entorno.client.get(f"/api/estudios/{procesado}", headers=cab).json()
    assert {k: detalle[k] for k in CAMPOS} == filas[procesado]
    assert filas[pendiente]["estado"] == "pendiente"
    assert filas[pendiente]["id_ultimo_trabajo"] == id_pendiente
    assert filas[pendiente]["dice"] is None and filas[pendiente]["iou"] is None
    assert filas[sin_procesar]["estado"] == "listo para procesar"


def test_no_muestra_estudios_de_otros_usuarios(entorno):
    cab_ana, cab_luis = entorno.cabeceras("ana"), entorno.cabeceras("luis")
    de_ana = _cargar(entorno, cab_ana)
    de_luis = [_cargar(entorno, cab_luis) for _ in range(2)]
    assert [f["id"] for f in _historial(entorno, cab_ana).json()] == [de_ana]
    assert sorted(f["id"] for f in _historial(entorno, cab_luis).json()) == de_luis
    assert _historial(entorno, entorno.cabeceras("eva")).json() == []


def test_sin_token_da_401(entorno):
    r = entorno.client.get("/api/estudios")
    assert r.status_code == 401
    assert r.json() == {"detalle": "Sesión no válida o vencida. Ingrese de nuevo."}


def test_token_alterado_da_401(entorno):
    r = _historial(entorno, {"Authorization": "Bearer no-es-un-token"})
    assert r.status_code == 401
