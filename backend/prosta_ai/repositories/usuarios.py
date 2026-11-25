"""Usuarios (CU01): solo alias y hash de la contraseña."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from prosta_ai.models import Usuario


class RepositorioUsuarios:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    def crear(self, alias: str, hash_contrasena: str) -> Usuario:
        """Recibe el hash ya calculado (bcrypt, 1705), nunca la contraseña."""
        usuario = Usuario(alias=alias, hash_contrasena=hash_contrasena)
        self.sesion.add(usuario)
        self.sesion.flush()
        return usuario

    def por_alias(self, alias: str) -> Usuario | None:
        return self.sesion.scalar(select(Usuario).where(Usuario.alias == alias))

    def obtener(self, id_usuario: int) -> Usuario | None:
        return self.sesion.get(Usuario, id_usuario)
