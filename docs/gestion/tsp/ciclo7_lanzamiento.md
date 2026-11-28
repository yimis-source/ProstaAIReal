# Lanzamiento del ciclo 7 · Cierre académico

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha del lanzamiento:** 25/11/2026 (miércoles) · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2

## Replanificación (27/11)

Registrada el 27/11/2026 a primera hora por Fernando (Gerente de planeación), siguiendo la sección 9 de la metodología. Donde esta sección y las siguientes no coincidan, vale esta; las secciones 3, 5 y 7 ya están actualizadas.

| | Fechas originales (Acta) | Fechas del lanzamiento (25/11) | Fechas nuevas (27/11) |
|---|---|---|---|
| Ciclo 7 | 03/12–09/12 | 25/11–28/11 | 25/11–27/11, se cierra junto con el ciclo 6 |
| Hito H009 | 09/12 | 28/11 | **27/11** |

**Motivo.** El equipo decidió cerrar el ciclo 7 el 27/11, el mismo día que el ciclo 6, para dejar todo el proyecto terminado ese día en lugar de repartir el cierre en dos días. No cambia la fecha de entrega que fijó el docente (28/11); se usa el 28/11 como margen.

**Qué cambia en el plan.**

| Cambio | Antes | Ahora |
|---|---|---|
| Fecha de las tareas 1802 a 1808 | 27/11 y 28/11 | 27/11 |
| 1802 · Documentación técnica | 4 h: instalación, uso y API | 5,5 h: se revisa y actualiza toda `documentacion-tecnica/`, `frontend/README.md` y los README de las pruebas |
| 1806 · GitBook y README final | 2 h, Yimis | 3,5 h: README de la raíz, GitBook, `docs-tecnicos/` y `reports/`; Yimis 3 h y revisión final de Juan como Gerente de calidad 0,5 h |
| 1803, 1804 y 1805 | Documentos del ciclo | Siguen en el plan con sus horas y sus responsables, pero son entregables del curso que Yimis prepara fuera del repositorio (acta de aceptación, Informe de Fin de Proyecto en la plantilla de OpenPM² y el Excel de lecciones aprendidas). En el repositorio solo se registra su estado |
| 1807 · RA-01 y RU-01 | RA-01 desde cero y RU-01 corta con 3 estudiantes | RA-01 sin cambios (Fernando). RU-01 no se hace dentro del repositorio: queda como riesgo residual y lo registra Juan (su 1,5 h de la 1807) |
| DICOM | «Si hay tiempo» en el ciclo 6 | Fuera de la versión entregada |

**Efectos.**

| Efecto | Cómo se maneja |
|---|---|
| Horas del ciclo: 27 h → **30 h** (+3 h, todas en la 1802 y la 1806) | El valor planificado se recalcula sobre 30 h (tabla de la sección 5 y LOGT L13). El valor ganado al 26/11 pasa de 18,5 % (5 h de 27) a 16,7 % (5 h de 30); las horas reales no cambian |
| Todo el ciclo 7 que quedaba (25 h) cae el 27/11, el mismo día de las 17 h del ciclo 6: 42 h del equipo en un día | Orden del día: primero lo que queda del ciclo 6 (1713 a 1715), después el congelamiento del código con `v0.6-ciclo6` (1716), y solo entonces la revisión de la documentación (1802), RA-01 (1807), README y GitBook (1806) y el cierre `v0.7-ciclo7` (1808). El 28/11 queda libre como margen |
| Sergio llega a 12,25 h el 27/11 (5 h del ciclo 6 y 7,25 h del ciclo 7) y Yimis a 10 h | La 1803 y la 1804 las prepara Yimis fuera del repositorio con lo que aporte Sergio; si Sergio no alcanza, Yimis las termina y sus horas se registran como ayuda en el LOGT. Juan (5 h el 27/11) y Fernando ayudan primero si alguien se atrasa |
| Riesgo 10 (documentación que no coincide con la versión congelada): ya no hay un día entero entre el congelamiento y la documentación | La 1802 no se da por terminada hasta revisarla contra `v0.6-ciclo6`, y RA-01 se hace siguiendo esa misma documentación. Lo que no coincida y no se alcance a corregir queda como limitación |
| RU-01 sin evidencia con usuarios | Juan lo registra como riesgo residual con lo que faltó y por qué. El acta de aceptación lo marca como no cumplido en esta versión |
| DICOM fuera | Se registra como limitación en la documentación final y en el acta |
| Cambia el hito H009 | Se informa al Propietario del Proyecto (ver «Aprobación») |

**Aprobación.** Aprueba Yimis (Líder). Como cambia el hito H009 (28/11 → 27/11), se informa al Propietario del Proyecto (docente Jair Enrique Sanclemente Castro), que puede objetar. No hay respuesta suya registrada en el repositorio, así que este plan no depende de ella. El LOGT sube a la versión L13 con el plan nuevo y la tabla de ciclos de `metodologia_tsp.md` conserva las fechas originales junto a las nuevas. En el postmortem del ciclo 7 se mide contra este plan (30 h, cierre el 27/11), contra el del lanzamiento (27 h, cierre el 28/11) y contra el plan original del Acta.

## 1. Contexto

El ciclo 7 es el último del proyecto: documentación final, lecciones aprendidas y acta de aceptación (Entregable 8, hito H009). Ya quedó replanificado en el lanzamiento del ciclo 6 (`ciclo6_lanzamiento.md`, sección 2) y en el análisis de impacto de Juan (`docs/gestion/replanificacion/impacto_ciclo6.md`, tarea 1701), así que aquí no se repite la replanificación, solo se resume:

| Ciclo | Fechas del plan original (Acta) | Fechas nuevas | Hito |
|---|---|---|---|
| Ciclo 7 | 03/12–09/12 | 25/11–28/11, en paralelo con el ciclo 6 | H009: 09/12 → 28/11 |

El ciclo 6 sigue en curso hasta el 27/11 y el código se congela la noche del 27/11 (`v0.6-ciclo6`). Por eso este ciclo tiene dos partes:

- **Del 25/11 al 27/11:** lo que no depende del código final (riesgos residuales, decisiones, el borrador de la documentación técnica a partir del contrato de la API). Son pocas horas, porque esos días el equipo está en el ciclo 6.
- **El 28/11:** lo que sí depende del código, sobre la versión congelada: instrucciones de instalación y uso verificadas, reproducibilidad desde cero (RA-01), prueba corta de usabilidad (RU-01), acta de aceptación, informe de fin de proyecto, lecciones aprendidas, GitBook, README final, postmortem y cierre `v0.7-ciclo7`.

Lo que dice el análisis de Juan para este ciclo:

- **RA-01** (Should) se hace en el ciclo 7: un integrante distinto del autor sigue las instrucciones desde cero el 28/11.
- **RU-01** (Should) queda reducido: prueba corta con 3 estudiantes el 28/11 sobre la versión congelada. Los hallazgos se registran y solo se corrigen textos que no toquen código; el resto queda como riesgo residual.
- **Riesgo 10** (nuevo, Sergio, NR 12): que la documentación final no coincida con la versión congelada por hacerse en paralelo. Se maneja como dice el análisis: hasta el 27/11 se escribe lo que no depende del código y el 28/11 se completan instrucciones, evidencias y capturas sobre `v0.6-ciclo6`.
- El Entregable 8 debe incluir el recorte, lo que quedó fuera (CU06, visor 3D y lo condicionado que no entre) y los riesgos residuales.

La respuesta del Propietario del Proyecto al informe del 24/11 (`informe_docente_ciclo6.md`) no está registrada en el repositorio. Este plan no depende de ella: el acta de aceptación (1803) y la matriz T7 marcan lo que quede fuera con la decisión que conste en ese momento.

Plantillas del curso que se usan (están fuera del repositorio):

- Informe de Fin de Proyecto de OpenPM², `ES (OPM2-33.C.TPL.v3.0.1)` (tarea 1804).
- Registro de Lecciones Aprendidas, el Excel del docente (tarea 1805).

## 2. Objetivos

1. Dejar la documentación técnica de la aplicación (instalación, uso y API) que corresponda exactamente a `v0.6-ciclo6`.
2. Comprobar que el proyecto se puede reproducir desde cero siguiendo solo esa documentación (RA-01) y hacer la prueba corta de usabilidad (RU-01).
3. Registrar los riesgos residuales y las decisiones técnicas y de gestión del proyecto, incluido el recorte del 24/11.
4. Preparar el acta de aceptación contra los criterios de la sección 3.2 del Acta y el Informe de Fin de Proyecto en la plantilla de OpenPM².
5. Pasar las lecciones aprendidas de los ciclos 6 y 7 al registro del curso.
6. Cerrar el proyecto según la sección 10 de la metodología (Cierre PMBOK): postmortems, trazabilidad, etiqueta y acta de aceptación.

## 3. Criterios de salida

Son los de la sección 8 de la metodología para el último ciclo, más los del Entregable 8.

| # | Criterio | Cómo lo comprobamos |
|---|---|---|
| 1 | Documentación técnica (instalación, uso y API) revisada contra `v0.6-ciclo6`; las rutas y respuestas coinciden con `docs/ejecucion/contrato_api.md` | Revisión en el PR de la 1802; la prueba de la 1807 se hace con esa misma documentación |
| 2 | RA-01: un integrante que no escribió las instrucciones instala y ejecuta la aplicación desde cero y procesa un caso | Informe de la 1807 con equipo usado, pasos, tiempos y problemas encontrados |
| 3 | RU-01: queda como riesgo residual (replanificación del 27/11); se registra qué faltó y por qué | Registro de Juan en los riesgos residuales; el acta lo marca como no cumplido en esta versión |
| 4 | Riesgos residuales y registro de decisiones escritos, con lo que quedó fuera de la versión entregada | Documento de la 1801 |
| 5 | Acta de aceptación con cada criterio de la sección 3.2 del Acta, su estado y su evidencia | Documento de la 1803, preparado fuera del repositorio; en el repositorio se registra su estado |
| 6 | Informe de Fin de Proyecto en la plantilla `ES (OPM2-33.C.TPL.v3.0.1)` | Archivo de la 1804, fuera del repositorio; en el repositorio se registra su estado |
| 7 | Lecciones aprendidas de los ciclos 6 y 7 en el Registro de Lecciones Aprendidas del curso | Excel de la 1805, fuera del repositorio; en el repositorio se registra su estado |
| 8 | GitBook, README de la raíz, `docs-tecnicos/` y `reports/` al día, con enlaces a la documentación técnica, la de gestión y el aviso de uso no diagnóstico | Revisión final de Juan en la 1806 |
| 9 | Postmortem del ciclo 7 escrito antes del merge de cierre; LOGD y LOGT al día; trazabilidad T7; verificación del Tester de que no queda ningún dato personal en el repositorio; PR `desarrollo` → `main` y etiqueta `v0.7-ciclo7` | `docs/gestion/tsp/` y PR de cierre (1808) |

## 4. Roles TSP del ciclo

Los mismos del ciclo 6.

| Rol TSP | Persona | Rol de desarrollo / gestión del Acta |
|---|---|---|
| Líder | Yimis Buenaventura | Director de Proyecto, Trazabilidad |
| Gerente de desarrollo | Yeison Bolaños Ruiz | Desarrollador, Inicio |
| Gerente de planeación | Fernando José Angulo Núñez | Tester, Planeación |
| Gerente de calidad y proceso | Juan David Riascos Erazo | Analista, Monitoreo y control |
| Gerente de soporte | Sergio Gabriel Meneses Silva | Diseñador, Cierre |

## 5. Tareas

Las horas plan incluyen el margen de 15 % que usamos desde el ciclo 5. No hay tareas de código: si al documentar aparece un defecto, se registra en el LOGD y se trata como dice el lanzamiento del ciclo 6 (solo se corrige si impide la demostración y Yimis lo aprueba).

| ID | Tarea | Responsable | Fecha | Plan h |
|---|---|---|---|---:|
| 1800 | Lanzamiento del ciclo 7 (y replanificación del 27/11) | Fernando | 25/11 | 2 |
| 1801 | Riesgos residuales y registro de decisiones | Juan | 26/11 | 3 |
| 1802 | Documentación técnica: toda `documentacion-tecnica/`, `frontend/README.md` y los README de las pruebas | Yeison / Sergio | 27/11 | 5,5 |
| 1803 | Acta de aceptación (fuera del repositorio) | Sergio | 27/11 | 2 |
| 1804 | Informe de Fin de Proyecto (OpenPM², fuera del repositorio) | Sergio / Yimis | 27/11 | 5 |
| 1805 | Lecciones aprendidas de los ciclos 6 y 7 en el registro del curso (fuera del repositorio) | Juan (con todos) | 27/11 | 3 |
| 1806 | README de la raíz, GitBook, `docs-tecnicos/` y `reports/` | Yimis / Juan (revisión final) | 27/11 | 3,5 |
| 1807 | Prueba de reproducibilidad desde cero (RA-01) y registro de RU-01 como riesgo residual | Fernando / Juan | 27/11 | 3 |
| 1808 | Postmortem del ciclo 7, LOGT final y cierre `v0.7-ciclo7` | Fernando / Yimis | 27/11 | 3 |
| | **Total** | | | **30** |

Plan del lanzamiento del 25/11, para comparar: 1802 4 h y 1806 2 h, total 27 h, con las tareas 1803 a 1808 el 28/11.

Notas sobre las tareas:

- **1802:** se revisa y actualiza toda `documentacion-tecnica/` (introducción, instalación, uso, arquitectura, flujo, código, decisiones y limitaciones), `frontend/README.md` y los README de las pruebas. El borrador sale del contrato de la API; se da por terminada cuando se revisó contra `v0.6-ciclo6` y tiene las capturas.
- **1803, 1804 y 1805:** son entregables del curso que Yimis prepara fuera del repositorio con lo que aporta cada responsable. En el repositorio solo se registra su estado (en el LOGT y en el postmortem).
- **1806:** Yimis actualiza el README de la raíz, el GitBook, `docs-tecnicos/` y `reports/`; Juan hace la revisión final como Gerente de calidad (0,5 h).
- **1805:** Juan pasa las lecciones al registro, pero cada integrante aporta las suyas (por eso «con todos»). Las horas de los demás en esta tarea se registran como ayuda en el LOGT.
- **1807:** Fernando sigue las instrucciones de instalación desde cero (RA-01), porque no las escribió. RU-01 no se hace dentro del repositorio: Juan lo registra como riesgo residual. Los resultados alimentan el acta (1803), el informe (1804) y las lecciones (1805).
- **1808:** incluye el postmortem del ciclo 7, el LOGT final con el valor ganado del proyecto, la trazabilidad T7 (Yimis, rol de Trazabilidad) y la verificación del Tester sin datos personales.

Reparto por persona (plan; las tareas compartidas se reparten así: 1802 2,75 h y 2,75 h, 1804 2,5 h y 2,5 h, 1806 3 h Yimis y 0,5 h Juan, 1807 1,5 h y 1,5 h, 1808 1,5 h y 1,5 h):

| Persona | Tareas | Plan h | % del ciclo |
|---|---|---:|---:|
| Juan | 1801, 1805, 1806 (revisión final), 1807 (RU-01 como riesgo residual) | 8 | 26,7 % |
| Sergio | 1802 (uso y capturas), 1803, 1804 | 7,25 | 24,2 % |
| Yimis | 1804, 1806, 1808 (cierre) | 7 | 23,3 % |
| Fernando | 1800, 1807 (RA-01), 1808 (postmortem y LOGT) | 5 | 16,7 % |
| Yeison | 1802 (instalación y API) | 2,75 | 9,2 % |
| **Total** | | **30** | **100,0 %** |

Por el redondeo, los porcentajes por persona suman 100,1 %. Nadie pasa del 30 % de las horas del ciclo. Yeison sigue con la menor carga: el ciclo 6 le pide 21 h entre el 24/11 y el 27/11.

Valor planificado por tarea (horas plan / 30): 2 h = 6,7 %; 3 h = 10,0 %; 3,5 h = 11,7 %; 5 h = 16,7 %; 5,5 h = 18,3 %. Por el redondeo, la suma de las nueve tareas da 100,1 %. El detalle por tarea está en el LOGT.

Orden por fecha (replanificado el 27/11):

| Fecha | Qué queda listo |
|---|---|
| Miércoles 25/11 | Lanzamiento del ciclo 7 y su plan en el LOGT |
| Jueves 26/11 | Riesgos residuales y registro de decisiones (1801) |
| Viernes 27/11 | En la mañana: replanificación (esta sección) y lo que queda del ciclo 6 (1713 a 1715). Después: código congelado con `v0.6-ciclo6` (1716) y, sobre esa versión, documentación técnica (1802), RA-01 y el registro de RU-01 (1807), README, GitBook, `docs-tecnicos/` y `reports/` con la revisión de Juan (1806), y el estado de la 1803, la 1804 y la 1805. Al final: postmortem, LOGT final, trazabilidad T7 y `v0.7-ciclo7` (1808) |
| Sábado 28/11 | Sin tareas: margen antes de la entrega |

### Nota: cómo se suman estas horas a las del ciclo 6

Del 25/11 al 27/11 los dos ciclos van al mismo tiempo, así que la carga de cada persona es la suma de los dos planes. Las horas del ciclo 6 son las del plan del LOGT por fecha: 25/11, tareas 1705 a 1708 (21 h); 26/11, 1709 a 1712 (21 h); 27/11, 1713 a 1717 (17 h, con la 1713 repartida 4 h para Yeison y 4 h para Sergio). Con la replanificación del 27/11, todo lo que queda del ciclo 7 cae ese mismo día.

| Persona | 25/11 (C6 + C7) | 26/11 (C6 + C7) | 27/11 (C6 + C7) | Total 25/11–27/11 |
|---|---:|---:|---:|---:|
| Yimis | 5 + 0 = 5 | 5 + 0 = 5 | 3 + 7 = 10 | 20 |
| Juan | 0 + 0 = 0 | 4 + 3 = 7 | 0 + 5 = 5 | 12 |
| Sergio | 6 + 0 = 6 | 5 + 0 = 5 | 5 + 7,25 = 12,25 | 23,25 |
| Yeison | 6 + 0 = 6 | 7 + 0 = 7 | 4 + 2,75 = 6,75 | 19,75 |
| Fernando | 4 + 2 = 6 | 0 + 0 = 0 | 5 + 3 = 8 | 14 |
| **Equipo** | **23** | **24** | **42** | **89** |

Comprobación: las 89 h son las 59 h del ciclo 6 que quedan desde el 25/11 (81 h del plan menos las 22 h del 24/11) más las 30 h del ciclo 7. Antes de la replanificación eran 86 h repartidas en cuatro fechas (27/11 19 h y 28/11 20 h).

Lo que muestra la tabla:

- El 27/11 es el día más pesado del proyecto: 42 h del equipo. Por eso el ciclo 6 va primero y la documentación se hace después del congelamiento, sobre `v0.6-ciclo6` (riesgo 10).
- Sergio es quien más carga ese día (12,25 h). La 1803 y la 1804 las prepara Yimis fuera del repositorio; si Sergio no alcanza, Yimis las termina y se registra como ayuda.
- Juan tiene 5 h el 27/11 y Fernando 8 h; son quienes ayudan primero si alguien se atrasa. Las ayudas se registran aparte en el LOGT.
- En promedio son 5,9 h por persona por día (89 h / 5 personas / 3 fechas), por encima de las 4,3 h/día del plan del 25/11. Si se repite la desviación media de los ciclos 1 a 5 (+12,8 %), las 89 h se vuelven unas 100 h. El 28/11 queda como margen.

## 6. Riesgos del Acta que tocan este ciclo

| Riesgo | Qué hacemos en este ciclo |
|---|---|
| 10. Documentación final que no coincide con la versión congelada, por hacerse en paralelo (Sergio, NR 12; análisis de Juan) | Riesgo principal. Hasta el 27/11 solo se escribe lo que no depende del código; el 28/11 la documentación técnica se revisa contra `v0.6-ciclo6` y RA-01 (1807) se hace siguiendo esa documentación, así que cualquier diferencia aparece en la prueba |
| 6. Retrasos por baja disponibilidad de integrantes (Yimis, NR 12 en el Acta, 16 en el análisis de Juan) | Con la replanificación del 27/11 todo el cierre cae ese día, junto con el del ciclo 6. Las tareas se ordenan para que el acta y el informe no esperen a quien falte: si alguien no puede, la tarea compartida la termina la otra persona y se registra la ayuda. El 28/11 queda como margen |
| 5. Que una salida experimental se interprete como uso médico (Sergio, NR 10 en el Acta, 15 en el análisis) | La documentación técnica, el README, el GitBook y las capturas llevan el aviso de uso no diagnóstico; las capturas de la 1802 se toman de pantallas de resultados que ya lo muestran. RU-01 queda como riesgo residual, así que no hay evidencia con usuarios de que vean el aviso |
| 7. Problemas de integración entre frontend, backend y modelo (Yeison, NR 12 en el Acta, 16 en el análisis) | Lo que no quede integrado la noche del 27/11 no entra. RA-01 comprueba la integración en un equipo distinto; lo que falle queda como riesgo residual en la 1801 y en el acta |
| 8. Agentes de IA con resultados no verificables o que amplíen el alcance (Juan, NR 9 en el Acta, 3 en el análisis) | CU06 está fuera de la versión entregada. Se documenta como trabajo futuro en la 1801, en el acta y en el Informe de Fin de Proyecto |
| 12. Que el Propietario objete el recorte cuando ya no hay tiempo para cambiarlo (Yimis, NR 10; análisis de Juan) | El acta de aceptación muestra, criterio por criterio, qué se entrega y qué quedó fuera, con la decisión que conste el 28/11 |
| 14. Horas y defectos registrados tarde (Juan, NR 6; análisis de Juan) | Cada persona anota sus horas del ciclo 7 al terminar cada tarea, separadas de las del ciclo 6; Fernando revisa el LOGT cada noche hasta el 28/11 |

## 7. Entregable del ciclo

Entregable 8 del Acta (hito H009, ahora 27/11 por la replanificación del 27/11), **documentación final**: repositorio organizado, instrucciones de ejecución, decisiones técnicas, riesgos residuales, aprendizajes, conclusiones y recomendaciones. Para el cierre del proyecto (metodología, sección 10, Cierre PMBOK) también se entregan:

- Acta de aceptación contra los criterios de la sección 3.2 del Acta (1803, fuera del repositorio).
- Informe de Fin de Proyecto en la plantilla de OpenPM² `ES (OPM2-33.C.TPL.v3.0.1)` (1804, fuera del repositorio).
- Registro de Lecciones Aprendidas del curso con los ciclos 6 y 7 (1805, fuera del repositorio).
- Postmortem del ciclo 7, LOGT final, trazabilidad T7 y etiqueta `v0.7-ciclo7` (1808).
- Evidencia de RA-01 y el registro de RU-01 como riesgo residual (1807).

Etiqueta de cierre: `v0.7-ciclo7`.

*Uso académico y experimental. Los resultados de Prosta-AI no son un diagnóstico, no sustituyen la valoración de un profesional de la salud y la aplicación no es un dispositivo médico.*

*Las horas son las del registro de tiempos (`LOGT_registro_tiempos.md`, versión L13, del 27/11/2026). Las horas reales del ciclo 7 las registra cada integrante en sus filas al terminar su tarea.*
