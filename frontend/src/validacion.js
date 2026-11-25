// Validación en el navegador de la carga (contrato 4.4). La API vuelve a validar todo:
// esto solo evita subir archivos que de todas formas se rechazarían. Mensajes iguales a los del contrato.
export const MB = 1024 * 1024;
export const MAX_ARCHIVO = 50 * MB;
export const MAX_ESTUDIO = 150 * MB;

export const MENSAJES = {
  sinImagen: 'Seleccione al menos un archivo de imagen.',
  formato: 'Formato no admitido. En esta versión solo se aceptan archivos NIfTI (.nii o .nii.gz).',
  archivo: 'El archivo supera el máximo de 50 MB.',
  estudio: 'El estudio supera el máximo de 150 MB.',
  vacio: 'El archivo está dañado o no es un NIfTI válido.',
};

export const esNifti = (nombre) => /\.nii(\.gz)?$/i.test(nombre);

// Devuelve el mensaje del primer problema o '' si la selección es válida
export function validarCarga(imagen, referencia) {
  if (!imagen) return MENSAJES.sinImagen;
  for (const f of [imagen, referencia].filter(Boolean)) {
    if (!esNifti(f.name)) return MENSAJES.formato;
    if (f.size === 0) return MENSAJES.vacio;
    if (f.size > MAX_ARCHIVO) return MENSAJES.archivo;
  }
  const total = imagen.size + (referencia ? referencia.size : 0);
  if (total > MAX_ESTUDIO) return MENSAJES.estudio;
  return '';
}

export function formatoTamano(bytes) {
  if (bytes < MB) return `${Math.max(1, Math.round(bytes / 1024))} KB`;
  return `${(bytes / MB).toFixed(1).replace('.', ',')} MB`;
}
