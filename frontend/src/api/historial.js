// CU05 (RF-19): historial de estudios del usuario (docs/ejecucion/contrato_api.md, 4.10)
// Usa la sesión y el error del cliente; pedir() no se exporta desde cliente.js
import { ErrorApi, sesion } from './cliente.js';

const MSG_SIN_CONEXION = 'No hay conexión con la API. Revisa que esté en ejecución.';

// 4.10 GET /api/estudios -> [{id, codigo, formato, fecha_carga, estado, id_ultimo_trabajo, dice, iou}]
// del más reciente al más antiguo; [] si el usuario no tiene estudios
export async function listarEstudios() {
  const token = sesion.token();
  const cabeceras = token ? { Authorization: `Bearer ${token}` } : {};
  let respuesta;
  try {
    respuesta = await fetch('/api/estudios', { headers: cabeceras });
  } catch {
    throw new ErrorApi(MSG_SIN_CONEXION, 0);
  }
  const datos = await respuesta.json().catch(() => null);
  if (!respuesta.ok) {
    const detalle = datos && typeof datos.detalle === 'string' ? datos.detalle : '';
    throw new ErrorApi(
      detalle || `No se pudo completar la solicitud (código ${respuesta.status}).`,
      respuesta.status
    );
  }
  return Array.isArray(datos) ? datos : [];
}
