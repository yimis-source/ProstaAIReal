"""Servicio de procesamiento (Facade): corre un trabajo y deja su avance en la base.

Uso desde la tarea en segundo plano (1709):
    servicio = ServicioProcesamiento(fabrica_sesiones, almacenamiento, ProveedorPipeline(...))
    servicio.recuperar_interrumpidos()   # al arrancar
    while servicio.procesar_siguiente(): ...
"""
from __future__ import annotations

import logging
import time
from decimal import Decimal
from pathlib import Path
from typing import Any, Protocol

from sqlalchemy.orm import Session, sessionmaker

from prosta_ai.constantes import (
    COMPLETADO, EN_PROCESO, FALLIDO, MENSAJE_ERROR_GENERICO, MENSAJE_INTERRUMPIDO, MENSAJE_MODELO,
    NO_COMPATIBLE,
)
from prosta_ai.db import ahora
from prosta_ai.pipeline.base import PipelineInput
from prosta_ai.pipeline.errors import StageError
from prosta_ai.pipeline.progress import PipelineProgress
from prosta_ai.pipeline.stages import CONTROL_CALIDAD, SEGMENTACION
from prosta_ai.repositories import (
    RepositorioArchivos, RepositorioModelos, RepositorioResultados, RepositorioTrabajos,
)
from prosta_ai.storage import AlmacenamientoPrivado, rol_de_ruta

log = logging.getLogger(__name__)


class Proveedor(Protocol):
    """Lo que el servicio necesita del pipeline: construirlo y describir el modelo."""

    def pipeline(self) -> Any: ...

    def info(self) -> dict: ...


class ProveedorPipeline:
    """Proveedor real: construye el pipeline una sola vez (los pesos se leen al primer uso)."""

    def __init__(self, nombre_modelo: str, carpeta_modelo: Path):
        self.nombre_modelo = nombre_modelo
        self.carpeta_modelo = Path(carpeta_modelo)
        self._pipeline = None
        self._info: dict | None = None

    @classmethod
    def desde_ajustes(cls, settings) -> "ProveedorPipeline":
        return cls(settings.modelo_nombre, settings.modelo_dir)

    def pipeline(self):
        if self._pipeline is None:
            from prosta_ai.pipeline.factory import build_pipeline

            self._pipeline = build_pipeline(self.nombre_modelo, self.carpeta_modelo)
        return self._pipeline

    def info(self) -> dict:
        if self._info is None:
            from prosta_ai.pipeline.factory import model_info

            self._info = model_info(self.nombre_modelo, self.carpeta_modelo)
        return self._info


class ObservadorEtapas:
    """Observer del pipeline: escribe en etapa_trabajo el avance de cada etapa."""

    def __init__(self, fabrica_sesiones: sessionmaker[Session], id_trabajo: int):
        self._fabrica = fabrica_sesiones
        self._id = id_trabajo

    def on_stage_start(self, stage: str) -> None:
        with self._fabrica() as s:
            etapa = RepositorioTrabajos(s).etapa(self._id, stage)
            if etapa is not None:
                etapa.estado, etapa.fecha_inicio = EN_PROCESO, ahora()
                s.commit()

    def on_stage_end(self, stage: str, duration_s: float) -> None:
        with self._fabrica() as s:
            etapa = RepositorioTrabajos(s).etapa(self._id, stage)
            if etapa is not None:
                etapa.estado, etapa.fecha_fin = COMPLETADO, ahora()
                etapa.duracion_s = Decimal(str(round(duration_s, 2)))
                s.commit()

    def on_stage_failed(self, stage: str, message: str) -> None:
        with self._fabrica() as s:
            etapa = RepositorioTrabajos(s).etapa(self._id, stage)
            if etapa is not None:
                etapa.estado, etapa.fecha_fin = FALLIDO, ahora()
                s.commit()


class ServicioProcesamiento:
    def __init__(
        self, fabrica_sesiones: sessionmaker[Session], almacenamiento: AlmacenamientoPrivado,
        proveedor_pipeline: Proveedor,
    ):
        self._fabrica = fabrica_sesiones
        self._almacen = almacenamiento
        self._proveedor = proveedor_pipeline
        self._id_modelo: int | None = None

    # --- modelo ---
    def id_modelo_activo(self) -> int:
        """Registra el modelo en la tabla modelo la primera vez y guarda su id."""
        if self._id_modelo is None:
            with self._fabrica() as s:
                modelo = RepositorioModelos(s).registrar(self._proveedor.info())
                s.commit()
                self._id_modelo = modelo.id_modelo
        return self._id_modelo

    # --- cola ---
    def recuperar_interrumpidos(self) -> int:
        """Al arrancar: los «en proceso» de un cierre anterior quedan fallidos y sin salidas."""
        with self._fabrica() as s:
            trabajos = RepositorioTrabajos(s).recuperar_interrumpidos(MENSAJE_INTERRUMPIDO)
            pares = [(t.estudio.codigo_anonimo, t.id_trabajo) for t in trabajos]
            s.commit()
        for codigo, id_trabajo in pares:
            self._almacen.borrar_salidas(codigo, id_trabajo)
        return len(pares)

    def procesar_siguiente(self) -> bool:
        """Procesa el pendiente más antiguo; False si no había ninguno.

        Se marca «en proceso» y se confirma en la misma transacción que tomó el bloqueo
        (FOR UPDATE SKIP LOCKED): otro proceso no puede tomar el mismo trabajo.
        """
        with self._fabrica() as s:
            repo = RepositorioTrabajos(s)
            trabajo = repo.siguiente_pendiente()
            if trabajo is None:
                return False
            repo.iniciar(trabajo)
            id_trabajo = trabajo.id_trabajo
            s.commit()
        self._ejecutar(id_trabajo)
        return True

    # --- ejecución ---
    def procesar(self, id_trabajo: int) -> None:
        """Marca en proceso y corre el pipeline; siempre termina en completado o fallido."""
        with self._fabrica() as s:
            repo = RepositorioTrabajos(s)
            trabajo = repo.obtener(id_trabajo)
            if trabajo is None:
                raise LookupError("Trabajo no encontrado")
            repo.iniciar(trabajo)
            s.commit()
        self._ejecutar(id_trabajo)

    def _ejecutar(self, id_trabajo: int) -> None:
        """Corre el pipeline de un trabajo ya marcado en proceso."""
        codigo, entrada = self._entrada(id_trabajo)
        inicio = time.perf_counter()
        try:
            with self._almacen.carpeta_temporal() as tmp:
                try:
                    pipeline = self._proveedor.pipeline()
                except Exception:
                    log.exception("No se pudo construir el pipeline (trabajo %s)", id_trabajo)
                    raise StageError(SEGMENTACION, MENSAJE_MODELO)
                progreso = PipelineProgress()
                progreso.attach(ObservadorEtapas(self._fabrica, id_trabajo))
                entrada.output_dir = Path(tmp)
                salida = pipeline.run(entrada, progreso)
                rutas = self._guardar_salidas(codigo, id_trabajo, salida, Path(tmp))
            self._completar(id_trabajo, salida, rutas, time.perf_counter() - inicio)
        except StageError as exc:
            self._almacen.borrar_salidas(codigo, id_trabajo)
            # El control de calidad rechaza el estudio: queda «no compatible» (contrato_api.md, 3)
            self._fallar(id_trabajo, exc.stage, exc.message,
                         no_compatible=exc.stage == CONTROL_CALIDAD)
        except Exception:
            # El detalle va al registro; al usuario solo un mensaje general (RF-08)
            log.exception("Error inesperado en el trabajo %s", id_trabajo)
            self._almacen.borrar_salidas(codigo, id_trabajo)
            self._fallar(id_trabajo, None, MENSAJE_ERROR_GENERICO)

    def _entrada(self, id_trabajo: int) -> tuple[str, PipelineInput]:
        """Arma la entrada del pipeline con las rutas del almacenamiento."""
        with self._fabrica() as s:
            estudio = RepositorioTrabajos(s).obtener(id_trabajo).estudio
            imagen, referencia = [], []
            for archivo in RepositorioArchivos(s).del_estudio(estudio.id_estudio):
                destino = imagen if rol_de_ruta(archivo.ruta) == "imagen" else referencia
                destino.append(self._almacen.absoluta(archivo.ruta))
            entrada = PipelineInput(
                files=imagen, fmt=estudio.formato, reference_files=referencia,
                output_dir=Path(),
            )
            return estudio.codigo_anonimo, entrada

    def _guardar_salidas(self, codigo: str, id_trabajo: int, salida, tmp: Path) -> dict:
        from prosta_ai.pipeline.visualizacion import guardar_imagen_roi

        png = tmp / "roi.png"
        guardar_imagen_roi(Path(salida.image_path), Path(salida.mask_path), png)
        origenes = {"volumen": salida.image_path, "mascara": salida.mask_path, "roi": png}
        return {
            rol: self._almacen.guardar_salida(codigo, id_trabajo, rol, Path(origen)).ruta
            for rol, origen in origenes.items()
        }

    def _completar(self, id_trabajo: int, salida, rutas: dict, segundos: float) -> None:
        with self._fabrica() as s:
            RepositorioResultados(s).crear(
                id_trabajo, rutas["mascara"], ruta_imagen=rutas["volumen"],
                ruta_roi=rutas["roi"], dice=salida.dice, iou=salida.iou,
                tiempo_total_s=segundos,
            )
            repo = RepositorioTrabajos(s)
            repo.completar(repo.obtener(id_trabajo))
            s.commit()

    def _fallar(self, id_trabajo: int, etapa: str | None, mensaje: str,
                no_compatible: bool = False) -> None:
        with self._fabrica() as s:
            repo = RepositorioTrabajos(s)
            trabajo = repo.obtener(id_trabajo)
            # Si nadie avisó del fallo, se cierra la etapa que quedó en proceso
            for e in trabajo.etapas:
                if e.estado == EN_PROCESO:
                    e.estado, e.fecha_fin = FALLIDO, ahora()
                    etapa = etapa or e.nombre
            repo.fallar(trabajo, etapa, mensaje)
            if no_compatible:
                trabajo.estudio.estado_admision = NO_COMPATIBLE
            s.commit()
