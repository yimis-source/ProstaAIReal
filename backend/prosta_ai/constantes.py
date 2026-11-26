"""Constantes compartidas del procesamiento."""

# Aviso único de resultado no diagnóstico (RF-15, RF-16). Lo imprime la imagen de la ROI
# y, en el ciclo 6, lo mostrarán todas las pantallas de resultados.
AVISO_EXPERIMENTAL = (
    "Resultado experimental con fines académicos. No es un diagnóstico ni "
    "sustituye la valoración de un profesional de la salud."
)

# Estados del trabajo y de cada etapa (contrato_api.md, sección 3)
PENDIENTE = "pendiente"
EN_PROCESO = "en proceso"
COMPLETADO = "completado"
FALLIDO = "fallido"

# Estado de admisión que pone el control de calidad al rechazar un estudio (contrato_api.md, 3)
NO_COMPATIBLE = "no compatible"

# Mensajes al usuario cuando el error no viene de un StageError (RF-08: sin datos internos)
MENSAJE_ERROR_GENERICO = "Ocurrió un error inesperado durante el procesamiento. Intente de nuevo."
MENSAJE_INTERRUMPIDO = "El procesamiento se interrumpió. Vuelva a pulsar «Procesar»."
MENSAJE_MODELO = "No se pudo cargar el modelo de segmentación."
