import { ESTADOS_FINALES } from '../constantes.js';

export const INTERVALO_MS = 2000; // RF-07: el estado se consulta cada 2 s

// Consulta un trabajo cada `intervalo` ms hasta que quede `completado` o `fallido`.
// Espera a que termine cada respuesta antes de programar la siguiente (sin consultas solapadas).
// Devuelve la función que detiene la consulta (al salir de la pantalla).
export function consultarTrabajo(idTrabajo, { obtener, alCambiar, alError, intervalo = INTERVALO_MS }) {
  let activa = true;
  let temporizador = null;

  async function consultar() {
    try {
      const trabajo = await obtener(idTrabajo);
      if (activa) alCambiar(trabajo);
      if (ESTADOS_FINALES.includes(trabajo.estado)) return;
    } catch (e) {
      if (activa) alError(e);
    }
    temporizador = setTimeout(consultar, intervalo);
  }

  consultar();
  return () => {
    activa = false;
    clearTimeout(temporizador);
  };
}
