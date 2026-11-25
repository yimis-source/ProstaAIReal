"""Acceso a la base por tabla. Los repositorios hacen flush, no commit:
la ruta de la API confirma o revierte todo junto (estudio y archivos)."""
from prosta_ai.repositories.archivos import RepositorioArchivos
from prosta_ai.repositories.estudios import RepositorioEstudios, formato_codigo
from prosta_ai.repositories.usuarios import RepositorioUsuarios

__all__ = ["RepositorioArchivos", "RepositorioEstudios", "RepositorioUsuarios", "formato_codigo"]
