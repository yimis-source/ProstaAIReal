# Inconsistencias y vacíos entre documentos

Revisión cruzada de los documentos de ejecución. Severidad: **Alta** = contradicción de contenido que un evaluador notaría; **Media** = desalineación que confunde; **Baja** = forma o citación.

| ID | Severidad | Documentos | Inconsistencia | Corrección sugerida |
|---|---|---|---|---|
| I-01 | Resuelta | SRS (RC-05), Matriz 4.7 vs. DEC-01 | Parecía que el diseño implementaba registro de usuarios. **Aclaración del equipo:** no hay registro de cuentas; el sistema solo identifica a quien entra por primera vez (alias + contraseña confirmada). Es compatible con RC-05 y con 4.7 | Resuelta el 13/11/2026: la nota se agregó en el SRS tras la tabla de RC-05/RC-06 |
| I-02 | Resuelta | Diseño de interfaz (pantalla CU03 y diagrama de navegación) | El botón que inicia el procesamiento debe llamarse **«Procesar»** (decisión del equipo); en la pantalla y en el diagrama de navegación aparece «Ejecutar» por descuido | Resuelta el 13/11/2026: «Ejecutar» cambiado por «Procesar» en la pantalla CU03, el diagrama de navegación y la introducción. |
| I-03 | Resuelta | SRS (1.3.3 y 1.5) vs. arquitectura del sistema | El SRS ubicaba la inferencia en Colab y trataba a Colab como componente interno. **Decisión:** Colab es un servicio externo para entrenar y para pruebas de inferencia durante el desarrollo; la aplicación en uso infiere en su servidor | Resuelta el 13/11/2026: corregidos los apartados 1.3.3 y 1.5 del SRS. |
| I-04 | Resuelta | SRS (nota de CU02, RF-03) vs. arquitectura, patrones, datos y diseño | El SRS deja los formatos «por confirmar al cierre del Ciclo 1»; los demás documentos fijan **DICOM y NIfTI** | Resuelta (13/11/2026): el equipo confirma DICOM y NIfTI y límites de 50 MB por archivo y 150 MB por estudio; la nota de CU02 del SRS se actualizó. |
| I-05 | Resuelta | SRS (RF-06) y Matriz 4.2 vs. DEC-02 | RF-06 y 4.2 piden ejecución «sin intervención manual, desde la carga hasta el resultado»; el diseño separa carga (CU02) e inicio (CU03, botón). La justificación lo interpreta como automatización desde «Procesar» | Resuelta: el procesamiento es automático desde que el usuario pulsa «Procesar» (DEC-02). |
| I-06 | Aceptada | Arquitectura de software («Definición y propósito») vs. arquitectura de datos | Dice que «los esquemas de tablas… van en entregables posteriores», pero la arquitectura de datos del mismo Ciclo 2 ya define las tablas | No se corrige: la arquitectura de datos ya existe y la justificación remite a ella |
| I-07 | Aceptada | Arquitectura de software | La sección «Definición y propósito» empieza con «Este documento aplica **ese** enfoque» sin definir ningún enfoque antes (falta la definición de Bass, Clements y Kazman). Además, Bass (2013) y Pressman y Maxim (2020) están en las referencias pero **no se citan en el texto** (incumple APA) | No se corrige por decisión del equipo |
| I-08 | Media | SRS (1.3.5 y 2.1) vs. diseño de interfaz y módulos | El SRS remite los **contratos de la API** al documento de diseño de la solución, pero ningún documento entregado los define | Agregar una tabla breve de endpoints (acceso, carga, procesar, estado, resultados) o retirar la remisión |
| I-09 | Resuelta | Diseño de interfaz (Mis estudios) | «Ver detalle» de un estudio **no compatible** lleva a Procesamiento («Procesar / Ver detalles»), aunque un estudio no compatible no puede procesarse | Resuelta: el equipo confirma el destino de «Ver detalle» tal como está en el diagrama. |
| I-10 | Resuelta | Justificación (archivo) | El archivo se llama `1_3_2_3_Arquitectura_del_sistema_-_Justificación`, pero el contenido justifica la **arquitectura de software** (paquete 1.3.2.4) | Resuelta el 13/11/2026: el archivo original se renombró a «1.3.2.4 Arquitectura de software - Justificación.pdf» en docs/docsf. |
| I-11 | Resuelta | Arquitectura de datos vs. justificación | La arquitectura de datos tiene fecha **22/10/2026**; la justificación la cita como «del 24/10/2026» | Resuelta el 13/11/2026: se unificó a 22/10/2026. |
| I-12 | Baja | SRS, patrones, sistema, datos (referencias) | Versiones citadas distintas: SRS cita Acta v1.0 y Matriz v1.0; patrones cita Acta v1.1, Matriz v1.1 y Arquitectura de software v1.1; el archivo de la matriz dice «Versión 1.0 · 08/10/2026» | Unificar versiones según lo realmente entregado |
| I-13 | Resuelta (☰ pendiente) | Diseño de interfaz | La tabla de pantallas pequeñas aparece como **«Cuadro 1»** y el texto la llama «Tabla 1»; el ícono del menú (☰) no se imprime en el PDF | 13/11/2026: «Cuadro 1» cambiado por «Tabla 1»; el ícono ☰ queda pendiente (usar una fuente con ☰ o escribir «botón de menú»). |
| I-14 | Baja | Arquitectura del sistema | Dice que «el Acta excluye los roles y la administración de cuentas» para justificar un solo actor; es correcto, pero convive con la creación de usuarios (ver I-01) | Mantener; queda resuelto al corregir I-01 |
| I-15 | Resuelta | SRS (alcance 1.2) | Declara que los requisitos 6.2–6.5 de la matriz son de gestión y quedan fuera, pero RA-02 tiene origen en 6.4 | Resuelta el 13/11/2026: rango ajustado a «6.2, 6.3 y 6.5» en el alcance 1.2 del SRS. |
| I-16 | Resuelta | Matriz 4.7 | Redacción con errores: «basico», «aplicacion», «ussurios»; criterio dice «no guarda datos personales de pacientes» (debería ser de nadie) | Resuelta el 13/11/2026: corregidas ortografía y alcance del criterio en la matriz 4.7. |

## Coherencias verificadas (sin conflicto)
- Casos de uso CU01–CU06 idénticos en diagrama, SRS, matriz, arquitecturas, patrones y diseño.
- Siete componentes iguales en arquitectura de software, justificación y diagrama de módulos.
- Estados del trabajo (pendiente, en proceso, completado, fallido) iguales en arquitectura, patrones (State) y base de datos.
- Usuario con solo alias y hash en arquitectura, patrones y base de datos.
- Metas técnicas consistentes: Dice ≥ 0,80, ≤ 120 s, cero datos personales, aviso no diagnóstico.
- Actividades 1306–1309 (Ciclo 2), 1408 (Ciclo 3), 1701–1706 (Ciclo 6) coherentes con el cronograma.
- Equivalencia SRS ↔ matriz disponible en la columna «Origen» del SRS.
