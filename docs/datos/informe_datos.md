# Informe de datos del ciclo 1

| Campo | Valor |
|---|---|
| Tarea | 1208 |
| Responsable | Juan David Riascos Erazo (Analista), con apoyo de Sergio Gabriel Meneses Silva |
| Fecha | 24/10/2026 |
| Versión | 1.0 |

Resume lo que se hizo en el ciclo 1 (adquisición y comprensión de datos). Todas las cifras salen de los informes generados en `reports/datos/`.

## 1. Criterios y elección

Criterios en [`criterios_seleccion.md`](criterios_seleccion.md); decisión en [`eleccion_dataset.md`](eleccion_dataset.md); una ficha por conjunto en [`fichas/`](fichas/).

| Conjunto | Papel | Motivo |
|---|---|---|
| MSD Task05_Prostate | **Principal** | Licencia clara (CC BY-SA), con máscaras de zona periférica y de transición |
| Prostate158 | Respaldo, **solo de referencia** | Licencia no verificada; no se usa para entrenar |
| PROMISE12 | Para comparar | Licencia del reto por verificar; falta comprobar pacientes compartidos con MSD (tarea 1304) |

## 2. Inventario

Fuente: [`reports/datos/inventario_datos.md`](../../reports/datos/inventario_datos.md) (detalle con SHA-256 en `inventario_datos.csv`).

| Conjunto | Casos | Archivos de imagen | Tamaño (MB) |
|---|---|---:|---:|
| MSD Task05_Prostate | 32 con máscara + 16 sin máscara | 80 | 239,8 |
| Prostate158 (entrenamiento) | 139 | 844 | 2784,6 |
| PROMISE12 (entrenamiento) | 50 | 200 | 786,5 |
| PROMISE12 (prueba) | 30 | 120 | 466,6 |

PROMISE12 trae un archivo `a.py` no esperado en cada carpeta. No es dato: no se abre ni se ejecuta.
La carpeta de prueba de PROMISE12 trae 30 máscaras (`*_segmentation.mhd`); la ficha quedó corregida con esto.

## 3. Anonimización

Fuente: [`reports/datos/verificacion_anonimizacion.md`](../../reports/datos/verificacion_anonimizacion.md). Resultado: **sin hallazgos** (844 NIfTI de Prostate158, 80 de MSD, 100 + 60 MetaImage de PROMISE12; sin DICOM, nombres neutros, sin fechas en nombres).
El único texto libre es `descrip = «5.0.10»` en los 80 NIfTI de MSD: es una cadena de versión de software, no un dato personal.

## 4. Geometría

Fuente: [`reports/datos/geometria.md`](../../reports/datos/geometria.md).

| Conjunto | Forma más frecuente | Espaciado en plano (mm) | Grosor de corte (mm) | Orientación | Volumen próstata (mL) |
|---|---|---|---|---|---|
| msd_task05 (32) | 320x320x20 (8 formas) | 0,600–0,750 | 3,00–4,00 (mediana 3,60) | RAS | 16,0–315,4 (mediana 62,0) |
| prostate158 (139) | 270x270x24 (15 formas) | 0,272–0,469 | 3,00 | LPS | 14,8–197,4 (mediana 52,4) |
| promise12 entrenamiento (50) | 320x320x24 (19 formas) | 0,273–0,750 | 2,20–4,00 | LPS | 14,9–315,4 (mediana 43,2) |
| promise12 prueba (30) | 320x320x24 (11 formas) | 0,273–0,625 | 2,20–3,60 | LPS | 23,6–114,0 (mediana 39,0) |

- MSD tiene 2 canales (T2 y ADC), cortes de 11–24 y grosor 3–4 mm.
- MSD viene en RAS y los demás en LPS: hay que unificar la orientación.
- Los espaciados y formas varían entre casos, así que hace falta remuestrear.
- El volumen máximo de PROMISE12 entrenamiento (315,4 mL) coincide con el de prostate_16 de MSD: **indicio de pacientes compartidos** entre ambos conjuntos.

## 5. Revisión en 3D Slicer

Detalle en [`revision_3d_slicer.md`](revision_3d_slicer.md). Revisión solo visual (sin métricas): máscaras alineadas, máscara escalonada por los cortes de 3–4 mm, ADC con menos resolución, sin datos personales visibles.

## 6. Riesgos

| Riesgo | Efecto | Respuesta |
|---|---|---|
| Fuga entre MSD y PROMISE12 (pacientes compartidos) | Evaluación inflada | Verificar en 1304 y no mezclar hasta entonces |
| Licencias de Prostate158 y PROMISE12 sin verificar | No poder usarlos para entrenar o redistribuir | Solo referencia/comparación, no se suben |
| Pocos casos (32 con máscara) y volúmenes muy variables | Conjuntos de validación poco representativos | Dividir por paciente cuidando los extremos |
| Corte grueso (3–4 mm) | Máscaras escalonadas en sagital/coronal | Tenerlo en cuenta al preprocesar |

## 7. Decisiones para el ciclo 2

1. Control de calidad de imágenes y máscaras (`scripts/control_calidad.py`).
2. Formato unificado NIfTI (conversión de los MetaImage de PROMISE12).
3. División por paciente de MSD Task05.
4. Verificar fuga con PROMISE12 (`scripts/verificar_fuga.py`, tarea 1304), partiendo del indicio de 315,4 mL.
