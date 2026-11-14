# Arquitectura de software

Detalla los componentes internos de Prosta-AI, sus responsabilidades y dependencias, y cubre los casos de uso y requisitos de la matriz.

## Ficha

| Campo | Detalle |
|---|---|
| Paquete EDT | 1.3.2.4 |
| Fecha y versión | 22/10/2026 |
| Autores | Yeison Bolaños Ruiz, Juan David Riascos Erazo, Sergio Gabriel Meneses Silva, Yimis Buenaventura y Fernando José Angulo Núñez |
| Formato | PDF |

## Contenido principal

* **Actividades:** corresponde a las actividades 1306 a 1309 del Ciclo 2.
* **Estilo elegido:** monolito modular de un solo proceso, frente a un backend con ejecutor separado y a microservicios.
* **Siete componentes:** presentación React, API y servicios (FastAPI), validación y preparación, segmentación y ROI, evaluación (Dice e IoU), repositorios y archivos (PostgreSQL), y orientación opcional con agentes de IA.
* **Coordinación:** la API nunca invoca directamente la segmentación; la tabla de trabajos en PostgreSQL es el punto de coordinación.
* **Control de factibilidad:** el tiempo de inferencia se mide en el Ciclo 3 (actividad 1408); si supera 120 s se usa un modelo más ligero o menor resolución (Colab solo para pruebas).
* **Cobertura:** una tabla relaciona los casos de uso con componentes para comprobar que cubren los requisitos de la matriz.
* **Alcance:** esquemas de tablas, rutas y algoritmos quedan para entregables posteriores.
* **Complemento:** véase la [justificación de la arquitectura](justificacion-arquitectura.md) y la [arquitectura de datos](arquitectura-de-datos.md).

## Documento original

* [Arquitectura de software (PDF)](https://github.com/yimis-source/ProstaAIReal/tree/main/docs) — `docs/docsf/1.3 Ejecución/1.3.2.4 Arquitectura de software.pdf`
* [Resumen en Markdown del repositorio](https://github.com/yimis-source/ProstaAIReal/tree/main/docs) — `docs/ejecucion/02_arquitectura.md`
