"""Procesamiento de trabajos: une la base de datos, el almacenamiento y el pipeline."""
from prosta_ai.processing.service import (
    ObservadorEtapas, ProveedorPipeline, ServicioProcesamiento,
)

__all__ = ["ObservadorEtapas", "ProveedorPipeline", "ServicioProcesamiento"]
