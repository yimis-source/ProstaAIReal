"""Contraseñas con bcrypt y token de acceso firmado (JWT HS256) para CU01."""
from datetime import timedelta

import bcrypt
import jwt

from prosta_ai.db import ahora

ALGORITMO = "HS256"
# Costo de bcrypt; las pruebas lo bajan para ir más rápido
ROUNDS = 12
# bcrypt solo toma en cuenta los primeros 72 bytes
_MAX_BYTES = 72


class TokenNoValido(Exception):
    """Token ausente, alterado o vencido."""


def _bytes(contrasena: str) -> bytes:
    return contrasena.encode("utf-8")[:_MAX_BYTES]


def hash_contrasena(contrasena: str) -> str:
    """Hash con sal; es lo único que se guarda de la contraseña."""
    return bcrypt.hashpw(_bytes(contrasena), bcrypt.gensalt(rounds=ROUNDS)).decode("ascii")


def verificar_contrasena(contrasena: str, hash_guardado: str) -> bool:
    try:
        return bcrypt.checkpw(_bytes(contrasena), hash_guardado.encode("ascii"))
    except ValueError:
        # Hash guardado con formato no reconocido
        return False


def crear_token(id_usuario: int, alias: str, clave: str, horas: int) -> str:
    momento = ahora()
    datos = {
        "sub": str(id_usuario),
        "alias": alias,
        "iat": momento,
        "exp": momento + timedelta(hours=horas),
    }
    return jwt.encode(datos, clave, algorithm=ALGORITMO)


def leer_token(token: str, clave: str) -> dict:
    """Devuelve el contenido del token o lanza TokenNoValido."""
    try:
        return jwt.decode(token, clave, algorithms=[ALGORITMO], options={"require": ["sub", "exp"]})
    except jwt.PyJWTError as exc:
        raise TokenNoValido(str(exc)) from exc
