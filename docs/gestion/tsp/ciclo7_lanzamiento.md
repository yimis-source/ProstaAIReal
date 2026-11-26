# Lanzamiento del ciclo 7 · Cierre académico

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha del lanzamiento:** 25/11/2026 (miércoles) · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2

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
| 3 | RU-01 reducido: 3 estudiantes completan carga, procesamiento y visualización; tareas completadas y observaciones registradas | Informe de la 1807; los hallazgos que no se corrijan quedan como riesgo residual |
| 4 | Riesgos residuales y registro de decisiones escritos, con lo que quedó fuera de la versión entregada | Documento de la 1801 |
| 5 | Acta de aceptación con cada criterio de la sección 3.2 del Acta, su estado y su evidencia | Documento de la 1803 |
| 6 | Informe de Fin de Proyecto en la plantilla `ES (OPM2-33.C.TPL.v3.0.1)` | Archivo de la 1804 |
| 7 | Lecciones aprendidas de los ciclos 6 y 7 en el Registro de Lecciones Aprendidas del curso | Excel de la 1805 |
| 8 | GitBook y README final que enlazan la documentación técnica, la de gestión y el aviso de uso no diagnóstico | Revisión de la 1806 |
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
| 1800 | Lanzamiento del ciclo 7 | Fernando | 25/11 | 2 |
| 1801 | Riesgos residuales y registro de decisiones | Juan | 26/11 | 3 |
| 1802 | Documentación técnica de la aplicación (instalación, uso y API) | Yeison / Sergio | 27/11–28/11 | 4 |
| 1803 | Acta de aceptación | Sergio | 28/11 | 2 |
| 1804 | Informe de Fin de Proyecto (OpenPM²) | Sergio / Yimis | 28/11 | 5 |
| 1805 | Lecciones aprendidas de los ciclos 6 y 7 en el registro del curso | Juan (con todos) | 28/11 | 3 |
| 1806 | GitBook y README final | Yimis | 28/11 | 2 |
| 1807 | Prueba de reproducibilidad desde cero (RA-01) y prueba corta de usabilidad (RU-01) | Fernando / Juan | 28/11 | 3 |
| 1808 | Postmortem del ciclo 7, LOGT final y cierre `v0.7-ciclo7` | Fernando / Yimis | 28/11 | 3 |
| | **Total** | | | **27** |

Notas sobre las tareas:

- **1802:** la carpeta es `documentacion-tecnica/` (`instalacion.md`, `uso.md` y la parte de la API). El 27/11 se escribe a partir del contrato de la API y de lo que ya esté integrado; el 28/11 se revisa contra `v0.6-ciclo6` y se agregan las capturas.
- **1805:** Juan pasa las lecciones al registro, pero cada integrante aporta las suyas (por eso «con todos»). Las horas de los demás en esta tarea se registran como ayuda en el LOGT.
- **1807:** Fernando sigue las instrucciones de instalación desde cero (RA-01), porque no las escribió. Juan coordina la prueba con los 3 estudiantes (RU-01). Los resultados alimentan el acta (1803), el informe (1804) y las lecciones (1805).
- **1808:** incluye el postmortem del ciclo 7, el LOGT final con el valor ganado del proyecto, la trazabilidad T7 (Yimis, rol de Trazabilidad) y la verificación del Tester sin datos personales.

Reparto por persona (plan; las tareas compartidas se reparten a partes iguales: 1802 2 h y 2 h, 1804 2,5 h y 2,5 h, 1807 1,5 h y 1,5 h, 1808 1,5 h y 1,5 h):

| Persona | Tareas | Plan h | % del ciclo |
|---|---|---:|---:|
| Juan | 1801, 1805, 1807 (RU-01) | 7,5 | 27,8 % |
| Sergio | 1802 (uso y capturas), 1803, 1804 | 6,5 | 24,1 % |
| Yimis | 1804, 1806, 1808 (cierre) | 6 | 22,2 % |
| Fernando | 1800, 1807 (RA-01), 1808 (postmortem y LOGT) | 5 | 18,5 % |
| Yeison | 1802 (instalación y API) | 2 | 7,4 % |
| **Total** | | **27** | **100,0 %** |

Nadie pasa del 30 % de las horas del ciclo. Yeison tiene la menor carga a propósito: el ciclo 6 le pide 21 h entre el 24/11 y el 27/11.

Valor planificado por tarea (horas plan / 27): 2 h = 7,4 %; 3 h = 11,1 %; 4 h = 14,8 %; 5 h = 18,5 %. Por el redondeo, la suma de las nueve tareas da 99,9 %. El detalle por tarea está en el LOGT.

Orden por fecha:

| Fecha | Qué queda listo |
|---|---|
| Miércoles 25/11 | Lanzamiento del ciclo 7 y su plan en el LOGT |
| Jueves 26/11 | Riesgos residuales y registro de decisiones (1801) |
| Viernes 27/11 | Borrador de la documentación técnica a partir del contrato de la API (1802). Código congelado en la noche (`v0.6-ciclo6`) |
| Sábado 28/11 | En la mañana: documentación técnica revisada contra `v0.6-ciclo6` (1802) y, con ella, RA-01 y RU-01 (1807). Después: acta de aceptación (1803), Informe de Fin de Proyecto (1804), lecciones aprendidas (1805), GitBook y README (1806). Al final: postmortem, LOGT final, trazabilidad T7 y `v0.7-ciclo7` (1808) |

### Nota: cómo se suman estas horas a las del ciclo 6

Del 25/11 al 27/11 los dos ciclos van al mismo tiempo, así que la carga de cada persona es la suma de los dos planes. Las horas del ciclo 6 son las del plan del LOGT (L10) por fecha: 25/11, tareas 1705 a 1708 (21 h); 26/11, 1709 a 1712 (21 h); 27/11, 1713 a 1717 (17 h, con la 1713 repartida 4 h para Yeison y 4 h para Sergio). La 1802 se reparte por igual entre sus dos fechas (1 h por persona el 27/11 y 1 h el 28/11).

| Persona | 25/11 (C6 + C7) | 26/11 (C6 + C7) | 27/11 (C6 + C7) | 28/11 (C7) | Total 25/11–28/11 |
|---|---:|---:|---:|---:|---:|
| Yimis | 5 + 0 = 5 | 5 + 0 = 5 | 3 + 0 = 3 | 6 | 19 |
| Juan | 0 + 0 = 0 | 4 + 3 = 7 | 0 + 0 = 0 | 4,5 | 11,5 |
| Sergio | 6 + 0 = 6 | 5 + 0 = 5 | 5 + 1 = 6 | 5,5 | 22,5 |
| Yeison | 6 + 0 = 6 | 7 + 0 = 7 | 4 + 1 = 5 | 1 | 19 |
| Fernando | 4 + 2 = 6 | 0 + 0 = 0 | 5 + 0 = 5 | 3 | 14 |
| **Equipo** | **23** | **24** | **19** | **20** | **86** |

Comprobación: las 86 h son las 59 h del ciclo 6 que quedan desde el 25/11 (81 h del plan menos las 22 h del 24/11) más las 27 h del ciclo 7.

Lo que muestra la tabla:

- El ciclo 7 suma poco del 25/11 al 27/11 (2 h el 25/11, 3 h el 26/11 y 2 h el 27/11); casi todo cae el 28/11, cuando el ciclo 6 ya terminó. Así se respeta el riesgo 10: lo que depende del código se escribe sobre la versión congelada.
- El día más pesado por persona es de 7 h: Yeison el 26/11 (1709) y Juan el 26/11, este solo si se abre la 1712 (CU05) en el punto de decisión de las 12:00. Si no se abre, Juan tiene 3 h ese día.
- Fernando no tiene tareas el 26/11 y Juan no tiene tareas el 25/11 ni el 27/11. Son quienes ayudan primero si alguien se atrasa en el ciclo 6; las ayudas se registran aparte en el LOGT.
- En promedio son 4,3 h por persona por día (86 h / 5 personas / 4 fechas), por encima de las 3,0 h/día del ciclo 5. Si se repite la desviación media de los ciclos 1 a 5 (+12,8 %), las 86 h se vuelven unas 97 h.

## 6. Riesgos del Acta que tocan este ciclo

| Riesgo | Qué hacemos en este ciclo |
|---|---|
| 10. Documentación final que no coincide con la versión congelada, por hacerse en paralelo (Sergio, NR 12; análisis de Juan) | Riesgo principal. Hasta el 27/11 solo se escribe lo que no depende del código; el 28/11 la documentación técnica se revisa contra `v0.6-ciclo6` y RA-01 (1807) se hace siguiendo esa documentación, así que cualquier diferencia aparece en la prueba |
| 6. Retrasos por baja disponibilidad de integrantes (Yimis, NR 12 en el Acta, 16 en el análisis de Juan) | Todo el cierre cae el 28/11 (sábado). Las tareas del 28/11 se ordenan para que el acta y el informe no esperen a quien falte: si alguien no puede, la tarea compartida la termina la otra persona y se registra la ayuda |
| 5. Que una salida experimental se interprete como uso médico (Sergio, NR 10 en el Acta, 15 en el análisis) | La documentación técnica, el README, el GitBook y las capturas llevan el aviso de uso no diagnóstico; las capturas de la 1802 se toman de pantallas de resultados que ya lo muestran. En la RU-01 se registra si los 3 estudiantes ven el aviso |
| 7. Problemas de integración entre frontend, backend y modelo (Yeison, NR 12 en el Acta, 16 en el análisis) | Lo que no quede integrado la noche del 27/11 no entra. RA-01 comprueba la integración en un equipo distinto; lo que falle queda como riesgo residual en la 1801 y en el acta |
| 8. Agentes de IA con resultados no verificables o que amplíen el alcance (Juan, NR 9 en el Acta, 3 en el análisis) | CU06 está fuera de la versión entregada. Se documenta como trabajo futuro en la 1801, en el acta y en el Informe de Fin de Proyecto |
| 12. Que el Propietario objete el recorte cuando ya no hay tiempo para cambiarlo (Yimis, NR 10; análisis de Juan) | El acta de aceptación muestra, criterio por criterio, qué se entrega y qué quedó fuera, con la decisión que conste el 28/11 |
| 14. Horas y defectos registrados tarde (Juan, NR 6; análisis de Juan) | Cada persona anota sus horas del ciclo 7 al terminar cada tarea, separadas de las del ciclo 6; Fernando revisa el LOGT cada noche hasta el 28/11 |

## 7. Entregable del ciclo

Entregable 8 del Acta (hito H009, ahora 28/11), **documentación final**: repositorio organizado, instrucciones de ejecución, decisiones técnicas, riesgos residuales, aprendizajes, conclusiones y recomendaciones. Para el cierre del proyecto (metodología, sección 10, Cierre PMBOK) también se entregan:

- Acta de aceptación contra los criterios de la sección 3.2 del Acta (1803).
- Informe de Fin de Proyecto en la plantilla de OpenPM² `ES (OPM2-33.C.TPL.v3.0.1)` (1804).
- Registro de Lecciones Aprendidas del curso con los ciclos 6 y 7 (1805).
- Postmortem del ciclo 7, LOGT final, trazabilidad T7 y etiqueta `v0.7-ciclo7` (1808).
- Evidencias de RA-01 y RU-01 (1807), que completan el Entregable 7 del ciclo 6 en lo que corresponde a usabilidad.

Etiqueta de cierre: `v0.7-ciclo7`.

*Uso académico y experimental. Los resultados de Prosta-AI no son un diagnóstico, no sustituyen la valoración de un profesional de la salud y la aplicación no es un dispositivo médico.*

*Las horas son las del registro de tiempos (`LOGT_registro_tiempos.md`, versión L11). Las horas reales del ciclo 7 las registra cada integrante en sus filas al terminar su tarea.*
