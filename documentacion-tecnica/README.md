# Prosta-AI: documentación técnica

Prosta-AI es un proyecto académico (Gestión de Proyectos de TI, Ingeniería de Sistemas, Universidad Santiago de
Cali, 2026-2) que segmenta en 3D la próstata en resonancia magnética (NIfTI), devuelve la región de interés (ROI)
a la rejilla de la imagen original, exporta una imagen de la ROI con un aviso impreso y mide Dice e IoU contra
una máscara de referencia.

> **Uso académico y experimental.** Los resultados no son un diagnóstico, no sustituyen la valoración de un
> profesional de la salud y el programa no es un dispositivo médico.

## Organización

| Página | Contenido |
|---|---|
| [Introducción](introduccion.md) | Propósito y alcance actual |
| [Instalación](instalacion.md) | Requisitos, entorno, datos, modelo y pruebas |
| [Arquitectura](arquitectura.md) | Carpetas, componentes y diagramas |
| [Código](codigo.md) | Módulos del pipeline, scripts y entrenamiento |
| [Flujo](flujo.md) | De la entrada NIfTI a la máscara, la imagen y las métricas |
| [Uso](uso.md) | Comandos reales y salidas esperadas |
| [Decisiones](decisiones.md) | Tecnologías elegidas y por qué |
| [Limitaciones](limitaciones.md) | Límites conocidos y mejoras previstas |

## Estado actual

El desarrollo sigue TSP en 7 ciclos. Los ciclos 1 a 4 están cerrados (etiquetas `v0.1-ciclo1` a `v0.4-ciclo4`):
datos, control de calidad y división por paciente; segmentación 3D con un modelo preentrenado; ROI e imagen con
aviso. Paquete `prosta-ai` versión 0.4.0. Los ciclos 5 (evaluación técnica), 6 (aplicación web) y 7 (cierre)
están pendientes.
