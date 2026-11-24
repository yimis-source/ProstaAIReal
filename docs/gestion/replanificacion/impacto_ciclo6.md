# Análisis de impacto del recorte de los ciclos 6 y 7

**Autor:** Juan David Riascos Erazo (Analista, Monitoreo y control; Gerente de calidad y proceso) · **Fecha:** 24/11/2026 · **Versión:** 1.1 · **Tarea:** 1701 · **Aprueba:** Yimis Buenaventura (Director de Proyecto) · Proyecto Prosta-AI, Universidad Santiago de Cali 2026-2

Este análisis es el paso 2 de la replanificación (metodología TSP, sección 9) y del control de cambios del Acta (sección 5.2.1). La replanificación se registra en el lanzamiento del ciclo 6 (`docs/gestion/tsp/ciclo6_lanzamiento.md`, a cargo de Fernando), que enlaza este documento. El informe al Propietario del Proyecto está en `informe_docente_ciclo6.md`, en esta misma carpeta.

Fuentes: Acta de Constitución v1.1 (`docs/docsf/1.1 Inicio/`), SRS v1.0 (`docs/ejecucion/fuentes/1.3.1.1_SRS_requisitos_ISO29148.md`), matriz de requisitos (`1.3.1.2_matriz_trazabilidad.md`), resumen de requisitos (`docs/ejecucion/01_requisitos.md`), trazabilidad T5 (`docs/gestion/trazabilidad.md`), postmortem del ciclo 5 y pantallas CU00 a CU06 (`docs/ejecucion/assets/pantallas/`).

## 1. El cambio

El Propietario del Proyecto adelantó la entrega final: todo debe estar terminado el **sábado 28/11/2026**.

| Ciclo | Fechas antes | Fechas después | Hito | Fecha del hito antes → después |
|---|---|---|---|---|
| 6 · Desarrollo web e integración completa (Entregables 6 y 7) | 26/11–02/12 | **24/11–27/11** (código congelado la noche del 27/11) | H008 | 02/12 → 27/11 |
| 7 · Cierre académico: documentación final, lecciones aprendidas y acta de aceptación (Entregable 8) | 03/12–09/12 | **25/11–28/11**, en paralelo con el ciclo 6 | H009 | 09/12 → 28/11 |

Punto de partida al 24/11:

- El ciclo 5 cerró el 23/11 (`v0.5-ciclo5`), dos días antes de H007 (25/11).
- El pipeline está probado: control de calidad, preparación, segmentación 3D con el modelo preentrenado `prostate_mri_anatomy`, ROI alineada e imagen exportada con aviso. Hay 84 pruebas en verde.
- Métricas en los 5 casos de prueba: Dice 0,8925 ± 0,0340 e IoU 0,8071 ± 0,0534. Tiempo por estudio: 14,1 s en CPU y 5,0 s en GPU (Colab).
- **La aplicación web no existe todavía**: no hay código de FastAPI, React (Vite) ni PostgreSQL.
- La lectura de DICOM no está implementada: `backend/prosta_ai/pipeline/io.py` la deja para el ciclo 6.
- D-006 («Ejecutar» en lugar de «Procesar») sigue abierto. El diseño ya se corrigió; falta la interfaz.

## 2. Impacto en el alcance

### 2.1 Requisito por requisito

Prioridad y origen tal como aparecen en la SRS (tablas 5 a 17) y en la matriz. «Se hace»: entra en el ciclo 6 recortado. «Se mantiene»: ya está verificado o se verifica sin trabajo nuevo de desarrollo. «Condicionado»: entra solo si se cumple el punto de decisión de la sección 2.3. «Sale»: no se implementa en esta versión.

| Requisito | Qué pide (resumen) | CU | Prioridad SRS | Matriz | Decisión | Nota |
|---|---|---|---|---|---|---|
| RF-01 | Inicio de sesión básico | CU01 | Should | 4.7 | Se hace | Acceso con alias y contraseña, sin registro de cuentas (DEC-01, RC-05). Es Should, pero lo necesitamos para asociar los estudios a una sesión |
| RF-02 | Cargar uno o varios estudios | CU02 | Must | 4.1 | Se hace | Solo NIfTI (`.nii`, `.nii.gz`), con selección múltiple |
| RF-03 | Validar formato y tamaño (50 MB por archivo, 150 MB por estudio) | CU02 | Must | 4.1 | Se hace, con cambio | Formato admitido: NIfTI. La nota de la SRS admite DICOM y NIfTI; DICOM pasa a condicionado (ver RF-02 DICOM abajo). Los límites de tamaño no cambian |
| RF-04 | Rechazar archivos corruptos con mensaje claro | CU02 | Must | 4.1 | Se hace | Se reutiliza `validators.py` (el NIfTI truncado ya se rechaza en el pipeline) |
| RF-05 | Eliminar metadatos que identifiquen a una persona o rechazar el archivo | CU02 | Must | 2.2 | Se hace | **No estaba en la lista propuesta (RF-02 a RF-04).** Lo agregamos: es Must y sostiene el criterio de aceptación 6 del Acta (vital). En NIfTI: vaciar los campos de texto de la cabecera y reemplazar el nombre del archivo por el ID anónimo |
| RF-02 / RF-03 (DICOM) | Carga de DICOM en `.zip` | CU02 | Must (parte de RF-02 y RF-03) | 4.1 | Condicionado | Exige leer series DICOM y desidentificarlas (RF-05), que es lo más costoso de CU02. Si no entra, la versión del 28/11 admite solo NIfTI y se documenta |
| RF-06 | Flujo automático desde «Procesar» | CU03 | Must | 4.2 | Se hace | En segundo plano; la API llama al pipeline existente. Incluye la corrección de D-006 |
| RF-07 | Estado de cada etapa | CU03 | Must | 4.2 | Se hace | Las cuatro etapas de `stages.py` (control de calidad, preparación, segmentación y ROI), notificadas con el observador de `progress.py` |
| RF-08 | Mensaje claro y parada controlada si falla una etapa | CU03 | Must | 4.2 | Se hace | `StageError` del pipeline convertido en estado «Error» con su mensaje |
| RF-09 | Mismas transformaciones en entrenamiento e inferencia | CU03 | Must | 3.2 | Se mantiene | Verificado (ciclos 2 y 5); la API no cambia la preparación |
| RF-10 | Excluir y registrar imágenes que no pasen el control de calidad | CU03 | Must | 3.2 | Se mantiene | Verificado en scripts y pipeline |
| RF-11 | Segmentación 3D y máscara | CU03 | Must | 3.4 | Se mantiene | Modelo preentrenado (decisión de la tarea 1603) |
| RF-12 | ROI alineada con la imagen original | CU03 | Must | 4.3 | Se mantiene | Verificado (ciclo 4) |
| RF-13 | ROI superpuesta en el visor | CU04 | Must | 4.3 | Se hace | Visor por cortes 2D de `visor_roi.md`; hoy está «Parcial» en la trazabilidad |
| RF-14 | Comparar con y sin máscara | CU04 | Must | 4.3 | Se hace | Dos paneles sincronizados e interruptor de la ROI |
| RF-15 | Aviso en toda pantalla de resultados y salida exportada | CU04 | Must | 2.3 | Se hace | Un solo componente de aviso con el texto de `AVISO_EXPERIMENTAL`; la exportación sigue pasando por `renderizador_exportacion()` |
| RF-16 | Sin lenguaje clínico | CU04 | Must | 2.3 | Se hace | Inspección de todos los textos de las pantallas |
| RF-17 | Panel de explicación (qué muestra, métricas, limitaciones) | CU04 | Must | 4.4 | Se hace | Texto de `docs/diseno/texto_roi.md` |
| RF-18 | Registrar cada estudio con resultado y métricas | CU05 | Should | 4.5 | Se hace en parte | El registro de estudios, trabajos y resultados ya lo exigen RB-01 y el procesamiento en segundo plano. Métricas por estudio solo cuando hay máscara de referencia |
| RF-19 | Consultar estudios y resultados registrados | CU05 | Should | 4.5 | Condicionado | Pantalla «Mis estudios» (`cu05_estudios`, `cu05_estudios_vacio`) |
| RF-20 | Asistente de IA de orientación | CU06 | Could | 4.6 | Sale | La SRS (nota de la tabla 10) ya prevé dejarlo documentado como opcional si pone en riesgo el alcance |
| RF-21 | Agentes con funciones definidas y salidas revisables | CU06 | Could | 4.6 | Sale | Igual que RF-20 |
| RF-22 | Agentes sin decisiones autónomas ni contenido clínico | CU06 | Could | 4.6 | Sale | Igual que RF-20 |
| RF-23 | Dice e IoU por caso y promedio | — | Must | 3.5 | Se mantiene | Cumplido en el ciclo 5 |
| RF-24 | Dice medio ≥ 0,80 | — | Should | 3.5 | Se mantiene | Cumplido en el ciclo 5 (0,8925) |
| RU-01 | Usuarios de prueba completan carga, procesamiento y visualización sin ayuda | CU01 a CU05 | Should | 5.2 | Condicionado (reducido) | Prueba corta el 28/11 sobre la versión congelada; los hallazgos se registran, pero solo se corrigen textos (ver sección 4) |
| RR-01 | Un estudio en ≤ 2 min | CU03 | Should | 5.1 | Se hace | 5 casos de prueba enviados por la API, de punta a punta; tiempo promedio y máximo |
| RB-01 | Modelo de datos con estudios, resultados y métricas, sin campos personales | CU05 | Must | 4.5, 2.2 | Se hace | PostgreSQL: usuarios (alias y hash), estudios, trabajos con estado y resultados; archivos en disco |
| RB-02 | Sin datos personales en base de datos ni archivos | — | Must | 2.2 | Se hace | Verificación del Tester antes de cada integración |
| RC-01 | Stack React, FastAPI, PostgreSQL, PyTorch/MONAI, Git/GitHub | — | Must | 5.3 | Se mantiene | Vite es la herramienta de construcción de React; no cambia el stack |
| RC-02 | Cliente-servidor con el módulo de IA desacoplado | — | Must | 5.3, 3.4 | Se mantiene | El procesamiento corre fuera de la petición HTTP |
| RC-03 | Solo datos públicos y anónimos con ficha | — | Must | 2.1, 3.1 | Se mantiene | Sin efecto (ciclo 1) |
| RC-04 | División por paciente | — | Must | 3.3 | Se mantiene | Sin efecto (ciclo 2) |
| RC-05 | Sin cuentas, roles ni permisos adicionales | — | Must | 4.7 | Se mantiene | Se verifica por inspección en el ciclo 6 |
| RC-06 | Solo aplicación web | — | Must | Acta 3.1.2 | Se mantiene | Sin efecto |
| RN-01 | Ley 1581 de 2012 y Decreto 1377 de 2013 | — | Must | 2.1, 2.2 | Se mantiene | Depende de RF-05 y RB-02 |
| RN-02 | No presentarse como software ni dispositivo médico | — | Must | 2.3 | Se mantiene | Depende de RF-15 y RF-16 |
| RN-03 | Requisitos según ISO/IEC/IEEE 29148 | — | Must | 6.1 | Se mantiene | Sin efecto |
| RA-01 | Reproducibilidad (instrucciones, versiones, semillas, pesos) | — | Should | 5.4 | Se hace en el ciclo 7 | Un integrante distinto del autor sigue las instrucciones desde cero el 28/11 |
| RA-02 | Cada requisito vinculado en la matriz | — | Must | 6.1, 6.4 | Se mantiene | Trazabilidad T6 (27/11) y T7 (28/11) |

Fuera de los requisitos: el **visor 3D** sale. No es un requisito de la SRS, que pide un visor por cortes (sección 1.3.2); quitarlo no afecta ningún RF.

### 2.2 Resumen

| Prioridad | Total en la SRS | Se hace o se mantiene | Condicionado | Sale |
|---|---:|---:|---:|---:|
| Must | 29 | 29 (en RF-03 cambia el contenido: solo NIfTI si DICOM no entra) | 0 | 0 |
| Should | 7 | 5 (RF-01, RF-18 en parte, RF-24, RR-01, RA-01) | 2 (RF-19, RU-01) | 0 |
| Could | 3 | 0 | 0 | 3 (RF-20 a RF-22) |
| **Total** | **39** | **34** | **2** | **3** |

Por caso de uso: CU01, CU02 (sin DICOM), CU03 y CU04 completos; CU05 condicionado (el registro sí se hace); CU06 fuera.

Efecto en las pantallas diseñadas (`docs/ejecucion/assets/pantallas/`):

- **CU00 (inicio):** se mantienen sus tres tarjetas: «Cargar estudios» (CU02), «Procesar un estudio» (CU03) y «Visualizar ROI» (CU04). Salen el enlace «Abrir asistente» (CU06) y, si CU05 no entra, la tabla «Últimos estudios» con su botón «Ver todos los estudios». Si DICOM no entra, la tarjeta de carga dice solo «NIfTI» y no «DICOM · NIfTI».
- **Menú lateral (todas las pantallas):** sale «Asistente IA» y, si CU05 no entra, también «Mis estudios».
- **CU02:** si DICOM no entra, el texto de formatos admitidos dice solo NIfTI (`.nii`, `.nii.gz`).

### 2.3 Punto de decisión de lo condicionado

**Jueves 26/11 a las 18:00.** Si CU02, CU03 y CU04 pasan la prueba de integración con los 5 casos de prueba, se abre CU05 (RF-19) y, después, la carga de DICOM en `.zip`. Si no pasan, lo condicionado sale y se documenta igual que CU06. Decide Yimis con el informe de pruebas de Fernando. El orden no se invierte: CU05 cuesta menos porque los datos ya están en PostgreSQL; DICOM implica leer series y desidentificarlas.

## 3. Impacto en el tiempo

### 3.1 Fechas e hitos

| Hito | Descripción (Acta 4.2) | Antes | Después | Diferencia |
|---|---|---|---|---|
| H007 | Ciclo 5: evaluación técnica del modelo | 25/11 | Cumplido el 23/11 | Sin cambio |
| H008 | Ciclo 6: desarrollo web e integración completa (Entregables 6 y 7) | 02/12 | 27/11 | −5 días |
| H009 | Ciclo 7: cierre académico, documentación final, lecciones aprendidas y acta de aceptación (Entregable 8) | 09/12 | 28/11 | −11 días |

| Ciclo | Días antes | Días después | Variación |
|---|---:|---:|---:|
| 6 | 7 (26/11–02/12) | 4 (24/11–27/11) | −3 (−43 %) |
| 7 | 7 (03/12–09/12) | 4 (25/11–28/11) | −3 (−43 %) |
| Lo que queda del proyecto desde el 24/11 | 16 (24/11–09/12) | 5 (24/11–28/11) | −11 (−69 %) |

Los ciclos 6 y 7 se solapan del 25/11 al 27/11. El 28/11 es sábado.

### 3.2 Horas

El plan del ciclo 6 es de **81 h** (lanzamiento de Fernando).

| Medida | Con 7 días | Con 4 días |
|---|---:|---:|
| Horas del equipo por día | 11,6 h | 20,3 h |
| Horas por persona por día (5 personas) | 2,3 h | 4,1 h |

- En el ciclo 5 trabajamos en promedio 3,0 h por persona en cada día con tarea asignada. El ciclo 6 recortado pide 4,1 h, un 35 % más, y eso **sin contar las horas del ciclo 7**, que corre en paralelo del 25/11 al 28/11 y todavía no tiene plan.
- La desviación media de los ciclos 1 a 5 fue +12,8 % (+15, +17, +16, +7 y +9 %). Si se repite, las 81 h se vuelven unas 91 h, es decir, 22,8 h del equipo por día.
- Las 81 h solo caben en 4 días si el alcance es el de la sección 2 (lo condicionado no está en ese plan o entra solo con horas que sobren) y si las tareas del ciclo 7 son de documentación, sin código.

### 3.3 Efecto en el proceso TSP

- **Postmortem del ciclo 6:** la regla de la sección 4 de la metodología dice que se escribe al iniciar el ciclo siguiente. Como el ciclo 7 empieza el 25/11, antes de que termine el 6, el postmortem del ciclo 6 se escribe el 28/11 junto con el del ciclo 7, en su propio PR y antes del merge de cierre.
- **Lanzamiento del ciclo 7:** Fernando lo escribe el 25/11, con su plan de horas en el LOGT el mismo día (lección 2 del ciclo 5).
- **Etiquetas:** `v0.6-ciclo6` sobre el merge de cierre del 27/11 y `v0.7-ciclo7` el 28/11.
- En el postmortem se mide contra las fechas nuevas y también contra el plan original (metodología, sección 9, paso 5).

## 4. Impacto en la calidad

### 4.1 Qué se mantiene

| Control | Se mantiene | Ajuste por el ritmo |
|---|---|---|
| Revisión de todo PR por otra persona | Sí | Lista de verificación corta (aviso, lenguaje, datos personales, pruebas en verde); se pide revisión en menos de 2 h y no se juntan los PR al final del día |
| Pruebas existentes (84) en verde antes de cada integración | Sí | Sin cambio |
| Pruebas de la API (pytest con el cliente de pruebas de FastAPI) | Sí | RF-02 a RF-08: carga válida, formato no admitido, tamaño excesivo, archivo corrupto, metadatos de texto en la cabecera, estado por etapa y error controlado |
| Prueba de integración de punta a punta | Sí | Con los 5 casos de prueba de Task05 (RF-06, RF-13) |
| RR-01 | Sí | Los mismos 5 casos por la API, desde la carga hasta que el resultado está guardado; promedio y máximo frente a 120 s |
| Inspección de pantallas (RF-15, RF-16, RF-17, D-006) | Sí | Sergio y Juan, una sola pasada sobre la versión del 27/11 |
| Verificación del Tester sin datos personales (RB-02, criterio 6 del Acta) | Sí | Antes de cada integración y sobre la versión congelada |
| Inspección de RC-05 (sin cuentas ni roles) | Sí | Sobre las tablas de PostgreSQL y las rutas de la API |
| Criterios de salida de la metodología (sección 8, puntos 1 a 8) | Sí | El punto 6 (postmortem) se cumple el 28/11, como se explicó en la sección 3.3 |

### 4.2 Qué se reduce

- **Pruebas del frontend:** no habrá pruebas automatizadas de los componentes de React. Las pantallas se prueban con un guion funcional manual de Fernando (CU01 a CU04) y con la inspección.
- **Usabilidad (RU-01):** prueba corta con 3 estudiantes el 28/11 sobre la versión congelada, con el registro de tareas completadas y observaciones. Los hallazgos se registran; solo se corrigen textos si no tocan código. El resto queda como riesgo residual en la documentación final.
- **Corrección de defectos después del 27/11:** solo los que rompan el flujo vital (cargar, procesar, ver la ROI con el aviso) o dejen datos personales. Los demás quedan abiertos en el LOGD con «fuera de la versión entregada».

### 4.3 Riesgos de calidad por el ritmo

- Revisiones de PR superficiales: el rendimiento de revisión del ciclo 5 ya fue 0 de 2.
- Defectos de interfaz (tipo 50) entre la API y React, porque se construyen al mismo tiempo. Se mitiga fijando los contratos de la API el 24/11 a partir de `docs/ejecucion/02_arquitectura.md`.
- Que la documentación del ciclo 7 describa una versión distinta de la congelada.
- Que las horas y los defectos no se registren al momento y haya que reconstruirlos (lección 4 del ciclo 5).

## 5. Impacto en los riesgos

Mismo formato del Acta (sección 3.8): probabilidad (P) e impacto (I) de 1 a 5, NR = P × I.

### 5.1 Riesgos del Acta afectados

| ID | Riesgo | Estado | P antes → después | I antes → después | NR antes → después | Dueño | Estrategia | Detalle de la acción |
|---|---|---|---|---|---|---|---|---|
| 1 | Capacidad de cómputo para ejecutar el modelo 3D | Abierto | 4 → 2 | 4 → 4 | 16 → 8 | Yeison Bolaños | Reducir | Baja: la inferencia ya se midió en CPU (14,1 s por estudio). La aplicación infiere en CPU y no depende de Colab |
| 2 | Curva de aprendizaje más lenta de lo previsto | Abierto | 4 → 4 | 3 → 4 | 12 → 16 | Yimis Buenaventura | Reducir | FastAPI, React y PostgreSQL son nuevos para la mayoría y ya no hay margen. Se trabaja en parejas el 24/11 y el 25/11 sobre una base mínima (API con una ruta, una pantalla y una tabla) antes de repartir |
| 5 | Que una salida experimental se interprete como uso médico | Abierto | 2 → 3 | 5 → 5 | 10 → 15 | Sergio Meneses | Evitar | Hay pantallas nuevas hechas con prisa. Un solo componente de aviso en el diseño de las pantallas de resultados, una prueba que busca el texto de `AVISO_EXPERIMENTAL` en las respuestas, e inspección de textos el 27/11 |
| 6 | Retrasos por baja disponibilidad de integrantes | Abierto | 4 → 4 | 3 → 4 | 12 → 16 | Yimis Buenaventura | Reducir | Ya no hay colchón: un día perdido es el 25 % del ciclo. Se reasignan tareas el mismo día y lo condicionado es lo primero que sale |
| 7 | Problemas de integración entre frontend, backend y modelo | Abierto | 3 → 4 | 4 → 4 | 12 → 16 | Yeison Bolaños | Reducir | El riesgo más alto del recorte. Flujo de punta a punta mínimo el 25/11 (carga de un NIfTI, procesamiento y respuesta) y crecer desde ahí; contratos de la API fijados el 24/11 |
| 8 | Agentes de IA con resultados no verificables o que amplíen el alcance | Abierto (se cierra si el Propietario aprueba el recorte) | 3 → 1 | 3 → 3 | 9 → 3 | Juan David Riascos | Reducir → Evitar | CU06 sale del alcance (RF-20 a RF-22): al quitar los agentes se elimina la causa del riesgo, por eso la estrategia pasa de reducir a evitar |

Los riesgos 3 (datos insuficientes o con licencias restringidas) y 4 (fuga entre entrenamiento y prueba) no cambian: se trataron en los ciclos 1, 2 y 5 y el recorte no toca los datos ni el modelo.

### 5.2 Riesgos nuevos

| ID | Riesgo | Estado | P | I | NR | Dueño | Estrategia | Detalle de la acción |
|---|---|---|---:|---:|---:|---|---|---|
| 9 | Defectos que llegan a la entrega porque las revisiones de PR se hacen con prisa | Abierto | 4 | 4 | 16 | Juan David Riascos | Reducir | Lista de verificación corta por PR, revisión en menos de 2 h, LOGD revisado cada noche. Congelamiento el 27/11 para tener un día de verificación sin cambios de código |
| 10 | Documentación final (ciclo 7) que no coincide con la versión congelada, por hacerse en paralelo | Abierto | 4 | 3 | 12 | Sergio Meneses | Reducir | Hasta el 27/11 se escribe lo que no depende del código (lecciones, riesgos, decisiones); el 28/11 se completan instrucciones, evidencias y capturas sobre la versión `v0.6-ciclo6` |
| 11 | Entorno de PostgreSQL y procesamiento en segundo plano que no funciona igual en todos los equipos | Abierto | 3 | 4 | 12 | Yeison Bolaños | Reducir | Una guía de instalación y un script que crea las tablas, probados el 24/11 en dos equipos distintos; versiones fijadas en el repositorio |
| 12 | Que el Propietario objete el recorte cuando ya no hay tiempo para cambiarlo | Abierto | 2 | 5 | 10 | Yimis Buenaventura | Reducir | Informe enviado el 24/11 con plazo de respuesta el 25/11 a las 12:00. Lo que está en «Se hace» no cambia con ninguna respuesta, así que se avanza en eso mientras tanto |
| 13 | Que el tiempo de punta a punta en la web (carga y guardado incluidos) pase de 2 minutos | Abierto | 2 | 3 | 6 | Fernando Angulo | Aceptar | La inferencia sola tarda 14,1 s en CPU, lejos del límite. Se mide el 26/11 con los 5 casos; si falla, se documenta la causa (RR-01 es Should) |
| 14 | Que las horas y los defectos se registren tarde y haya que reconstruirlos | Abierto | 3 | 2 | 6 | Juan David Riascos | Reducir | Cada persona anota sus horas al terminar cada tarea; Juan revisa el LOGD y Fernando el LOGT cada noche del 24/11 al 28/11 |

## 6. Efecto en los criterios del Acta

### 6.1 Criterios de éxito del proyecto (Acta 3.2)

| Criterio | Efecto |
|---|---|
| Entregar todos los entregables dentro de las fechas del calendario 2026-2 (vital) | La fecha la fijó el Propietario: 28/11. Los entregables 6, 7 y 8 se entregan ese día con el alcance de la sección 2 |
| Siete ciclos cerrados, al menos 6 de 7 en la fecha planificada | Los ciclos 6 y 7 se miden contra las fechas replanificadas (27/11 y 28/11) y también contra las originales. Los ciclos 1 a 5 cerraron en su fecha o antes |
| Aprobación del Propietario de las herramientas de gestión (vital) | Requiere que apruebe esta replanificación (Acta 5.2.1) |

### 6.2 Criterios de aceptación del producto (Acta 3.2)

| # | Criterio | Efecto | Estado esperado el 28/11 |
|---|---|---|---|
| 1 | Flujo completo: cargar, procesar, segmentar y ver la ROI en la web (vital) | Ninguno: es exactamente lo que se hace (CU01 a CU04) | Se cumple, con NIfTI |
| 2 | 100 % de los requisitos aprobados con solución implementada y evidencia de prueba en la matriz (vital) | **Afectado.** Con el recorte, RF-19 y RU-01 pueden quedar sin evidencia completa, y RF-20 a RF-22 no se implementan. El criterio solo se puede cumplir si el Propietario aprueba que esos requisitos queden fuera de esta versión. La matriz los marcará como «Fuera de la versión entregada (cambio aprobado el …)» | Se cumple solo con la aprobación del cambio |
| 3 | Dice medio ≥ 0,80, con IoU, condiciones y limitaciones | Ninguno | Cumplido en el ciclo 5 (0,8925) |
| 4 | Tiempo por estudio ≤ 2 min | Ninguno en el criterio; la medición pasa a hacerse por la API con 5 casos | Esperado; la inferencia tarda 14,1 s en CPU |
| 5 | Aviso de salida experimental y no diagnóstica en todas las pantallas de resultados (vital) | Ninguno; sube el riesgo 5 | Se cumple (RF-15) |
| 6 | Ningún dato personal almacenado, verificado por el Tester antes de cada integración (vital) | Ninguno, siempre que RF-05 se haga (por eso se agregó) | Se cumple (RF-05, RB-02) |

## 7. Efecto en los entregables 6, 7 y 8

| Entregable (Acta 3.4) | Qué se entrega el 28/11 | Qué cambia frente al Acta |
|---|---|---|
| 6 · Aplicación web unida (React, FastAPI, PostgreSQL, almacenamiento y módulo de IA) | Acceso básico, carga y validación de NIfTI, procesamiento en segundo plano con estado y errores, visor con y sin ROI, aviso y panel de explicación; datos en PostgreSQL y archivos en disco | Sin asistente de IA (CU06) ni visor 3D. Historial (CU05) y DICOM solo si pasan el punto de decisión |
| 7 · Evidencias de calidad (unitarias, integración, funcionales, usabilidad, rendimiento; Dice e IoU) | Pruebas unitarias y de la API, integración de punta a punta y rendimiento con 5 casos, guion funcional, métricas del ciclo 5 | Usabilidad reducida a una prueba corta con 3 usuarios sobre la versión congelada; sin pruebas automatizadas del frontend |
| 8 · Documentación final (repositorio, instrucciones, decisiones, riesgos residuales, aprendizajes, conclusiones) | Lo mismo que pide el Acta, más el acta de aceptación del ciclo 7 | Se hace en 4 días en paralelo con el ciclo 6 y no en 7 días después de él. Debe incluir este recorte, lo que quedó fuera y los riesgos residuales (CU05/CU06, DICOM, usabilidad reducida) |

## 8. Decisión recomendada

1. **Aprobar el recorte** con el alcance de la sección 2, con dos ajustes a la propuesta:
   - Agregar **RF-05** (Must) a lo que se hace en CU02. Sin él no se puede sostener el criterio 6 del Acta.
   - Dejar escrito que **RF-03 cambia de contenido**: si DICOM no entra, la versión del 28/11 admite solo NIfTI.
2. Lo condicionado (RF-19 y DICOM) se decide el **26/11 a las 18:00** con el informe de pruebas, en ese orden. RU-01 se hace reducido el 28/11.
3. CU06 (RF-20 a RF-22) y el visor 3D **salen** de esta versión. Quedan documentados como trabajo futuro en el Entregable 8 y en la matriz.
4. Como el cambio toca hitos (H008, H009), el contenido del Entregable 6 y el criterio de aceptación 2, **se eleva al Propietario del Proyecto** para su aprobación explícita (Acta 5.2.1; metodología, sección 9, paso 3). Yimis aprueba la replanificación interna y firma el informe como Director.
5. Si el Propietario aprueba:
   - Se registra la solicitud de cambio con la etiqueta «cambio» (Acta 5.2.1).
   - Se actualizan el LOGT (plan del ciclo 6 en 4 días y plan del ciclo 7), el calendario de la metodología y la trazabilidad T6.
   - La tabla de hitos del Acta sube de versión mayor, porque el cambio lo aprueba el Propietario (Acta 5.2.2).
6. El congelamiento del 27/11 se respeta aunque quede algo condicionado sin terminar: lo que no esté integrado y probado esa noche no entra.

*Versión 1.1 (24/11/2026): al revisar el documento contra las pantallas CU00 a CU06 y el Acta se corrigió el efecto en la pantalla de inicio (CU00) y en el menú lateral, y el estado y la estrategia del riesgo 8. Los números de requisitos, prioridades y orígenes no cambiaron.*

*Para este análisis no hay horas reales del ciclo 6: las 81 h son las del plan del lanzamiento. Los números de requisitos, prioridades y orígenes son los de la SRS v1.0 y la matriz v1.0.*
