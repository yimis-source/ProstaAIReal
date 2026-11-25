# Pruebas de integración (1708)

Recorren la API real de punta a punta contra **PostgreSQL** con el esquema creado por la migración de
Alembic (no con `create_all`) y una carpeta de almacenamiento temporal. Complementan las pruebas unitarias de
`backend/tests/api/`, que usan SQLite. Los NIfTI se generan en cada prueba con nibabel: nunca se usan datos
reales. Uso académico, no diagnóstico.

## Cómo correrlas

Desde la raíz del repositorio:

```bash
scripts/postgres_local.sh iniciar
createdb -h localhost -p 5433 -U prosta prosta_ai_pruebas   # solo la primera vez
PROSTA_TEST_DATABASE_URL=postgresql+psycopg://prosta@localhost:5433/prosta_ai_pruebas \
  backend/.venv/bin/python -m pytest -q backend/tests/integracion
scripts/postgres_local.sh detener
```

- Sin `PROSTA_TEST_DATABASE_URL` se omiten con el motivo «sin PROSTA_TEST_DATABASE_URL: las pruebas de
  integración necesitan PostgreSQL». Con `-rs` se ve el motivo.
- La misma variable activa la comparación de la migración en PostgreSQL de `backend/tests/db/`, así que con
  ella definida `python -m pytest -q` corre todo.
- Cada prueba hace `alembic downgrade base` y `upgrade head` al empezar y `downgrade base` al terminar: la
  base queda vacía (solo la tabla `alembic_version`, sin filas). Por eso la base **debe** ser aparte: si el
  nombre no contiene «prueba» (por ejemplo, `prosta_ai`), las pruebas fallan sin tocarla.
- Los archivos van a la carpeta temporal de pytest, nunca a `almacenamiento/`.

## Qué cubren

| Prueba | Qué comprueba |
|---|---|
| `test_esquema_creado_por_la_migracion` | La base queda en la revisión `0001` de Alembic y sin filas |
| `test_flujo_cuenta_ingreso_carga_y_detalle` | Verificar alias, crear cuenta, ingresar, 401 con otra clave, hash bcrypt; carga sin referencia (201, `EST-0001`), detalle con `fecha_carga` con zona; filas de estudio y archivo, ruta relativa, SHA-256 y tamaño iguales al archivo en disco, cabecera limpia (RF-05) y el nombre original ausente de la base y del disco |
| `test_carga_con_referencia` | Imagen y referencia: dos filas de archivo, rutas `imagen` y `referencia`, huellas, cabeceras limpias y vóxeles de la referencia intactos |
| `test_rechazo_no_registra_nada[...]` | `.zip`, gzip dañado, `.nii` truncado y referencia dañada: 422 con el mensaje del contrato, ninguna fila nueva, ninguna carpeta ni archivo nuevo, y la carga siguiente conserva la numeración |
| `test_estudio_de_otro_usuario_da_404` | Estudio ajeno e inexistente dan el mismo 404 «Estudio no encontrado.»; sin token, 401 |
| `test_dos_cargas_codigos_distintos_y_correlativos` | Dos cargas seguidas: `EST-0001` y `EST-0002`, ids seguidos y una carpeta por código |
