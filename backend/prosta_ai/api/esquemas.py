"""Cuerpos JSON de entrada de la API."""
from pydantic import BaseModel, Field

# 3 a 30 caracteres: letras sin tilde, números, «_», «.» o «-» (contrato 4.2)
ALIAS_PATRON = r"^[A-Za-z0-9_.-]{3,30}$"


class AliasEntrada(BaseModel):
    alias: str = Field(pattern=ALIAS_PATRON)


class AccesoEntrada(BaseModel):
    alias: str = Field(pattern=ALIAS_PATRON)
    contrasena: str = Field(min_length=1, max_length=128)
    # Solo en el primer acceso
    confirmacion: str | None = Field(default=None, max_length=128)
