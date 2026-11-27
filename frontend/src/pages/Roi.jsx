import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { obtenerEstudio, obtenerResultado } from '../api/cliente.js';
import ErrorApi from '../components/ErrorApi.jsx';
import Mensaje from '../components/Mensaje.jsx';
import Pasos from '../components/Pasos.jsx';
import Visor from '../components/Visor.jsx';

// El último trabajo `completado` del estudio (contrato 4.5); null si no hay ninguno
function ultimoCompletado(estudio) {
  const completados = (estudio.trabajos || []).filter((t) => t.estado === 'completado');
  if (completados.length === 0) return null;
  return completados.reduce((a, b) => (b.id > a.id ? b : a));
}

// CU04 (RF-13 a RF-17): región de interés superpuesta sobre los cortes del estudio
export default function Roi() {
  const { id } = useParams();
  const [resultado, setResultado] = useState(null);
  const [sinResultado, setSinResultado] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    let activo = true;
    setResultado(null);
    setSinResultado(false);
    setError(null);
    obtenerEstudio(id)
      .then((estudio) => {
        const trabajo = ultimoCompletado(estudio);
        if (!trabajo) {
          if (activo) setSinResultado(true);
          return null;
        }
        return obtenerResultado(trabajo.id).then((r) => activo && setResultado(r));
      })
      .catch((e) => activo && setError(e));
    return () => {
      activo = false;
    };
  }, [id]);

  return (
    <section>
      <h1>Región de interés (ROI)</h1>
      <p className="subtitulo">{resultado ? `Estudio ${resultado.codigo}` : 'Resultado del procesamiento'}</p>
      <Pasos actual={3} />
      <ErrorApi error={error} />
      {!resultado && !sinResultado && !error && <p className="nota" role="status">Consultando el resultado…</p>}
      {sinResultado && (
        <Mensaje tipo="info">
          Este estudio todavía no tiene un procesamiento completado.{' '}
          <Link to={`/estudios/${id}/estado`}>Ver el estado del estudio</Link>
        </Mensaje>
      )}
      {resultado && (
        <div className="roi">
          <Visor key={resultado.id_trabajo} idTrabajo={resultado.id_trabajo} cortes={resultado.cortes} />
        </div>
      )}
    </section>
  );
}
