// Cliente HTTP mínimo para la API de Prosta-AI (proxy de Vite: /api -> http://localhost:8000)
const BASE = '/api';

export class ErrorApi extends Error {
  constructor(mensaje, estado) {
    super(mensaje);
    this.estado = estado;
  }
}

// La API devuelve los errores como {"detalle": ...} (texto o lista)
function mensajeDe(datos, estado) {
  const d = datos && datos.detalle;
  if (typeof d === 'string') return d;
  if (Array.isArray(d) && d.length) return d.map((x) => (x && x.msg) || String(x)).join('. ');
  return `No se pudo completar la solicitud (código ${estado}).`;
}

export async function pedir(ruta, opciones = {}) {
  let respuesta;
  try {
    respuesta = await fetch(BASE + ruta, opciones);
  } catch {
    throw new ErrorApi('No hay conexión con la API.', 0);
  }
  const datos = await respuesta.json().catch(() => null);
  if (!respuesta.ok) throw new ErrorApi(mensajeDe(datos, respuesta.status), respuesta.status);
  return datos;
}

// GET /api/salud -> {"estado": "ok", "version": "0.6.0"}
export const consultarSalud = () => pedir('/salud');
