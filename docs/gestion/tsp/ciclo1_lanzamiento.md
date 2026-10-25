# Lanzamiento del ciclo 1 · Adquisición y comprensión de datos

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha:** 13/10/2026 · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2

## 1. Contexto

Ya cerramos H002 (SRS y matriz de trazabilidad v1.0, PR #4 a `main` el 12/10). Este es el primer ciclo de construcción de los siete que planteamos en el Acta. Fechas planificadas: **13/10 al 25/10/2026**, hito H003 del Acta (25/10). Etiqueta de cierre: `v0.1-ciclo1`.

## 2. Objetivos

1. Definir criterios para escoger conjuntos públicos y anónimos de MRI de próstata y elegir uno principal y uno de respaldo.
2. Documentar una ficha de licencia por conjunto (procedencia, licencia, condiciones de uso y forma de citarlo).
3. Descargar los conjuntos y hacer un inventario con SHA-256 por archivo.
4. Verificar que no hay datos personales (anonimización).
5. Entender los datos: tamaños, espaciado, número de casos y revisión visual en 3D Slicer.
6. Dejar un informe de datos y los registros TSP del ciclo (LOGD y LOGT).

## 3. Criterios de salida

| # | Criterio | Cómo lo comprobamos |
|---|---|---|
| 1 | Hay criterios de selección y una decisión escrita del conjunto principal y del de respaldo | `docs/datos/criterios_seleccion.md`, `eleccion_dataset.md` |
| 2 | Cada conjunto tiene su ficha de licencia | `docs/datos/fichas/` |
| 3 | El inventario trae SHA-256 y los datos no se versionan | `reports/datos/inventario_datos.md/.csv`, `.gitignore` |
| 4 | La verificación de anonimización no deja hallazgos sin explicar | `reports/datos/verificacion_anonimizacion.md` |
| 5 | Informe de datos revisado por otra persona | PR con revisión aprobada |
| 6 | LOGD y LOGT actualizados, trazabilidad T1 | `docs/gestion/tsp/`, `docs/gestion/trazabilidad.md` |
| 7 | PR desarrollo → main y etiqueta `v0.1-ciclo1` | PR de cierre |

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
| 1200 | Lanzamiento del ciclo 1 (metas, roles, plan, LOGD/LOGT) | Fernando | 13/10 | 3 |
| 1201 | Criterios de selección de conjuntos | Juan | 14/10 | 4 |
| 1202 | Elección del conjunto principal (MSD Task05) y respaldo | Juan | 15/10–16/10 | 5 |
| 1203 | Una ficha de licencia por conjunto | Juan | 17/10 | 6 |
| 1204 | Descarga e inventario con SHA-256 | Yeison | 17/10–19/10 | 6 |
| 1205 | Verificación de anonimización | Fernando | 19/10–20/10 | 5 |
| 1206 | Análisis de tamaños, espaciado y casos | Juan | 21/10–22/10 | 6 |
| 1207 | Revisión visual en 3D Slicer | Sergio | 22/10–23/10 | 5 |
| 1208 | Informe de datos | Juan | 23/10–24/10 | 4 |
| 1209 | Cierre: trazabilidad, LOGD/LOGT, etiqueta | Yimis | 24/10–25/10 | 3 |
| | **Total** | | | **47** |

Notas del plan: Sergio instala y documenta 3D Slicer como gerente de soporte (dentro de 1207). Juan crea el LOGD con 1 h de ayuda a Fernando en 1200.

## 6. Riesgos del Acta que tocan este ciclo

| Riesgo del Acta (3.8) | Qué hacemos en este ciclo |
|---|---|
| 3. Datos insuficientes, incompletos, sesgados o con licencias con restricciones (Juan, nivel 12) | Es el riesgo de este ciclo. Verificamos licencia, calidad y etiquetas desde el principio, documentamos sesgos y dejamos un conjunto de respaldo identificado. Juan lleva el seguimiento. |
| 2. Curva de aprendizaje de las tecnologías más lenta de lo previsto (Yimis, nivel 12) | Sergio instala 3D Slicer por primera vez y Yeison lee los formatos NIfTI y MetaImage; trabajamos en parejas (Yeison ayuda a Juan en 1206, Juan a Sergio en 1207). |
| 6. Retrasos por baja disponibilidad de integrantes (cargas académicas o laborales) (Yimis, nivel 12) | Plan de ≈ 47 h en 13 días con dedicación parcial; si alguien no llega, se reasigna una tarea puntual. |
| 4. Fuga de información entre entrenamiento y prueba que sobrestime el desempeño (Fernando, nivel 8) | Todavía no se divide nada, pero 1206 y 1205 dejan lo necesario para verificar después que no haya pacientes repetidos. |

## 7. Entregable del ciclo

Primera parte del Entregable 2 (adquisición de conjuntos de datos): fichas, inventario con hashes, verificación de anonimización, análisis de geometría y revisión visual. La división por paciente y el preprocesamiento son del ciclo 2.

## 8. Forma de trabajo

- Una rama por rol (`analista`, `desarrollador`, `tester`, `disenador`, `lider`) que entra a `desarrollo` por PR revisado por otra persona; `main` solo recibe el PR de cierre.
- Las horas reales se anotan cada día en el LOGT; los defectos que se encuentren en revisión o prueba, en el LOGD.

*Las horas son las del registro de tiempos (`LOGT_registro_tiempos.md`), reconstruidas a partir de la bitácora del equipo (simuladas para este registro).*
