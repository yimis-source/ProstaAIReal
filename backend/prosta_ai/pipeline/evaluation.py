"""Métricas de comparación entre la máscara obtenida y la referencia."""
from __future__ import annotations

import numpy as np
from scipy.ndimage import binary_erosion, distance_transform_edt


def _binarias(pred: np.ndarray, ref: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray(pred) > 0
    r = np.asarray(ref) > 0
    if p.shape != r.shape:
        raise ValueError(f"Las máscaras tienen formas distintas: {p.shape} y {r.shape}")
    return p, r


def dice(pred: np.ndarray, ref: np.ndarray) -> float:
    """Coeficiente de Dice entre dos máscaras binarias. Ambas vacías -> 1.0."""
    p, r = _binarias(pred, ref)
    total = int(p.sum()) + int(r.sum())
    if total == 0:
        return 1.0
    return float(2.0 * np.logical_and(p, r).sum() / total)


def iou(pred: np.ndarray, ref: np.ndarray) -> float:
    """Índice de Jaccard (IoU) entre dos máscaras binarias. Ambas vacías -> 1.0."""
    p, r = _binarias(pred, ref)
    union = int(np.logical_or(p, r).sum())
    if union == 0:
        return 1.0
    return float(np.logical_and(p, r).sum() / union)


def _superficie(mask: np.ndarray) -> np.ndarray:
    """Extrae la superficie de una máscara binaria en cualquier dimensión."""
    return np.logical_and(mask, np.logical_not(binary_erosion(mask, border_value=0)))


def _distancias_superficie(
    pred: np.ndarray,
    ref: np.ndarray,
    spacing: tuple[float, ...] | None = None,
) -> np.ndarray:
    """Distancias simétricas entre superficies, en unidades de ``spacing``."""
    p, r = _binarias(pred, ref)
    if spacing is not None:
        spacing = tuple(float(s) for s in spacing)
        if len(spacing) != p.ndim or any(not np.isfinite(s) or s <= 0 for s in spacing):
            raise ValueError("spacing debe contener un valor positivo y finito por dimensión")

    if not p.any() and not r.any():
        return np.array([0.0])
    if not p.any() or not r.any():
        return np.array([np.inf])

    sup_p, sup_r = _superficie(p), _superficie(r)
    dist_a_r = distance_transform_edt(~sup_r, sampling=spacing)
    dist_a_p = distance_transform_edt(~sup_p, sampling=spacing)
    return np.concatenate((dist_a_r[sup_p], dist_a_p[sup_r]))


def hd95(
    pred: np.ndarray,
    ref: np.ndarray,
    spacing: tuple[float, ...] | None = None,
) -> float:
    """HD95 simétrica; con spacing se expresa en unidades físicas (p. ej. mm).

    Dos máscaras vacías producen 0; si solo una está vacía, produce infinito.
    """
    return float(np.percentile(_distancias_superficie(pred, ref, spacing), 95))


def distancia_media_superficie(
    pred: np.ndarray,
    ref: np.ndarray,
    spacing: tuple[float, ...] | None = None,
) -> float:
    """Distancia media simétrica entre superficies, en unidades de spacing.

    Dos máscaras vacías producen 0; si solo una está vacía, produce infinito.
    """
    return float(np.mean(_distancias_superficie(pred, ref, spacing)))
