# Revisión visual en 3D Slicer

| Campo | Valor |
|---|---|
| Tarea | 1207 |
| Responsable | Sergio Gabriel Meneses Silva (Diseñador, gerente de soporte), con apoyo de Juan David Riascos Erazo |
| Fecha | 23/10/2026 |
| Versión | 1.0 |

> **Esto es una revisión visual, sin métricas.** No se calculó Dice ni ninguna otra medida. Sirve para entender los datos y detectar problemas evidentes antes de la división y el entrenamiento. Las únicas cifras (volúmenes) vienen de `reports/datos/geometria_msd_task05.csv`.

## 1. Instalación de 3D Slicer 5.x (guía breve de soporte)

1. Descargar el instalador estable 5.x desde https://download.slicer.org/ (versión para el sistema operativo del equipo; en Linux, el `.tar.gz`).
2. Windows: ejecutar el instalador. Linux: descomprimir y lanzar `./Slicer` desde la carpeta. macOS: arrastrar la aplicación a Aplicaciones.
3. Abrir Slicer y comprobar que arranca el módulo *Welcome*. No hace falta instalar extensiones para esta tarea.
4. Si en Linux no abre por falta de librerías gráficas, instalar las dependencias OpenGL/Qt del sistema (problema habitual, se resolvió así en el portátil de Juan).
5. Los datos se leen desde `datos/` en local. **No se suben a ningún sitio.**

## 2. Procedimiento

1. *File → Add Data* y cargar la imagen T2 (canal 0) de un caso de `datos/Task05_Prostate/imagesTr`.
2. Cargar la máscara de `labelsTr` marcándola como **Segmentation** (opción *Show Options → Segmentation*), para verla superpuesta y con colores por etiqueta (1 zona periférica, 2 zona de transición).
3. Poner la vista en la disposición de tres planos (axial, sagital y coronal) y recorrer los cortes con la rueda del ratón.
4. Comprobar la alineación imagen–máscara: que el contorno siga el borde de la glándula en los tres planos y que no haya desplazamientos ni giros.
5. Fijarse en el efecto de los cortes gruesos (3–4 mm) al cambiar de plano.
6. Repetir con el canal 1 (ADC) del mismo caso.

## 3. Muestra revisada

Elegida con `reports/datos/geometria_msd_task05.csv` (32 casos con máscara): los casos de menor y mayor volumen y algunos de volumen típico (la mediana del conjunto es 62,0 mL).

| Grupo | Casos | Volumen (mL) |
|---|---|---|
| Menor volumen | prostate_07, prostate_13, prostate_40, prostate_17, prostate_46 | 16,0 / 33,6 / 33,8 / 34,3 / 35,1 |
| Mayor volumen | prostate_16, prostate_38, prostate_04, prostate_24, prostate_18 | 315,4 / 202,3 / 108,9 / 106,8 / 101,6 |
| Típicos | prostate_06, prostate_34, prostate_25 | 60,9 / 63,1 / 67,2 |

prostate_07 es el más pequeño (16,0 mL) y prostate_16 el más grande (315,4 mL).

## 4. Hallazgos (cualitativos)

- Las máscaras están alineadas con la glándula en los casos revisados, también en los extremos de volumen.
- Con cortes de 3–4 mm, la máscara se ve **escalonada** en sagital y coronal. Es efecto de la resolución entre cortes, no un error de la máscara.
- El canal 1 (ADC) tiene menos resolución que el T2 y se ve más borroso; el T2 es el que conviene para delimitar la glándula.
- Los casos extremos (prostate_07 muy pequeña, prostate_16 muy grande) se ven distintos al resto: hay que tenerlos en cuenta en la división por paciente del ciclo 2.
- No se vio ningún dato personal visible en las imágenes (sin texto ni rótulos incrustados), coherente con `reports/datos/verificacion_anonimizacion.md`.

## 5. Notas

- Las capturas de pantalla **no se versionan**: MSD Task05 tiene licencia CC BY-SA y la política del proyecto es no subir imágenes de pacientes al repositorio.
- Revisar todos los casos uno por uno no era viable en la tarea; la muestra es una comprobación de sentido común, no una auditoría.
