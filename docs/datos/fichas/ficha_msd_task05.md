# Ficha de conjunto: MSD Task05_Prostate

| Campo | Valor |
|---|---|
| Tarea | 1203 |
| Responsable | Juan David Riascos Erazo (Analista), con apoyo de Yimis Buenaventura |
| Fecha | 17/10/2026 |
| Versión | 1.0 |

| Ítem | Detalle |
|---|---|
| Nombre | Medical Segmentation Decathlon, Task05_Prostate |
| Fuente / URL | http://medicaldecathlon.com/ ; copia usada por MONAI: https://msd-for-monai.s3-us-west-2.amazonaws.com/Task05_Prostate.tar |
| Citas | Antonelli, M., Reinke, A., Bakas, S. et al. The Medical Segmentation Decathlon. *Nat Commun* 13, 4128 (2022). doi: 10.1038/s41467-022-30695-9. Simpson, A. L. et al. A large annotated medical image dataset for the development and evaluation of segmentation algorithms. arXiv:1902.09063 (2019) |
| Institución de la tarea | Radboud University, Nijmegen Medical Centre (campo `reference` de `dataset.json`) |
| Licencia | CC-BY-SA 4.0 (campo `licence` de `dataset.json`; https://creativecommons.org/licenses/by-sa/4.0/) |
| Qué permite | Usar, adaptar y compartir, incluso con fines comerciales |
| Qué exige | Atribución (citar la fuente) y compartir bajo la misma licencia lo que se derive de los datos |
| Condiciones de uso en Prosta-AI | Uso académico y experimental; no se usa para diagnóstico. Se cita en `datos/FUENTE.md`, README e informes |
| Modalidades | T2 (canal 0) y ADC (canal 1), en un NIfTI 4D `(x, y, z, 2)` |
| Casos | 32 con máscara (`imagesTr`/`labelsTr`) + 16 sin máscara (`imagesTs`), según el inventario |
| Archivos | 80 de imagen y máscara, 1 de metadatos (`dataset.json`), 0 no esperados |
| Tamaño | 239,8 MB |
| Formato | NIfTI (`.nii.gz`) |
| Etiquetas | 0 = fondo, 1 = zona periférica (PZ), 2 = zona de transición (TZ). La próstata completa es la unión (etiqueta > 0) |
| Anonimización | Sin hallazgos en `verificar_anonimizacion.py`: 80 NIfTI revisados; texto libre en cabecera solo `descrip` = «5.0.10» (80 archivos); sin nombres no neutros ni fechas |
| Cómo se descargó | Automático con `scripts/descargar_datos.py` en `datos/Task05_Prostate/` (ver `procedimiento_descarga.md`) |
| ¿Se puede redistribuir? | Sí, bajo CC-BY-SA 4.0 con atribución. Aun así, en el proyecto no se versionan (`datos/` en `.gitignore`) |
| Limitaciones | Pocos casos (32), un observador por caso, cortes gruesos (el espesor exacto por caso se mide en el análisis de geometría, no en esta ficha) |
| Estado en Prosta-AI | **Principal.** Aceptado el 16/10/2026 (tarea 1202) |
