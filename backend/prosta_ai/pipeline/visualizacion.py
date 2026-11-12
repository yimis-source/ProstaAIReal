"""Imagen de la ROI: corte axial con la máscara superpuesta y el aviso no diagnóstico.

Trabaja sobre los NIfTI que deja la etapa ROI (`imagen.nii.gz` y `mascara.nii.gz`).
No depende de la aplicación web: el ciclo 6 reutilizará estos renderizadores para
servir los cortes al visor.

Patrones: Strategy para el tipo de capa (`SliceRenderer`) y Decorator para añadir el
aviso experimental a cualquier imagen exportada (`AvisoDecorator`, RF-15).
"""
from __future__ import annotations

import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import nibabel as nib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ..constantes import AVISO_EXPERIMENTAL

COLOR_ROI = (45, 212, 191)  # verde azulado (#2dd4bf) del diseño del visor
ALFA_ROI = 0.45
ANCHO_MINIMO_EXPORTAR = 512
COLOR_BANDA_AVISO = (20, 20, 20)

_RUTA_FUENTE = Path(__file__).resolve().parent.parent / "recursos" / "DejaVuSans.ttf"


def _fuente(tam: int) -> ImageFont.FreeTypeFont:
    """Fuente con tildes y eñes para el aviso; si falta, la de Pillow."""
    try:
        return ImageFont.truetype(str(_RUTA_FUENTE), tam)
    except OSError:
        return ImageFont.load_default(size=tam)


@dataclass
class VolumenCortes:
    imagen: np.ndarray  # uint8, orientación canónica RAS (x, y, z)
    mascara: np.ndarray | None  # bool, misma forma

    @property
    def forma(self) -> tuple[int, int, int]:
        return tuple(int(n) for n in self.imagen.shape)  # type: ignore[return-value]

    @property
    def cortes(self) -> int:
        return self.imagen.shape[2]


def _normalizar(datos: np.ndarray) -> np.ndarray:
    """Lleva la intensidad a 0-255 usando los percentiles 1 y 99."""
    p1, p99 = np.percentile(datos, [1, 99])
    if p99 <= p1:
        return np.zeros(datos.shape, dtype=np.uint8)
    return (np.clip((datos - p1) / (p99 - p1), 0, 1) * 255).astype(np.uint8)


def _leer(ruta: Path) -> np.ndarray:
    img = nib.as_closest_canonical(nib.load(str(ruta)))
    datos = np.asarray(img.get_fdata(dtype=np.float32))
    if datos.ndim == 4:
        datos = datos[..., 0]
    return datos


def cargar_volumen(ruta_imagen: Path, ruta_mascara: Path | None = None) -> VolumenCortes:
    """Lee la imagen y, si existe, la máscara (deben tener la misma forma)."""
    imagen = _normalizar(_leer(Path(ruta_imagen)))
    mascara = None
    if ruta_mascara is not None and Path(ruta_mascara).exists():
        mascara = _leer(Path(ruta_mascara)) > 0.5
        if mascara.shape != imagen.shape:
            raise ValueError("La máscara no tiene la misma forma que la imagen")
    return VolumenCortes(imagen, mascara)


def corte_representativo(vol: VolumenCortes) -> int:
    """Corte axial con más área de ROI; sin ROI, el corte central."""
    if vol.mascara is not None and vol.mascara.any():
        return int(np.argmax(vol.mascara.sum(axis=(0, 1))))
    return vol.cortes // 2


def _plano(arr2d: np.ndarray) -> np.ndarray:
    """Corte axial con la fila 0 arriba (y hacia arriba, x hacia la derecha)."""
    return np.rot90(arr2d)


class SliceRenderer(ABC):
    @abstractmethod
    def render(self, vol: VolumenCortes, indice: int) -> Image.Image: ...


class ImageSliceRenderer(SliceRenderer):
    """Corte en escala de grises, sin ROI."""

    def render(self, vol: VolumenCortes, indice: int) -> Image.Image:
        return Image.fromarray(_plano(vol.imagen[:, :, indice]), mode="L")


class MaskSliceRenderer(SliceRenderer):
    """RGBA transparente con la ROI en color."""

    def render(self, vol: VolumenCortes, indice: int) -> Image.Image:
        if vol.mascara is None:
            raise FileNotFoundError("No hay máscara")
        roi = _plano(vol.mascara[:, :, indice])
        rgba = np.zeros(roi.shape + (4,), dtype=np.uint8)
        rgba[roi] = (*COLOR_ROI, int(ALFA_ROI * 255))
        return Image.fromarray(rgba, mode="RGBA")


class OverlaySliceRenderer(SliceRenderer):
    """Imagen en gris con la ROI mezclada encima."""

    def render(self, vol: VolumenCortes, indice: int) -> Image.Image:
        base = Image.fromarray(_plano(vol.imagen[:, :, indice]), mode="L").convert("RGBA")
        if vol.mascara is not None:
            base = Image.alpha_composite(base, MaskSliceRenderer().render(vol, indice))
        return base.convert("RGB")


class AvisoDecorator(SliceRenderer):
    """Decorator: añade el aviso experimental impreso debajo de lo que dibuje el renderizador."""

    def __init__(self, renderer: SliceRenderer, aviso: str = AVISO_EXPERIMENTAL):
        self._renderer = renderer
        self._aviso = aviso

    def render(self, vol: VolumenCortes, indice: int) -> Image.Image:
        img = self._renderer.render(vol, indice).convert("RGB")
        factor = max(1, -(-ANCHO_MINIMO_EXPORTAR // img.width))
        if factor > 1:
            img = img.resize((img.width * factor, img.height * factor), Image.Resampling.BILINEAR)
        tam = max(12, img.width // 38)
        fuente = _fuente(tam)
        medidor = ImageDraw.Draw(img)
        max_chars = max(10, int(img.width / (tam * 0.55)))
        lineas = textwrap.wrap(self._aviso, width=max_chars)
        # reajusta el ancho de línea con la medida real de la fuente
        while len(lineas) > 1 and max(medidor.textlength(l, font=fuente) for l in lineas) > img.width - 20:
            max_chars -= 2
            lineas = textwrap.wrap(self._aviso, width=max_chars)
        alto_linea = int(tam * 1.3)
        pie = Image.new("RGB", (img.width, alto_linea * len(lineas) + 16), COLOR_BANDA_AVISO)
        dib = ImageDraw.Draw(pie)
        for i, linea in enumerate(lineas):
            dib.text((10, 8 + i * alto_linea), linea, fill=(255, 255, 255), font=fuente)
        lienzo = Image.new("RGB", (img.width, img.height + pie.height))
        lienzo.paste(img, (0, 0))
        lienzo.paste(pie, (0, img.height))
        return lienzo


def renderizador_exportacion() -> SliceRenderer:
    """Lo que se exporta siempre lleva el aviso (RF-15)."""
    return AvisoDecorator(OverlaySliceRenderer())


def guardar_imagen_roi(ruta_imagen: Path, ruta_mascara: Path, destino: Path, indice: int | None = None) -> int:
    """Escribe un PNG con el corte, la ROI superpuesta y el aviso. Devuelve el corte usado."""
    vol = cargar_volumen(ruta_imagen, ruta_mascara)
    k = corte_representativo(vol) if indice is None else indice
    if not 0 <= k < vol.cortes:
        raise IndexError(f"El corte {k} no existe; el volumen tiene {vol.cortes} cortes.")
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    renderizador_exportacion().render(vol, k).save(destino, format="PNG")
    return k
