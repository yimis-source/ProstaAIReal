# Modelo de segmentación y licencias

Responsable: Juan David Riascos Erazo (Analista). Tareas 1402 y 1411 del ciclo 3; actualizado en el ciclo 4 (imagen de la ROI con aviso).

## 1. Decisión vigente

Desde el 04/11/2026, Prosta-AI usa **por ahora** el modelo preentrenado `prostate_mri_anatomy` del MONAI Model Zoo, sin ajuste propio.

- **Motivo:** la inferencia ya integrada en el pipeline delimita bien la glándula en los primeros casos revisados y funciona en CPU en menos de 20 s por estudio, dentro de RR-01 (≤ 120 s). Además se ajusta a la respuesta prevista para el riesgo 1 del Acta: «modelos preentrenados con ajustes ligeros». La evaluación formal del 06/11/2026 lo confirmó: en el conjunto de prueba de Task05 obtiene un Dice medio de 0,8925, frente a la meta de 0,80 (RF-24).
- **Ajuste ligero:** queda como mejora posterior. El procedimiento ya está preparado en `entrenamiento/`.
  - Si se ejecuta, el modelo ajustado solo se adopta si mejora el Dice del preentrenado en el mismo conjunto de prueba.
  - Cambiar de modelo no requiere tocar código: basta con dejar la carpeta del modelo en `modelos/<nombre>/` con su `preparacion.json` (ver `entrenamiento/README.md`).

## 2. Ficha del modelo

| Campo | Valor |
|---|---|
| Nombre | Prostate MRI Anatomy (`prostate_mri_anatomy`), versión 0.3.6 |
| Origen | MONAI Model Zoo, publicado en https://huggingface.co/MONAI/prostate_mri_anatomy (revisión fijada en `scripts/descargar_modelo.py`) |
| Autores | Lisa C. Adams y Keno K. Bressem (Charité – Universitätsmedizin Berlin) |
| Licencia del modelo | Apache License 2.0. Copyright (c) Keno Bressem |
| SHA-256 de los pesos | `3c18e4c658bb088f551b1d63219ef8340fe6256d016c75fc140d3da49dda696d` |
| Uso previsto según sus autores | «This is an example, not to be used for diagnostic purposes» |
| Versiones con que se publicó | MONAI 1.4.0, PyTorch 2.4.0 |

### Con qué datos se entrenó

- **Conjunto:** Prostate158 (https://doi.org/10.5281/zenodo.6481141). Son 158 resonancias biparamétricas de próstata adquiridas a 3 T en la Charité – Universitätsmedizin Berlin y anotadas por radiólogos expertos.
- **División de los autores:**
  - 139 estudios para entrenamiento, que son los publicados en Zenodo (los mismos 139 que descargamos en el ciclo 1 como respaldo de referencia).
  - 19 estudios de prueba, publicados aparte y anotados por dos evaluadores.
- **Secuencia usada:** solo T2 ponderada (T2w). No se usaron DWI ni ADC.
- **Etiquetas:** 0 = fondo, 1 = glándula central (zona de transición), 2 = zona periférica.

### Cómo se entrenó

- **Arquitectura:** U-Net 3D de MONAI (`monai.networks.nets.UNet`).
  - Entrada de 1 canal y salida de 3 clases.
  - Canales 16-32-64-128-256-512, pasos de 2 y 4 unidades residuales por nivel.
  - Normalización por lotes, activación PReLU y *dropout* de 0,15.
- **Tarea:** clasificación de cada vóxel en fondo, glándula central o zona periférica.
- **Función de pérdida:** *focal soft-Dice*, optimizada por descenso de gradiente.
- **Entrada:** parches de 96 × 96 × 96 vóxeles con intensidad escalada a [0, 1].
- **Preprocesamiento de los autores:**
  - Recorte centrado del campo de visión: el FOV axial original es de 180 mm y la próstata rara vez supera los 100 mm.
  - Remuestreo; el T2w original es de 0,47 × 0,47 × 3 mm.
- **Desempeño publicado:** sobre la prueba de Prostate158.

| Métrica | Zona de transición (evaluador 1 / 2) | Zona periférica (evaluador 1 / 2) |
|---|---|---|
| Dice | 0,877 / 0,875 | 0,754 / 0,730 |
| Distancia de Hausdorff (mm) | 18,3 / 17,5 | 22,8 / 33,2 |
| Distancia de superficie (mm) | 2,19 / 2,59 | 1,95 / 1,88 |

Fuente: `modelos/prostate_mri_anatomy/docs/README.md` y `configs/metadata.json`, que se descargan con el modelo. Artículo de referencia:

> Adams, L. C., Makowski, M. R., Engel, G., Rattunde, M., Busch, F., Asbach, P., … & Bressem, K. K. (2022). Prostate158 – An expert-annotated 3T MRI dataset and algorithm for prostate cancer detection. *Computers in Biology and Medicine, 148*, 105817. https://doi.org/10.1016/j.compbiomed.2022.105817

### Cómo lo usa Prosta-AI

- **Preprocesamiento:** el mismo de la configuración de inferencia del modelo (RF-09). Orientación RAS, espaciado de 0,5 mm, `ScaleIntensity` y `NormalizeIntensity`. Los parámetros están en `modelos/prostate_mri_anatomy/preparacion.json`, que genera `scripts/descargar_modelo.py` a partir de `configs/inference.json`.
- **Inferencia:** por ventana deslizante de 96³, con `sw_batch_size` 4 y solapamiento de 0,5. La red se usa siempre en modo evaluación (`.eval()`; ver el defecto registrado en el LOGD del ciclo 3).
- **Posprocesado:** se conserva el componente conexo más grande de cada etiqueta.
- **Máscara de próstata:** es la unión de las etiquetas > 0. La ROI no distingue zonas.
- **Evaluación propia:** en MSD Task05 (división por paciente, semilla 2026) da un Dice medio de 0,8925 ± 0,034 en los 5 casos de prueba (informe del 06/11/2026 en `reports/evaluacion/`).

## 3. Con qué datos se evalúa y por qué no con los otros conjuntos

La evaluación del modelo se hace **solo con los 5 casos de prueba de MSD Task05** (`entrenamiento/division_task05.json`).

| Conjunto | ¿Sirve para evaluar este modelo? | Motivo |
|---|---|---|
| MSD Task05_Prostate | Sí (conjunto de prueba de la división) | Licencia clara (CC BY-SA 4.0), máscaras de referencia y división por paciente verificada por el Tester (ciclo 2) |
| Prostate158 | **No** | Es el conjunto con el que los autores **entrenaron** el modelo preentrenado: medir sobre él sería medir sobre datos ya vistos y sobreestimaría el resultado. Además su licencia **no es CC BY verificada** (ver sección 4). En el ciclo 1 quedó solo como respaldo de referencia |
| PROMISE12 | **No** | Comparte pacientes con MSD Task05 (Radboud): el informe de fuga del ciclo 2 (`reports/division/`) encontró casos repetidos, algunos de ellos en nuestro conjunto de prueba. Usarlo mezclaría pacientes entre conjuntos |

## 4. Licencias y derechos de uso

| Componente | Licencia | Qué permite | Qué exige | Cómo se cumple en Prosta-AI |
|---|---|---|---|---|
| Pesos y configuración de `prostate_mri_anatomy` | Apache 2.0 | Usar, modificar y redistribuir, incluso con fines comerciales | Conservar el aviso de copyright y el texto de la licencia; indicar cambios si se redistribuye modificado | Los pesos no se versionan en git: `scripts/descargar_modelo.py` los descarga junto con su `LICENSE` y genera `FICHA.md` con autoría y cita |
| Datos de entrenamiento del modelo (Prostate158) | **No es CC BY verificada.** Zenodo lo publica como acceso abierto sin indicar una licencia concreta. El sitio del reto (prostate158.grand-challenge.org) exige aceptar un acuerdo de uso | Uso personal en investigación no comercial | No redistribuir los datos, no crear obras derivadas de los datos, no usarlos para diagnóstico ni atención de pacientes, no intentar reidentificar | Prosta-AI **no versiona, no redistribuye y no usa para evaluar** Prostate158. La copia descargada en el ciclo 1 queda local y fuera de git, solo como referencia. Se usan los pesos que publicaron los mismos autores del conjunto bajo Apache 2.0 |
| Datos de evaluación (MSD Task05_Prostate) | CC BY-SA 4.0 | Usar, adaptar y compartir, incluso con fines comerciales | Atribución, y compartir bajo la misma licencia lo que se derive de los datos | Los datos no se versionan (`datos/` está en `.gitignore`). Se cita en `README.md`, en `docs/datos/fichas/` y en los informes. Los informes publican solo métricas, no imágenes |
| MONAI | Apache 2.0 | Uso libre | Conservar avisos | Dependencia instalada, no modificada |
| PyTorch | BSD (3 cláusulas) | Uso libre | Conservar avisos | Dependencia instalada, no modificada |
| Pillow | MIT-CMU (HPND) | Uso libre | Conservar avisos | Dependencia instalada para dibujar la imagen de la ROI |
| Fuente DejaVu Sans (texto del aviso en la imagen de la ROI) | Licencia libre de Bitstream Vera / DejaVu | Uso y redistribución | Conservar el aviso | Incluida en `backend/prosta_ai/recursos/` junto con `DejaVuSans-LICENCIA.txt` |

## 5. Riesgos y conclusión

**Conclusión:** el modelo **se puede usar** en Prosta-AI tal como está planteado. El proyecto es académico, no comercial y no clínico, y no redistribuye datos de pacientes.

| Riesgo | Nivel | Explicación | Respuesta |
|---|---|---|---|
| Restricciones heredadas de Prostate158 | Bajo para uso académico | Los pesos tienen licencia Apache 2.0, pero se entrenaron con datos cuyo acuerdo del reto limita el uso a investigación no comercial. Que un modelo entrenado sea «obra derivada» de los datos no está resuelto jurídicamente. Los propios autores del conjunto publicaron los pesos con licencia abierta, lo que indica su consentimiento | Mantener el uso académico y no comercial. Si el proyecto pasara a uso comercial, consultar a los autores o entrenar con datos de licencia compatible |
| Uso clínico | Fuera de alcance | Los autores del modelo y del conjunto lo excluyen expresamente | La imagen de la ROI (`pipeline/visualizacion.py`, `scripts/generar_roi.py`) lleva impreso el aviso experimental; las pantallas de resultados lo mostrarán en el ciclo 6 |
| Atribución | Bajo | Apache 2.0 y CC BY-SA 4.0 exigen reconocer la autoría | Se cita en `README.md`, en este documento, en `FICHA.md` y en los informes de evaluación. Incluir las citas en la presentación final |
| Compartir bajo la misma licencia (CC BY-SA) | Bajo | Afectaría a material derivado de Task05 que se publique, por ejemplo imágenes con la ROI o un modelo ajustado con Task05 | Si se publican capturas con imágenes de Task05 o un modelo ajustado con ellas, hacerlo bajo CC BY-SA 4.0 y con atribución |
| Sobreestimación de métricas | Medio (técnico, no legal) | No se puede descartar que el preentrenamiento haya visto datos parecidos a Task05 | Documentado en el informe de evaluación |
| Cambio de la fuente | Bajo | El modelo se descarga de Hugging Face | La revisión está fijada y el hash SHA-256 se verifica en la ficha |

**Obligaciones del equipo:**
1. Mantener `LICENSE` y `FICHA.md` junto a los pesos si alguna vez se redistribuyen.
2. Citar el modelo, Prostate158 y el Medical Segmentation Decathlon en la documentación final y en la presentación.
3. No subir al repositorio imágenes ni máscaras de los conjuntos de datos (tampoco las ROI que genera `scripts/generar_roi.py`, que van a `salidas/`).
4. No presentar la aplicación como herramienta de diagnóstico.

Referencias de licencias:
- Apache 2.0: https://www.apache.org/licenses/LICENSE-2.0
- CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
- Acuerdo de uso de Prostate158: https://prostate158.grand-challenge.org/data/

Licencias consultadas el 02/11/2026.
