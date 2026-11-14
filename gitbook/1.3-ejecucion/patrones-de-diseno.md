# Informe de patrones de diseño aplicados

Explica seis patrones de diseño y cómo se aplican a Prosta-AI, vinculados a casos de uso, requisitos y arquitectura.

## Ficha

| Campo | Detalle |
|---|---|
| Paquete EDT | 1.3.2.2 |
| Fecha y versión | 22/10/2026 |
| Autores | Yimis Buenaventura, Juan David Riascos Erazo, Sergio Gabriel Meneses Silva, Yeison Bolaños Ruiz y Fernando José Angulo Núñez |
| Formato | PDF |

## Contenido principal

| Patrón | Para qué se usa en Prosta-AI |
|---|---|
| Facade | Una sola llamada para todo el procesamiento |
| Template Method | Orden fijo: control de calidad, preparación, segmentación, ROI y evaluación |
| Strategy | Cambiar el modelo de segmentación por configuración versionada |
| Chain of Responsibility | Validaciones encadenadas del archivo |
| State | Estados válidos del trabajo (pendiente, en proceso, completado, fallido) |
| Observer | Registrar avance y tiempos sin acoplar el procesamiento |

* El informe explica el concepto de patrón, su propósito, motivación y participantes.
* Cada patrón se relaciona con casos de uso, requisitos de la matriz y la [arquitectura de software](arquitectura-de-software.md).
* Se mencionan como complementarios opcionales Decorator, Adapter, Factory Method, Singleton y Composite.
* Es parte del entregable de diseño de la solución (Entregable 3).

## Documento original

* [Informe de patrones (PDF)](https://github.com/yimis-source/ProstaAIReal/tree/main/docs) — `docs/docsf/1.3 Ejecución/1.3.2.2 Informe de patrones de diseño aplicados.pdf`
* [Resumen en Markdown del repositorio](https://github.com/yimis-source/ProstaAIReal/tree/main/docs) — `docs/ejecucion/03_modulos.md`
