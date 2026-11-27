// Cliente HTTP de la API de Prosta-AI (docs/ejecucion/contrato_api.md, secciones 1, 2 y 4)
// En desarrollo, Vite envía /api a http://localhost:8000 (vite.config.js)
const BASE = '/api';
const CLAVE_TOKEN = 'prosta_token';
const CLAVE_ALIAS = 'prosta_alias';

// Token y alias en la memoria de la sesión del navegador (contrato 4.3)
export const sesion = {
  token: () => sessionStorage.getItem(CLAVE_TOKEN),
  alias: () => sessionStorage.getItem(CLAVE_ALIAS),
  guardar(token, alias) {
    sessionStorage.setItem(CLAVE_TOKEN, token);
    sessionStorage.setItem(CLAVE_ALIAS, alias);
  },
  borrar() {
    sessionStorage.removeItem(CLAVE_TOKEN);
    sessionStorage.removeItem(CLAVE_ALIAS);
  },
};

// Lo que se hace ante un 401 con sesión abierta (lo registra AuthContext)
let alExpirar = () => {};
export const registrarAlExpirar = (fn) => {
  alExpirar = fn;
};

export class ErrorApi extends Error {
  constructor(mensaje, estado, campos = []) {
    super(mensaje);
    this.estado = estado;
    this.campos = campos;
  }
}

// El contrato fija {"detalle": "texto"}; un 422 de validación agrega "campos": [...]
function errorDe(datos, estado) {
  const detalle = datos && typeof datos.detalle === 'string' ? datos.detalle : '';
  const campos = datos && Array.isArray(datos.campos) ? datos.campos : [];
  const mensaje = detalle || `No se pudo completar la solicitud (código ${estado}).`;
  return new ErrorApi(mensaje, estado, campos);
}

// Hace la petición con el token Bearer de la sesión. Se exporta para que los demás módulos de
// api/ (historial.js) compartan el manejo de errores y el cierre de sesión ante un 401.
// Con `binario: true` devuelve el cuerpo como Blob (los PNG de los cortes, contrato 4.9).
export async function pedir(ruta, { metodo = 'GET', json, formData, conToken = true, binario = false } = {}) {
  const cabeceras = {};
  const token = sesion.token();
  if (conToken && token) cabeceras.Authorization = `Bearer ${token}`;
  let cuerpo;
  if (json !== undefined) {
    cabeceras['Content-Type'] = 'application/json';
    cuerpo = JSON.stringify(json);
  } else if (formData) {
    cuerpo = formData; // el navegador pone el Content-Type con el límite del multipart
  }

  let respuesta;
  try {
    respuesta = await fetch(BASE + ruta, { method: metodo, headers: cabeceras, body: cuerpo });
  } catch {
    throw new ErrorApi('No hay conexión con la API. Revisa que esté en ejecución.', 0);
  }

  if (!respuesta.ok) {
    const datos = await respuesta.json().catch(() => null);
    // Con sesión abierta, un 401 es token vencido o no válido; en /acceso es contraseña incorrecta
    if (respuesta.status === 401 && conToken && token) alExpirar();
    throw errorDe(datos, respuesta.status);
  }
  if (binario) return respuesta.blob();
  return respuesta.json().catch(() => null);
}

// 4.1 GET /api/salud -> {"estado": "ok", "version": "0.6.0"}
export const consultarSalud = () => pedir('/salud', { conToken: false });

// 4.2 POST /api/acceso/verificar -> {"existe": bool}
export const verificarAlias = (alias) =>
  pedir('/acceso/verificar', { metodo: 'POST', json: { alias }, conToken: false });

// 4.3 POST /api/acceso -> {"token", "alias", "primer_acceso"}; confirmacion solo en el primer acceso
export const acceder = (alias, contrasena, confirmacion) =>
  pedir('/acceso', {
    metodo: 'POST',
    json: confirmacion === undefined ? { alias, contrasena } : { alias, contrasena, confirmacion },
    conToken: false,
  });

// 4.4 POST /api/estudios (multipart): imagen obligatoria y máscara de referencia opcional
export function cargarEstudio(imagen, referencia) {
  const datos = new FormData();
  datos.append('archivos', imagen); // nombre del campo según el contrato 4.4
  if (referencia) datos.append('referencia', referencia);
  return pedir('/estudios', { metodo: 'POST', formData: datos });
}

// 4.5 GET /api/estudios/{id_estudio}
export const obtenerEstudio = (id) => pedir(`/estudios/${encodeURIComponent(id)}`);

// 4.6 POST /api/estudios/{id_estudio}/procesar (botón «Procesar», D-006) -> 201 trabajo `pendiente`
// con las 5 etapas en `pendiente`; 409 si el estudio no es compatible o ya tiene un trabajo activo
export const procesarEstudio = (idEstudio) =>
  pedir(`/estudios/${encodeURIComponent(idEstudio)}/procesar`, { metodo: 'POST' });

// 4.7 GET /api/trabajos/{id_trabajo} -> estado del trabajo y de cada etapa (se consulta cada 2 s)
export const obtenerTrabajo = (idTrabajo) => pedir(`/trabajos/${encodeURIComponent(idTrabajo)}`);

// 4.8 GET /api/trabajos/{id_trabajo}/resultado -> {id_trabajo, codigo, dice, iou, tiempo_total_s,
// modelo: {nombre, version}, cortes, forma, aviso}; 404 si el trabajo no está `completado`
export const obtenerResultado = (idTrabajo) =>
  pedir(`/trabajos/${encodeURIComponent(idTrabajo)}/resultado`);

// 4.9 GET /api/trabajos/{id_trabajo}/corte/{indice}?capa=imagen|mascara -> PNG (Blob)
// `indice` va de 0 a cortes - 1. La ruta pide token y un <img src> no manda cabeceras, así que el
// PNG se pide aquí y quien lo muestra crea la URL con URL.createObjectURL y la libera después.
export const obtenerCorte = (idTrabajo, indice, capa = 'imagen') =>
  pedir(
    `/trabajos/${encodeURIComponent(idTrabajo)}/corte/${encodeURIComponent(indice)}?capa=${encodeURIComponent(capa)}`,
    { binario: true }
  );
