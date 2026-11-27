# Postmortem del ciclo 6 · Desarrollo web e integración

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha:** 27/11/2026 · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2

## 1. Resumen

El ciclo 6 se replanificó en su lanzamiento del 24/11 (`ciclo6_lanzamiento.md`, sección 2): el plan original del Acta lo ponía del 26/11 al 02/12 (hito H008) y, como el docente adelantó la entrega final al 28/11, quedó del 24/11 al 27/11, con el alcance recortado con MoSCoW. Como acordamos (registro de decisiones, RD-30), este postmortem se escribe el 27/11, con el código ya congelado y en su propio PR. Las dieciocho tareas (1700 a 1717) están terminadas y el código se congeló el 27/11 a media tarde, antes de la noche que fijaba el plan.

Qué quedó en la versión del ciclo:

| Tema | Resultado |
|---|---|
| CU01 acceso | Alias y contraseña, confirmación en el primer acceso, token (1705, 1706) |
| CU02 carga | Solo NIfTI (`.nii`, `.nii.gz`), con validación de formato, tamaño y archivo corrupto; RF-05 en la carga: la API vacía los campos de texto de la cabecera antes de guardar (1705, D-022) |
| CU03 procesamiento | En segundo plano, con estado de las cinco etapas y errores controlados; el estudio queda «no compatible» si falla el control de calidad (1709, 1710, 1711) |
| CU04 ROI | Visor de cortes con el interruptor «Mostrar ROI», panel «¿Qué estoy viendo?» con Dice e IoU y aviso de uso no diagnóstico (1713) |
| CU05 historial | Se abrió en el punto de decisión del 26/11 al mediodía (RD-33) y se terminó ese día (1712) |
| Persistencia | PostgreSQL con las migraciones `0001` y `0002`; archivos en disco con ruta relativa y SHA-256 (1702, 1707, 1711) |
| D-006 | Cerrado: el botón dice «Procesar» (1714) |
| Fuera | CU06 (asistente), visor 3D y DICOM. RU-01 no se hizo con personas |

- **RR-01 por la API (1715, `reports/rendimiento/rr01_api_2026-11-27.md`):** 5 de 5 casos completados en CPU (Ryzen 5 5600G). De punta a punta (carga, procesamiento y resultado) media 20,8 s y máximo 24,0 s; solo el procesamiento, media 15,2 s y máximo 17,5 s. RR-01 (≤ 120 s) **se cumple**.
- **Pruebas al congelar:** 229 pasan y 12 se omiten sin PostgreSQL, con las ramas del 27/11 integradas. Con PostgreSQL pasan también las de integración y las de la cola.
- **Punta a punta con el cliente real de la interfaz contra la API y PostgreSQL:** el 26/11, `prostate_13` (18 s, Dice 0,901); el 27/11, `prostate_28` (Dice 0,832), con el resultado y los cortes.

## 2. Plan frente a real

| ID | Tarea | Responsable | Plan h | Real h | Estado | Evidencia |
|---|---|---|---:|---:|---|---|
| 1700 | Lanzamiento, replanificación y contrato de la API | Fernando | 4 | 4,5 | Terminada (24/11) | `ciclo6_lanzamiento.md`, `docs/ejecucion/contrato_api.md` |
| 1701 | Impacto del recorte e informe al docente | Juan | 3 | 4 | Terminada (24/11) | `docs/gestion/replanificacion/impacto_ciclo6.md`, `informe_docente_ciclo6.md` |
| 1702 | Entorno, PostgreSQL, esquema y migración inicial | Yimis | 6 | 7,5 | Terminada (24/11) | `scripts/postgres_local.sh`, migración `0001` |
| 1703 | Esqueleto FastAPI y /api/salud | Yeison | 4 | 4,5 | Terminada (24/11) | `backend/prosta_ai/api/`, `test_salud.py` |
| 1704 | Esqueleto React con Vite, rutas y aviso fijo | Sergio | 5 | 5,5 | Terminada (24/11) | `frontend/`, `frontend/README.md` |
| 1705 | CU02 carga de NIfTI y validación (API), con el acceso de CU01 | Yeison | 6 | 7 | Terminada (25/11) | `admision.py`, `test_estudios.py` |
| 1706 | CU01 acceso y CU02 pantalla de carga | Sergio | 6 | 6,5 | Terminada (25/11) | Pantallas de acceso y carga |
| 1707 | Persistencia de estudios y archivos | Yimis | 5 | 4,5 | Terminada (25/11) | Repositorios y almacenamiento con sus pruebas |
| 1708 | Pruebas de integración de la carga | Fernando | 4 | 3,5 | Terminada (25/11) | `backend/tests/integracion/` |
| 1709 | CU03 procesamiento en segundo plano, estado y errores (API) | Yeison | 7 | 7,5 | Terminada (26/11) | Pruebas de procesamiento y de la cola |
| 1710 | CU03 pantalla de estado | Sergio | 5 | 5,5 | Terminada (26/11) | `frontend/src/pages/Estado.jsx` |
| 1711 | Integración API, base de datos y pipeline | Yimis | 5 | 6 | Terminada (26/11) | Servicio de procesamiento, migración `0002` |
| 1712 | CU05 historial (si hay tiempo) | Juan | 4 | 3 | Terminada (26/11) | `GET /api/estudios` y pantalla «Mis estudios» |
| 1713 | CU04 ROI con y sin máscara, panel y aviso | Yeison (4,5 h) / Sergio (5 h) | 8 | 9,5 | Terminada (27/11) | Rutas del resultado y de los cortes (contrato 4.8 y 4.9), visor y panel |
| 1714 | D-006 «Procesar» en la interfaz | Sergio | 1 | 0,5 | Terminada (27/11): solo verificación | LOGD, D-006 cerrado |
| 1715 | RR-01 con 5 casos por la API | Fernando | 3 | 3,5 | Terminada (27/11) | `reports/rendimiento/rr01_api_2026-11-27.md`, `scripts/medir_rr01_api.py` |
| 1716 | Trazabilidad T6 y cierre v0.6-ciclo6 | Yimis | 3 | 3 | Terminada (27/11) | `docs/gestion/trazabilidad.md` |
| 1717 | Postmortem del ciclo 6 | Fernando | 2 | 2 | Terminada (27/11) | Este documento |
| | **Total** | | **81** | **88** | | |

**Desviación del ciclo:** +9 % (88 h reales frente a 81 h plan). Es el ciclo más grande del proyecto y su desviación es de las más bajas: C1 +15 %, C2 +17 %, C3 +16 %, C4 +7 %, C5 +9 %, C6 +9 %.

Por fecha:

| Fecha | Tareas | Plan h | Real h | Desviación |
|---|---|---:|---:|---:|
| 24/11 | 1700 a 1704 | 22 | 26 | +18 % |
| 25/11 | 1705 a 1708 | 21 | 21,5 | +2 % |
| 26/11 | 1709 a 1712 | 21 | 22 | +5 % |
| 27/11 | 1713 a 1717 | 17 | 18,5 | +9 % |
| **Total** | | **81** | **88** | **+9 %** |

- Lo que más se pasó fue la 1701 (+33 %, dos correcciones del análisis de impacto: D-015 y D-019) y la 1702 (+25 %, el clúster de PostgreSQL que no arrancaba, D-012, y la corrección de la migración, D-011). El 24/11 fue la fecha con más desviación: todas las herramientas eran nuevas.
- La 1711 (+20 %) se alargó por las dos correcciones que salieron al integrar la API (D-027 y D-028), y la 1713 (+19 %) por las dos del 27/11 (D-030 y D-031).
- La 1715 (+17 %) incluyó corregir el script de RR-01 (D-032).
- Quedaron por debajo la 1712 (-25 %), que reutilizó las vistas del detalle del estudio, y la 1714 (-50 %): D-006 ya estaba corregido en la interfaz y solo hubo que verificarlo.

**Ayudas:** no se registraron ayudas en el ciclo 6. La 1713 es compartida: plan 4 h y 4 h, real Yeison 4,5 h y Sergio 5 h.

**Por persona:**

| Persona | Plan h | Real h | Desviación | Días con tarea | h/día |
|---|---:|---:|---:|---:|---:|
| Yimis | 19 | 21 | +11 % | 4 | 5,2 |
| Juan | 7 | 7 | 0 % | 2 | 3,5 |
| Sergio | 21 | 23 | +10 % | 4 | 5,8 |
| Yeison | 21 | 23,5 | +12 % | 4 | 5,9 |
| Fernando | 13 | 13,5 | +4 % | 3 | 4,5 |
| **Equipo** | **81** | **88** | **+9 %** | | **5,0** |

Promedio de 5,0 h por día con tarea asignada, el más alto del proyecto (3,0 h/día en el ciclo 5). El lanzamiento preveía ≈ 5,3 h/día para Yeison y Sergio; quedaron en 5,9 y 5,8.

## 3. Fechas

Plan replanificado (lanzamiento del 24/11) y plan original del Acta (ciclo 6 del 26/11 al 02/12, H008 el 02/12):

| Tarea | Plan replanificado | Real | Desviación | Frente al plan original |
|---|---|---|---|---|
| Inicio del ciclo | 24/11 | 24/11; lanzamiento, contrato de la API y plan en el LOGT versionados ese mismo día (commits `023a5e0`, `a97f5bd` y `dde1841`) | a tiempo | 2 días antes (26/11) |
| 1700 a 1704 | 24/11 | 24/11 | a tiempo | — |
| 1705 a 1708 | 25/11 | 25/11 | a tiempo | — |
| 1709 a 1711 | 26/11 | 26/11 | a tiempo | — |
| 1712 (condicionada) | 26/11, si se abría en el punto de decisión del mediodía | Abierta en el punto de decisión (RD-33) y terminada el 26/11 | a tiempo | — |
| 1713 a 1715 | 27/11 | 27/11 | a tiempo | — |
| Código congelado | 27/11 en la noche | 27/11 a media tarde | unas horas antes | 5 días antes (02/12) |
| 1716, 1717 y cierre (H008) | 27/11 | 27/11 (`v0.6-ciclo6`) | a tiempo | 5 días antes (02/12) |

Ninguna tarea se corrió de fecha. Contra el plan original, el ciclo empezó 2 días antes, duró 4 días en vez de 7 y cerró 5 días antes del hito.

## 4. Defectos del ciclo

21 defectos del ciclo 6 (LOGD), 5,9 h de corrección en total. Además se cerró D-006, que es del ciclo 2.

| ID | Fecha | Tarea | Tipo | Inyectado → removido | Descripción corta |
|---|---|---|---:|---|---|
| D-011 | 24/11 | 1702 | 70 | IMP → PU | `etapa_trabajo.estado` sin NOT NULL en la migración inicial |
| D-012 | 24/11 | 1702 | 100 | IMP → EJE | El clúster de PostgreSQL no arrancaba por la longitud de la ruta del socket |
| D-013 | 24/11 | 1703 | 50 | IMP → PU | El 404 de Starlette no usaba el formato común de error |
| D-014 | 24/11 | 1704 | 20 | IMP → COMP | Import con otras mayúsculas; `npm run build` fallaba |
| D-015 | 24/11 | 1701 | 10 | REQ → REV | El análisis de impacto describía mal CU00 y el riesgo 8 |
| D-016 | 24/11 | 1702 | 40 | IMP → REV | Límite de carga de 500 MB; RF-03 pide 50 MB por archivo y 150 MB por estudio |
| D-017 | 24/11 | 1700 | 50 | DIS → REV | El contrato decía `detail` y la API y la interfaz usan `detalle` |
| D-018 | 24/11 | 1700 | 10 | DIS → REV | RF-05 dado por cubierto por un validador que no revisa metadatos |
| D-019 | 24/11 | 1701 | 10 | REQ → REV | Etapas, estado fallido y punto de decisión distintos del lanzamiento |
| D-020 | 25/11 | 1707 | 80 | IMP → PU | El almacenamiento devolvía la ruta absoluta y no la relativa |
| D-021 | 25/11 | 1706 | 50 | IMP → PU | La interfaz enviaba `archivo` y el contrato pide `archivos` |
| D-022 | 25/11 | 1705 | 80 | IMP → PU | RF-05: se guardaban los bytes originales y no el NIfTI limpio |
| D-023 | 26/11 | 1711 | 80 | IMP → PU | La etapa que fallaba quedaba «en proceso» |
| D-025 | 26/11 | 1709 | 80 | IMP → INT | El 409 de procesar no miraba los trabajos pendientes |
| D-026 | 26/11 | 1710 | 80 | IMP → PU | La consulta periódica seguía al salir de la pantalla |
| D-027 | 26/11 | 1711 | 80 | DIS → INT | Nadie marcaba el estudio «no compatible» al fallar el control de calidad |
| D-028 | 26/11 | 1711 | 80 | IMP → REV | El bloqueo de la cola se cerraba antes de marcar el trabajo |
| D-029 | 26/11 | 1708 | 60 | IMP → PU | La prueba de integración esperaba la revisión `0001` fija |
| D-030 | 27/11 | 1713 | ver LOGD | ver LOGD | El índice del corte aceptaba un valor igual al número de cortes (el último válido es cortes − 1) |
| D-031 | 27/11 | 1713 | ver LOGD | ver LOGD | El visor no liberaba las URL de los PNG al cambiar de corte o salir |
| D-032 | 27/11 | 1715 | ver LOGD | ver LOGD | El script de RR-01 leía Dice e IoU de la ruta del resultado, que no estaba en la versión medida |

D-024 es del ciclo 7 (tarea 1801) y no cuenta aquí.

- **Rendimiento de revisión:** 6 de 21 (29 %): D-015 a D-019 y D-028. Al 26/11 iba en 6 de 18 (33 %); los tres del 27/11 los encontraron pruebas y el uso, no la revisión. Aun así es mejor que el 0 % de los ciclos 3, 4 y 5.
- Casi todos los defectos se inyectaron en implementación y los encontraron las pruebas unitarias o de integración antes de fusionar. Los de documentación (D-015, D-018, D-019) salieron en la revisión de integración del 24/11, cuando se comparó el análisis de impacto con el lanzamiento y el contrato.
- **D-006** («Ejecutar» en lugar de «Procesar»), abierto desde el 28/10, queda cerrado: la pantalla de estado dice «Procesar».

## 5. Valor ganado

Todas las tareas terminadas al 27/11: 81 h plan de 81 (100,0 %). La 1712 era condicionada; sin ella el máximo habría sido 77 h (95,1 %). Acumulado del proyecto: 387 h plan ganadas.

| Fecha | Valor ganado acumulado del ciclo |
|---|---:|
| 24/11 | 22 h de 81 (27,2 %) |
| 25/11 | 43 h de 81 (53,1 %) |
| 26/11 | 64 h de 81 (79,0 %) |
| 27/11 | 81 h de 81 (100,0 %) |

## 6. Decisiones del ciclo

El detalle y la evidencia de cada una están en `docs/gestion/cierre/registro_decisiones.md`.

| Decisión | Con qué evidencia | Resultado |
|---|---|---|
| Replanificar el ciclo 6 al 24/11–27/11 por el adelanto de la entrega (RD-20) | Lanzamiento, sección 2; análisis de impacto de Juan | Ciclo de 4 días; H008 del 02/12 al 27/11 |
| Recortar con MoSCoW (RD-21) | Análisis de impacto, secciones 2 y 8 | CU01 a CU04 y persistencia hechos; CU06 y visor 3D fuera |
| Contrato de la API antes del código (RD-22) | Contrato versionado antes del primer commit de la API (24/11) | Backend e interfaz en paralelo desde el 24/11 |
| Solo NIfTI; DICOM condicionado (RD-23) | Análisis de impacto (RF-02 y RF-03) | DICOM no entró: con la replanificación del ciclo 7 del 27/11 queda fuera de la versión entregada |
| RF-05 en la carga (RD-24) | D-018 y D-022 | La API guarda el NIfTI con la cabecera limpia, con su prueba |
| PostgreSQL local con un clúster propio por TCP (RD-25) | D-012 | La base se levanta sin Docker ni permisos de administrador |
| Pruebas de integración contra PostgreSQL con la migración (RD-31) | `backend/tests/integracion/README.md` | Fueron el criterio del punto de decisión |
| Punto de decisión del 26/11 al mediodía: primero CU05, después DICOM (RD-29, RD-33) | 9 pruebas de integración en verde (PR #94) y un caso procesado por la API | CU05 abierto y terminado el mismo día |
| Código congelado el 27/11 (RD-27) | Lanzamiento, sección 2 | Congelado a media tarde |
| RU-01 reducido el 28/11 (RD-28), cambiado el 27/11 | Replanificación del ciclo 7 | RU-01 no se hace con personas; queda como riesgo residual (1807) |

## 7. Qué funcionó

- El contrato de la API se escribió antes de programar. Sergio hizo las pantallas contra el documento sin esperar la API, y los desajustes entre las dos partes (D-017, D-021) aparecieron antes de integrar.
- Probar la carga de punta a punta contra PostgreSQL el 25/11 (1708) e integrar el pipeline el 26/11 (1711), no el 27/11. D-025, D-027 y D-028 salieron un día antes de congelar el código.
- El punto de decisión tenía un criterio escrito. CU05 se abrió con evidencia, y DICOM salió sin discusión porque no se cumplía su condición.
- Las horas y los defectos se registraron cada noche (LOGT y LOGD del 24/11, 25/11, 26/11 y 27/11); el riesgo 14 se mantuvo mitigado hasta el cierre.
- Las tareas de cada fecha terminaron en su fecha, sin corrimientos, en un ciclo de 81 h.
- La prueba con el cliente real de la interfaz contra la API y PostgreSQL (`prostate_13` el 26/11 y `prostate_28` el 27/11) mostró el flujo completo antes de cerrar, no solo las pruebas de la API por separado.
- RR-01 se cumple con mucho margen: 24,0 s de punta a punta en el caso más lento, frente a 120 s.
- Actualizar las cinco ramas con avance rápido a `desarrollo` cada día dejó a todos trabajando sobre lo último integrado.

## 8. Qué no funcionó

- **PR abiertos mal.** Un PR se abrió desde la cuenta del líder y no desde la del integrante (#94). Otro se abrió invertido (#99): se cerró sin fusionar y se rehízo como #100. Los títulos de #93 y #96 estaban equivocados y los corrigió el líder.
- **Dependencias en cadena entre ramas.** El trabajo de una rama dependía del de otra (Yimis → Yeison → Fernando y Juan), así que hubo que fusionar ramas entre sí y luego los PR en orden. Un PR fusionado fuera de orden habría traído a `desarrollo` cambios todavía sin revisar.
- **El rendimiento de revisión bajó** de 33 % al 26/11 a 29 % al cierre. Los tres defectos del 27/11 los encontraron las pruebas y el uso. Las tareas más grandes (1709, 1711, 1713) se revisaron con menos tiempo, como advertía el riesgo 9.
- **RR-01 se midió antes de integrar la 1713.** La versión medida no tenía la ruta del resultado; el script tuvo que leer Dice e IoU del detalle del estudio (D-032). El tiempo de RR-01 no cambia, pero la ruta del resultado no quedó medida.
- **El ritmo fue alto:** 5,0 h/día de promedio y 5,9 y 5,8 h/día para Yeison y Sergio, por encima de lo previsto en el lanzamiento.
- **La 1714 se planeó sin revisar el estado del defecto.** D-006 ya estaba corregido en la interfaz (el riesgo RT-12 lo decía el 26/11), y la tarea quedó en media hora de verificación.
- **El alcance quedó recortado:** CU06, visor 3D y DICOM fuera, y RU-01 sin prueba con personas. El criterio de aceptación 2 del Acta depende de que se apruebe ese recorte; en el repositorio no está registrada la respuesta del docente al informe del 24/11.
- El 24/11 hubo tres commits seguidos sin compilar la interfaz (D-014).

## 9. Pendientes que pasan al ciclo 7

| Pendiente | Responsable | Tarea |
|---|---|---|
| Revisar toda la documentación técnica contra `v0.6-ciclo6` (rutas del resultado y de los cortes, solo NIfTI, CU05, PostgreSQL) | Yeison / Sergio | 1802 |
| Riesgos residuales versión 1.1: poner el resultado de las filas «se revisa al congelar el código» (1, 2, 5, 7, 9, 13, RT-01, RT-02, RT-04, RT-06, RT-12) con la evidencia de este ciclo | Juan | 1807 / 1808 |
| Agregar al registro de decisiones que DICOM queda fuera de la versión entregada | Juan | 1807 / 1808 |
| Registrar RU-01 como riesgo residual: no se hizo con personas | Juan | 1807 |
| RA-01: levantar la aplicación desde cero siguiendo la documentación; si alcanza, repetir un caso de RR-01 con la ruta del resultado | Fernando | 1807 |
| CU06, visor 3D y DICOM como limitaciones y trabajo futuro en el Informe de Fin de Proyecto y en la matriz («Fuera de la versión entregada») | Sergio / Yimis | 1804, 1806 |
| Postmortem del ciclo 7, LOGT final y cierre `v0.7-ciclo7` | Fernando / Yimis | 1808 |

## 10. Lecciones

1. El contrato de la API antes del código nos dejó trabajar en paralelo: lo repetiríamos en cualquier proyecto con backend e interfaz separados.
2. Integrar un día antes del cierre, y no el mismo día, fue lo que nos dio tiempo de corregir lo que solo aparece al juntar las partes.
3. Cuando una rama depende de otra, lo decimos en el PR y acordamos el orden de fusión antes de abrirlo. Mejor todavía: fusionamos a `desarrollo` lo que otros necesitan antes de seguir construyendo encima.
4. Abrimos cada PR desde la cuenta de quien hizo el trabajo y revisamos base, rama y título antes de crearlo.
5. Antes de planear la corrección de un defecto, miramos en qué estado está.
6. Un requisito se mide sobre la versión que se entrega. Si medimos antes de integrar la última tarea, lo decimos en el informe y volvemos a medir.
7. Con cuatro días, la revisión de PR es lo primero que se acorta. Las pruebas encontraron la mayoría de los defectos, así que escribirlas junto con el código no es opcional cuando el ciclo es corto.

## 11. Medición contra el plan original (metodología, sección 9)

| Aspecto | Plan original (Acta) | Plan replanificado (24/11) | Real |
|---|---|---|---|
| Fechas del ciclo | 26/11–02/12 (7 días) | 24/11–27/11 (4 días) | 24/11–27/11 |
| Hito H008 | 02/12 | 27/11 | 27/11 (`v0.6-ciclo6`): a tiempo frente al replanificado, 5 días antes del original |
| Código congelado | No fijado en el Acta | 27/11 en la noche | 27/11 a media tarde |
| Horas | El plan de horas del ciclo es el del lanzamiento | 81 h | 88 h (+9 %) |
| Alcance | Entregable 6 (Acta 3.4): aplicación web unida con los casos de uso del SRS, CU01 a CU06, y carga de DICOM y NIfTI | MoSCoW: CU01 a CU04, persistencia y RR-01; CU05 y DICOM si hay tiempo; CU06 y visor 3D fuera | CU01 a CU05 (CU02 solo NIfTI), persistencia y RR-01; CU06, visor 3D y DICOM fuera |
| Entregable 7 (evidencias de calidad) | Pruebas unitarias, de integración, funcionales, de usabilidad y de rendimiento; Dice e IoU | Igual, con usabilidad reducida a una prueba corta y sin pruebas automatizadas de la interfaz | Pruebas (229 pasan sin PostgreSQL y las de integración con PostgreSQL), RR-01 medido, Dice e IoU; RU-01 sin prueba con personas |

Contra el plan replanificado, el ciclo cumplió fechas y alcance, con un 9 % más de horas. Contra el plan original, terminó 5 días antes, pero con menos alcance: lo que falta (CU06, visor 3D, DICOM y RU-01) se documenta en el ciclo 7 como limitación de la versión entregada.

*Las horas plan son las del lanzamiento (`ciclo6_lanzamiento.md`); las reales, las del LOGT (`LOGT_registro_tiempos.md`, versión L14). Los defectos, los del LOGD con D-030 a D-032 del 27/11.*
