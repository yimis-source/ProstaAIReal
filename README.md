# Prosta-AI

Aplicación web académica y experimental para la segmentación 3D de la próstata en resonancia magnética
(MRI) y la visualización de la región de interés (ROI). Proyecto del curso Gestión de Proyectos de TI,
Ingeniería de Sistemas, Universidad Santiago de Cali, periodo 2026-2.

> **Uso académico y experimental. Los resultados no son un diagnóstico, no sustituyen la evaluación de un
> profesional de la salud y la aplicación no es un dispositivo médico.**

## Alcance

- Solo conjuntos de datos públicos y anónimos, con procedencia y licencia documentadas (Ley 1581 de 2012,
  Decreto 1377 de 2013).
- Modelo de segmentación 3D (U-Net / nnU-Net con PyTorch y MONAI), evaluado con Dice e IoU.
- Aplicación web: React, FastAPI, PostgreSQL y almacenamiento de archivos.
- Gestión con PMBOK 6 (plantillas Open PM / PM²); desarrollo con **TSP en 7 ciclos**; requisitos según
  ISO/IEC/IEEE 29148. Detalle en el [Acta de Constitución](docs/gestion/Acta_de_Constitucion-Prosta-AI-1.pdf)
  y en la [metodología TSP](docs/gestion/metodologia_tsp.md).

## Equipo

| Integrante | Rol de desarrollo | Grupo de procesos | Rol TSP |
|---|---|---|---|
| Yimis Buenaventura | Director de Proyecto / Líder | Trazabilidad | Líder del equipo |
| Juan David Riascos Erazo | Analista | Monitoreo y control | Gerente de calidad y proceso |
| Sergio Gabriel Meneses Silva | Diseñador | Cierre | Gerente de soporte |
| Yeison Bolaños Ruiz | Desarrollador | Inicio | Gerente de desarrollo |
| Fernando José Angulo Núñez | Tester | Planeación | Gerente de planeación |

Propietario del Proyecto: Ing. Jair Enrique Sanclemente Castro (docente).

## Ramas y versiones

- `main`: versión entregada; solo recibe merges desde `desarrollo` al cerrar un hito o un ciclo.
- `desarrollo`: integración. Todo cambio entra por pull request revisado.
- Una rama por integrante: `lider/yimis-buenaventura`, `analista/juan-riascos`, `disenador/sergio-meneses`,
  `desarrollador/yeison-bolanos`, `tester/fernando-angulo`. Antes de trabajar, cada rama se sincroniza con
  `desarrollo`.
- Al cerrar cada ciclo: pull request `desarrollo → main` y etiqueta `v0.N-cicloN`.
- Mensajes de commit: `tipo(ámbito): descripción` con `feat`, `fix`, `docs`, `test` o `chore`.

## Estructura

```
docs/gestion/     Acta, metodología TSP y registros TSP (tsp/)
docs/ejecucion/   Requisitos y diseño (a partir de H002)
```

## Datos

Ningún dato médico se sube al repositorio: `datos/`, imágenes (`*.nii*`, `*.mhd`, `*.raw`, `*.dcm`),
archivos comprimidos y pesos de modelos están en `.gitignore`.
