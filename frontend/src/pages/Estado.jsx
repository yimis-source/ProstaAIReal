import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { obtenerEstudio, obtenerTrabajo, procesarEstudio } from '../api/cliente.js';
import { consultarTrabajo } from '../api/consultaPeriodica.js';
import { ESTADOS_FINALES, capitalizar } from '../constantes.js';
import ErrorApi from '../components/ErrorApi.jsx';
import Etapas from '../components/Etapas.jsx';
import EtiquetaEstado from '../components/EtiquetaEstado.jsx';
import Mensaje from '../components/Mensaje.jsx';
import Pasos from '../components/Pasos.jsx';

// El último trabajo del estudio (contrato 4.5: `trabajos` e `id_ultimo_trabajo`)
function ultimoTrabajo(estudio) {
  const trabajos = estudio.trabajos || [];
  return trabajos.find((t) => t.id === estudio.id_ultimo_trabajo) || trabajos[trabajos.length - 1] || null;
}

// CU03: estado del estudio, botón «Procesar» (D-006) y progreso de las 5 etapas
export default function Estado() {
  const { id } = useParams();
  const [estudio, setEstudio] = useState(null);
  const [trabajo, setTrabajo] = useState(null);
  const [error, setError] = useState(null);
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    let activo = true;
    setEstudio(null);
    setTrabajo(null);
    setError(null);
    obtenerEstudio(id)
      .then((d) => {
        if (!activo) return;
        setEstudio(d);
        setTrabajo(ultimoTrabajo(d));
      })
      .catch((e) => activo && setError(e));
    return () => {
      activo = false;
    };
  }, [id]);

  // Mientras el trabajo esté `pendiente` o `en proceso`, se consulta GET /api/trabajos/{id} cada 2 s
  const idActivo = trabajo && !ESTADOS_FINALES.includes(trabajo.estado) ? trabajo.id : null;
  useEffect(() => {
    if (idActivo === null) return undefined;
    return consultarTrabajo(idActivo, {
      obtener: obtenerTrabajo,
      alCambiar: (t) => {
        setError(null);
        setTrabajo(t);
      },
      alError: setError,
    });
  }, [idActivo]);

  async function procesar() {
    setEnviando(true);
    setError(null);
    try {
      setTrabajo(await procesarEstudio(id));
    } catch (e) {
      // 409: se muestra el mensaje de la API tal cual y se vuelve a leer el estudio por si ya
      // tiene un trabajo en curso (por ejemplo, abierto en otra pestaña) para seguir su progreso
      setError(e);
      if (e.estado === 409) {
        obtenerEstudio(id)
          .then((d) => {
            setEstudio(d);
            setTrabajo(ultimoTrabajo(d));
          })
          .catch(() => {});
      }
    } finally {
      setEnviando(false);
    }
  }

  const estado = trabajo ? trabajo.estado : estudio?.estado;
  const puedeProcesar =
    estudio && (trabajo ? trabajo.estado === 'fallido' : estudio.estado === 'listo para procesar');

  return (
    <section>
      <h1>Estado del procesamiento</h1>
      <p className="subtitulo">El procesamiento corre en segundo plano; esta pantalla se actualiza sola.</p>
      <Pasos actual={2} />
      <ErrorApi error={error} />
      {!estudio && !error && <p className="nota" role="status">Consultando el estudio…</p>}
      {estudio && (
        <div className="tarjeta detalle">
          <p className="nota">CÓDIGO ANÓNIMO</p>
          <p className="codigo">{estudio.codigo}</p>
          <dl className="resumen">
            <dt>Formato</dt><dd>{estudio.formato}</dd>
            <dt>Estado</dt><dd><EtiquetaEstado estado={estado} /></dd>
          </dl>
          {estudio.estado === 'no compatible' && (
            <Mensaje tipo="info">El estudio no es compatible y no se puede procesar.</Mensaje>
          )}
          {!trabajo && estudio.estado === 'listo para procesar' && (
            <Mensaje tipo="ok">El estudio se cargó y está listo para procesar.</Mensaje>
          )}
          {trabajo && !ESTADOS_FINALES.includes(trabajo.estado) && (
            <p className="nota" role="status">
              {trabajo.estado === 'pendiente' ? 'En cola: el procesamiento empieza en breve.' : 'Procesando…'} La
              pantalla se actualiza cada 2 segundos.
            </p>
          )}
          {trabajo?.estado === 'fallido' && (
            <Mensaje>
              {trabajo.etapa_fallida && <strong>Falló la etapa «{capitalizar(trabajo.etapa_fallida)}». </strong>}
              {trabajo.mensaje_error || 'El procesamiento no se pudo completar.'} Puedes revisar el archivo y
              procesar de nuevo.
            </Mensaje>
          )}
          {trabajo?.estado === 'completado' && (
            <Mensaje tipo="ok">El procesamiento terminó. La región de interés está lista para revisar.</Mensaje>
          )}
          {trabajo && <Etapas etapas={trabajo.etapas} />}
          <div className="acciones">
            <button type="button" className="btn btn-primario" onClick={procesar} disabled={!puedeProcesar || enviando}>
              {trabajo?.estado === 'fallido' ? 'Procesar de nuevo' : 'Procesar'}
            </button>
            {trabajo?.estado === 'completado' && (
              <Link className="btn" to={`/estudios/${id}/roi`}>Ver resultado</Link>
            )}
          </div>
        </div>
      )}
    </section>
  );
}
