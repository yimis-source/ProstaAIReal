# Verificación de la división por paciente y de fuga entre conjuntos

Generado con `scripts/verificar_fuga.py`.

## 1. División de MSD Task05 (RC-04)

- Archivo: `entrenamiento/division_task05.json`, semilla 2026, huella `728fae869f02e7c7…` (verificada).
- Cantidades: entrenamiento 22, validacion 5, prueba 5 (total 32).
- En Task05 cada caso es un paciente distinto (no hay identificador de paciente aparte).

| Intersección | Casos |
|---|---|
| entrenamiento ∩ validacion | vacía |
| entrenamiento ∩ prueba | vacía |
| validacion ∩ prueba | vacía |

**Resultado:** sin pacientes repetidos entre conjuntos.

## 2. Pacientes compartidos con otros conjuntos

Pendiente: comparar MSD Task05 con PROMISE12 (ambos tienen estudios de Radboud, Nijmegen).
