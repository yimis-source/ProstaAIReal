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

## Estado

| Hito / ciclo | Contenido | Estado |
|---|---|---|
| H001 | Acta, metodología TSP | Cerrado (05/10) |
| H002 | SRS, casos de uso, matriz de trazabilidad | Cerrado (12/10) |
| Ciclo 1 | Adquisición y comprensión de datos | Cerrado (25/10, `v0.1-ciclo1`) |
| Ciclo 2 | Control de calidad, formato NIfTI, división por paciente, preprocesamiento y diseño | Cerrado (30/10, `v0.2-ciclo2`) |
| Ciclo 3 | Segmentación 3D con el modelo preentrenado, inferencia y evaluación preliminar | Cerrado (10/11, `v0.3-ciclo3`; replanificado desde el 13/11) |
| Ciclo 4 | Generación de la región de interés (ROI) | En curso (08/11–12/11) |

## Estructura

```
docs/gestion/     Acta, metodología TSP, trazabilidad y registros TSP (tsp/)
docs/ejecucion/   Requisitos y diseño (arquitectura, pantallas, módulo de IA, base de datos)
docs/datos/       Criterios, elección del conjunto, fichas de licencia, revisión en 3D Slicer, informe de datos
scripts/          Descarga, inventario, anonimización, geometría, control de calidad, conversión a NIfTI,
                  verificación de fuga y preprocesamiento
entrenamiento/    División por paciente, evaluación (evaluar.py) y ajuste fino preparado (entrenar.py, cuaderno de Colab)
backend/          Paquete prosta_ai: pipeline de control de calidad, preparación, segmentación 3D y evaluación
docs-tecnicos/    Modelo preentrenado y licencias
reports/          datos/, calidad/, division/, evaluacion/ y rendimiento/: resultados de los scripts
tests/            Pruebas de los scripts
```

## Uso rápido

Requiere Python 3.12 con las versiones de `backend/pyproject.toml` (guía en `docs/entorno_desarrollo.md`).

```bash
python scripts/descargar_datos.py               # MSD Task05_Prostate (CC BY-SA 4.0) en datos/
python scripts/inventario_datos.py              # reports/datos/inventario_datos.md y .csv
python scripts/verificar_anonimizacion.py       # reports/datos/verificacion_anonimizacion.md
python scripts/analizar_geometria.py            # reports/datos/geometria.md
python scripts/control_calidad.py               # reports/calidad/control_calidad.md (RF-10)
python scripts/convertir_nifti.py               # datos/convertidos/ (NIfTI 3D)
python scripts/verificar_fuga.py                # reports/division/verificacion_division.md (RC-04)
python scripts/preprocesar.py ENTRADA SALIDA    # RAS, 0,5 mm, normalización
python scripts/descargar_modelo.py              # modelos/prostate_mri_anatomy (Apache 2.0)
python -m entrenamiento.evaluar --modelo prostate_mri_anatomy   # reports/evaluacion/
python scripts/medir_rendimiento.py             # reports/rendimiento/ (tarea 1408)
python -m pytest -q
```

Prostate158 y PROMISE12 se descargan a mano (ver `docs/datos/procedimiento_descarga.md`).

## Modelo y resultados

- Modelo: `prostate_mri_anatomy` v0.3.6 del MONAI Model Zoo (U-Net 3D, Apache 2.0), entrenado por sus autores
  con Prostate158; por eso Prostate158 no sirve para evaluarlo. Ver `docs-tecnicos/modelo-y-licencias.md`.
- Evaluación en los 5 casos de prueba de MSD Task05: **Dice 0,8925 ± 0,0340**, IoU 0,8071 ± 0,0534
  (meta RF-24: ≥ 0,80). Es una evaluación técnica preliminar; la formal es del ciclo 5.
- Rendimiento (CPU AMD Ryzen 5 5600G, sin GPU): 13–16 s por estudio, memoria pico ≈ 2 GB (RR-01: ≤ 120 s).
  La medición en GPU queda pendiente (Colab, ciclo 5).

## Datos

| Conjunto | Uso en Prosta-AI | Licencia |
|---|---|---|
| Medical Segmentation Decathlon, Task05_Prostate (32 casos con máscara) | Conjunto principal | CC BY-SA 4.0 |
| Prostate158 (139 casos de entrenamiento) | Respaldo, solo de referencia | Sin licencia indicada en Zenodo; el reto exige acuerdo de uso no comercial y sin redistribución |
| PROMISE12 (50 + 30 casos) | Solo referencia: 12 casos de MSD son el mismo estudio (ver `reports/division/`) | Condiciones del reto (registro) |

Detalle en `docs/datos/`. División por paciente de MSD Task05: 22 entrenamiento / 5 validación / 5 prueba
(semilla 2026, `entrenamiento/division_task05.json`). Ningún dato médico se sube al repositorio: `datos/`, imágenes (`*.nii*`, `*.mhd`,
`*.raw`, `*.dcm`), archivos comprimidos y pesos de modelos están en `.gitignore`.

Cita del conjunto principal: Antonelli, M. et al. The Medical Segmentation Decathlon. *Nat Commun* 13, 4128
(2022). https://doi.org/10.1038/s41467-022-30695-9
