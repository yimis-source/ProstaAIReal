# Registro de defectos (LOGD) · Prosta-AI

**Versión:** D6.2 · **Fecha:** 26/11/2026 · **Autor:** Juan David Riascos Erazo (Gerente de calidad y proceso) · TSP adaptado (ver `docs/gestion/metodologia_tsp.md`)

Se agrega D-008 (ciclo 4). El 23/11/2026 se agregan al resumen los defectos del ciclo 5 (D-009 y D-010). El 13/11/2026 (PR #50) se corrigió D-006 en el diseño; queda abierto hasta implementarlo en la interfaz del ciclo 6.

El 24/11/2026 se agregan los defectos del ciclo 6 (D-011 a D-019) y la fase COMP (compilación del frontend). El 25/11/2026 se agregan D-020 a D-022. El 26/11/2026 se agregan D-023 a D-029 (D-024 es del ciclo 7).

## Leyenda

**Tipos de defecto (TSP):**

| Tipo | Nombre |
|---:|---|
| 10 | Documentación |
| 20 | Sintaxis |
| 30 | Construcción / paquetes |
| 40 | Asignación |
| 50 | Interfaz |
| 60 | Chequeo |
| 70 | Datos |
| 80 | Función |
| 90 | Sistema |
| 100 | Entorno |

**Fases (donde se inyecta o se remueve el defecto):**

| Fase | Significado |
|---|---|
| REQ | Requisitos |
| DIS | Diseño |
| IMP | Implementación (código) |
| REV | Revisión (por PR o entre pares) |
| EJE | Ejecución / uso |
| PU | Prueba unitaria |
| INT | Integración |
| COMP | Compilación / construcción (`npm run build`) |

El tiempo de corrección es el tiempo que costó arreglarlo (horas), sin contar el de encontrarlo. «—» significa que sigue abierto.

## Registro

| ID | Fecha | Ciclo | Tarea | Tipo | Fase inyectado | Fase removido | Tiempo de corrección | Descripción | Encontró | Corrigió | Commit / PR |
|---|---|---|---|---:|---|---|---:|---|---|---|---|
| D-001 | 11/10 | H002 | H04 | 10 | REQ | REV | 0,3 h | En `01_requisitos.md` RF-04 quedó sin caso de uso (CU02) y sin origen en la matriz (4.1). | Yimis (revisión del PR #3) | Juan | PR #3 |
| D-002 | 19/10 | C1 | 1204 | 80 | IMP | REV | 0,3 h | `inventario_datos.py` contaba «con máscara» la unión de `imagesTr` y `labelsTr` (contaría imágenes sin etiqueta); debe ser la intersección. | Juan (revisión del PR) | Yeison | PR #7 |
| D-003 | 23/10 | C1 | 1203 | 10 | DIS | REV | 0,2 h | La ficha de PROMISE12 dejaba «por verificar» si la carpeta de prueba trae máscaras; el inventario muestra 30 máscaras. | Fernando | Juan | PR #10 |
| D-004 | 29/10 | C2 | 1301 | 60 | IMP | PU | 1,5 h | Un `.nii.gz` truncado pasaba el control de calidad: SimpleITK lo abre sin error y rellena con ceros los cortes faltantes. Ahora se comprueba el flujo gzip completo antes de leer. | Fernando (prueba `test_archivo_truncado_se_excluye`) | Yeison | PR #19 |
| D-005 | 29/10 | C2 | 1304 | 80 | IMP | PU | 0,2 h | `verificar_fuga.py` comparaba el Dice de las máscaras con `== 1.0` (flotante) y no marcaba prostate_16 ≡ Case23 como misma máscara. | Fernando | Fernando (con Juan) | PR #19 |
| D-006 | 28/10 | C2 | 1307 | 50 | DIS | REV (detectado; sin corregir) | — (abierto) | La pantalla CU03 y el diagrama de navegación dicen «Ejecutar»; debe ser «Procesar». El diseño se corrigió el 13/11/2026 (pantalla CU03, diagrama de navegación e introducción); (PR #50); queda pendiente aplicarlo en la implementación del ciclo 6. | Juan (revisión del PR #17) | Sergio (pendiente) | PR #17 (abierto) |
| D-007 | 05/11 | C3 | 1407 | 80 | IMP | PU | 2,5 h | Sin `.eval()` el dropout (0,15) y la normalización por lotes seguían en modo entrenamiento: prostate_13 Dice 0,2065 (61 289 vóxeles) y prostate_28 0,1726; con `.eval()` 0,9012 (22 172 vóxeles) y 0,8320. Prueba de regresión `assert not modelo.training`. | Fernando (depuración en pareja) | Yeison | PR #29 |
| D-008 | 10/11 | C4 | 1503 | 50 | IMP | PU | 0,5 h | Al agregar la etapa ROI, `PipelineInput` exige `output_dir` y `entrenamiento/evaluar.py` dejó de funcionar; ahora escribe las salidas en una carpeta temporal. | Yeison (al correr la evaluación) | Yeison | PR #41 |
| D-009 | 19/11 | C5 | 1604 | 80 | IMP | PU | 0,2 h | `hd95()` y `distancia_media_superficie()` devuelven `nan` en vez de `inf` cuando solo una máscara está vacía (`np.percentile`/`np.mean` de `[inf]`); la prueba `test_metricas_superficie_mascaras_vacias` falla. Origen: tarea 1604. No afecta los 5 casos reales (ninguna máscara vacía). | Juan (prueba `test_metricas_superficie_mascaras_vacias`) | Juan | `fix(evaluacion): HD95 y distancia media devuelven inf con una máscara vacía (1604)` |
| D-010 | 13/11 | C5 | 1602 | 80 | IMP | EJE | — (dentro de las horas de 1602) | `scripts/medir_rendimiento.py` (tarea 1408) escribía siempre «## GPU: No disponible en este equipo», aunque se midiera con `--dispositivo cuda`, y no medía la memoria de la GPU. Se vio al medir en Colab (Tesla T4). Ahora la sección depende del dispositivo, pone el nombre de la GPU y su memoria pico, y el informe se llama `rendimiento_1408_gpu_<fecha>.md`. Prueba: `tests/test_medir_rendimiento.py`. | Yimis (medición en Colab) | Fernando | `feat(rendimiento): informe y memoria de la GPU en la medición, y resultados en Colab (1602)` |
| D-011 | 24/11 | C6 | 1702 | 70 | IMP | PU | 0,6 h | En la migración `0001_esquema_inicial.py`, escrita a mano, `etapa_trabajo.estado` quedó sin `nullable=False`; en `models.py` es NOT NULL. Lo detectó `test_migracion_igual_a_modelos_sqlite` (y la misma prueba en PostgreSQL con `compare_metadata`). Al corregirlo se ajustó la prueba para ignorar en SQLite un `modify_default` falso de las claves IDENTITY, que SQLite no refleja. | Yimis (prueba `test_db_migracion.py`) | Yimis | `fce2b06` |
| D-012 | 24/11 | C6 | 1702 | 100 | IMP | EJE | 0,3 h | `scripts/postgres_local.sh` no arrancaba el servidor: la ruta del socket Unix dentro de `.pgdata/` medía 111 bytes y el límite es 107. Ahora el clúster escucha solo por TCP en localhost (`unix_socket_directories=''`). | Yimis (al iniciar el clúster) | Yimis | `8b81ca8` |
| D-013 | 24/11 | C6 | 1703 | 50 | IMP | PU | 0,5 h | El manejador del formato común de error se registró para `fastapi.HTTPException`; el 404 de una ruta inexistente lo lanza Starlette con su propia clase, así que salía `{"detail": "Not Found"}`. Prueba: `test_ruta_inexistente_devuelve_404_con_detalle`. Ahora se registra para `starlette.exceptions.HTTPException`. | Yeison (prueba `test_salud.py`) | Yeison | `e44d5ec` |
| D-014 | 24/11 | C6 | 1704 | 20 | IMP | COMP | 0,1 h | `Layout.jsx` importaba `./EstadoAPI.jsx` y el archivo es `EstadoApi.jsx`; en Linux no lo encuentra y `npm run build` fallaba («Could not resolve "./EstadoAPI.jsx"»). Se hicieron tres commits sin compilar. | Sergio (`npm run build`) | Sergio | `c1104d9` |
| D-015 | 24/11 | C6 | 1701 | 10 | REQ | REV | 0,4 h | El análisis de impacto describía mal la pantalla de inicio (CU00) y no mencionaba el menú lateral; el riesgo 8 figuraba «Cerrado» con estrategia distinta a la del Acta, y el informe al docente decía «16 días de trabajo» (son días calendario). | Juan (revisión contra pantallas y Acta) | Juan | `2a8d817` |
| D-016 | 24/11 | C6 | 1702 | 40 | IMP | REV | 0,1 h | `config.py` tenía `max_upload_mb = 500`; RF-03 pide 50 MB por archivo y 150 MB por estudio. Se agregó `max_estudio_mb`. | Fernando (al escribir el contrato) | Yimis | `9ea8a5d` |
| D-017 | 24/11 | C6 | 1700 | 50 | DIS | REV | 0,2 h | El contrato de la API definía el error como `{"detail": ...}`, pero la API (1703) y el cliente de la interfaz (1704) usan `{"detalle": ...}`, con `campos` en el 422. Se igualó el contrato. | Yimis (revisión de integración) | Fernando | `940846c` |
| D-018 | 24/11 | C6 | 1700 | 10 | DIS | REV | 0,3 h | El lanzamiento y el contrato daban RF-05 por cubierto con el `MetadataValidator`, que no revisa metadatos; el contrato pedía validar antes de guardar y a la vez registrar el estudio rechazado; y el criterio para abrir lo condicionado no coincidía con el del análisis de impacto. RF-05 pasa a la 1705. | Yimis (revisión de integración) | Fernando | `76a4507` |
| D-019 | 24/11 | C6 | 1701 | 10 | REQ | REV | 0,3 h | El análisis de impacto hablaba de cuatro etapas (son cinco, con evaluación) y de un estado «Error» (es `fallido`), ponía el punto de decisión el 26/11 a las 18:00 con CU04 incluido (CU04 va el 27/11) y fechas distintas del lanzamiento para el postmortem del ciclo 6 y RR-01. | Yimis (revisión de integración) | Juan | `76b4ea5` |
| D-020 | 25/11 | C6 | 1707 | 80 | IMP | PU | 0,2 h | `AlmacenamientoPrivado.guardar` devolvía la ruta absoluta en disco y no la ruta relativa a `storage_dir`, que es la que pide RB-02 para la base. Fallaron `test_guarda_con_ruta_relativa_y_sha256` y dos pruebas de repositorios (`RepositorioArchivos.registrar` rechaza rutas absolutas). | Yimis (pruebas de almacenamiento) | Yimis | `6344072` |
| D-021 | 25/11 | C6 | 1706 | 50 | IMP | PU | 0,1 h | El cliente de la interfaz enviaba la imagen en el campo `archivo` del multipart y el contrato (4.4) pide `archivos`: toda carga habría dado 422 «Seleccione al menos un archivo de imagen.». `npm run build` no lo detecta; se vio con una prueba del cliente contra una API mínima del contrato. | Sergio (prueba del cliente en node) | Sergio | `dce7ba2` |
| D-022 | 25/11 | C6 | 1705 | 80 | IMP | PU | 0,6 h | RF-05: la cabecera NIfTI se limpiaba en memoria, pero se guardaban los bytes originales, así que el archivo en disco conservaba `descrip`, `aux_file`, `intent_name` y `db_name`. Prueba: `test_rf05_cabecera_guardada_sin_texto_libre`. Ahora se guarda el NIfTI limpio y la prueba comprueba también que vóxeles y matriz no cambian. | Yeison (prueba `test_estudios.py`) | Yeison | `8b5feea` |
| D-023 | 26/11 | C6 | 1711 | 80 | IMP | PU | 0,3 h | Cuando una etapa del pipeline fallaba, el observador del servicio de procesamiento solo escribía la hora de fin y la etapa quedaba `en proceso` (el trabajo sí quedaba `fallido`). Fallaron `test_fallo_en_una_etapa` y `test_fallo_inesperado_no_muestra_datos_internos`. Ahora la etapa queda `fallido` y, si el error no lo avisó el pipeline, se cierra igual. | Yimis (pruebas del servicio) | Yimis | `c9a3c3a` |
| D-024 | 26/11 | C7 | 1801 | 10 | DIS | REV | 0,1 h | En `riesgos_residuales.md`, el riesgo 7 contaba D-022 entre los defectos de interfaz; en el LOGD es tipo 80 (función). | Juan (verificación contra el LOGD) | Juan | `343fed5` |
| D-025 | 26/11 | C6 | 1709 | 80 | IMP | INT | 0,5 h | El 409 «El estudio ya tiene un procesamiento pendiente o en curso.» solo miraba si el último trabajo estaba `en proceso`, no los `pendiente`: un segundo «Procesar» seguido creaba otro trabajo. Se vio al procesar prostate_13 por la API y lo confirmaron `test_procesar_con_trabajo_pendiente_da_409` y otra prueba. | Yeison (prueba por la API) | Yeison | `08af627` |
| D-026 | 26/11 | C6 | 1710 | 80 | IMP | PU | 0,2 h | Al salir de la pantalla de estado con una respuesta en camino, la consulta periódica seguía llamando a `GET /api/trabajos/{id}` cada 2 s, porque no miraba si se había detenido después del `await`. Prueba del cliente en node: «siguió consultando la API tras detener: 3 llamadas». | Sergio (prueba del cliente) | Sergio | `74752bc` |
| D-027 | 26/11 | C6 | 1711 | 80 | DIS | INT | 0,2 h | Ningún componente marcaba el estudio como `no compatible` cuando fallaba el control de calidad, como pide el contrato (4.4); el 409 «no compatible» de la API nunca se alcanzaba. Ahora lo marca el servicio en la misma transacción del fallo. | Yeison (al integrar la 1709) | Yimis | `94bb45c` |
| D-028 | 26/11 | C6 | 1711 | 80 | IMP | REV | 0,4 h | `procesar_siguiente()` cerraba la sesión del `SELECT … FOR UPDATE SKIP LOCKED` antes de marcar el trabajo `en proceso`, así que el bloqueo no protegía nada: con dos procesos ambos podían tomar el mismo trabajo. Prueba con dos sesiones contra PostgreSQL: «el segundo proceso tomó el mismo trabajo que el primero». | Yeison (revisión del código de la 1711) | Yimis | `a09077b` |
| D-029 | 26/11 | C6 | 1708 | 60 | IMP | PU | 0,1 h | La prueba de integración `test_esquema_creado_por_la_migracion` esperaba la revisión `0001` fija y falló al agregar la migración `0002` («assert '0002' == '0001'»). | Yimis (pruebas con PostgreSQL) | Yimis | `a09077b` |

## Resumen por ciclo

| Ciclo | Defectos | Inyectados en | Removidos en | Tipos | Tiempo total de corrección | Rendimiento de revisión (% encontrados antes de PU) |
|---|---:|---|---|---|---:|---|
| H002 | 1 | REQ 1 | REV 1 | 10: 1 | 0,3 h | 1 de 1 (100 %) |
| C1 | 2 | IMP 1, DIS 1 | REV 2 | 80: 1, 10: 1 | 0,5 h | 2 de 2 (100 %) |
| C2 | 3 | IMP 2, DIS 1 | PU 2, REV 1 | 60: 1, 80: 1, 50: 1 | 1,7 h | 1 de 3 (33 %) |
| C3 | 1 | IMP 1 | PU 1 | 80: 1 | 2,5 h | 0 de 1 (0 %) |
| C4 | 1 | IMP 1 | PU 1 | 50: 1 | 0,5 h | 0 de 1 (0 %) |
| C5 | 2 | IMP 2 | PU 1, EJE 1 | 80: 2 | 0,2 h (D-010 dentro de 1602) | 0 de 2 (0 %) |
| C6 (al 26/11) | 18 | IMP 13, DIS 3, REQ 2 | PU 8, REV 6, INT 2, EJE 1, COMP 1 | 80: 7, 10: 3, 50: 3, 20: 1, 40: 1, 60: 1, 70: 1, 100: 1 | 5,4 h | 6 de 18 (33 %) |
| C7 (al 26/11) | 1 | DIS 1 | REV 1 | 10: 1 | 0,1 h | 1 de 1 (100 %) |
| **Acumulado** | 29 | | | | 11,2 h | 11 de 29 (38 %) |

**Defectos por fase (acumulado):**

| Fase | Inyectados | Removidos |
|---|---:|---:|
| REQ | 3 | 0 |
| DIS | 6 | 0 |
| IMP | 20 | 0 |
| REV | 0 | 11 |
| EJE | 0 | 2 |
| PU | 0 | 13 |
| COMP | 0 | 1 |
| INT | 0 | 2 |

**Defectos por tipo (acumulado):**

| Tipo | Cantidad |
|---|---:|
| 10 Documentación | 6 |
| 20 Sintaxis | 1 |
| 40 Asignación | 1 |
| 50 Interfaz | 5 |
| 60 Chequeo | 2 |
| 70 Datos | 1 |
| 80 Función | 12 |
| 100 Entorno | 1 |

Rendimiento de revisión = defectos encontrados en revisión (REV) / defectos totales del ciclo. En D-006 la revisión lo encontró pero todavía no está corregido, así que cuenta como encontrado en REV y sigue abierto.

