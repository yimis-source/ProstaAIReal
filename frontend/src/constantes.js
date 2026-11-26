// Texto fijo del aviso: igual a AVISO_EXPERIMENTAL de backend/prosta_ai/constantes.py
export const AVISO_EXPERIMENTAL =
  'Resultado experimental con fines académicos. No es un diagnóstico ni sustituye la valoración de un profesional de la salud.';

// Etapas del trabajo en su orden fijo (contrato, sección 3)
export const ETAPAS = ['control de calidad', 'preparación', 'segmentación', 'ROI', 'evaluación'];

// Estados con los que el trabajo ya no cambia
export const ESTADOS_FINALES = ['completado', 'fallido'];

export const capitalizar = (texto = '') => (texto ? texto.charAt(0).toUpperCase() + texto.slice(1) : '');

// Duración en segundos -> «1,4 s» o «1 min 05 s»; sin dato, «—»
export function formatearSegundos(s) {
  if (s === null || s === undefined) return '—';
  if (s < 60) return `${s.toFixed(1).replace('.', ',')} s`;
  const min = Math.floor(s / 60);
  const seg = Math.round(s % 60);
  return `${min} min ${String(seg).padStart(2, '0')} s`;
}
