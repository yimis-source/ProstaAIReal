# Texto explicativo de la ROI y revisión de lenguaje no clínico

| Campo | Valor |
|---|---|
| Tarea | 1505 |
| Responsable | Sergio Gabriel Meneses Silva (Diseñador) |
| Fecha | 10/11/2026 |
| Versión | 1.0 |

Cubre RF-17 (panel que explica la ROI, las métricas y sus límites), RF-15 y RF-16 (aviso y lenguaje no clínico). Las cifras vienen de `reports/evaluacion/`.

## 1. Texto del panel «¿Qué estoy viendo?»

**Aviso (texto exacto de `AVISO_EXPERIMENTAL`):**
Resultado experimental con fines académicos. No es un diagnóstico ni sustituye la valoración de un profesional de la salud.

**Qué muestra la ROI.**
La zona verde azulada es la región de interés (ROI): el contorno que el modelo calculó para la próstata en este corte de la imagen T2. Es una marca generada por un programa para que veas qué región delimitó; no interpreta la imagen ni dice nada sobre el estado de la persona. Puedes ver la imagen con y sin la ROI y cambiar su opacidad.

**Qué significan Dice e IoU.**
Son dos números entre 0 y 1 que comparan la ROI del modelo con una referencia dibujada a mano en datos públicos de prueba. Valen 1 si coinciden del todo y 0 si no se solapan.
- Dice: el doble del solapamiento dividido entre la suma de las dos áreas.
- IoU: el solapamiento dividido entre el área de la unión de ambas.
Solo se calculan cuando hay una referencia; con una imagen propia sin referencia no se muestran.
En los 5 casos de prueba el Dice medio fue 0,8925 ± 0,0340 y el IoU medio 0,8071 ± 0,0534 (informe del 06/11/2026). Son cifras del conjunto público de prueba, no de tus datos.

**Límites que debes conocer.**
- Solo se evaluó con 5 casos de prueba; con tan pocos casos la media es poco estable (el más bajo fue prostate_28, Dice 0,8320).
- Cambio de dominio: el modelo se entrenó con otros datos (Prostate158) y los casos de prueba (MSD Task05) tienen otra resolución y protocolo, con cortes gruesos de 4 mm.
- Los cortes gruesos hacen que los bordes de la base y el ápex sean menos precisos.
- Posible sesgo del modelo preentrenado: la documentación no menciona los datos de Task05, pero no se puede garantizar que no se hayan usado en su entrenamiento; si así fuera, las cifras estarían sobreestimadas.
- Al ampliar a los 32 casos, el Dice medio baja a 0,8736 ± 0,1222 porque prostate_07 tiene Dice 0,2255: el modelo marcó una región falsa cerca del borde del campo de visión (24 225 vóxeles). Ese caso muestra que la ROI puede fallar.
- Uso académico: no hay validación clínica ni externa.

## 2. Revisión de lenguaje no clínico (RF-15, RF-16)

### 2.1 Palabras y expresiones a evitar

No deben aparecer en textos de la interfaz, informes ni imágenes, salvo dentro del aviso experimental o en negaciones como «no diagnóstico»:

diagnóstico, diagnosticar, tumor, cáncer, maligno, benigno, lesión, patología, tratamiento, pronóstico, biopsia, recomendación clínica, «se recomienda», «el paciente tiene», sospechoso, normal/anormal (como juicio), aprobado/certificado por médicos, «detecta», «confirma», «descarta», puntuación de riesgo.

Alternativas: «región de interés (ROI)», «segmentación», «máscara», «resultado experimental», «el modelo marcó».

### 2.2 Resultado de revisar el repositorio

Se buscó con `grep -rniE` (diagn, tumor, cáncer, malign, patolog, lesi, paciente, tratamiento, biops, PI-RADS, certific, recomendaci…cl) en `backend/prosta_ai/`, `scripts/generar_roi.py`, `scripts/verificar_roi.py` y `reports/roi/`, que son los textos que produce la imagen de la ROI.

- Las únicas apariciones son negaciones o el propio aviso: `constantes.py` (el aviso), el docstring de `__init__.py` («uso académico, no diagnóstico»), el docstring de `visualizacion.py`, `scripts/generar_roi.py` («aviso no diagnóstico») y la frase «no es una evaluación clínica ni diagnóstica» de `verificar_roi.py` y su informe.
- No se encontró ninguna de las demás palabras de la lista en esos archivos.
- La imagen exportada solo contiene el corte, la ROI y el aviso; no lleva nombre de paciente ni identificadores (las cabeceras de los NIfTI generados no tienen texto, según `reports/roi/verificacion_roi_2026-11-11.md`).

**Conclusión:** sin hallazgos que corregir en los textos de la imagen de la ROI. La revisión se repetirá en el ciclo 6 con los textos de la interfaz.
