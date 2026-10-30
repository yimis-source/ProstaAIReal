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

## 2. Pacientes compartidos entre MSD Task05 y PROMISE12

Se comparan los vóxeles de la imagen T2 de cada par con la misma forma (admitiendo inversión de ejes x/y).

| Caso MSD | Conjunto en la división | Caso PROMISE12 | Imagen | Dice entre máscaras |
|---|---|---|---|---:|
| prostate_00 | entrenamiento | entrenamiento/Case13 | idéntica | 0.9535 |
| prostate_01 | entrenamiento | entrenamiento/Case14 | idéntica | 0.9845 |
| prostate_07 | entrenamiento | entrenamiento/Case17 | idéntica | 0.8904 |
| prostate_13 | prueba | entrenamiento/Case20 | idéntica | 0.9520 |
| prostate_14 | entrenamiento | entrenamiento/Case21 | idéntica | 0.9494 |
| prostate_16 | entrenamiento | entrenamiento/Case23 | idéntica | 1.0000 |
| prostate_17 | prueba | entrenamiento/Case24 | idéntica | 0.9264 |
| prostate_18 | entrenamiento | entrenamiento/Case25 | idéntica | 0.9394 |
| prostate_20 | entrenamiento | prueba/Case00 | idéntica | 0.9310 |
| prostate_21 | entrenamiento | prueba/Case01 | idéntica | 0.9086 |
| prostate_24 | entrenamiento | prueba/Case03 | idéntica | 0.9222 |
| prostate_25 | entrenamiento | prueba/Case04 | idéntica | 0.9043 |

**Resultado:** 12 casos de MSD Task05 (con máscara) son exactamente el mismo estudio que un caso de PROMISE12; 0 de ellos con la misma máscara (ninguno) y el resto con otra anotación. 2 están en el conjunto de prueba.

**Decisión:** PROMISE12 no se usa para entrenar ni para evaluar: mezclarlo con MSD metería los mismos pacientes en entrenamiento y prueba. Se conserva solo como referencia.
