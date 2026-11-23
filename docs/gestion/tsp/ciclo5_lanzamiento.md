# Lanzamiento del ciclo 5 · Evaluación técnica del modelo

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha del lanzamiento:** 16/11/2026 (registrado en el repositorio el 23/11/2026) · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2

## 1. Contexto

El ciclo 4 cerró el 12/11 (`v0.4-ciclo4`), 8 días antes de lo planificado en el Acta. El postmortem del ciclo 4 dejó del 13/11 al 20/11 como colchón y pidió decidir en este lanzamiento si se usaba.

**Decisión (aprobada por Yimis):** usar el colchón. El ciclo 5 empieza el **16/11** en lugar del 21/11 y mantiene el cierre del Acta, **25/11** (hito H007). Así el ciclo tiene 10 días en vez de 5 y hay tiempo para la medición en GPU y el ajuste fino en Colab, que dependen de que haya GPU disponible. Etiqueta de cierre: `v0.5-ciclo5`.

## 2. Objetivos

1. Evaluación formal del modelo en los 5 casos de prueba: Dice e IoU por caso y promedio, con condiciones y limitaciones (RF-23, RF-24).
2. Métricas de borde: HD95 y distancia media de superficie.
3. Medición en GPU que quedó pendiente de la tarea 1408 (RR-01).
4. Ejecutar el ajuste fino en Colab y adoptarlo solo si supera el Dice del preentrenado en los mismos 5 casos.
5. Revisión visual de las predicciones en 3D Slicer y textos de resultados sin lenguaje clínico.
6. Trazabilidad con la evidencia del ciclo 5, postmortem y cierre.

## 3. Criterios de salida

| # | Criterio | Cómo lo comprobamos |
|---|---|---|
| 1 | Informe de métricas con Dice, IoU, HD95 y distancia media por caso y promedio, y sus límites | `reports/evaluacion/informe_metricas_ciclo5.md` |
| 2 | Decisión del ajuste fino tomada con los mismos casos y métricas | Sección del ajuste fino en el informe de métricas y `docs-tecnicos/modelo-y-licencias.md` |
| 3 | Informe de rendimiento con cifras reales de GPU que aclare que no son comparables con las de CPU | `reports/rendimiento/rendimiento_1408_gpu_<fecha>.md` |
| 4 | Pruebas en verde, incluidas las de las métricas nuevas y del informe de rendimiento | `python -m pytest -q` |
| 5 | Revisión visual y textos sin lenguaje clínico | `docs/datos/revision_slicer_predicciones.md`, `docs/diseno/texto_roi.md` |
| 6 | Postmortem en su propio PR antes del cierre; LOGD/LOGT, trazabilidad T5 y etiqueta `v0.5-ciclo5` | `docs/gestion/tsp/` y PR de cierre |

## 4. Roles TSP del ciclo

| Rol TSP | Persona | Rol de desarrollo / gestión del Acta |
|---|---|---|
| Líder | Yimis Buenaventura | Director de Proyecto, Trazabilidad |
| Gerente de desarrollo | Yeison Bolaños Ruiz | Desarrollador, Inicio |
| Gerente de planeación | Fernando José Angulo Núñez | Tester, Planeación |
| Gerente de calidad y proceso | Juan David Riascos Erazo | Analista, Monitoreo y control |
| Gerente de soporte | Sergio Gabriel Meneses Silva | Diseñador, Cierre |

## 5. Tareas

Las horas plan ya incluyen el margen de 15 % que acordamos en el postmortem del ciclo 4. Las tareas que el equipo no ha hecho nunca (ajuste fino en Colab y métricas de superficie) llevan un margen mayor.

| ID | Tarea | Responsable | Fechas | Plan h |
|---|---|---|---|---:|
| 1601 | Lanzamiento del ciclo 5 | Fernando | 16/11 | 3 |
| 1602 | Rendimiento en GPU (cierra lo pendiente de la tarea 1408) | Fernando | 16/11–18/11 | 5 |
| 1603 | Ajuste fino del modelo en Google Colab | Yeison | 16/11–21/11 | 10 |
| 1604 | Métricas adicionales (HD95 y distancia media de superficie) | Juan (ayuda: Yeison) | 17/11–20/11 | 5 |
| 1605 | Informe de métricas y límites (RF-23, RF-24) | Juan | 21/11–24/11 | 6 |
| 1606 | Revisión visual en 3D Slicer y textos de resultados | Sergio | 18/11–23/11 | 5 |
| 1607 | Trazabilidad, revisión de PR y cierre (`v0.5-ciclo5`) | Yimis | 23/11–25/11 | 5 |
| 1608 | Postmortem del ciclo 5, en su propio PR antes del cierre | Fernando | 25/11 | 2 |
| | **Total** | | | **41** |

Reparto por persona (plan): Fernando 10 h, Yeison 10 h, Juan 11 h, Sergio 5 h, Yimis 5 h. Ninguna persona pasa del 30 % de las horas del ciclo, para no repetir la concentración de los ciclos 1 y 3.

## 6. Riesgos del Acta que tocan este ciclo

| Riesgo del Acta (3.8) | Qué hacemos en este ciclo |
|---|---|
| 1. Capacidad de cómputo de los equipos personales para ajustar o ejecutar el modelo 3D (Yeison, nivel 16) | Riesgo principal. La GPU solo está en Colab gratuito, que no garantiza disponibilidad. El ajuste fino y la medición en GPU van al principio del ciclo para tener margen si Colab no asigna GPU. Si no hay GPU, se documenta y el modelo preentrenado sigue siendo el adoptado. |
| 4. Fuga de información entre entrenamiento y prueba que sobrestime el desempeño (Fernando, nivel 8) | El ajuste fino entrena solo con los 22 casos de entrenamiento de Task05 y se compara con los mismos 5 casos de prueba; los casos de prueba no se usan para elegir la época. |
| 5. Que una salida experimental se tome como diagnóstico médico (Sergio, nivel 10) | Los textos de resultados y las notas de la revisión visual no usan lenguaje clínico; las métricas se presentan como evaluación técnica. |
| 6. Retrasos por baja disponibilidad de integrantes (cargas académicas o laborales) (Yimis, nivel 12) | El ciclo dura 10 días gracias al colchón; las tareas se escalonan para no juntar todos los PR el último día. |

## 7. Entregable del ciclo

Evaluación técnica del modelo (hito H007): informe de métricas por caso con sus límites, decisión del ajuste fino, rendimiento en CPU y GPU, y revisión visual. La integración web es del ciclo 6; el defecto D-006 (Ejecutar/Procesar) se corrige ahí.

*Las horas son las del registro de tiempos (`LOGT_registro_tiempos.md`). Las horas reales del ciclo 5 las registra cada integrante en sus filas.*
