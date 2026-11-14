# Plan de gestión del alcance

Define cómo se define, valida y controla el alcance de Prosta-AI, e incluye el enunciado del alcance y el diccionario de la EDT.

## Ficha

| Campo | Detalle |
|---|---|
| Paquete EDT | 1.2.1 |
| Fecha y versión | 11/10/2026, versión 1.0 |
| Autor | Equipo Prosta-AI; responsable del alcance: Yimis Buenaventura |
| Formato | DOCX |

## Contenido principal

* **Procesos PMBOK 6:** planificar el alcance, recopilar requisitos, definir el alcance, crear la EDT, validar y controlar el alcance.
* **Línea base del alcance:** enunciado del alcance, [EDT](edt.md) y diccionario de la EDT, apoyados en la [matriz de trazabilidad](matriz-de-trazabilidad.md), los casos de uso CU01 a CU10 y la priorización MoSCoW.
* **Producto:** cinco funciones: cargar y validar estudios eliminando datos identificables, flujo automático con modelo tipo U-Net o nnU-Net, visualización de la ROI con aviso experimental, registro y consulta de estudios, y orientación con agentes de IA (opcional).
* **Entregables E1 a E8:** requisitos, datasets, diseño, modelo 3D, ROI, aplicación web, evidencias de calidad y documentación final, cada uno asignado a uno o más ciclos.
* **Criterios imprescindibles:** flujo operativo completo, requisitos con implementación y prueba, aviso en todas las pantallas de resultados y ningún dato personal almacenado (verificado por el Tester).
* **Criterios no imprescindibles:** Dice medio de 0,80 o más y procesamiento en 2 minutos o menos.
* **Exclusiones (Won't):** uso clínico, validación médica, datos identificables, registro ante el INVIMA, agentes autónomos, producción de alta disponibilidad, aplicación móvil y gestión de usuarios más allá del acceso básico.
* **Restricciones:** tiempo (calendario 2026-2), equipo de cinco, recursos gratuitos, datos públicos, stack predefinido, normativa y metodología impuesta.
* **Supuestos:** calidad suficiente de los datos públicos, capacitación posible con documentación pública, acceso a Google Colab y suficiencia de siete ciclos; se revisan en cada cierre de ciclo.
* **Control de cambios:** solicitud en GitHub con la etiqueta «cambio»; el director aprueba los menores y el propietario los que afecten alcance, entregables, hitos o requisitos Must o Won't.
* **MoSCoW como control:** si falta tiempo se protege el producto mínimo viable (Must) y se reducen primero los Should.
* **Aceptación:** el propietario acepta los entregables parciales en cada hito y el producto final mediante el acta de aceptación del Ciclo 7.

## Documento original

* [Plan de alcance v1.0 (DOCX)](https://github.com/yimis-source/ProstaAIReal/tree/main/docs) — `docs/docsf/1.2 Planeación/1.2.1 Plan de Alcance - Prosta-AI v1.0.docx`
