# Arquitectura del sistema

Describe Prosta-AI en bloques grandes: qué partes tiene, qué información intercambian y dónde se ejecuta cada una.

## Ficha

| Campo | Detalle |
|---|---|
| Paquete EDT | 1.3.2.3 |
| Fecha y versión | 22/10/2026 |
| Autores | Yeison Bolaños Ruiz, Juan David Riascos Erazo, Sergio Gabriel Meneses Silva, Yimis Buenaventura y Fernando José Angulo Núñez |
| Formato | PDF |

## Contenido principal

* **Base teórica:** Sommerville (2011); es una vista de bloques, distinta de la [arquitectura de software](arquitectura-de-software.md), que detalla el interior del backend.
* **Alternativas comparadas:** monolítica, cliente-servidor en capas (elegida) y microservicios (descartada por desproporcionada).
* **Capas:** presentación en React, aplicación en FastAPI, procesamiento de imagen con PyTorch/MONAI y persistencia en PostgreSQL con almacenamiento privado.
* **Nodos:** equipo del usuario (navegador), servidor de la aplicación, Google Colab (entrenamiento, fuera de la aplicación en uso) y GitHub (código y documentación).
* **Flujo principal:** acceso, carga con validación, botón «Procesar» que crea un trabajo pendiente, tarea local de preparación y segmentación, y visualización de la ROI con el aviso experimental.
* **Estados del trabajo:** pendiente, en proceso, completado o fallido, con posibilidad de reintento.
* **Atributos que guiaron la decisión:** rendimiento de 2 minutos o menos, protección de datos, mantenibilidad, reproducibilidad y restricciones del equipo.

## Documento original

* [Arquitectura del sistema (PDF)](https://github.com/yimis-source/ProstaAIReal/blob/main/docs/docsf/1.3%20Ejecuci%C3%B3n/1.3.2.3%20Arquitectura%20del%20sistema.pdf)
* [Resumen en Markdown del repositorio](https://github.com/yimis-source/ProstaAIReal/blob/main/docs/ejecucion/02_arquitectura.md)
