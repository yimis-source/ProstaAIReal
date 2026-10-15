# Criterios de selección de conjuntos de datos

| Campo | Valor |
|---|---|
| Tarea | 1201 |
| Responsable | Juan David Riascos Erazo (Analista) |
| Fecha | 14/10/2026 |
| Versión | 1.0 |
| Ciclo | 1 (13/10–25/10/2026) |

## 1. Para qué sirven

Estos criterios son los que usamos para decidir qué conjuntos de datos entran al proyecto y cuáles no. Responden a tres cosas del Acta de Constitución y del SRS:

- **RC-03:** solo conjuntos públicos y anónimos, cada uno con ficha de fuente, licencia, condiciones y cita.
- **RN-01:** cumplir la Ley 1581 de 2012 y el Decreto 1377 de 2013 (datos personales). Por eso no se aceptan datos que identifiquen a pacientes.
- **Riesgo 3 del Acta** (datos insuficientes, incompletos, con sesgos o con licencias problemáticas; NR = 3 × 4 = 12; responsable: Juan David Riascos): la mitigación dice verificar licencias, calidad y etiquetas en el primer ciclo, documentar los sesgos y **tener un conjunto alterno**.

## 2. Criterios de inclusión

Un conjunto se acepta solo si cumple **todos** los obligatorios (O). Los deseables (D) sirven para desempatar.

| # | Criterio | Tipo | Cómo se verifica | Requisito |
|---|---|---|---|---|
| I1 | Público: se puede obtener sin pagar y sin pedir estudios a un hospital | O | Se descarga desde el sitio del autor (con registro gratuito si lo exige) | RC-03 |
| I2 | Anónimo: sin nombres, fechas de estudio ni identificadores del paciente en archivos ni cabeceras | O | `scripts/verificar_anonimizacion.py` sobre lo descargado | RN-01 |
| I3 | Licencia clara que permita uso académico (texto de la licencia o acuerdo de uso localizable y leído) | O | Se lee la licencia en la fuente; si no está clara, el conjunto queda como «por verificar» | RC-03, riesgo 3 |
| I4 | Resonancia magnética de próstata en T2 | O | Documentación del conjunto y revisión de cabeceras | Alcance del Acta |
| I5 | Máscaras de segmentación de la glándula (o de sus zonas, de modo que su unión dé la glándula) | O | Existencia de archivos de máscara por caso | Riesgo 3 (etiquetas) |
| I6 | Formato legible con las herramientas del proyecto: NIfTI, MetaImage (.mhd/.raw) o DICOM | O | Se abre con nibabel/SimpleITK | Pila del proyecto |
| I7 | Tamaño manejable sin GPU: cabe en el disco de un portátil de estudiante y se procesa en CPU | O | Tamaño medido en `inventario_datos.py` | Restricción de recursos |
| I8 | Procedencia documentada: institución, artículo o reto de referencia y cita | O | Se puede llenar la ficha completa (tarea 1203) | RC-03 |
| I9 | Etiquetas de más de un observador o validadas por expertos | D | Documentación del conjunto | Riesgo 3 (calidad) |
| I10 | Más casos etiquetados que el conjunto principal | D | Conteo en el inventario | Riesgo 3 (cantidad) |

## 3. Criterios de exclusión

Se descarta un conjunto si ocurre **cualquiera** de estos casos:

| # | Causa de exclusión |
|---|---|
| E1 | Exige un convenio con un hospital o una solicitud con aprobación ética propia |
| E2 | No se encuentra una licencia ni un acuerdo de uso, o prohíbe el uso académico |
| E3 | Contiene datos identificables (nombre, fecha de nacimiento, identificador de historia clínica en cabeceras o nombres de archivo) |
| E4 | No es T2 de próstata (por ejemplo, solo CT, solo ecografía o solo secuencias de difusión) |
| E5 | No trae máscaras de la glándula |
| E6 | Formato propietario que obliga a software de pago |
| E7 | Tamaño que requiere GPU o almacenamiento que el equipo no tiene |
| E8 | No se puede citar (sin artículo, sin DOI ni página del reto) |

## 4. Reglas de uso del resultado

1. **Un solo conjunto principal** (cumple todo I1–I8 con licencia verificada) y **al menos uno de respaldo** (riesgo 3).
2. Un conjunto con licencia «por verificar» **no puede ser el principal**. Puede servir de respaldo solo de referencia, sin redistribuirlo.
3. Cuando un conjunto exige acuerdo de uso, se respeta la restricción más estricta: no redistribuir ni subir al repositorio.
4. Los datos descargados no se versionan: `datos/` está en `.gitignore`.
5. Los criterios se aplican a cada candidato en `eleccion_dataset.md` (tarea 1202) y los resultados quedan en las fichas (tarea 1203).
