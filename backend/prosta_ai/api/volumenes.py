"""Caché pequeño de volúmenes de resultado (CU04).

Mover el deslizador del visor pide un corte tras otro del mismo trabajo: el NIfTI
se lee una vez y se guarda en memoria. Solo se guardan los últimos trabajos vistos.
"""
from __future__ import annotations

import threading
from collections import OrderedDict
from pathlib import Path

from prosta_ai.pipeline.visualizacion import VolumenCortes, cargar_volumen

MAX_VOLUMENES = 4


class CacheVolumenes:
    def __init__(self, maximo: int = MAX_VOLUMENES):
        self._maximo = maximo
        self._datos: OrderedDict[tuple, VolumenCortes] = OrderedDict()
        self._candado = threading.Lock()

    def obtener(self, id_trabajo: int, ruta_imagen: Path, ruta_mascara: Path | None) -> VolumenCortes:
        # La ruta va en la clave: un trabajo con el mismo id en otra base no choca
        clave = (id_trabajo, str(ruta_imagen), str(ruta_mascara))
        with self._candado:
            if clave in self._datos:
                self._datos.move_to_end(clave)
                return self._datos[clave]
        vol = cargar_volumen(ruta_imagen, ruta_mascara)
        with self._candado:
            self._datos[clave] = vol
            self._datos.move_to_end(clave)
            while len(self._datos) > self._maximo:
                self._datos.popitem(last=False)
        return vol

    def __len__(self) -> int:
        return len(self._datos)
