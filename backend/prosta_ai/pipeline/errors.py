"""Errores controlados del pipeline."""


class StageError(Exception):
    """Fallo controlado de una etapa del procesamiento."""

    def __init__(self, stage: str, message: str):
        super().__init__(f"{stage}: {message}")
        self.stage = stage
        self.message = message
