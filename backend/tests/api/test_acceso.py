"""CU01: verificación de alias, primer acceso, ingreso y token."""
import jwt

from prosta_ai.models import Usuario
from prosta_ai.seguridad import crear_token, hash_contrasena, verificar_contrasena

from apoyo_api import CONTRASENA


def test_hash_con_sal_y_verificacion():
    h1, h2 = hash_contrasena("una-clave-larga"), hash_contrasena("una-clave-larga")
    assert h1 != h2 and "una-clave-larga" not in h1
    assert verificar_contrasena("una-clave-larga", h1)
    assert not verificar_contrasena("otra-clave", h1)
    assert not verificar_contrasena("una-clave-larga", "no-es-un-hash")


def test_verificar_alias_inexistente_y_existente(entorno):
    r = entorno.client.post("/api/acceso/verificar", json={"alias": "ana"})
    assert r.status_code == 200 and r.json() == {"existe": False}
    entorno.acceder("ana")
    assert entorno.client.post("/api/acceso/verificar", json={"alias": "ana"}).json() == {
        "existe": True
    }


def test_verificar_alias_no_valido_da_422(entorno):
    r = entorno.client.post("/api/acceso/verificar", json={"alias": "a b"})
    assert r.status_code == 422
    assert r.json()["campos"] == ["alias"]


def test_primer_acceso_crea_cuenta_y_guarda_solo_hash(entorno):
    r = entorno.acceder("estudiante01")
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["alias"] == "estudiante01" and cuerpo["primer_acceso"] is True
    datos = jwt.decode(cuerpo["token"], "clave-de-pruebas", algorithms=["HS256"])
    assert datos["alias"] == "estudiante01"
    assert datos["exp"] - datos["iat"] == 8 * 3600
    with entorno.app.state.fabrica_sesiones() as s:
        usuario = s.query(Usuario).one()
        assert usuario.hash_contrasena != CONTRASENA
        assert verificar_contrasena(CONTRASENA, usuario.hash_contrasena)


def test_ingreso_posterior(entorno):
    entorno.acceder("ana")
    r = entorno.acceder("ana", confirmacion=None)
    assert r.status_code == 200
    assert r.json()["primer_acceso"] is False


def test_contrasena_incorrecta_da_401(entorno):
    entorno.acceder("ana")
    r = entorno.acceder("ana", contrasena="otra-clave-9", confirmacion=None)
    assert r.status_code == 401
    assert r.json() == {"detalle": "Alias o contraseña incorrectos."}


def test_primer_acceso_contrasena_corta_o_sin_confirmar(entorno):
    r = entorno.acceder("ana", contrasena="corta", confirmacion="corta")
    assert r.status_code == 422 and "8 caracteres" in r.json()["detalle"]
    r = entorno.acceder("ana", confirmacion="otra-cosa-123")
    assert r.status_code == 422 and "confirmación" in r.json()["detalle"]
    r = entorno.acceder("ana", confirmacion=None)
    assert r.status_code == 422
    assert entorno.contar(Usuario) == 0


def test_json_mal_formado_no_lista_posiciones(entorno):
    r = entorno.client.post(
        "/api/acceso", content=b'{"alias": "ana",', headers={"Content-Type": "application/json"}
    )
    assert r.status_code == 422
    assert r.json()["detalle"] == "Datos no válidos."
    assert all(not c.isdigit() for c in r.json()["campos"])


def test_ruta_protegida_sin_token_da_401(entorno):
    r = entorno.client.get("/api/estudios/1")
    assert r.status_code == 401
    assert r.json()["detalle"] == "Sesión no válida o vencida. Ingrese de nuevo."
    assert entorno.client.post("/api/estudios").status_code == 401


def test_token_alterado_o_vencido_da_401(entorno):
    entorno.acceder("ana")
    vencido = crear_token(1, "ana", "clave-de-pruebas", -1)
    otra_clave = crear_token(1, "ana", "otra-clave", 8)
    for token in (vencido, otra_clave, "no-es-un-token"):
        r = entorno.client.get("/api/estudios/1", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 401, token
