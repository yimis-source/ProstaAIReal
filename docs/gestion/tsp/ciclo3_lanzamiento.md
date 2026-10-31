# Lanzamiento del ciclo 3 · Segmentación 3D, modelo e inferencia

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha:** 31/10/2026 · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2

## 1. Contexto

El ciclo 2 cerró a tiempo el 30/10 (`v0.2-ciclo2`). El ciclo 3 es el de mayor riesgo técnico del Acta (modelo y cómputo). Hoy, además del lanzamiento, se decide una **replanificación** (sección 2). El 02/11 es festivo (Todos los Santos).

## 2. Replanificación

| Ciclo | Fechas del plan original (Acta, hitos 5 y 6) | Fechas nuevas | Efecto en el hito |
|---|---|---|---|
| Ciclo 3 | 31/10–13/11 | 31/10–10/11 | H005: 13/11 → 10/11 (3 días antes) |
| Ciclo 4 | 14/11–20/11 | 08/11–12/11 | H006: 20/11 → 12/11 (8 días antes) |

**Motivo.** Al revisar modelos para el ciclo 3 vimos que el modelo preentrenado `prostate_mri_anatomy` (MONAI Model Zoo) evita el entrenamiento completo, que era lo que más tiempo y cómputo nos iba a costar (riesgo 1). Con eso el ciclo 3 se puede acortar, y queremos usar el tiempo ganado como margen para los ciclos 5 a 7 (evaluación, integración web y cierre), que son los que más se apretaron en el calendario del Acta.

**Efectos y cómo los manejamos.**

| Efecto | Qué haremos |
|---|---|
| Más horas por día: pasamos de ≈ 2 h/día por persona en los ciclos 1–2 a ≈ 3–4 h/día en los días con tarea | Se pidió disponibilidad a cada integrante antes de aprobar; el plan de 76 h se reparte con Yeison como mayor carga (núcleo del pipeline y modelo) |
| Trabajo en paralelo | Sergio adelanta el diseño del visor (1502, desde el 07/11); Fernando prepara las pruebas con datos sintéticos (1410, desde el 02/11) sin esperar al modelo; Juan escribe el protocolo de evaluación (1409) antes de tener predicciones, para no ajustar el protocolo a los resultados |
| Solapamiento: el cierre del ciclo 3 (09–10/11) se cruza con el inicio del ciclo 4 (08/11) | El lanzamiento del ciclo 4 se hace el 08/11 con el 3 todavía en cierre; el postmortem del ciclo 3 (1509) se hace el 11/11 y entra en su propio PR |
| Riesgo de sobrecarga (riesgo 6) | Se vigila en el LOGT las horas por día; si alguien pasa de lo razonable, se reasigna una tarea puntual; las ayudas se registran |

**Aprobación.** Aprobada por Yimis (Líder) el 31/10 siguiendo la gestión de cambios del Acta (5.2): Juan revisó el impacto en tiempo, calidad y riesgos. Como mueve fechas de hitos, se **informa al Propietario del Proyecto** (docente Jair Enrique Sanclemente Castro). El LOGT versión L5 ya trae el plan replanificado.

## 3. Objetivos

1. Elegir el modelo preentrenado, revisar su licencia y fijar su versión y SHA-256.
2. Dejar el entorno de IA con versiones fijadas y una guía de instalación.
3. Construir el núcleo del pipeline (etapas, errores controlados, lectura de NIfTI, validadores y avance) y la preparación con las mismas transformaciones del modelo (RF-09).
4. Implementar la segmentación con ventana deslizante y llevar la máscara a la rejilla original.
5. Medir tiempo y memoria en CPU (1408); la GPU queda pendiente para Colab.
6. Escribir el protocolo de evaluación y evaluar sobre los 5 casos de prueba (con la verificación de la división antes de evaluar).
7. Dejar preparado, sin ejecutarlo, el ajuste fino y decidir qué modelo se usa.

## 4. Criterios de salida

| # | Criterio | Cómo lo comprobamos |
|---|---|---|
| 1 | El pipeline corre de la lectura a la máscara y falla de forma controlada | `backend/prosta_ai/pipeline/`, `backend/tests/pipeline/` |
| 2 | Modelo con versión fija, SHA-256 y licencia documentada | `scripts/descargar_modelo.py`, `docs-tecnicos/modelo-y-licencias.md` |
| 3 | Protocolo de evaluación escrito antes de las predicciones y evaluación sobre el conjunto de prueba | `docs/datos/protocolo_evaluacion.md`, `reports/evaluacion/` |
| 4 | Tiempo y memoria medidos en CPU, GPU declarada como pendiente | `reports/rendimiento/` |
| 5 | Decisión del modelo registrada (preentrenado o ajuste fino) | `docs-tecnicos/modelo-y-licencias.md` |
| 6 | Revisión visual de las máscaras predichas | `docs/datos/revision_3d_slicer.md` |
| 7 | LOGD/LOGT, trazabilidad T3, PR a `main`, etiqueta `v0.3-ciclo3` | PR de cierre |

## 5. Roles TSP del ciclo

| Rol TSP | Persona | Rol de desarrollo / gestión del Acta |
|---|---|---|
| Líder | Yimis Buenaventura | Director de Proyecto, Trazabilidad |
| Gerente de desarrollo | Yeison Bolaños Ruiz | Desarrollador, Inicio |
| Gerente de planeación | Fernando José Angulo Núñez | Tester, Planeación |
| Gerente de calidad y proceso | Juan David Riascos Erazo | Analista, Monitoreo y control |
| Gerente de soporte | Sergio Gabriel Meneses Silva | Diseñador, Cierre |

## 6. Tareas (plan replanificado)

| ID | Tarea | Responsable | Fechas | Plan h |
|---|---|---|---|---:|
| 1401 | Lanzamiento, postmortem C2 y replanificación | Fernando | 31/10 | 4 |
| 1402 | Selección del modelo preentrenado y licencias | Juan | 31/10–02/11 | 6 |
| 1403 | Entorno: versiones fijadas de MONAI/torch y guía de instalación | Sergio | 31/10–01/11 | 4 |
| 1404 | Núcleo del pipeline (stages, errors, io, validators, progress) | Yeison | 01/11–03/11 | 8 |
| 1405 | Descarga del modelo con versión fija y SHA-256 | Yeison | 02/11–03/11 | 3 |
| 1406 | Preparación (mismas transformaciones, RF-09) | Yeison | 03/11 | 4 |
| 1407 | Segmentación e inferencia por ventana deslizante | Yeison | 03/11–05/11 | 8 |
| 1408 | Tiempos de preparación e inferencia y memoria (CPU; GPU pendiente) | Fernando | 06/11–07/11 | 4 |
| 1409 | Protocolo de evaluación y evaluar.py | Juan | 02/11–05/11 | 7 |
| 1410 | Pruebas del pipeline con datos sintéticos | Fernando | 02/11–05/11 | 8 |
| 1411 | Verificación de la división y evaluación en los 5 casos de prueba | Fernando | 06/11 | 4 |
| 1412 | Ajuste fino preparado (no ejecutado) y decisión del modelo | Yeison | 06/11–08/11 | 8 |
| 1413 | Revisión en 3D Slicer de las máscaras predichas | Sergio | 06/11–07/11 | 4 |
| 1414 | Matriz de trazabilidad, LOGD/LOGT y cierre (v0.3-ciclo3) | Yimis | 09/11–10/11 | 4 |
| | **Total** | | | **76** |

## 7. Riesgos del Acta que tocan este ciclo

| Riesgo del Acta (3.8) | Qué hacemos en este ciclo |
|---|---|
| 1. Capacidad de cómputo de los equipos personales para ajustar o ejecutar el modelo 3D (Yeison, nivel 16) | El preentrenado con CPU baja el riesgo (no hace falta entrenar). El ajuste fino se prepara para Colab pero no se ejecuta en este ciclo. Yeison responsable. |
| 4. Fuga de información entre entrenamiento y prueba que sobrestime el desempeño (Fernando, nivel 8) | Fernando verifica la división (1411) antes de evaluar y las pruebas usan datos sintéticos, sin datos reales en el repo. |
| 2. Curva de aprendizaje de las tecnologías más lenta de lo previsto (Yimis, nivel 12) | Yeison y Fernando trabajan en pareja en la inferencia (primera vez con MONAI y ventana deslizante). |
| 6. Retrasos por baja disponibilidad de integrantes (cargas académicas o laborales) (Yimis, nivel 12) | La replanificación sube las horas por día; ver sección 2. |
| 7. Problemas de integración entre frontend, backend y modelo al final (Yeison, nivel 12) | El pipeline queda como núcleo desacoplado (etapas, errores, validadores) para integrarlo después con la API. |
| 3. Datos insuficientes, incompletos, sesgados o con licencias con restricciones (Juan, nivel 12) | El modelo se entrenó con Prostate158 y nosotros evaluamos en Task05; hay que dejarlo dicho en la ficha del modelo. |

## 8. Entregable del ciclo

Entregable 4 (modelo de segmentación 3D con inferencia operativa, configuración, métricas del conjunto de prueba y limitaciones).

*Las horas son las del registro de tiempos (`LOGT_registro_tiempos.md`), reconstruidas a partir de la bitácora del equipo (simuladas para este registro).*
