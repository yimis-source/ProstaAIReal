# Lanzamiento del ciclo 4 · Generación de la ROI

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha:** 08/11/2026 · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2

## 1. Contexto

Este lanzamiento se hace el 08/11, **con el ciclo 3 todavía en cierre** (queda 1412 hasta hoy y 1414, trazabilidad y etiqueta, el 09 y 10/11). Es consecuencia de la replanificación del 31/10: el ciclo 4 pasa de 14/11–20/11 a **08/11–12/11** (H006: 20/11 → 12/11). Etiqueta de cierre: `v0.4-ciclo4`. El diseño del visor (1502) lo adelantó Sergio desde el 07/11.

## 2. Objetivos

1. Diseñar el visor y la superposición de la ROI (la implementación web es del ciclo 6).
2. Etapa ROI del pipeline: máscara en la rejilla original de la imagen, guardada como NIfTI junto con la imagen.
3. Imagen del corte con la ROI superpuesta y el aviso de salida experimental impreso (RF-13, RF-15).
4. Texto explicativo de la ROI sin lenguaje clínico (RF-16, RF-17).
5. Pruebas de la etapa ROI y de la imagen con aviso.
6. Verificación de alineación (script y 3D Slicer) y análisis de errores por caso.
7. Postmortem del ciclo 3 (1509), que no se alcanzó a escribir antes.

## 3. Criterios de salida

| # | Criterio | Cómo lo comprobamos |
|---|---|---|
| 1 | La ROI sale alineada con la imagen original (forma y afín iguales, máscara binaria) | `reports/roi/`, `backend/tests/pipeline/test_pipeline_roi.py` |
| 2 | La imagen de la ROI lleva el aviso experimental y no usa lenguaje clínico | `backend/tests/pipeline/test_pipeline_visualizacion.py`, texto revisado |
| 3 | Diseño del visor y texto explicativo documentados | `docs/diseno/` |
| 4 | Análisis de errores por caso con lectura de los resultados | `reports/evaluacion/` |
| 5 | Postmortem del ciclo 3 en su PR; postmortem del ciclo 4 antes del cierre | `docs/gestion/tsp/` |
| 6 | LOGD/LOGT, trazabilidad T4, PR a `main`, etiqueta `v0.4-ciclo4` | PR de cierre |

## 4. Roles TSP del ciclo

| Rol TSP | Persona | Rol de desarrollo / gestión del Acta |
|---|---|---|
| Líder | Yimis Buenaventura | Director de Proyecto, Trazabilidad |
| Gerente de desarrollo | Yeison Bolaños Ruiz | Desarrollador, Inicio |
| Gerente de planeación | Fernando José Angulo Núñez | Tester, Planeación |
| Gerente de calidad y proceso | Juan David Riascos Erazo | Analista, Monitoreo y control |
| Gerente de soporte | Sergio Gabriel Meneses Silva | Diseñador, Cierre |

## 5. Tareas

| ID | Tarea | Responsable | Fechas | Plan h |
|---|---|---|---|---:|
| 1501 | Lanzamiento del ciclo 4 (con el ciclo 3 en cierre) | Fernando | 08/11 | 3 |
| 1502 | Diseño del visor y de la superposición de la ROI | Sergio | 07/11–09/11 | 6 |
| 1503 | Etapa ROI (rejilla original, NIfTI de salida) | Yeison | 09/11–10/11 | 6 |
| 1504 | Imagen de la ROI con aviso no clínico | Yeison | 10/11–11/11 | 6 |
| 1505 | Texto explicativo de la ROI y revisión de lenguaje no clínico | Sergio | 10/11 | 3 |
| 1506 | Pruebas de la ROI y de la imagen con aviso | Fernando | 10/11–11/11 | 5 |
| 1507 | Verificación de alineación (3D Slicer + script) | Juan | 11/11 | 4 |
| 1508 | Análisis de errores por caso (incluye prostate_07, 32 casos) | Juan | 11/11 | 3 |
| 1509 | Postmortem del ciclo 3 | Fernando | 11/11 | 2 |
| 1510 | Postmortem C4, matriz y cierre (v0.4-ciclo4) | Fernando / Yimis | 12/11 | 4 |
| | **Total** | | | **42** |

## 6. Riesgos del Acta que tocan este ciclo

| Riesgo del Acta (3.8) | Qué hacemos en este ciclo |
|---|---|
| 5. Que una salida experimental se tome como diagnóstico médico (Sergio, nivel 10) | Riesgo principal: aviso visible en la imagen de la ROI, texto sin lenguaje clínico y revisión de Sergio (dueño del riesgo). |
| 6. Retrasos por baja disponibilidad de integrantes (cargas académicas o laborales) (Yimis, nivel 12) | Se acumulan el cierre del ciclo 3 y el ciclo 4 en 5 días; se registran las horas por día y las ayudas. |
| 4. Fuga de información entre entrenamiento y prueba que sobrestime el desempeño (Fernando, nivel 8) | El análisis de errores por caso incluye todos los casos con máscara, pero la evaluación formal sigue siendo solo sobre el conjunto de prueba. |
| 7. Problemas de integración entre frontend, backend y modelo al final (Yeison, nivel 12) | La etapa ROI cambia la API del pipeline (se agrega `output_dir`); hay que correr la evaluación y las pruebas completas al integrar. |

## 7. Solapamiento con el ciclo 3

| Qué | Ciclo 3 | Ciclo 4 |
|---|---|---|
| Fecha de cierre | 10/11 (PR a `main` con `v0.3-ciclo3`) | 12/11 |
| Tareas abiertas hoy | 1412 (hasta el 08/11), 1414 (09–10/11) | 1501 (hoy) y 1502 (en curso) |
| Postmortem | 1509 el 11/11 | 1510 el 12/11 |

## 8. Entregable del ciclo

Entregable 5 (generación del mapa/ROI): ROI alineada, imagen con superposición y aviso, y texto explicativo. La visualización dentro de la aplicación web es del ciclo 6.

*Las horas son las del registro de tiempos (`LOGT_registro_tiempos.md`), reconstruidas a partir de la bitácora del equipo (simuladas para este registro).*
