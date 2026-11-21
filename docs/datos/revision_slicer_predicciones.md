# Revisión visual en 3D Slicer de las máscaras predichas

| Campo | Valor |
|---|---|
| Tarea | 1413, repetida en 1606 |
| Responsable | Sergio Gabriel Meneses Silva (Diseñador, gerente de soporte), con Juan David Riascos Erazo |
| Fecha | 21/11/2026 |
| Versión | 1.1 |

> **Esto es una revisión visual, sin métricas nuevas.** No se calculó ninguna medida. Las únicas cifras (Dice, HD95) vienen de `reports/evaluacion/informe_metricas_ciclo5.md`. Uso académico y experimental; no es una evaluación clínica ni diagnóstica.

## 1. Qué se compara

- **Máscara predicha:** la genera el pipeline en el equipo local (`build_pipeline`, modelo `prostate_mri_anatomy`) y se devuelve a la rejilla de la imagen original. **No se versiona**: se guarda en una carpeta local ignorada por git.
- **Referencia:** las etiquetas de MSD Task05 (zona periférica + zona de transición, etiquetas > 0), que son la unión que usa el informe de evaluación.
- **Casos:** los 5 de prueba: prostate_13, prostate_17, prostate_28, prostate_34 y prostate_44.

## 2. Procedimiento

1. Abrir 3D Slicer (esta revisión usó la 5.12.4; instalación en `docs/datos/revision_3d_slicer.md`, tarea 1207).
2. *File → Add Data*: cargar la imagen del caso desde `datos/Task05_Prostate/imagesTr` (no se verificó qué canal se cargó).
3. Cargar la referencia de `labelsTr` como **Segmentation** y la máscara predicha local también como **Segmentation**. La referencia tiene dos etiquetas y Slicer la carga como dos segmentos con sus colores por defecto: **verde** = zona periférica (etiqueta 1) y **amarillo** = zona de transición (etiqueta 2). La predicha se deja en un color distinto.
4. En el módulo *Segmentations* usar *Jump slices* para ir a la máscara, y alternar la visibilidad con el icono del ojo.
5. Disposición de tres planos (axial, sagital, coronal) y vista 3D. Recorrer el deslizador axial de S negativo (ápex) a S positivo (base) y revisar varios cortes por caso, no todos.
6. Anotar, por caso: (a) si la predicha y la referencia ocupan la misma zona, (b) en qué cortes difieren (base, ápex, bordes laterales), (c) si aparece alguna región predicha lejos de la glándula.
7. Observar en coronal y sagital, donde se nota más el grosor de los cortes (3–4 mm).
8. Cerrar la escena sin guardarla en el repositorio.

La orientación ápex/base se dedujo de los valores S del deslizador.

## 3. Cifras de referencia (informe del 19/11/2026)

| Caso | Dice | HD95 (mm) |
|---|---:|---:|
| prostate_13 | 0,9012 | 3,60 |
| prostate_17 | 0,9097 | 3,54 |
| prostate_28 | 0,8320 | 5,69 |
| prostate_34 | 0,9105 | 4,00 |
| prostate_44 | 0,9090 | 3,60 |
| Media ± desv. | 0,8925 ± 0,0340 | 4,09 ± 0,92 |

## 4. Observaciones cualitativas

Son impresiones de una revisión visual hecha por personas que no son profesionales de la salud; no sustituyen a las métricas ni tienen valor clínico. «Modelo» es la máscara predicha.

- **prostate_13, 17, 34 y 44:** el modelo y la referencia ocupan la misma zona; las diferencias varían por caso (ver la tabla de abajo).
- **prostate_28:** es el caso con el Dice más bajo (0,8320). En los cortes revisados el modelo cubre menos que la referencia en varios cortes. No se probó a explicar la causa solo con la revisión visual.
- **Extremos:** el comportamiento no es el mismo en todos los casos. En prostate_28 y 34 el modelo cubre menos que la referencia hacia la base; en prostate_44 se extiende más cortes que ella en ambos extremos. Es una observación en pocos cortes, no una medición. El informe de evaluación señala además que los anotadores pueden delimitar base y ápex con criterios distintos, y que los cortes gruesos (4 mm en Task05) hacen menos precisos esos bordes.
- **Regiones falsas:** en los 5 casos de prueba no se vio ninguna región predicha lejos de la glándula; en 3D el modelo es una sola región compacta. Esto no se extiende a los demás casos: el informe de 32 casos documenta aparte el caso prostate_07, que no está en el conjunto de prueba.
- **Alineación modelo–referencia:** sin desplazamiento ni giro en los cortes revisados. No se comprobó contra la imagen.
- **Bordes:** en los cinco casos el modelo sobresale levemente en algunos bordes y quedan franjas o trozos pequeños de la referencia sin cubrir en otros. Los bordes en escalón de coronal y sagital se deben al grosor de los cortes.

### Observaciones por caso

Colores: **verde** = zona periférica de la referencia, **amarillo** = zona de transición de la referencia y «modelo» = máscara predicha. Por eso en algunos cortes se ven tres máscaras: el modelo y las dos zonas de la referencia.

| Caso | Ápex (S negativo) | Zona media | Base (S positivo) |
|---|---|---|---|
| prostate_13 | Modelo y referencia empiezan casi en el mismo corte. | — | Terminan en el mismo corte que la zona amarilla; en S = -8,9 mm el modelo es un trazo muy pequeño dentro de la referencia. |
| prostate_17 | Empiezan juntos, pero el modelo no cubre toda la zona amarilla. | El modelo cubre casi toda la zona amarilla. | El modelo cubre toda la zona amarilla y termina un corte después que ella (comparado con el amarillo). |
| prostate_28 | En S = -94,5 mm el modelo es el más pequeño de las tres máscaras. | El modelo y el verde tienen tamaño parecido; el amarillo es menor. | En S = -58,5 mm el verde ya no aparece y el modelo cubre menos que el amarillo; termina junto con el amarillo, cubriendo menos. |
| prostate_34 | En S = -92,3 mm el modelo cubre más que la zona amarilla. | En S = -80,3 mm los tres tamaños son parecidos (el amarillo, algo menor). | El verde desaparece y el modelo cubre mucho menos que el amarillo; en S = -40,3 mm es una franja delgada sobre él. |
| prostate_44 | En S = -37,2 mm aparece solo el modelo. | En S = -26,4 mm el modelo y el amarillo tienen el mismo tamaño. En S = -1,2 mm los dos son grandes. | En S = 6,0 mm solo queda el modelo, sin amarillo ni verde. |

## 5. Limitaciones de esta revisión

- Es una revisión visual de 5 casos y algunos cortes por caso; no cuantifica nada.
- La mayoría de las capturas mostraban solo las máscaras sobre fondo negro: no se evaluó cómo se ve el contorno sobre la imagen ni qué canal (T2 o ADC) se cargó.
- Solo se comparó con una referencia por caso, sin variabilidad entre observadores.
- Es del modelo preentrenado; si se adopta el modelo ajustado (tarea 1603), habría que repetir la revisión.
- Lo observado no cambia las conclusiones del informe de evaluación; solo las acompaña.