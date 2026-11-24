import { Link, useParams } from 'react-router-dom';

// CU03: estado del procesamiento de un estudio
export default function Estado() {
  const { id } = useParams();
  return (
    <section>
      <h1>Estado del procesamiento</h1>
      <p className="subtitulo">Estudio {id}</p>
      <p>
        Aquí irán las etapas (control de calidad, preparación, segmentación, ROI y evaluación), el
        estado de cada una y el tiempo transcurrido, consultados a la API cada pocos segundos.
      </p>
      <p><Link to={`/estudios/${id}/roi`}>Ver la ROI del estudio</Link></p>
    </section>
  );
}
