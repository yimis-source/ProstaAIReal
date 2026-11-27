"""Medición de RR-01 por la API con los casos del conjunto de prueba (tarea 1715).

RR-01 (SRS): el sistema debería procesar un estudio en dos minutos o menos, desde
que inicia el procesamiento hasta que se muestra el resultado, con la
infraestructura disponible.

Contra una API ya levantada (no la arranca), el script:

1. crea una cuenta de prueba con un alias al azar (primer acceso);
2. para cada caso del conjunto de prueba de `entrenamiento/division_task05.json`
   carga la imagen con su máscara de referencia (`POST /api/estudios`), pulsa
   «Procesar» (`POST /api/estudios/{id}/procesar`), consulta el trabajo
   (`GET /api/trabajos/{id}`) hasta `completado` o `fallido` y pide el resultado
   (`GET /api/trabajos/{id}/resultado`);
3. escribe un informe en Markdown con los tiempos y el Dice e IoU de cada caso.

Tiempos por caso (reloj del script, `time.perf_counter`):

- carga: desde que empieza a subir los archivos hasta la respuesta 201;
- cola y procesamiento: desde que pulsa «Procesar» hasta que el resultado está
  disponible (es lo que mide RR-01);
- total de punta a punta: desde que empieza a subir hasta que el resultado está
  disponible.

También copia los tiempos que registra la API (espera en cola, procesamiento y
duración de cada etapa). El script no copia datos: lee las rutas que se le pasan
y en el informe solo pone los ids públicos del conjunto (`prostate_13`, ...).

Uso (desde la raíz del repositorio, con la API ya arriba):
    python scripts/medir_rr01_api.py --url http://localhost:8000 \\
        --imagenes ruta/Task05_Prostate/imagesTr --etiquetas ruta/Task05_Prostate/labelsTr \\
        --salida reports/rendimiento/rr01_api_<fecha>.md

Uso académico y experimental; no es un diagnóstico.
"""
from __future__ import annotations

import argparse
import json
import platform
import secrets
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from importlib import metadata
from pathlib import Path
from typing import Any, Callable

RAIZ = Path(__file__).resolve().parents[1]
DIVISION = RAIZ / "entrenamiento" / "division_task05.json"
LIMITE_S = 120.0  # RR-01: dos minutos por estudio
TERMINALES = ("completado", "fallido")
AVISO = ("Uso académico y experimental. Los resultados de Prosta-AI no son un diagnóstico, no "
         "sustituyen la valoración de un profesional de la salud y la aplicación no es un "
         "dispositivo médico.")


class ErrorMedicion(RuntimeError):
    """La API respondió algo que no permite seguir con el caso."""


@dataclass
class ResultadoCaso:
    caso: str
    estado: str = "sin medir"
    carga_s: float | None = None
    procesar_s: float | None = None  # «Procesar» → resultado disponible (RR-01)
    total_s: float | None = None  # inicio de la carga → resultado disponible
    cola_api_s: float | None = None  # fecha_creacion → fecha_inicio del trabajo
    proceso_api_s: float | None = None  # fecha_inicio → fecha_fin del trabajo
    etapas: dict[str, float | None] = field(default_factory=dict)
    dice: float | None = None
    iou: float | None = None
    modelo: dict | None = None
    consultas: int = 0
    error: str | None = None


# --- Casos y archivos ---

def casos_de_prueba(division: Path, conjunto: str = "prueba") -> list[str]:
    datos = json.loads(Path(division).read_text(encoding="utf-8"))
    casos = datos["conjuntos"][conjunto]
    if not casos:
        raise ValueError(f"El conjunto «{conjunto}» de {division} está vacío.")
    return list(casos)


def rutas_caso(caso: str, imagenes: Path, etiquetas: Path) -> tuple[Path, Path]:
    imagen = Path(imagenes) / f"{caso}.nii.gz"
    mascara = Path(etiquetas) / f"{caso}.nii.gz"
    for ruta in (imagen, mascara):
        if not ruta.is_file():
            raise FileNotFoundError(f"No existe {ruta}")
    return imagen, mascara


# --- Llamadas a la API ---

def _json(r, esperado: int, que: str) -> dict:
    if r.status_code != esperado:
        try:
            detalle = r.json().get("detalle", r.text)
        except ValueError:
            detalle = r.text
        raise ErrorMedicion(f"{que}: HTTP {r.status_code}: {detalle}")
    return r.json()


def crear_cuenta(cliente) -> dict[str, str]:
    """Primer acceso con un alias y una contraseña al azar; devuelve la cabecera con el token."""
    alias = f"rr01_{secrets.token_hex(6)}"
    contrasena = secrets.token_urlsafe(12)
    cuerpo = {"alias": alias, "contrasena": contrasena, "confirmacion": contrasena}
    token = _json(cliente.post("/api/acceso", json=cuerpo), 200, "Acceso")["token"]
    return {"Authorization": f"Bearer {token}"}


def _segundos(inicio: str | None, fin: str | None) -> float | None:
    if not inicio or not fin:
        return None
    return (datetime.fromisoformat(fin) - datetime.fromisoformat(inicio)).total_seconds()


def medir_caso(cliente, cab: dict, caso: str, imagen: Path, mascara: Path, *,
               intervalo_s: float = 0.5, espera_max_s: float = 600.0,
               reloj: Callable[[], float] = time.perf_counter,
               dormir: Callable[[float], None] = time.sleep) -> ResultadoCaso:
    res = ResultadoCaso(caso)
    try:
        t0 = reloj()
        with open(imagen, "rb") as fi, open(mascara, "rb") as fm:
            # Nombres genéricos: el nombre original no hace falta y la API no lo guarda
            archivos = {"archivos": ("imagen.nii.gz", fi, "application/gzip"),
                        "referencia": ("referencia.nii.gz", fm, "application/gzip")}
            estudio = _json(cliente.post("/api/estudios", files=archivos, headers=cab), 201, "Carga")
        t1 = reloj()
        res.carga_s = t1 - t0

        trabajo = _json(cliente.post(f"/api/estudios/{estudio['id']}/procesar", headers=cab),
                        201, "Procesar")
        id_trabajo = trabajo["id"]
        while trabajo["estado"] not in TERMINALES:
            if reloj() - t1 > espera_max_s:
                raise ErrorMedicion(f"El trabajo no terminó en {espera_max_s:.0f} s "
                                    f"(último estado: {trabajo['estado']}).")
            dormir(intervalo_s)
            trabajo = _json(cliente.get(f"/api/trabajos/{id_trabajo}", headers=cab), 200, "Estado")
            res.consultas += 1

        res.estado = trabajo["estado"]
        res.cola_api_s = _segundos(trabajo.get("fecha_creacion"), trabajo.get("fecha_inicio"))
        res.proceso_api_s = _segundos(trabajo.get("fecha_inicio"), trabajo.get("fecha_fin"))
        res.etapas = {e["nombre"]: e.get("duracion_s") for e in trabajo.get("etapas", [])}
        if res.estado == "fallido":
            res.error = (f"Trabajo fallido en «{trabajo.get('etapa_fallida')}»: "
                         f"{trabajo.get('mensaje_error')}")
            return res

        resultado = _json(cliente.get(f"/api/trabajos/{id_trabajo}/resultado", headers=cab),
                          200, "Resultado")
        t2 = reloj()
        res.procesar_s = t2 - t1
        res.total_s = t2 - t0
        res.dice = resultado.get("dice")
        res.iou = resultado.get("iou")
        res.modelo = resultado.get("modelo")
    except (ErrorMedicion, OSError) as e:
        res.estado = "error" if res.estado == "sin medir" else res.estado
        res.error = str(e)
    return res


def medir(cliente, casos: list[str], imagenes: Path, etiquetas: Path, **opciones) -> dict:
    salud = _json(cliente.get("/api/salud"), 200, "Salud")
    cab = crear_cuenta(cliente)
    filas = []
    for caso in casos:
        imagen, mascara = rutas_caso(caso, imagenes, etiquetas)
        fila = medir_caso(cliente, cab, caso, imagen, mascara, **opciones)
        filas.append(fila)
        print(f"{caso}: {fila.estado}, total {_s(fila.total_s)} s, Dice {_m(fila.dice)}", flush=True)
    modelo = next((f.modelo for f in filas if f.modelo), None)
    return {"filas": filas, "version_api": salud.get("version"), "modelo": modelo}


# --- Informe ---

def _s(v: float | None) -> str:
    return "—" if v is None else f"{v:.1f}"


def _m(v: float | None) -> str:
    return "—" if v is None else f"{v:.3f}"


def resumen(filas: list[ResultadoCaso]) -> dict:
    ok = [f for f in filas if f.estado == "completado" and f.total_s is not None]
    r: dict[str, Any] = {"medidos": len(ok), "casos": len(filas)}
    if not ok:
        r["cumple"] = False
        return r
    for clave in ("carga_s", "procesar_s", "total_s"):
        valores = [getattr(f, clave) for f in ok]
        r[clave] = {"media": statistics.mean(valores), "max": max(valores)}
    dices = [f.dice for f in ok if f.dice is not None]
    r["dice_media"] = statistics.mean(dices) if dices else None
    ious = [f.iou for f in ok if f.iou is not None]
    r["iou_media"] = statistics.mean(ious) if ious else None
    caliente = [f.procesar_s for f in ok[1:]] if ok[0] is filas[0] else [f.procesar_s for f in ok]
    r["procesar_caliente_media"] = statistics.mean(caliente) if caliente else None
    # RR-01 se cumple si todos los casos terminan y ninguno pasa de 120 s
    r["cumple"] = len(ok) == len(filas) and r["procesar_s"]["max"] <= LIMITE_S
    r["cumple_total"] = len(ok) == len(filas) and r["total_s"]["max"] <= LIMITE_S
    return r


def informe(res: dict, condiciones: dict, fecha: str) -> str:
    filas: list[ResultadoCaso] = res["filas"]
    rs = resumen(filas)
    modelo = res.get("modelo") or {}
    nombres_etapas: list[str] = []
    for f in filas:
        for nombre in f.etapas:
            if nombre not in nombres_etapas:
                nombres_etapas.append(nombre)

    l = [f"# RR-01 por la API con los casos de prueba (tarea 1715) — {fecha}", "",
         AVISO, "",
         "Mide el tiempo de procesamiento de un estudio por la API web, con los casos del conjunto "
         "de prueba de MSD Task05, para comprobar RR-01 del SRS: procesar un estudio en dos minutos "
         "o menos, desde que inicia el procesamiento hasta que se muestra el resultado.", "",
         "## Condiciones", "",
         f"- Casos: los {len(filas)} del conjunto de prueba de `entrenamiento/division_task05.json` "
         f"({', '.join(f'`{f.caso}`' for f in filas)}), cada uno con su máscara de referencia.",
         f"- API: versión {res.get('version_api') or '—'} en `{condiciones['url']}`, con PostgreSQL "
         "local y la tarea en segundo plano de la propia API (un trabajo a la vez).",
         f"- Modelo: `{modelo.get('nombre', '—')}` {modelo.get('version', '—')}.",
         f"- Dispositivo: {condiciones['dispositivo']}. CPU: {condiciones['cpu']}; "
         f"RAM {condiciones['ram_gb']:.1f} GB; {condiciones['so']}.",
         f"- Software: {condiciones['software']}.",
         f"- Versión del código medida: `{condiciones['commit']}`.",
         f"- Consulta del estado cada {condiciones['intervalo_s']:g} s (la interfaz consulta cada 2 s).",
         "- El primer caso incluye la carga de los pesos (arranque en frío): la API construye el "
         "pipeline al primer trabajo.",
         "- Cuenta de prueba creada por el script con un alias al azar; el informe no lo guarda.", "",
         "## Qué se mide", "",
         "- **Carga:** desde que empieza a subir la imagen y la referencia hasta la respuesta 201.",
         "- **Procesamiento (RR-01):** desde que se pulsa «Procesar» hasta que el resultado está "
         "disponible (`GET /api/trabajos/{id}/resultado` responde 200). Incluye la espera en cola, "
         "las cinco etapas, guardar el resultado y el retardo de la consulta periódica.",
         "- **Total:** de punta a punta, desde que empieza la carga hasta que el resultado está "
         "disponible.",
         "- **Cola (API)** y **Proceso (API):** tiempos que registra la API en el trabajo "
         "(`fecha_creacion` → `fecha_inicio` y `fecha_inicio` → `fecha_fin`).", "",
         "## Resultados por caso (segundos)", "",
         "| Caso | Estado | Carga | Procesamiento (RR-01) | Total | Cola (API) | Proceso (API) | Dice | IoU |",
         "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for i, f in enumerate(filas):
        nombre = f"`{f.caso}`" + (" (en frío)" if i == 0 else "")
        l.append(f"| {nombre} | {f.estado} | {_s(f.carga_s)} | **{_s(f.procesar_s)}** | {_s(f.total_s)} "
                 f"| {_s(f.cola_api_s)} | {_s(f.proceso_api_s)} | {_m(f.dice)} | {_m(f.iou)} |")
    if "carga_s" in rs:
        l.append(f"| **Media** | | {_s(rs['carga_s']['media'])} | **{_s(rs['procesar_s']['media'])}** "
                 f"| {_s(rs['total_s']['media'])} | | | {_m(rs['dice_media'])} | {_m(rs['iou_media'])} |")
        l.append(f"| **Máximo** | | {_s(rs['carga_s']['max'])} | **{_s(rs['procesar_s']['max'])}** "
                 f"| {_s(rs['total_s']['max'])} | | | | |")

    if nombres_etapas:
        l += ["", "### Duración de cada etapa según la API (segundos)", "",
              "| Caso | " + " | ".join(nombres_etapas) + " |",
              "|---|" + "---:|" * len(nombres_etapas)]
        for f in filas:
            l.append(f"| `{f.caso}` | " + " | ".join(_s(f.etapas.get(n)) for n in nombres_etapas) + " |")

    errores = [f for f in filas if f.error]
    if errores:
        l += ["", "### Errores", ""]
        l += [f"- `{f.caso}`: {f.error}" for f in errores]

    l += ["", "## Resumen", ""]
    if "carga_s" not in rs:
        l.append("- Ningún caso terminó: **RR-01 no se puede comprobar** con esta medición.")
    else:
        l.append(f"- Casos completados: {rs['medidos']} de {rs['casos']}.")
        l.append(f"- Procesamiento (RR-01): media {_s(rs['procesar_s']['media'])} s, máximo "
                 f"{_s(rs['procesar_s']['max'])} s.")
        if rs.get("procesar_caliente_media") is not None:
            l.append(f"- Sin el primer caso (con el modelo ya cargado): media "
                     f"{_s(rs['procesar_caliente_media'])} s.")
        l.append(f"- Total de punta a punta: media {_s(rs['total_s']['media'])} s, máximo "
                 f"{_s(rs['total_s']['max'])} s.")
        if rs["cumple"]:
            margen = LIMITE_S - rs["procesar_s"]["max"]
            l.append(f"- RR-01 (≤ 120 s por estudio): **se cumple** en los {rs['casos']} casos, con "
                     f"margen de {margen:.0f} s sobre el caso más lento.")
        else:
            l.append("- RR-01 (≤ 120 s por estudio): **no se cumple** en esta medición "
                     "(algún caso pasó de 120 s o no terminó).")
        if rs["cumple_total"]:
            l.append("- Aun contando la carga, ningún caso pasa de 120 s de punta a punta.")
    l += ["", "## GPU", "",
          f"Medición en {condiciones['dispositivo']}, en un solo equipo. **No se compara con GPU:** el "
          "informe de GPU de la tarea 1408 (`rendimiento_1408_gpu_2026-11-13.md`) mide solo la "
          "inferencia en otro equipo (Colab), sin la API, la base de datos ni la carga.", "",
          "## Limitaciones", "",
          "- Cinco casos y un solo equipo; los tiempos cambian con el tamaño del volumen y el hardware.",
          "- La API y el script corren en el mismo equipo: la carga no incluye la red entre "
          "navegador y servidor.",
          "- El tiempo de procesamiento tiene un error de hasta un intervalo de consulta por caso, "
          "más la espera de la tarea en segundo plano para tomar el trabajo "
          "(`PROSTA_WORKER_INTERVALO_S`).",
          "- No incluye el tiempo que tarda el navegador en dibujar los cortes.", ""]
    return "\n".join(l)


# --- Condiciones del equipo ---

def cpu_nombre() -> str:
    try:
        for linea in Path("/proc/cpuinfo").read_text().splitlines():
            if linea.startswith("model name"):
                return linea.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or platform.machine()


def ram_total_gb() -> float:
    try:
        for linea in Path("/proc/meminfo").read_text().splitlines():
            if linea.startswith("MemTotal:"):
                return int(linea.split()[1]) / 1024**2
    except OSError:
        pass
    return float("nan")


def versiones() -> str:
    partes = [f"Python {platform.python_version()}"]
    for paquete in ("torch", "monai", "fastapi", "uvicorn", "sqlalchemy", "psycopg"):
        try:
            partes.append(f"{paquete} {metadata.version(paquete)}")
        except metadata.PackageNotFoundError:
            pass
    return ", ".join(partes) + " (entorno del script; en esta medición, el mismo de la API)"


def commit_actual() -> str:
    try:
        sale = subprocess.run(["git", "-C", str(RAIZ), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, check=True)
        return sale.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "desconocido"


def condiciones_equipo(url: str, dispositivo: str, intervalo_s: float, commit: str | None) -> dict:
    return {"url": url, "dispositivo": dispositivo, "cpu": cpu_nombre(), "ram_gb": ram_total_gb(),
            "so": f"{platform.system()} {platform.release()}", "software": versiones(),
            "commit": commit or commit_actual(), "intervalo_s": intervalo_s}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", required=True, help="URL base de la API, p. ej. http://localhost:8000")
    ap.add_argument("--imagenes", type=Path, required=True, help="Carpeta imagesTr de MSD Task05")
    ap.add_argument("--etiquetas", type=Path, required=True, help="Carpeta labelsTr de MSD Task05")
    ap.add_argument("--division", type=Path, default=DIVISION)
    ap.add_argument("--conjunto", default="prueba")
    ap.add_argument("--salida", type=Path,
                    default=RAIZ / "reports" / "rendimiento" / f"rr01_api_{date.today().isoformat()}.md")
    ap.add_argument("--dispositivo", default="cpu", help="Solo para el informe: dónde corre la API")
    ap.add_argument("--intervalo", type=float, default=0.5, help="Segundos entre consultas del estado")
    ap.add_argument("--espera-max", type=float, default=600.0, help="Segundos máximos por trabajo")
    ap.add_argument("--commit", default=None, help="Versión del código medida (por defecto, HEAD)")
    ap.add_argument("--fecha", default=date.today().isoformat(), help="Fecha del informe (AAAA-MM-DD)")
    args = ap.parse_args(argv)

    import httpx

    casos = casos_de_prueba(args.division, args.conjunto)
    for caso in casos:  # falla antes de crear nada si falta un archivo
        rutas_caso(caso, args.imagenes, args.etiquetas)
    with httpx.Client(base_url=args.url.rstrip("/"), timeout=120.0) as cliente:
        res = medir(cliente, casos, args.imagenes, args.etiquetas,
                    intervalo_s=args.intervalo, espera_max_s=args.espera_max)
    cond = condiciones_equipo(args.url, args.dispositivo, args.intervalo, args.commit)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(informe(res, cond, args.fecha), encoding="utf-8")
    print(f"Informe: {args.salida}")
    return 0 if resumen(res["filas"])["cumple"] else 1


if __name__ == "__main__":
    sys.exit(main())
