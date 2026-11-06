"""Datos sintéticos de las pruebas del pipeline (sin red ni pesos reales)."""
from __future__ import annotations

import numpy as np

from prosta_ai.pipeline.segmentation import SegmentationStrategy


def esfera(shape=(48, 48, 16), centro=(24, 24, 8), radios=(10, 10, 5)) -> np.ndarray:
    """Volumen con una elipsoide brillante sobre fondo con algo de ruido."""
    rng = np.random.default_rng(0)
    x, y, z = np.indices(shape)
    d = sum(((c - o) / r) ** 2 for c, o, r in zip((x, y, z), centro, radios))
    img = rng.normal(100, 5, shape).astype(np.float32)
    img[d <= 1] += 400
    return img


class EstrategiaUmbral(SegmentationStrategy):
    """Estrategia falsa: umbraliza el volumen preparado."""

    name = "umbral"
    version = "test"
    weights_path = None

    def __init__(self, umbral: float = 0.0):
        self.umbral = umbral
        self.llamadas = 0

    def segment(self, prepared):
        self.llamadas += 1
        return (prepared.tensor[0].numpy() > self.umbral).astype(np.uint8)
