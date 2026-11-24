#!/usr/bin/env bash
# Clúster PostgreSQL local para desarrollo, sin permisos de administrador.
# Datos en .pgdata/ (ignorado por git). Solo TCP en localhost: sin socket Unix,
# porque rutas largas superan el límite de 107 bytes.
# Uso: scripts/postgres_local.sh iniciar|detener|estado
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
DATOS="$RAIZ/.pgdata"
PUERTO="${PROSTA_PG_PUERTO:-5433}"
USUARIO=prosta
BASE=prosta_ai

case "${1:-}" in
  iniciar)
    if [ ! -f "$DATOS/PG_VERSION" ]; then
      initdb -D "$DATOS" -U "$USUARIO" --auth=trust -E UTF8 --locale=C >/dev/null
    fi
    if ! pg_ctl -D "$DATOS" status >/dev/null 2>&1; then
      pg_ctl -D "$DATOS" -l "$DATOS/servidor.log" -w \
        -o "-p $PUERTO -c listen_addresses=localhost -c unix_socket_directories=''" start >/dev/null
    fi
    if ! psql -h localhost -p "$PUERTO" -U "$USUARIO" -d postgres -Atc \
        "SELECT 1 FROM pg_database WHERE datname='$BASE'" | grep -q 1; then
      createdb -h localhost -p "$PUERTO" -U "$USUARIO" "$BASE"
    fi
    echo "PostgreSQL activo en localhost:$PUERTO (base $BASE, usuario $USUARIO)"
    ;;
  detener)
    pg_ctl -D "$DATOS" -w stop
    ;;
  estado)
    pg_ctl -D "$DATOS" status
    ;;
  *)
    echo "Uso: $0 iniciar|detener|estado" >&2
    exit 1
    ;;
esac
