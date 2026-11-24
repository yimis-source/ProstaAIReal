# Informe al Propietario del Proyecto: replanificación de los ciclos 6 y 7

**Para:** Ing. Jair Enrique Sanclemente Castro, Propietario del Proyecto · **De:** Equipo Prosta-AI · **Fecha:** 24/11/2026 · **Asunto:** Cambio de hitos y de alcance por el adelanto de la entrega al 28/11/2026 · **Referencia:** Acta de Constitución v1.1, sección 5.2.1; análisis de impacto `impacto_ciclo6.md` (tarea 1701)

Ingeniero:

Por el adelanto de la entrega final al 28/11/2026, replanificamos los ciclos 6 y 7. El cambio toca hitos y el contenido de entregables del Acta, así que, como pide la sección 5.2.1, se lo presentamos para su aprobación.

## 1. Qué cambia

| Ciclo | Antes | Ahora | Hito |
|---|---|---|---|
| 6 · Desarrollo web e integración completa (Entregables 6 y 7) | 26/11–02/12 | 24/11–27/11; código congelado la noche del 27/11 | H008: 02/12 → 27/11 |
| 7 · Cierre académico (Entregable 8) | 03/12–09/12 | 25/11–28/11, en paralelo con el ciclo 6 | H009: 09/12 → 28/11 |

Pasamos de 16 días de trabajo a 5. El plan del ciclo 6 (81 h) se mantiene, pero ahora en 4 días.

## 2. Por qué recortamos el alcance

El pipeline de segmentación está probado: Dice medio 0,8925 en los 5 casos de prueba y 14,1 s por estudio en CPU. La aplicación web todavía no existe, y en 4 días no alcanzamos a construir todos los casos de uso con pruebas. Preferimos entregar completo y probado el flujo vital del Acta (cargar, procesar, segmentar y ver la ROI con el aviso) que entregar todo a medias.

## 3. Qué se entrega el 28/11

- **CU01:** acceso básico (RF-01).
- **CU02:** carga de estudios en formato NIfTI, con validación de formato y tamaño, rechazo de archivos corruptos y eliminación de metadatos que identifiquen a una persona (RF-02 a RF-05).
- **CU03:** procesamiento en segundo plano desde el botón «Procesar», con el estado de cada etapa y los mensajes de error (RF-06 a RF-08). Se corrige el defecto D-006 (el botón decía «Ejecutar»).
- **CU04:** ROI superpuesta y comparación con y sin máscara, el aviso de uso no diagnóstico en todas las pantallas de resultados y el panel de explicación (RF-13 a RF-17).
- **Datos:** PostgreSQL y archivos en disco, sin datos personales (RB-01, RB-02).
- **Evidencias (Entregable 7):** pruebas unitarias y de la API, integración de punta a punta, rendimiento con los 5 casos de prueba enviados por la API (RR-01), métricas del ciclo 5 y una prueba corta de usabilidad.
- **Documentación final (Entregable 8):** instrucciones de ejecución, decisiones, riesgos residuales, lecciones aprendidas y acta de aceptación.

Se mantienen los 29 requisitos Must de la SRS. Uno cambia de contenido: si la carga de DICOM no alcanza a entrar, RF-03 admitirá solo NIfTI en esta versión.

## 4. Qué queda condicionado y qué queda fuera

| Elemento | Requisitos (prioridad SRS) | Decisión |
|---|---|---|
| CU05 · Historial de estudios | RF-19 (Should); el registro de RF-18 sí se hace | Entra solo si CU02 a CU04 pasan la prueba de integración el 26/11 a las 18:00 |
| Carga de DICOM en `.zip` | Parte de RF-02 y RF-03 (Must) | Después de CU05 y con la misma condición |
| Usabilidad completa | RU-01 (Should) | Se reduce a una prueba con 3 usuarios sobre la versión congelada |
| CU06 · Asistente de IA | RF-20 a RF-22 (Could) | Fuera de esta versión, como ya prevé la SRS para este componente |
| Visor 3D | No es requisito de la SRS | Fuera |

**Cómo se documenta:** lo que quede fuera se marca en la matriz de trazabilidad como «Fuera de la versión entregada», con la fecha de su aprobación. También se describe en el Entregable 8 como riesgo residual y trabajo futuro, y queda en el postmortem de los ciclos 6 y 7, que medirán contra las fechas nuevas y las originales. Con su aprobación, la tabla de hitos del Acta sube de versión mayor y el cambio se registra con la etiqueta «cambio» en el repositorio.

## 5. Efecto en los criterios de aceptación

- **Se mantienen** el flujo completo en la web, el Dice ≥ 0,80 (ya cumplido), el tiempo ≤ 2 minutos, el aviso en todas las pantallas de resultados y la ausencia de datos personales.
- **El criterio de «100 % de los requisitos aprobados con evidencia»** solo se cumple si usted aprueba que CU06, y lo condicionado que no entre, queden fuera de esta versión.

## 6. Plazo para objetar

Le pedimos su aprobación o sus objeciones **antes del miércoles 25/11/2026 a las 12:00**. Mientras tanto avanzamos en lo de la sección 3, que no cambia con ninguna de las dos respuestas. Si objeta algún punto, ajustamos el orden de lo condicionado dentro del mismo plazo del 28/11.

El análisis completo (requisito por requisito, horas, calidad y riesgos) está en `docs/gestion/replanificacion/impacto_ciclo6.md`.

Atentamente,

| Nombre | Rol |
|---|---|
| Yimis Buenaventura | Director de Proyecto / Líder |
| Juan David Riascos Erazo | Analista · Monitoreo y control |
| Fernando José Angulo Núñez | Tester · Planeación |
| Yeison Bolaños Ruiz | Desarrollador · Inicio |
| Sergio Gabriel Meneses Silva | Diseñador · Cierre |

*Uso académico y experimental. Los resultados de Prosta-AI no son un diagnóstico, no sustituyen la valoración de un profesional de la salud y la aplicación no es un dispositivo médico.*
