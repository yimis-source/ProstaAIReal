# Contrato de la API · Prosta-AI (ciclo 6)

**Autor:** Fernando José Angulo Núñez (Tester, Gerente de planeación) · **Fecha:** 24/11/2026 · **Tarea:** 1700 · **Versión de la API:** 0.6.0

Este contrato se define **antes de programar** para que la API (Yeison, Yimis) y la interfaz (Sergio) avancen en paralelo durante el ciclo 6. Está recortado al alcance MoSCoW del lanzamiento (`docs/gestion/tsp/ciclo6_lanzamiento.md`, sección 4): no incluye el asistente de CU06, el borrado de estudios, la exportación ni el visor 3D.

Si alguien necesita cambiar una ruta, un código o un campo, primero lo cambia en este documento dentro de su PR y avisa a quien consume la ruta. Las pruebas de integración (1708 y 1715) se escriben contra este documento.

## 1. Reglas generales

| Tema | Regla |
|---|---|
| Prefijo | Todas las rutas empiezan por `/api` |
| Formato | JSON en UTF-8, salvo la carga de archivos (`multipart/form-data`) y los cortes (`image/png`) |
| Nombres de campos | En español, minúsculas y con guion bajo (`fecha_carga`, `estado_admision`). En las respuestas el identificador propio se llama `id`; en las rutas y en las referencias a otro recurso se usa el nombre completo (`id_estudio`, `id_trabajo`) |
| Fechas | ISO 8601 con zona horaria (`2026-11-25T10:30:00-05:00`) |
| Números | Dice e IoU entre 0 y 1, `null` si no hay máscara de referencia; tiempos en segundos |
| Autenticación | Todas las rutas, menos `/api/salud` y las de `/api/acceso`, piden la cabecera `Authorization: Bearer <token>`. Sin token o con token vencido: `401` |
| Propiedad | Cada usuario solo ve sus estudios y trabajos. Pedir uno ajeno devuelve `404`, igual que si no existiera |
| CORS | La API acepta el origen de la interfaz de Vite en desarrollo (`http://localhost:5173`), configurable con las variables `PROSTA_*` |
| Lenguaje | Ningún mensaje ni campo usa lenguaje clínico (RF-16). El aviso de uso no diagnóstico sale de `AVISO_EXPERIMENTAL` en `backend/prosta_ai/constantes.py` |

## 2. Formato de error

Todos los errores devuelven el mismo cuerpo, con un mensaje en español que la interfaz muestra tal cual:

```json
{"detalle": "El archivo no es un NIfTI válido."}
```

| Código | Cuándo |
|---|---|
| 401 | Sin token, token no válido o vencido; alias o contraseña incorrectos |
| 404 | El estudio o trabajo no existe o es de otro usuario; el trabajo todavía no tiene resultado |
| 409 | Conflicto de estado: procesar un estudio no compatible o que ya tiene un trabajo pendiente o en proceso; alias ya registrado |
| 422 | Datos no válidos: formato, tamaño, archivo corrupto, campos del cuerpo, corte fuera de rango |
| 500 | Error inesperado del servidor. El mensaje es genérico; el detalle va al registro del servidor, nunca a la respuesta |

Los errores de validación de FastAPI (pydantic) usan el mismo campo y agregan la lista de campos que fallaron: `{"detalle": "Datos no válidos.", "campos": ["alias"]}`. El campo es `detalle` y no `detail` (el nombre por defecto de FastAPI): la API lo cambia en sus manejadores de error y la interfaz lo lee así.

## 3. Estados y etapas

**Estado de admisión del estudio:** `admitido` o `no compatible` (como en `docs/ejecucion/04_modelo_datos.md`).

**Estado visible del estudio** (se calcula, no se guarda): `no compatible`, `listo para procesar`, `pendiente`, `en proceso`, `completado` o `fallido` (estos cuatro son el estado del último trabajo).

**Estado del trabajo:** `pendiente` → `en proceso` → `completado` o `fallido`.

**Etapas del trabajo**, en este orden fijo (`backend/prosta_ai/pipeline/stages.py`):

| # | Nombre | Qué hace |
|---|---|---|
| 1 | `control de calidad` | Integridad del volumen y metadatos (RF-05, RF-10) |
| 2 | `preparación` | Mismas transformaciones del modelo (RF-09) |
| 3 | `segmentación` | Máscara 3D con el modelo (RF-11) |
| 4 | `ROI` | Máscara en la rejilla de la imagen original (RF-12) |
| 5 | `evaluación` | Dice e IoU si se cargó una máscara de referencia; si no, quedan en `null` |

Cada etapa tiene estado `pendiente`, `en proceso`, `completado` o `fallido`. Si una etapa falla, el trabajo queda `fallido`, las siguientes siguen `pendiente`, y el trabajo trae `etapa_fallida` y `mensaje_error` (RF-08).

## 4. Rutas

### Resumen

| Método y ruta | Éxito | CU / requisitos | Implementa (tarea) | Consume (tarea) |
|---|---|---|---|---|
| `GET /api/salud` | 200 | — (comprobación del servicio) | Yeison (1703) | Sergio (1704) |
| `POST /api/acceso/verificar` | 200 | CU01 · RF-01 | Yeison (1705) | Sergio (1706) |
| `POST /api/acceso` | 200 | CU01 · RF-01, RC-05 | Yeison (1705) | Sergio (1706) |
| `POST /api/estudios` | 201 | CU02 · RF-02, RF-03, RF-04; RB-01, RB-02 | Yeison (1705), persistencia Yimis (1707) | Sergio (1706) |
| `GET /api/estudios/{id_estudio}` | 200 | CU02, CU03 · RF-07 | Yeison (1705) | Sergio (1706, 1710) |
| `POST /api/estudios/{id_estudio}/procesar` | 201 | CU03 · RF-06 | Yeison (1709), integración Yimis (1711) | Sergio (1710, 1714) |
| `GET /api/trabajos/{id_trabajo}` | 200 | CU03 · RF-07, RF-08 | Yeison (1709) | Sergio (1710) |
| `GET /api/trabajos/{id_trabajo}/resultado` | 200 | CU04 · RF-13, RF-15, RF-16, RF-17; RF-18 | Yeison (1713) | Sergio (1713) |
| `GET /api/trabajos/{id_trabajo}/corte/{indice}` | 200 | CU04 · RF-13, RF-14 | Yeison (1713) | Sergio (1713) |
| `GET /api/estudios` | 200 | CU05 · RF-19 (si hay tiempo) | Juan (1712) | Juan (1712) |

Fernando prueba todas las rutas en 1708 (carga y acceso) y 1715 (flujo completo con los 5 casos, RR-01).

### 4.1 `GET /api/salud`

Sin autenticación. Sirve para que la interfaz y las pruebas sepan que la API está arriba.

Respuesta `200`:

```json
{"estado": "ok", "version": "0.6.0"}
```

### 4.2 `POST /api/acceso/verificar` (CU01)

Dice si el alias ya existe, para que la pantalla sepa si pide confirmar la contraseña (primer acceso).

Cuerpo:

```json
{"alias": "estudiante01"}
```

El alias tiene de 3 a 30 caracteres: letras sin tilde, números, `_`, `.` o `-`. No se pide nombre, correo ni ningún otro dato personal (RB-02).

Respuesta `200`:

```json
{"existe": false}
```

Errores: `422` si el alias no cumple el patrón.

### 4.3 `POST /api/acceso` (CU01)

Ingresa. Si el alias no existe, lo crea (primer acceso) y exige `confirmacion` igual a `contrasena`, con mínimo 8 caracteres. La contraseña se guarda solo como hash con sal. No hay roles ni permisos (RC-05).

Cuerpo:

```json
{"alias": "estudiante01", "contrasena": "********", "confirmacion": "********"}
```

`confirmacion` solo se envía en el primer acceso.

Respuesta `200`:

```json
{"token": "<token firmado>", "alias": "estudiante01", "primer_acceso": true}
```

El token vence a las 8 horas. La interfaz lo guarda en memoria de la sesión del navegador y lo manda en `Authorization: Bearer <token>`.

Errores: `401` alias o contraseña incorrectos («Alias o contraseña incorrectos.»); `422` contraseña corta o confirmación distinta; `409` si dos personas crean el mismo alias al mismo tiempo.

### 4.4 `POST /api/estudios` (CU02)

Carga un estudio. `multipart/form-data` con:

| Campo | Obligatorio | Contenido |
|---|---|---|
| `archivos` | Sí | La imagen: un solo archivo `.nii` o `.nii.gz` |
| `referencia` | No | Máscara de referencia `.nii` o `.nii.gz`, para calcular Dice e IoU (se usa en RR-01 con los casos de prueba) |

Validación antes de guardar nada (RF-03, RF-04):

- Formato: solo NIfTI (`.nii`, `.nii.gz`), comprobando la extensión y la cabecera del archivo, no solo el nombre. DICOM en `.zip` queda para «si hay tiempo»; mientras no exista, un `.zip` o `.dcm` se rechaza con un mensaje que diga que en esta versión solo se admite NIfTI.
- Tamaño: máximo 50 MB por archivo y 150 MB por estudio (nota de RF-03). La configuración de la 1702 (variables `PROSTA_*`) debe usar estos límites.
- Archivo corrupto o vacío: se rechaza con mensaje claro.
- Metadatos (RF-05): al admitir, la API vacía los campos de texto de la cabecera NIfTI (`descrip`, `aux_file`, `intent_name`, `db_name`) antes de guardar el archivo. Tarea 1705.

Al admitir, la API asigna un código anónimo (`EST-0001`), guarda los archivos en disco bajo ese código con su SHA-256 y registra el estudio en PostgreSQL (RB-01, RB-02). El nombre original del archivo **no** se guarda, porque puede traer datos de una persona.

Respuesta `201`:

```json
{"id": 12, "codigo": "EST-0012", "formato": "NIfTI", "estado": "listo para procesar"}
```

Errores:

| Código | Ejemplo de `detalle` |
|---|---|
| 422 | «Seleccione al menos un archivo de imagen.» |
| 422 | «Formato no admitido. En esta versión solo se aceptan archivos NIfTI (.nii o .nii.gz).» |
| 422 | «El archivo supera el máximo de 50 MB.» |
| 422 | «El estudio supera el máximo de 150 MB.» (imagen más referencia) |
| 422 | «El archivo está dañado o no es un NIfTI válido.» |
| 500 | «No se pudo guardar el estudio. Intente de nuevo.» (se borra lo guardado a medias) |

Si la validación rechaza el archivo, la API responde `422` y **no registra nada**: ni el estudio ni el archivo. Así se cumple «validación antes de guardar nada» y no hace falta un formato para lo rechazado. El estado `no compatible` queda para un estudio ya admitido que el control de calidad del pipeline rechaza al procesarlo.

### 4.5 `GET /api/estudios/{id_estudio}` (CU02, CU03)

Detalle de un estudio con sus trabajos. La interfaz lo usa después de cargar y para volver a un estudio.

Respuesta `200`:

```json
{
  "id": 12,
  "codigo": "EST-0012",
  "formato": "NIfTI",
  "fecha_carga": "2026-11-25T10:30:00-05:00",
  "estado": "completado",
  "estado_admision": "admitido",
  "id_ultimo_trabajo": 7,
  "dice": 0.874,
  "iou": 0.776,
  "trabajos": [ { "...": "mismo cuerpo que GET /api/trabajos/{id_trabajo}" } ]
}
```

Errores: `404` «Estudio no encontrado.»

### 4.6 `POST /api/estudios/{id_estudio}/procesar` (CU03)

Lo llama el botón **«Procesar»** (D-006). La API no ejecuta la segmentación: crea un trabajo `pendiente` en PostgreSQL y responde de inmediato. Una tarea en segundo plano del mismo backend toma los trabajos pendientes de uno en uno y corre el pipeline (RF-06).

Sin cuerpo.

Respuesta `201`: el trabajo recién creado, con el mismo cuerpo de `GET /api/trabajos/{id_trabajo}` (estado `pendiente` y las cinco etapas en `pendiente`).

Errores: `404` estudio no encontrado; `409` «El estudio no es compatible y no se puede procesar.»; `409` «El estudio ya tiene un procesamiento pendiente o en curso.»

Un estudio con un trabajo `fallido` se puede volver a procesar; se crea un trabajo nuevo.

### 4.7 `GET /api/trabajos/{id_trabajo}` (CU03)

Estado del trabajo y de cada etapa. La pantalla de estado lo consulta cada 2 segundos hasta que el estado sea `completado` o `fallido` (RF-07).

Respuesta `200`:

```json
{
  "id": 7,
  "id_estudio": 12,
  "codigo": "EST-0012",
  "estado": "en proceso",
  "etapa_fallida": null,
  "mensaje_error": null,
  "fecha_creacion": "2026-11-26T09:00:00-05:00",
  "fecha_inicio": "2026-11-26T09:00:02-05:00",
  "fecha_fin": null,
  "etapas": [
    {"nombre": "control de calidad", "estado": "completado", "duracion_s": 1.4},
    {"nombre": "preparación", "estado": "completado", "duracion_s": 6.2},
    {"nombre": "segmentación", "estado": "en proceso", "duracion_s": null},
    {"nombre": "ROI", "estado": "pendiente", "duracion_s": null},
    {"nombre": "evaluación", "estado": "pendiente", "duracion_s": null}
  ]
}
```

Si falla una etapa (RF-08): `"estado": "fallido"`, `"etapa_fallida": "control de calidad"` y `"mensaje_error"` con el mensaje del `StageError` del pipeline (por ejemplo, «El estudio no es un volumen 3D.»). Un error no previsto se muestra con un mensaje genérico, sin trazas.

Errores: `404` «Trabajo no encontrado.»

### 4.8 `GET /api/trabajos/{id_trabajo}/resultado` (CU04)

Datos del resultado para la pantalla de la ROI: métricas, número de cortes y el aviso.

Respuesta `200`:

```json
{
  "id_trabajo": 7,
  "codigo": "EST-0012",
  "dice": 0.874,
  "iou": 0.776,
  "tiempo_total_s": 48.3,
  "modelo": {"nombre": "prostate_mri_anatomy", "version": "<versión fijada>"},
  "cortes": 20,
  "forma": [320, 320, 20],
  "aviso": "Resultado experimental con fines académicos. No es un diagnóstico ni sustituye la valoración de un profesional de la salud."
}
```

- `aviso` va siempre y la interfaz lo muestra en la pantalla de resultados (RF-15), además del aviso fijo del esqueleto (1704).
- El panel explicativo (RF-17: qué muestra la ROI, qué significan Dice e IoU y sus límites) lo escribe Sergio en la interfaz con los textos de `docs/diseno/texto_roi.md`; usa `dice` e `iou` de esta respuesta y dice «sin máscara de referencia» cuando son `null`.

Errores: `404` «Trabajo no encontrado.»; `404` «El trabajo no tiene resultado disponible.» (si no está `completado`).

### 4.9 `GET /api/trabajos/{id_trabajo}/corte/{indice}?capa=imagen|mascara` (CU04)

Un corte axial en PNG. `indice` va de `0` a `cortes - 1`. La interfaz pide la capa `imagen` y, encima, la capa `mascara` (PNG con fondo transparente) para mostrar la ROI superpuesta (RF-13); para comparar con y sin máscara (RF-14) solo oculta o muestra la capa `mascara`, sin pedir nada nuevo a la API.

| Parámetro | Valor por defecto | Valores |
|---|---|---|
| `capa` | `imagen` | `imagen` o `mascara` |

Respuesta `200`: `Content-Type: image/png`.

Errores: `404` trabajo sin resultado; `422` «El corte debe estar entre 0 y 19.»; `422` si `capa` no es `imagen` ni `mascara`.

### 4.10 `GET /api/estudios` (CU05, si hay tiempo)

Lista los estudios del usuario, del más reciente al más antiguo (RF-19).

Respuesta `200`:

```json
[
  {
    "id": 12,
    "codigo": "EST-0012",
    "formato": "NIfTI",
    "fecha_carga": "2026-11-25T10:30:00-05:00",
    "estado": "completado",
    "id_ultimo_trabajo": 7,
    "dice": 0.874,
    "iou": 0.776
  }
]
```

Si no hay estudios, devuelve `[]`.

## 5. Fuera de este contrato

| Ruta del proyecto de referencia | Por qué no está |
|---|---|
| Asistente de IA (`/api/asistente/...`) | CU06 (RF-20 a RF-22) queda fuera del ciclo |
| `DELETE /api/estudios/{id_estudio}` | No está en el alcance MoSCoW del ciclo |
| `GET /api/trabajos/{id_trabajo}/exportar` | No está en el alcance; la imagen de la ROI con aviso ya existe desde el ciclo 4 en el pipeline |
| Visor 3D | Fuera del ciclo |

## 6. Variables de configuración que usa la API

Se leen de variables de entorno con prefijo `PROSTA_` o de un `.env` local que **no** se sube al repositorio (tarea 1702). Como mínimo: URL de PostgreSQL, carpeta de almacenamiento, límite de tamaño de carga, nombre y carpeta del modelo, orígenes CORS y la clave para firmar el token.
