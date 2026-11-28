// CU05 (RF-19): historial de estudios del usuario (docs/ejecucion/contrato_api.md, 4.10)
// Usa pedir() de cliente.js: mismo token, mismos errores y, ante un 401, se cierra la sesión
import { pedir } from './cliente.js';

// 4.10 GET /api/estudios -> [{id, codigo, formato, fecha_carga, estado, id_ultimo_trabajo, dice, iou}]
// del más reciente al más antiguo; [] si el usuario no tiene estudios
export async function listarEstudios() {
  const datos = await pedir('/estudios');
  return Array.isArray(datos) ? datos : [];
}
