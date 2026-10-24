# Ficha de conjunto: PROMISE12

| Campo | Valor |
|---|---|
| Tarea | 1203 |
| Responsable | Juan David Riascos Erazo (Analista), con apoyo de Yimis Buenaventura |
| Fecha | 17/10/2026 |
| Versión | 1.0 |

| Ítem | Detalle |
|---|---|
| Nombre | PROMISE12 (Prostate MR Image Segmentation 2012) |
| Fuente / URL | https://promise12.grand-challenge.org/ |
| Cita | Litjens, G., Toth, R., van de Ven, W. et al. Evaluation of prostate segmentation algorithms for MRI: the PROMISE12 challenge. *Med Image Anal* 18(2):359-373 (2014). doi: 10.1016/j.media.2013.12.002 |
| Institución | Organizadores del reto (varios centros). Incluye casos de Radboud/Nijmegen; el resto de centros: por verificar en la documentación del reto |
| Licencia | Condiciones del reto, con registro, para uso de investigación. Texto exacto y si permite redistribuir: **por verificar** |
| Qué permite | Uso de investigación tras registrarse (por verificar el alcance) |
| Qué exige | Registro y aceptar las condiciones del reto; citar el artículo |
| Condiciones de uso en Prosta-AI | Solo comparación. No se redistribuye ni se sube al repositorio |
| Modalidades | MRI T2 (axial) |
| Casos | 50 de entrenamiento (`training_data`) y 30 de prueba (`test_data`), según el inventario |
| Archivos | 200 en entrenamiento y 120 en prueba (imagen y segmentación en `.mhd` + `.raw`); 1 `a.py` no esperado en cada carpeta; 0 metadatos |
| Tamaño | 786,5 MB (entrenamiento) + 466,6 MB (prueba) |
| Formato | MetaImage (`.mhd` + `.raw`) |
| Etiquetas | Máscara binaria de la glándula en entrenamiento. La carpeta de prueba también trae máscaras: el inventario muestra 30 casos con 30 archivos `*_segmentation.mhd` |
| Anonimización | Sin hallazgos en `verificar_anonimizacion.py`: 100 MetaImage de entrenamiento y 60 de prueba revisados, sin claves no estándar |
| Archivo no esperado | `a.py` en ambas carpetas. Venía en la descarga. No es dato: **no se abre, no se ejecuta ni se importa**; se borra o se ignora |
| Cómo se descargó | Manual, con registro en el reto (ver `procedimiento_descarga.md`); ubicado en `datos/externos/promise12/{training_data,test_data}` |
| ¿Se puede redistribuir? | No (hasta verificar la licencia) |
| Estado en Prosta-AI | **Para comparar.** Pendiente verificar pacientes compartidos con MSD Task05 (ambos incluyen casos de Radboud/Nijmegen); se hará en el ciclo 2 (tarea 1304). No se mezcla con MSD hasta entonces |
