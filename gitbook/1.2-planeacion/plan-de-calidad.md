# Plan de gestión de la calidad

Establece cómo se incorpora, verifica y documenta la calidad de Prosta-AI: objetivos, roles, métricas, controles y aceptación de entregables.

## Ficha

| Campo | Detalle |
|---|---|
| Paquete EDT | 1.2.3 |
| Fecha y versión | 15/10/2026, versión 0.1 para revisión (archivo «versión cuarta entrega») |
| Responsable | Equipo Prosta-AI; Fernando José Angulo Núñez (Tester y Planeación) elabora el plan; aprueba el propietario |
| Formato | PDF de 19 páginas; plantilla PM² 3.0.1 |

## Contenido principal

* **Base:** Acta v1.1 del 08/10/2026; se aplica a los ocho entregables, a los documentos de gestión, al código, a los datos y al modelo.
* **Lectura del plan:** las metas del Acta se mantienen; los controles añadidos son propuestas hasta la aprobación del propietario, y un indicador sin evidencia se registra como «no medido», nunca como cumplido.
* **Objetivos:** flujo completo con evidencia de extremo a extremo, 100 % de requisitos con implementación y prueba trazable, Dice medio de 0,80 o más con procesamiento en 120 s o menos, cero datos identificables, aviso no diagnóstico en toda pantalla de resultados y al menos 6 de 7 ciclos cerrados a tiempo.
* **Proceso de cinco pasos:** definir características de calidad, aseguramiento, control, aceptación de entregables y aceptación final al cerrar el Ciclo 7.
* **Roles:** el propietario aprueba; Yimis programa revisiones y controla versiones; Juan David verifica requisitos, licencias y trazabilidad; Sergio revisa visualización y avisos; Yeison implementa controles y corrige defectos; Fernando diseña y ejecuta pruebas y valida métricas y anonimización. Se usa una matriz RASCI.
* **Técnicas:** revisión entre pares, revisión preventiva de riesgos, comparación de modelos con las mismas particiones, pruebas por niveles, análisis de causa y regresión, y priorización del alcance.
* **Herramientas:** Git y GitHub, pytest, scripts de PyTorch/MONAI, 3D Slicer o ITK-SNAP (inspección técnica, no radiológica), Google Colab gratuito y registros de la API.
* **Controles por ciclo:** fechas objetivo del 12/10 al 09/12 con un control preventivo y una evidencia de salida por cada ciclo (por ejemplo, manifiesto sin pacientes compartidos en el Ciclo 2 y Dice e IoU en el Ciclo 5).
* **Métricas de gestión (G01 a G06):** entregas a tiempo, ciclos completados, gestión aprobada, revisión de artefactos, hallazgos bloqueantes y acciones correctivas.
* **Métricas del producto (P01 a P08):** cobertura de trazabilidad del 100 %, flujo completo, Dice de 0,80 o más, procesamiento de 120 s o menos, aviso en 100 % de pantallas de resultados, cero datos identificables, cero pacientes compartidos entre particiones y reproducibilidad.
* **Criterios vitales:** incumplir privacidad, aviso no diagnóstico, flujo completo, trazabilidad o aprobación de la gestión impide declarar el proyecto exitoso.
* **Esfuerzo:** se mide en horas por ciclo, sin valores monetarios.
* **Exclusiones:** no se crean comités, oficina de proyectos ni auditoría externa.

El seguimiento operativo de estas métricas está en los [artefactos de control TSP](../1.4-monitoreo-y-control/artefactos-tsp.md).

## Documento original

* [Plan de calidad (PDF)](https://github.com/yimis-source/ProstaAIReal/tree/main/docs) — `docs/docsf/1.2 Planeación/1.2.3 Plan de Calidad - Prosta-AI (versión cuarta entrega).pdf`
