# Elección del conjunto de datos

| Campo | Valor |
|---|---|
| Tarea | 1202 |
| Responsable | Juan David Riascos Erazo (Analista) |
| Fecha | 16/10/2026 |
| Versión | 1.0 |
| Ciclo | 1 (13/10–25/10/2026) |
| Criterios aplicados | `criterios_seleccion.md` (tarea 1201) |

## 1. Candidatos

| Candidato | Origen | Resultado |
|---|---|---|
| MSD Task05_Prostate | Medical Segmentation Decathlon (Radboud University, Nijmegen) | **Principal** |
| Prostate158 | Charité – Universitätsmedizin Berlin | **Respaldo, solo de referencia** |
| PROMISE12 | Reto MICCAI 2012 | Se descarga para comparar; pendiente de verificación |
| NCI-ISBI 2013 | Reto NCI-ISBI | Descartado sin descargar |
| Otros (conjuntos con solo difusión o solo tumor, o con acceso por solicitud a un archivo clínico) | Varios | Descartados sin descargar |

Los descartados sin descargar no se bajaron: no los necesitamos porque ya hay un principal y dos candidatos más, y se evita acumular datos sin ficha. Si el riesgo 3 llegara a materializarse, se retomarían con los criterios del documento 1201.

## 2. Comparación con los criterios

Las cifras de casos y tamaño salen de `inventario_datos.md` (generado con `scripts/inventario_datos.py` sobre lo descargado). El resultado de anonimización sale de `verificacion_anonimizacion.md` (`scripts/verificar_anonimizacion.py`).

| Criterio | MSD Task05_Prostate | Prostate158 | PROMISE12 |
|---|---|---|---|
| I1 Público | Sí, descarga directa | Sí, Zenodo; el reto pide acuerdo | Sí, con registro en el reto |
| I2 Anónimo | Sin hallazgos (80 NIfTI revisados; solo `descrip` = «5.0.10» en cabecera) | Sin hallazgos (844 NIfTI) | Sin hallazgos (160 MetaImage: 100 de entrenamiento + 60 de prueba) |
| I3 Licencia clara de uso académico | **Sí: CC-BY-SA 4.0** | **No verificada como abierta**: Zenodo no indica licencia; el reto exige acuerdo de uso de investigación no comercial y sin redistribución | Licencia del reto con registro, uso de investigación; texto exacto por verificar |
| I4 T2 de próstata | Sí (canal 0 = T2; canal 1 = ADC) | Sí (T2, ADC y DWI) | Sí (T2 axial) |
| I5 Máscaras de la glándula | Zonas PZ y TZ; su unión es la glándula | Anatomía (zonas) y tumor | Máscara de la glándula |
| I6 Formato | NIfTI 4D | NIfTI | MetaImage (.mhd + .raw) |
| I7 Tamaño | 239,8 MB | 2784,6 MB | 786,5 MB (entrenamiento) + 466,6 MB (prueba) |
| I8 Procedencia | Antonelli et al. 2022; Simpson et al. 2019 | Adams et al. 2022; Zenodo | Litjens et al. 2014 |
| I9 Más de un observador | No (un observador) | Hay lectores 1 y 2 en parte de los casos | Por verificar |
| I10 Casos etiquetados | 32 (+16 sin máscara) | 139 descargados (entrenamiento + validación) | 50 con máscara; 30 de prueba |

Nota sobre PROMISE12: el inventario cuenta 50 casos de entrenamiento y 30 de prueba. De la carpeta de prueba no se asume que tenga máscaras; **por verificar** al hacer la ficha.

## 3. Decisión

### 3.1 Principal: MSD Task05_Prostate

Es el único de los tres que cumple todos los criterios obligatorios con licencia **verificada y abierta** (CC-BY-SA 4.0). Pesa menos de 240 MB, tiene 32 casos con máscara de zona periférica (PZ) y zona de transición (TZ), y trae T2 y ADC en un NIfTI 4D. Es suficiente para el alcance académico del proyecto, aunque 32 casos son pocos y es un solo observador (sesgo que se documenta, riesgo 3).

Implica: atribución, y compartir bajo la misma licencia lo que se derive de los datos.

### 3.2 Respaldo solo de referencia: Prostate158

Tiene más casos (139) y anotaciones de dos lectores en parte de ellos, pero **su licencia no está verificada como CC-BY**:

- Zenodo (doi 10.5281/zenodo.6481141) no indica una licencia.
- El sitio del reto (prostate158.grand-challenge.org) exige un acuerdo de uso: investigación no comercial y sin redistribución.

Por eso no puede ser el principal (regla 2 de los criterios) y se maneja así: se usa solo como referencia, **no se redistribuye y no se sube al repositorio** (`datos/` está ignorado por git).

### 3.3 PROMISE12: se descarga para comparar

La licencia es la del reto: registro y uso de investigación (texto exacto por verificar). Se descarga solo para comparar con MSD. Queda **pendiente verificar si hay pacientes compartidos con MSD**: ambos incluyen casos de Radboud/Nijmegen y, si hubiera pacientes repetidos, se produciría fuga de datos entre entrenamiento y prueba. Esa verificación se hará en el ciclo 2 (tarea 1304). Hasta entonces PROMISE12 no se mezcla con MSD en ningún entrenamiento ni evaluación.

## 4. Riesgos de la decisión

| Riesgo | Mitigación |
|---|---|
| Pocos casos (32) | Dividir por paciente (un caso = un paciente) y reportar la incertidumbre; documentar el sesgo |
| Un solo observador y cortes gruesos | Documentarlo en la ficha y en el informe de datos |
| Licencias de respaldo no abiertas | No redistribuir; mantener el uso académico y no comercial |
| Posible solapamiento MSD–PROMISE12 | Tarea 1304, ciclo 2 |
| Archivo `a.py` no esperado en PROMISE12 | No se abre ni se ejecuta; el inventario lo marca como «no esperado» (1 en entrenamiento y 1 en prueba) |
