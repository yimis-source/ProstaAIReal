"""Tarea en segundo plano (RF-06): un hilo del mismo proceso que toma los pendientes de uno en uno."""
import logging
import threading

from prosta_ai.processing import ServicioProcesamiento

log = logging.getLogger(__name__)


class TareaProcesamiento:
    def __init__(self, servicio: ServicioProcesamiento, intervalo_s: float = 2.0):
        self._servicio = servicio
        self._intervalo = intervalo_s
        self._parar = threading.Event()
        self._hilo: threading.Thread | None = None

    @property
    def activa(self) -> bool:
        return self._hilo is not None and self._hilo.is_alive()

    def _bucle(self) -> None:
        while not self._parar.is_set():
            try:
                hubo = self._servicio.procesar_siguiente()
            except Exception:
                # Un fallo al tomar un trabajo no debe tumbar el hilo
                log.exception("La tarea en segundo plano no pudo tomar un trabajo")
                hubo = False
            if not hubo:
                self._parar.wait(self._intervalo)

    def iniciar(self) -> None:
        if self.activa:
            return
        self._parar.clear()
        self._hilo = threading.Thread(target=self._bucle, name="prosta-procesamiento", daemon=True)
        self._hilo.start()

    def detener(self, espera_s: float = 10.0) -> None:
        """Pide parar y espera; un trabajo a medias termina o queda para recuperar_interrumpidos."""
        self._parar.set()
        if self._hilo is not None:
            self._hilo.join(timeout=espera_s)
            if self._hilo.is_alive():
                log.warning("La tarea en segundo plano no terminó en %.0f s", espera_s)
