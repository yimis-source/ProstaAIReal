# Lanzamiento del ciclo 6 · Desarrollo web e integración

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha del lanzamiento:** 24/11/2026 (martes) · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2

## 1. Contexto

El ciclo 5 cerró el 23/11 (`v0.5-ciclo5`), dos días antes del hito H007. Ya tenemos el pipeline completo en `backend/prosta_ai/pipeline/` (control de calidad, preparación, segmentación, ROI y evaluación), el modelo preentrenado `prostate_mri_anatomy` adoptado y las métricas en los 5 casos de prueba. Lo que falta es la aplicación web: no hay API, ni base de datos, ni interfaz.

El docente (Ing. Jair Enrique Sanclemente Castro, Propietario del Proyecto) adelantó la entrega: **todo el proyecto debe estar terminado el 28/11/2026**. Por eso este lanzamiento trae una replanificación de los ciclos 6 y 7 (sección 2) y un recorte del alcance con MoSCoW (sección 4). El contrato de la API se escribe hoy, antes de programar, en `docs/ejecucion/contrato_api.md`, para que backend e interfaz trabajen en paralelo desde el 24/11.

## 2. Replanificación

| Ciclo | Fechas del plan original (Acta, hitos 8 y 9) | Fechas nuevas | Efecto en el hito |
|---|---|---|---|
| Ciclo 6 | 26/11–02/12 | 24/11–27/11, código congelado el 27/11 en la noche | H008: 02/12 → 27/11 (5 días antes) |
| Ciclo 7 | 03/12–09/12 | 25/11–28/11, en paralelo con el ciclo 6 | H009: 09/12 → 28/11 (11 días antes) |

**Motivo.** El docente adelantó la entrega final al 28/11/2026. No es una decisión del equipo; lo que sí decidimos es cómo acomodar el trabajo en los días que quedan.

**Efectos y cómo los manejamos.**

| Efecto | Qué haremos |
|---|---|
| El ciclo 6 pasa de 7 a 4 días y es el más grande del proyecto (81 h plan) | Se recorta el alcance con MoSCoW (sección 4): se hace solo el flujo carga → procesamiento → ROI con NIfTI. CU05 (historial) y DICOM en .zip quedan como «si hay tiempo»; CU06 y el visor 3D quedan fuera |
| Se dejan fuera o en espera requisitos del SRS: DICOM (RF-02 y RF-03 piden DICOM y NIfTI), RF-19 (consulta del historial, Should) y RF-20 a RF-22 (CU06, Could) | Es un cambio de alcance: se informa al docente (tarea 1701). Lo que no se haga queda registrado en el postmortem y en la documentación final como limitación |
| Más horas por día: el plan da ≈ 4 h/día por persona y ≈ 5,3 h/día a Yeison y Sergio (21 h en 4 días), por encima de las 3–4 h/día de los ciclos 3 a 5 | Se pidió disponibilidad a cada integrante antes de aprobar. Juan tiene la menor carga (7 h) y ayuda donde haga falta; las ayudas se registran aparte en el LOGT |
| Backend e interfaz se construyen al mismo tiempo | El contrato de la API (`docs/ejecucion/contrato_api.md`) se fija hoy; Sergio trabaja contra ese contrato sin esperar a que la API exista. Cualquier cambio al contrato se escribe primero en el documento y se avisa en el PR |
| El ciclo 7 (documentación final, lecciones aprendidas y acta de aceptación) se cruza con el 6 entre el 25/11 y el 27/11 | Lo que no depende del código final se escribe desde el 25/11. Lo que depende del código (instrucciones de ejecución y evidencias de pruebas) se cierra el 28/11, con el código ya congelado. El ciclo 7 tiene su propio lanzamiento (tareas 18xx) |
| Código congelado el 27/11 en la noche | Después de esa hora no entra código nuevo a `desarrollo`. Si el 28/11 aparece un defecto, se registra en el LOGD y se documenta como limitación; solo se corrige si impide la demostración y Yimis lo aprueba |
| El margen para integrar es corto (riesgo 7 del Acta) | La integración API–base de datos–pipeline (1711) va el 26/11, un día antes del cierre, y Fernando prueba la carga el 25/11 (1708) para no descubrir los problemas el 27/11 |

**Análisis de impacto.** Juan analiza el impacto en alcance, tiempo, calidad y riesgos en `docs/gestion/replanificacion/impacto_ciclo6.md` (tarea 1701, la escribe hoy) y prepara el informe al docente.

**Aprobación.** Aprobada por Yimis (Líder) el 24/11 siguiendo la gestión de cambios del Acta (5.2) y la sección 9 de la metodología. Como cambian los hitos H008 y H009 y el alcance, **se informa al Propietario del Proyecto** (docente Jair Enrique Sanclemente Castro), que puede objetar. El LOGT versión L10 trae el plan del ciclo 6 con las fechas nuevas, y la tabla de ciclos de `metodologia_tsp.md` conserva las fechas originales junto a las nuevas. En el postmortem se mide contra las fechas replanificadas y contra el plan original.

## 3. Objetivos

1. Fijar el contrato de la API antes de programar y respetarlo en backend e interfaz.
2. Dejar el entorno (Python 3.12 y PostgreSQL), el esquema de base de datos y la migración inicial.
3. Construir la API en FastAPI y la interfaz en React (Vite) para el flujo acceso → carga → procesamiento → resultado.
4. Procesar en segundo plano con estado por etapa y errores controlados, usando el pipeline que ya existe.
5. Mostrar la ROI superpuesta con y sin máscara, el panel explicativo y el aviso de uso no diagnóstico en toda pantalla de resultados; corregir D-006 («Procesar»).
6. Guardar estudios, trabajos y resultados en PostgreSQL y los archivos en disco, sin datos personales.
7. Medir RR-01 con los 5 casos de prueba a través de la API.

## 4. Alcance (MoSCoW)

Números verificados contra el SRS (`docs/ejecucion/fuentes/1.3.1.1_SRS_requisitos_ISO29148.md`).

| Prioridad | Qué | Requisitos | Tareas |
|---|---|---|---|
| Se hace | CU01 acceso básico (alias y contraseña, sin roles) | RF-01, RC-05 | 1705 (API), 1706 (pantalla) |
| Se hace | CU02 carga de NIfTI con validación de formato, tamaño y archivo corrupto | RF-02, RF-03, RF-04 | 1705, 1706 |
| Se hace | CU03 procesamiento en segundo plano, estado de cada etapa y errores controlados | RF-06, RF-07, RF-08 (RF-09 a RF-12 ya están en el pipeline) | 1709, 1710, 1711 |
| Se hace | CU04 ROI superpuesta, comparación con y sin máscara, aviso y panel explicativo; D-006 «Procesar» | RF-13, RF-14, RF-15, RF-16, RF-17 | 1713, 1714 |
| Se hace | PostgreSQL y archivos en disco, sin datos personales | RB-01, RB-02 (y el registro de RF-18) | 1702, 1707, 1711 |
| Se hace | Tiempo de procesamiento con 5 casos por la API | RR-01 | 1715 |
| Si hay tiempo | CU05 historial (consulta de los estudios del usuario) | RF-19 | 1712 |
| Si hay tiempo | DICOM en un .zip | RF-02, RF-03 (formato DICOM) | sin tarea; se abre solo si 1705 termina antes |
| Fuera | CU06 asistente con agentes de IA | RF-20, RF-21, RF-22 | — |
| Fuera | Visor 3D | — | — |

Notas sobre la verificación de números:

- CU02 incluye también RF-05 (quitar metadatos identificables o rechazar). Con NIfTI de conjuntos públicos lo cubre el `MetadataValidator` del pipeline en la etapa de control de calidad; no hace falta tarea aparte.
- CU05 son RF-18 y RF-19. El registro de cada estudio procesado (RF-18) sale de la persistencia (1707 y 1711); lo que queda en «si hay tiempo» es la consulta (RF-19).
- Los límites de tamaño de RF-03 son 50 MB por archivo y 150 MB por estudio.

## 5. Criterios de salida

| # | Criterio | Cómo lo comprobamos |
|---|---|---|
| 1 | Flujo completo en la web con un NIfTI: acceso, carga, «Procesar», estado por etapa y ROI con y sin máscara | Demostración y pruebas de integración de la API (`backend/tests/`) |
| 2 | La API cumple `docs/ejecucion/contrato_api.md` (rutas, códigos y cuerpos) | Pruebas de integración de 1708 y 1715; revisión en los PR |
| 3 | Archivos no válidos (formato, tamaño, corruptos) y etapas fallidas terminan con mensaje claro, sin caerse | Pruebas de la carga (1708) y del estado (1709) |
| 4 | Aviso de uso no diagnóstico y panel explicativo en toda pantalla de resultados; botón «Procesar»; D-006 cerrado en el LOGD | Revisión de pantallas y `LOGD_registro_defectos.md` |
| 5 | Esquema con migración inicial; base de datos y archivos sin datos personales | Migración en el repositorio y verificación del Tester (criterio 6 del Acta) |
| 6 | RR-01 medido con los 5 casos de prueba por la API, con el equipo usado | `reports/rendimiento/` (informe de 1715) |
| 7 | Pruebas en verde y build de la interfaz sin errores | `python -m pytest -q` y build de Vite |
| 8 | Código congelado el 27/11 en la noche; postmortem en su propio PR; LOGD/LOGT, trazabilidad T6 y etiqueta `v0.6-ciclo6` | `docs/gestion/tsp/` y PR de cierre |

## 6. Roles TSP del ciclo

| Rol TSP | Persona | Rol de desarrollo / gestión del Acta |
|---|---|---|
| Líder | Yimis Buenaventura | Director de Proyecto, Trazabilidad |
| Gerente de desarrollo | Yeison Bolaños Ruiz | Desarrollador, Inicio |
| Gerente de planeación | Fernando José Angulo Núñez | Tester, Planeación |
| Gerente de calidad y proceso | Juan David Riascos Erazo | Analista, Monitoreo y control |
| Gerente de soporte | Sergio Gabriel Meneses Silva | Diseñador, Cierre |

## 7. Tareas (plan replanificado)

Las horas plan incluyen el margen de 15 % que usamos desde el ciclo 5. Las tareas nuevas para el equipo (FastAPI, React con Vite, migraciones) llevan un poco más.

| ID | Tarea | Responsable | Fecha | Plan h |
|---|---|---|---|---:|
| 1700 | Lanzamiento, replanificación y contrato de la API | Fernando | 24/11 | 4 |
| 1701 | Impacto del recorte e informe al docente | Juan | 24/11 | 3 |
| 1702 | Entorno Python 3.12, PostgreSQL, esquema y migración inicial | Yimis | 24/11 | 6 |
| 1703 | Esqueleto FastAPI y /api/salud | Yeison | 24/11 | 4 |
| 1704 | Esqueleto React con Vite, rutas y aviso fijo | Sergio | 24/11 | 5 |
| 1705 | CU02 carga de NIfTI y validación (API) | Yeison | 25/11 | 6 |
| 1706 | CU01 acceso y CU02 pantalla de carga | Sergio | 25/11 | 6 |
| 1707 | Persistencia de estudios y archivos (RB-01, RB-02) | Yimis | 25/11 | 5 |
| 1708 | Pruebas de integración de la carga | Fernando | 25/11 | 4 |
| 1709 | CU03 procesamiento en segundo plano, estado y errores (API) | Yeison | 26/11 | 7 |
| 1710 | CU03 pantalla de estado | Sergio | 26/11 | 5 |
| 1711 | Integración API, base de datos y pipeline | Yimis | 26/11 | 5 |
| 1712 | CU05 historial (si hay tiempo) | Juan | 26/11 | 4 |
| 1713 | CU04 ROI con y sin máscara, panel y aviso | Yeison / Sergio | 27/11 | 8 |
| 1714 | D-006 «Procesar» en la interfaz | Sergio | 27/11 | 1 |
| 1715 | RR-01 con 5 casos por la API | Fernando | 27/11 | 3 |
| 1716 | Trazabilidad T6 y cierre v0.6-ciclo6 | Yimis | 27/11 | 3 |
| 1717 | Postmortem del ciclo 6 | Fernando | 27/11 | 2 |
| | **Total** | | | **81** |

Reparto por persona (plan; la 1713 se reparte 4 h para Yeison y 4 h para Sergio):

| Persona | Tareas | Plan h | % del ciclo |
|---|---|---:|---:|
| Yeison | 1703, 1705, 1709, 1713 (API) | 21 | 25,9 % |
| Sergio | 1704, 1706, 1710, 1713 (pantalla), 1714 | 21 | 25,9 % |
| Yimis | 1702, 1707, 1711, 1716 | 19 | 23,5 % |
| Fernando | 1700, 1708, 1715, 1717 | 13 | 16,0 % |
| Juan | 1701, 1712 | 7 | 8,6 % |
| **Total** | | **81** | **100,0 %** |

Nadie pasa del 30 % de las horas del ciclo. Si la 1712 no se hace, el valor ganado máximo del ciclo es 77 de 81 h (95,1 %) y se explica en el postmortem.

Valor planificado por tarea (horas plan / 81): 1 h = 1,2 %; 2 h = 2,5 %; 3 h = 3,7 %; 4 h = 4,9 %; 5 h = 6,2 %; 6 h = 7,4 %; 7 h = 8,6 %; 8 h = 9,9 %. El detalle por tarea está en el LOGT.

Orden por fecha:

| Día | Qué queda listo |
|---|---|
| Martes 24/11 | Contrato de la API, entorno y migración inicial, esqueletos de API e interfaz, análisis de impacto |
| Miércoles 25/11 | Acceso y carga de NIfTI de punta a punta con persistencia; pruebas de integración de la carga |
| Jueves 26/11 | Procesamiento en segundo plano con estado; integración con el pipeline; historial si hay tiempo |
| Viernes 27/11 | ROI con y sin máscara, panel y aviso, «Procesar», RR-01, postmortem y cierre; código congelado en la noche |

## 8. Riesgos del Acta que tocan este ciclo

| Riesgo del Acta (3.8) | Qué hacemos en este ciclo |
|---|---|
| 7. Problemas de integración entre frontend, backend y modelo al final del proyecto (Yeison, nivel 12) | Riesgo principal. Contrato de la API fijado antes de programar; carga probada de punta a punta el 25/11 (1708); integración con el pipeline el 26/11 (1711), no el 27/11 |
| 6. Retrasos por baja disponibilidad de integrantes (cargas académicas o laborales) (Yimis, nivel 12) | El ciclo tiene 4 días y no hay colchón. Se prioriza el producto mínimo (sección 4); si alguien no puede, se reasigna una tarea puntual y se registra la ayuda |
| 1. Capacidad de cómputo de los equipos personales para ejecutar el modelo 3D (Yeison, nivel 16) | La inferencia corre en segundo plano para no bloquear la API. RR-01 se mide en el equipo donde corre la aplicación y se dice cuál es; no se compara con las cifras de GPU del ciclo 5 |
| 2. Curva de aprendizaje de las tecnologías más lenta de lo previsto (Yimis, nivel 12) | FastAPI, SQLAlchemy con migraciones y React con Vite son nuevos para varios. Los esqueletos (1703, 1704) van el 24/11 y el contrato evita discutir formatos sobre la marcha |
| 5. Que una salida experimental se tome como diagnóstico médico (Sergio, nivel 10) | Aviso fijo en toda pantalla de resultados (RF-15) desde el esqueleto de la interfaz (1704); textos sin lenguaje clínico (RF-16); la API devuelve el mismo aviso de `constantes.py` |
| 8. Que los agentes de IA produzcan resultados no verificables o amplíen el alcance (Juan, nivel 9) | Se evita: CU06 queda fuera del ciclo |

## 9. Entregable del ciclo

Entregables 6 y 7 del Acta (hito H008, ahora 27/11):

- **Entregable 6, aplicación web unida:** interfaz React, API FastAPI, PostgreSQL, almacenamiento en disco y el módulo de IA, con carga, procesamiento automático y visualización de la ROI.
- **Entregable 7, evidencias de calidad:** pruebas unitarias del pipeline (ya existentes), pruebas de integración de la API, verificación sin datos personales, RR-01 por la API y las métricas Dice e IoU del ciclo 5. Lo que pase con las pruebas de usabilidad (RU-01) lo define el análisis de impacto de Juan.

Etiqueta de cierre: `v0.6-ciclo6`.

*Las horas son las del registro de tiempos (`LOGT_registro_tiempos.md`, versión L10). Las horas reales del ciclo 6 las registra cada integrante en sus filas al terminar su tarea.*
