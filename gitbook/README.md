# Prosta-AI

**Prosta-AI** es un proyecto académico de la Universidad Santiago de Cali (Facultad de Ingeniería, Programa de Ingeniería de Sistemas), desarrollado en la asignatura Gestión de Proyectos de TI, periodo 2026-2. Consiste en una aplicación web que carga estudios de resonancia magnética (MRI) de próstata públicos y anonimizados, los segmenta en 3D con un modelo de IA y muestra la región de interés (ROI) superpuesta a la imagen original.

> **Aviso de uso académico.** Prosta-AI es experimental y educativa. **No es diagnóstica**, no tiene uso clínico, no es un dispositivo médico y sus resultados no deben usarse para tomar decisiones sobre la salud de nadie.

El proyecto se gestiona con la Guía del PMBOK (sexta edición) y plantillas PM²/Open PM; el producto se desarrolla con TSP (Team Software Process) en siete ciclos. Los requisitos siguen la norma ISO/IEC/IEEE 29148. El docente y propietario del proyecto es el Ing. Jair Enrique Sanclemente Castro.

## Equipo y roles

| Integrante | Rol de desarrollo | Rol de gestión |
|---|---|---|
| Yimis Buenaventura | Director de proyecto / Líder | Trazabilidad |
| Juan David Riascos Erazo | Analista | Monitoreo y control |
| Sergio Gabriel Meneses Silva | Diseñador | Cierre |
| Yeison Bolaños Ruiz | Desarrollador | Inicio |
| Fernando José Angulo Núñez | Tester | Planeación |
| Jair Enrique Sanclemente Castro | Docente y propietario del proyecto | |

## Cómo está organizado el libro

El libro sigue la Estructura de Desglose del Trabajo (EDT) por grupos de procesos. Cada página resume un documento entregado y enlaza al original en GitHub.

| Grupo | Contenido | Primera página |
|---|---|---|
| 1.1 Inicio | Acta de constitución y matriz de partes interesadas | [Acta de constitución](1.1-inicio/acta-de-constitucion.md) |
| 1.2 Planeación | Planes de dirección, alcance, tiempo y calidad; trazabilidad, EDT, actividades, hitos y cronograma | [Plan para la dirección](1.2-planeacion/plan-para-la-direccion.md) |
| 1.3 Ejecución | Requisitos, casos de uso, diseño y arquitecturas | [Requisitos](1.3-ejecucion/requisitos.md) |
| 1.4 Monitoreo y control | Artefactos de control TSP | [Artefactos TSP](1.4-monitoreo-y-control/artefactos-tsp.md) |
| Desarrollo | Avance del producto por ciclo | [Avance del desarrollo](desarrollo/README.md) |

## Calendario de hitos

Fechas de la Lista de hitos (11/10/2026), coherentes con el Acta de constitución. Más detalle en [Lista de hitos](1.2-planeacion/lista-de-hitos.md) y [Cronograma](1.2-planeacion/cronograma.md).

| Hito | Fecha | Qué se entrega |
|---|---|---|
| H001 | 05/10/2026 | Acta aprobada, registro de interesados y requisitos iniciales archivados en la carpeta de gestión. |
| H002 | 12/10/2026 | Plan para la Dirección del Proyecto aprobado y especificación de requisitos con matriz de trazabilidad (Entregable 1). |
| H003 | 25/10/2026 | Ciclo 1 cerrado: fichas de cada dataset (procedencia, licencia, criterios de inclusión y exclusión) e informe de datos. |
| H004 | 30/10/2026 | Ciclo 2 cerrado: datos preprocesados y divididos por paciente, con informe del Tester sobre la ausencia de mezcla (Entregable 2), y diseño de la solución (Entregable 3). |
| H005 | 13/11/2026 | Ciclo 3 cerrado: modelo de segmentación 3D operativo que procesa un estudio de prueba, con configuración y pesos documentados (Entregable 4). |
| H006 | 20/11/2026 | Ciclo 4 cerrado: ROI superpuesta a la imagen original, con explicación, límites y aviso de uso experimental (Entregable 5). |
| H007 | 25/11/2026 | Ciclo 5 cerrado: informe con Dice e IoU, análisis de errores y limitaciones, y confirmación de la división por paciente. |
| H008 | 02/12/2026 | Ciclo 6 cerrado: aplicación web con el flujo completo operativo y evidencias de calidad (Entregables 6 y 7). |
| H009 | 09/12/2026 | Ciclo 7 cerrado: cierre académico, documentación final completa y repositorio organizado; el docente acepta la finalización (Entregable 8). |

## Repositorio

Código y documentos: [github.com/yimis-source/ProstaAIReal](https://github.com/yimis-source/ProstaAIReal).
