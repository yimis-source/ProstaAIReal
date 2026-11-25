import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { obtenerEstudio } from '../api/cliente.js';
import ErrorApi from '../components/ErrorApi.jsx';
import Mensaje from '../components/Mensaje.jsx';
import Pasos from '../components/Pasos.jsx';

// Detalle del estudio tras la carga (GET /api/estudios/{id}). Las etapas del procesamiento (CU03) llegan en 1710.
export default function Estado() {
  const { id } = useParams();
  const [estudio, setEstudio] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let activo = true;
    setEstudio(null);
    setError(null);
    obtenerEstudio(id)
      .then((d) => activo && setEstudio(d))
      .catch((e) => activo && setError(e));
    return () => {
      activo = false;
    };
  }, [id]);

  return (
    <section>
      <h1>Detalle del estudio</h1>
      <p className="subtitulo">Estudio cargado. El procesamiento es una acción aparte.</p>
      <Pasos actual={2} />
      <ErrorApi error={error} />
      {!estudio && !error && <p className="nota" role="status">Consultando el estudio…</p>}
      {estudio && (
        <div className="tarjeta detalle">
          <p className="nota">CÓDIGO ANÓNIMO</p>
          <p className="codigo">{estudio.codigo}</p>
          <dl className="resumen">
            <dt>Formato</dt><dd>{estudio.formato}</dd>
            <dt>Estado</dt><dd><span className="etiqueta">{estudio.estado}</span></dd>
          </dl>
          {estudio.estado === 'listo para procesar' && (
            <Mensaje tipo="ok">El estudio se cargó y está listo para procesar.</Mensaje>
          )}
          <div className="acciones">
            <button type="button" className="btn btn-primario" disabled aria-describedby="procesar-nota">Procesar</button>
            <span id="procesar-nota" className="nota">Disponible pronto.</span>
          </div>
        </div>
      )}
    </section>
  );
}
