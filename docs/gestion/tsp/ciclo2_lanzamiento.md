# Lanzamiento del ciclo 2 · Preprocesamiento, división por paciente y diseño

**Autor:** Fernando José Angulo Núñez (Gerente de planeación) · **Fecha:** 26/10/2026 · **Proyecto:** Prosta-AI, Universidad Santiago de Cali 2026-2

## 1. Contexto

El ciclo 1 cerró a tiempo el 25/10 (`v0.1-ciclo1`). Fechas planificadas del ciclo 2: **26/10 al 30/10/2026**, hito H004 del Acta. Etiqueta de cierre: `v0.2-ciclo2`. Es un ciclo corto (5 días), por eso las tareas de diseño (1306–1309) se empezaron a redactar el 22/10 en paralelo al cierre del ciclo 1; los documentos fuente tienen fecha 22–24/10 y se versionan en este ciclo.

## 2. Objetivos

1. Control de calidad de imágenes y máscaras (RF-10), con exclusión y registro del motivo.
2. Formato unificado NIfTI y script de preprocesamiento.
3. División por paciente 70/15/15 con semilla 2026 y verificación del Tester de que no hay pacientes repetidos ni fuga entre conjuntos.
4. Diseño de la solución (Entregable 3): arquitectura de sistema y de software, pantallas, módulo de IA y base de datos.
5. Revisión cruzada entre los documentos de diseño para encontrar inconsistencias.

## 3. Criterios de salida

| # | Criterio | Cómo lo comprobamos |
|---|---|---|
| 1 | El control de calidad corre sobre todos los conjuntos y deja un informe de aprobados y excluidos | `reports/calidad/control_calidad.md` |
| 2 | La división es reproducible (semilla y huella) y no repite pacientes | `entrenamiento/division_task05.json`, `reports/division/verificacion_division.md` |
| 3 | El informe del Tester revisa también la fuga entre MSD Task05 y PROMISE12 | `scripts/verificar_fuga.py` |
| 4 | Los cuatro documentos de diseño están versionados y sin inconsistencias abiertas (o registradas) | `docs/ejecucion/` |
| 5 | Pruebas unitarias en verde para los scripts nuevos | `tests/` |
| 6 | LOGD/LOGT, trazabilidad T2, PR a `main` y etiqueta `v0.2-ciclo2` | PR de cierre |

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
| 1300 | Postmortem ciclo 1 y lanzamiento ciclo 2 | Fernando | 26/10 | 3 |
| 1301 | Control de calidad (RF-10) | Yeison | 26/10–27/10 | 5 |
| 1302 | Formato unificado NIfTI | Yeison | 27/10 | 4 |
| 1303 | División por paciente 70/15/15 (semilla 2026) | Juan | 27/10–28/10 | 4 |
| 1304 | Informe del Tester: sin pacientes repetidos + fuga entre conjuntos | Fernando | 28/10–29/10 | 4 |
| 1305 | Script de preprocesamiento | Yeison | 29/10 | 4 |
| 1306 | Diseño de arquitectura (sistema y software) | Yimis | 22/10–28/10 | 8 |
| 1307 | Diseño de pantallas | Sergio | 22/10–28/10 | 10 |
| 1308 | Diseño del módulo de IA (componentes y patrones) | Yeison | 22/10–28/10 | 5 |
| 1309 | Diseño de base de datos | Juan | 22/10–28/10 | 5 |
| 1310 | Revisión cruzada (inconsistencias), cierre y etiqueta | Yimis / Juan | 29/10–30/10 | 4 |
| | **Total** | | | **56** |

## 6. Riesgos del Acta que tocan este ciclo

| Riesgo del Acta (3.8) | Qué hacemos en este ciclo |
|---|---|
| 4. Fuga de información entre entrenamiento y prueba que sobrestime el desempeño (Fernando, nivel 8) | Riesgo principal: la división por paciente y su verificación (Fernando, 1304). Comparamos también entre conjuntos, porque puede haber estudios repetidos. |
| 3. Datos insuficientes, incompletos, sesgados o con licencias con restricciones (Juan, nivel 12) | El control de calidad (1301) y el formato unificado (1302) cubren la parte de datos incompletos o dañados. |
| 6. Retrasos por baja disponibilidad de integrantes (cargas académicas o laborales) (Yimis, nivel 12) | Cinco días y 56 h planificadas: el diseño ya está adelantado desde el 22/10; si alguien se atrasa, Juan y Yimis se reparten la revisión cruzada. |
| 7. Problemas de integración entre frontend, backend y modelo al final (Yeison, nivel 12) | Los diseños de arquitectura y del módulo de IA (1306, 1308) dejan el pipeline desacoplado para integrar temprano. |
| 5. Que una salida experimental se tome como diagnóstico médico (Sergio, nivel 10) | El diseño de pantallas (1307) debe incluir el aviso de salida experimental y lenguaje no clínico. |

## 7. Entregable del ciclo

Segunda parte del Entregable 2 (datos preparados y divididos por paciente) y el Entregable 3 (diseño de la solución).

*Las horas son las del registro de tiempos (`LOGT_registro_tiempos.md`), reconstruidas a partir de la bitácora del equipo (simuladas para este registro).*
