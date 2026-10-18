# Ficha de conjunto: Prostate158

| Campo | Valor |
|---|---|
| Tarea | 1203 |
| Responsable | Juan David Riascos Erazo (Analista), con apoyo de Yimis Buenaventura |
| Fecha | 17/10/2026 |
| Versión | 1.0 |

| Ítem | Detalle |
|---|---|
| Nombre | Prostate158 (MRI de próstata a 3 T con anotación experta) |
| Fuente / URL | Zenodo: https://doi.org/10.5281/zenodo.6481141 ; reto: https://prostate158.grand-challenge.org/ |
| Cita | Adams, L. C., Makowski, M. R., Engel, G., Rattunde, M., Busch, F., Asbach, P., … Bressem, K. K. Prostate158 – An expert-annotated 3T MRI dataset and algorithm for prostate cancer detection. *Comput Biol Med* 148:105817 (2022). doi: 10.1016/j.compbiomed.2022.105817 |
| Institución | Charité – Universitätsmedizin Berlin |
| Licencia | **No verificada como CC-BY.** Zenodo lo publica como acceso abierto **sin indicar una licencia**. El sitio del reto exige aceptar un acuerdo de uso |
| Qué permite | Uso personal de investigación no comercial (según el acuerdo del reto) |
| Qué exige / prohíbe | No redistribuir los datos, no usarlos con fines comerciales ni para atención de pacientes. El texto completo del acuerdo se debe volver a leer antes de cualquier uso nuevo (por verificar el detalle) |
| Condiciones de uso en Prosta-AI | Solo referencia. No se redistribuye ni se sube al repositorio. No se usa como conjunto principal |
| Modalidades | T2, ADC y DWI (columnas de los csv de entrenamiento y validación) |
| Casos | 139 descargados (119 en `train.csv` y 20 en `valid.csv`), según el inventario y los csv. El conjunto completo publicado es de 158 pacientes; los casos de prueba **no** se descargaron |
| Archivos | 844 de imagen y máscara, 2 de metadatos (los csv), 0 no esperados |
| Tamaño | 2784,6 MB |
| Formato | NIfTI (`.nii.gz`) |
| Etiquetas | Anatomía de la próstata por lector 1 (y lector 2 en parte de los casos) y tumor en T2 y ADC (columnas de los csv). Valores y nombres de las clases de anatomía: por verificar contra la documentación del conjunto |
| Anonimización | Sin hallazgos en `verificar_anonimizacion.py`: 844 NIfTI revisados, sin texto libre en cabeceras, sin nombres no neutros ni fechas |
| Cómo se descargó | Manual desde Zenodo, aceptando las condiciones (ver `procedimiento_descarga.md`); ubicado en `datos/externos/prostate158_train/` |
| ¿Se puede redistribuir? | **No** |
| Estado en Prosta-AI | **Respaldo solo de referencia** (tarea 1202). El modelo base `prostate_mri_anatomy` se entrenó con este conjunto; eso se documenta en `docs-tecnicos/modelo-y-licencias.md` (ciclo 3) |
