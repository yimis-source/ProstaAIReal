# Metodología TSP adaptada al curso · Prosta-AI

**Autor:** Yimis Buenaventura (Líder) · **Fecha:** 03/10/2026 · **Versión:** 1.0 · Universidad Santiago de Cali, Gestión de Proyectos de TI, 2026-2

Este documento explica cómo vamos a usar el Team Software Process (TSP) en Prosta-AI. El Acta de Constitución (02/10/2026) dice que el desarrollo se hace con TSP en siete ciclos y la gestión con PMBOK 6; aquí bajamos eso a reglas concretas. No es el TSP completo: lo adaptamos a un equipo de cinco estudiantes con dedicación parcial.

## 1. Los siete ciclos

Trabajamos de forma incremental: cada ciclo deja algo que funciona o está documentado, termina con un PR a `main` y una etiqueta de versión.

| Ciclo | Fechas planificadas | Contenido | Hito del Acta | Etiqueta |
|---|---|---|---|---|
| 1 | 13/10–25/10 | Adquisición y comprensión de datos (parte del Entregable 2) | H003 · 25/10 | `v0.1-ciclo1` |
| 2 | 26/10–30/10 | Preprocesamiento, división por paciente (Entregable 2) y diseño de la solución (Entregable 3) | H004 · 30/10 | `v0.2-ciclo2` |
| 3 | 31/10–13/11 | Segmentación 3D, modelo e inferencia (Entregable 4) | H005 · 13/11 | `v0.3-ciclo3` |
| 4 | 14/11–20/11 | Generación del mapa/ROI (Entregable 5) | H006 · 20/11 | `v0.4-ciclo4` |
| 5 | 21/11–25/11 | Evaluación técnica del modelo: métricas, errores y limitaciones | H007 · 25/11 | `v0.5-ciclo5` |
| 6 | 26/11–02/12 | Desarrollo web e integración completa (Entregables 6 y 7) | H008 · 02/12 | `v0.6-ciclo6` |
| 7 | 03/12–09/12 | Cierre académico: documentación final, lecciones aprendidas y acta de aceptación (Entregable 8) | H009 · 09/12 | `v0.7-ciclo7` |

Hitos del Acta (sección 4.2) que enmarcan los ciclos:

| Hito | Fecha | Descripción |
|---|---|---|
| H001 | 05/10 | Aprobación del Acta, registro de interesados y requisitos iniciales |
| H002 | 12/10 | Plan de dirección y especificación de requisitos (Entregable 1) |
| H003 a H009 | 25/10, 30/10, 13/11, 20/11, 25/11, 02/12, 09/12 | Cierre de los ciclos 1 a 7 |

Las fechas del Acta son tentativas. Si un ciclo se replanifica, se sigue la sección 9.

## 2. Fases de cada ciclo

| # | Fase | Qué pasa |
|---|---|---|
| 1 | Lanzamiento | Se escribe `cicloN_lanzamiento.md`: objetivos, criterios de salida, tareas con responsable, fechas y horas plan, riesgos del Acta que tocan el ciclo |
| 2 | Requisitos y diseño | Se revisan los requisitos del ciclo (SRS y matriz) y se diseña lo que haga falta antes de codificar o redactar |
| 3 | Implementación | Cada persona trabaja en su rama y anota las horas reales en el LOGT |
| 4 | Revisión por PR | Todo cambio entra a `desarrollo` con un PR revisado por otra persona; los defectos que se encuentren se registran en el LOGD |
| 5 | Prueba | El Tester prueba antes de cada integración (unitarias, con datos sintéticos y verificaciones de los scripts) |
| 6 | Postmortem | Plan frente a real, defectos, valor ganado, ayudas, qué funcionó y qué no, acciones para el siguiente ciclo |
| 7 | Cierre | Trazabilidad actualizada, LOGD y LOGT al día, PR `desarrollo` → `main` y etiqueta `v0.N-cicloN` |

## 3. Roles

Cada integrante tiene tres roles: el de **desarrollo** del Acta, el de **gestión** (grupo de procesos PMBOK) y uno de **TSP** (gerente). El Acta no los llamaba así; los asignamos al adoptar TSP.

| Persona | Rol de desarrollo (Acta) | Grupo de procesos / gestión (Acta) | Rol TSP |
|---|---|---|---|
| Yimis Buenaventura | Líder / Director de Proyecto | Trazabilidad | Líder |
| Yeison Bolaños Ruiz | Desarrollador | Inicio | Gerente de desarrollo |
| Fernando José Angulo Núñez | Tester | Planeación | Gerente de planeación |
| Juan David Riascos Erazo | Analista | Monitoreo y control | Gerente de calidad y proceso |
| Sergio Gabriel Meneses Silva | Diseñador | Cierre | Gerente de soporte |
| Jair Enrique Sanclemente Castro | Propietario del Proyecto (docente) | | |

Qué hace cada rol TSP:

| Rol TSP | Responsabilidades |
|---|---|
| Líder | Coordinar, resolver bloqueos, hacer los merge de los PR, aprobar replanificaciones, mantener la trazabilidad y la versión del repositorio |
| Gerente de desarrollo | Estrategia de implementación, estándares de código, estimar el esfuerzo técnico |
| Gerente de planeación | Plan de cada ciclo, LOGT, lanzamientos y postmortems, seguimiento del valor ganado |
| Gerente de calidad y proceso | LOGD, rendimiento de revisión, listas de verificación y cumplimiento del proceso (revisión por PR, pruebas) |
| Gerente de soporte | Entorno y herramientas (por ejemplo 3D Slicer, guía de instalación), configuración, versiones fijadas |

## 4. Quién hace qué en cada fase

| Fase | Quién | Producto |
|---|---|---|
| Lanzamiento del ciclo N | Fernando, con aprobación de Yimis | `cicloN_lanzamiento.md` y el plan de tiempos en el LOGT |
| Requisitos y diseño | Juan (requisitos), Sergio (interfaz), Yimis y Yeison (arquitectura y módulos) | Documentos en `docs/` |
| Implementación | El responsable de cada tarea | Código, scripts, informes |
| Revisión por PR | Una persona distinta de quien escribió el cambio; Juan registra defectos en el LOGD | Aprobación del PR y entradas en LOGD |
| Prueba | Fernando (Tester) | Pruebas, informes, verificación antes de integrar |
| Postmortem | Fernando | `cicloN_postmortem.md` |
| Cierre | Yimis (merge y etiqueta), Juan (LOGD), Fernando (LOGT) | PR a `main` y etiqueta |

Regla de tiempos: **el postmortem del ciclo N y el lanzamiento del ciclo N+1 los hace Fernando al iniciar el ciclo N+1** (aparecen juntos en un mismo PR). **El postmortem del último ciclo entra en su propio PR antes del merge de cierre**, para que quede dentro de la etiqueta.

## 5. Registros TSP

Viven en `docs/gestion/tsp/`:

| Archivo | Autor | Qué tiene |
|---|---|---|
| `cicloN_lanzamiento.md` | Fernando | Plan del ciclo N |
| `cicloN_postmortem.md` | Fernando | Análisis del ciclo N |
| `LOGD_registro_defectos.md` | Juan | Todos los defectos del proyecto |
| `LOGT_registro_tiempos.md` | Fernando | Horas plan frente a real por persona y tarea |

Son documentos vivos: el LOGD y el LOGT son un solo archivo que crece (una versión por entrega).

### 5.1 LOGD

Columnas: ID (D-001, D-002, …), fecha, ciclo, tarea, tipo, fase en que se inyectó, fase en que se removió, tiempo de corrección, descripción, quién lo encontró, quién lo corrigió y PR.

Tipos de defecto (TSP):

| Tipo | Nombre |
|---:|---|
| 10 | Documentación |
| 20 | Sintaxis |
| 30 | Construcción / paquetes |
| 40 | Asignación |
| 50 | Interfaz |
| 60 | Chequeo |
| 70 | Datos |
| 80 | Función |
| 90 | Sistema |
| 100 | Entorno |

Fases: REQ (requisitos), DIS (diseño), IMP (implementación), REV (revisión), EJE (ejecución), PU (prueba unitaria), INT (integración). El resumen por ciclo incluye el rendimiento de revisión: porcentaje de defectos encontrados en REV, es decir, antes de la prueba.

### 5.2 LOGT

- Por ciclo, una tabla por tarea con responsable, horas plan, horas reales, desviación, valor planificado y valor ganado.
- **Desviación = (real − plan) / plan.**
- **Valor planificado** de una tarea = sus horas plan / horas plan del ciclo.
- **Valor ganado** = suma del valor planificado de las tareas terminadas.
- **Ayudas:** las horas que una persona le dedica a una tarea de otra se registran aparte (quién ayudó a quién, horas y tarea), no se cargan a la tarea.
- Totales por persona y horas por día.
- Las horas son una reconstrucción a partir de la bitácora del equipo; se dice así al pie del LOGT.

## 6. Ramas, PR y etiquetas

```
main  <-  desarrollo  <-  lider | analista | desarrollador | disenador | tester
```

| Regla | Detalle |
|---|---|
| Ramas por rol | `lider`, `analista`, `desarrollador`, `disenador`, `tester`; cada una sale de `desarrollo` |
| PR a `desarrollo` | Revisados por otra persona; los hace merge Yimis |
| PR de cierre | Al final de cada ciclo, `desarrollo` → `main`, solo cuando se cumplen los criterios de salida |
| Etiquetas | `v0.N-cicloN` sobre el merge de cierre (por ejemplo `v0.1-ciclo1`); el Acta pide un registro de revisión y aceptación por ciclo |
| Mensajes de commit | Convencionales (`feat:`, `fix:`, `docs:`, `test:`), con co-autor cuando se trabajó en pareja |
| Datos y modelos | No se versionan (`datos/`, `modelos/` y `salidas/` están en `.gitignore`) |

## 7. Numeración de tareas

El primer dígito después del 1 es el ciclo más uno, y los dos últimos son el consecutivo; el 00 es el lanzamiento (y, desde el ciclo 2, el postmortem anterior).

| Ciclo | Rango | Ejemplo |
|---|---|---|
| 1 | 12xx | 1200 lanzamiento, 1201 criterios de selección |
| 2 | 13xx | 1300 postmortem 1 y lanzamiento 2 |
| 3 | 14xx | 1401 lanzamiento y replanificación |
| 4 | 15xx | 1501 lanzamiento |
| 5 | 16xx | |
| 6 | 17xx | |
| 7 | 18xx | |

Las tareas de Inicio llevan I01, I02… y las de H002 llevan H01, H02…

## 8. Criterios de salida de un ciclo

Un ciclo se da por cerrado cuando se cumple todo esto:

1. Cada tarea planificada está terminada, o su aplazamiento está registrado con motivo en el postmortem.
2. Todos los PR del ciclo fueron revisados y entraron a `desarrollo`; las pruebas están en verde.
3. Los criterios de salida del lanzamiento del ciclo se verificaron uno por uno.
4. LOGD y LOGT están actualizados; los defectos abiertos están anotados con el ciclo en que se corrigen.
5. La matriz de trazabilidad (`docs/gestion/trazabilidad.md`) refleja lo que existe.
6. El postmortem está escrito (el del último ciclo, antes del merge de cierre).
7. El Líder hace el PR `desarrollo` → `main` y pone la etiqueta `v0.N-cicloN`.
8. Verificación del Tester de que no queda ningún dato personal en el repositorio (criterio de aceptación 6 del Acta).

## 9. Replanificación

Cambiar las fechas de un ciclo se trata como cambio de proyecto (Acta, 5.2):

1. Se propone y se registra **en el lanzamiento** del ciclo, en una sección «Replanificación» con fechas originales y nuevas, motivo, efectos y cómo se manejan.
2. Juan analiza el impacto en alcance, tiempo, calidad y riesgos.
3. **Aprueba el Líder** si no cambia entregables; si cambia el alcance o los hitos del Acta, **se informa al Propietario del Proyecto** (docente), que puede objetar.
4. Se actualizan los documentos afectados (LOGT con el plan nuevo, calendario) y se sube la versión.
5. En el postmortem se mide contra las fechas replanificadas y también contra el plan original.

## 10. Cómo se relaciona con la gestión PMBOK

| Grupo de procesos | Dónde se ve |
|---|---|
| Inicio | Acta, matriz de interesados |
| Planificación | Lanzamientos de ciclo, LOGT con el plan |
| Ejecución | Implementación y PR |
| Monitoreo y control | LOGD, LOGT, replanificaciones, revisión de riesgos |
| Cierre | Postmortems, trazabilidad, etiqueta y acta de aceptación del ciclo 7 |
