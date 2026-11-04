"""Nombres de las etapas, en el orden fijo en que se ejecutan."""

CONTROL_CALIDAD = "control de calidad"
PREPARACION = "preparación"
SEGMENTACION = "segmentación"
EVALUACION = "evaluación"

# La etapa ROI (máscara alineada con la imagen original y guardada en disco) entra en el ciclo 4.
STAGES = [CONTROL_CALIDAD, PREPARACION, SEGMENTACION, EVALUACION]
