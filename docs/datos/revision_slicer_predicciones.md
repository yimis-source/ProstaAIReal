# Revisión visual en 3D Slicer de las máscaras predichas

| Campo | Valor |
|---|---|
| Tarea | 1413 |
| Responsable | Sergio Gabriel Meneses Silva (Diseñador, gerente de soporte), con Juan David Riascos Erazo |
| Fecha | 07/11/2026 |
| Versión | 1.0 |

> **Esto es una revisión visual, sin métricas nuevas.** No se calculó ninguna medida. Las únicas cifras (Dice) vienen de `reports/evaluacion/evaluacion_prostate_mri_anatomy_2026-11-06.md`. Uso académico y experimental; no es una evaluación clínica ni diagnóstica.

## 1. Qué se compara

- **Máscara predicha:** la genera el pipeline en el equipo local (`build_pipeline`, modelo `prostate_mri_anatomy`) y se devuelve a la rejilla de la imagen original. **No se versiona**: se guarda en una carpeta local ignorada por git.
- **Referencia:** las etiquetas de MSD Task05 (zona periférica + zona de transición, etiquetas > 0), que son la unión que usa el informe de evaluación.
- **Casos:** los 5 de prueba: prostate_13, prostate_17, prostate_28, prostate_34 y prostate_44.

## 2. Procedimiento

1. Abrir 3D Slicer 5.x (instalación en `docs/datos/revision_3d_slicer.md`, tarea 1207).
2. *File → Add Data*: cargar la imagen T2 (canal 0) del caso desde `datos/Task05_Prostate/imagesTr`.
3. Cargar la referencia de `labelsTr` como **Segmentation** y la máscara predicha local también como **Segmentation**. Dejar la referencia en un color y la predicha en otro.
4. En el módulo *Segmentations* poner la referencia como contorno (*Outline*) y la predicha como relleno, o alternar la visibilidad con el icono del ojo.
5. Disposición de tres planos (axial, sagital, coronal) y recorrer todos los cortes con la rueda del ratón.
6. Anotar, por caso: (a) si el contorno predicho sigue el borde de la glándula, (b) en qué cortes difiere de la referencia (base, ápex, bordes laterales), (c) si aparece alguna región predicha lejos de la glándula.
7. Repetir las anotaciones con la predicha en el plano sagital, donde se nota más el grosor de los cortes (3–4 mm).
8. Cerrar la escena sin guardarla en el repositorio.

## 3. Cifras de referencia (del informe de evaluación, 06/11/2026)

| Caso | Dice |
|---|---:|
| prostate_13 | 0,9012 |
| prostate_17 | 0,9097 |
| prostate_28 | 0,8320 |
| prostate_34 | 0,9105 |
| prostate_44 | 0,9090 |
| Media ± desv. | 0,8925 ± 0,0340 |

## 4. Observaciones cualitativas

Son impresiones de una revisión visual por dos personas que no son profesionales de la salud; no sustituyen a las métricas ni tienen valor clínico.

- **prostate_13, 17, 34 y 44:** el contorno predicho sigue en general el borde de la glándula en los tres planos. Las diferencias que se ven son pequeñas y se concentran en la base y el ápex.
- **prostate_28:** es el caso con el Dice más bajo (0,8320) y es el que más difiere de la referencia a simple vista. Es coherente con la cifra del informe. No se probó a explicar la causa solo con la revisión visual.
- **Base y ápex:** en los cinco casos los extremos superior e inferior son donde más se separan la predicha y la referencia. Es esperable porque los cortes son gruesos (4 mm en Task05) y un mismo corte puede contener parte de la glándula y parte del tejido vecino. El informe de evaluación señala además que los anotadores pueden delimitar base y ápex con criterios distintos.
- **Regiones falsas:** en los 5 casos de prueba no se vio ninguna región predicha lejos de la glándula. Esto no se extiende a los demás casos: el informe de 32 casos (ciclo 4) documenta aparte el caso prostate_07, que no está en el conjunto de prueba.
- **Alineación imagen–máscara:** sin desplazamientos ni giros evidentes.

## 5. Limitaciones de esta revisión

- Es una revisión visual de 5 casos; no cuantifica nada.
- Solo se comparó con una referencia por caso, sin variabilidad entre observadores.
- Lo observado no cambia las conclusiones del informe de evaluación; solo las acompaña.
