import { useParams } from 'react-router-dom';

// CU04: visualización de la ROI con el panel «¿Qué estoy viendo?»
export default function Roi() {
  const { id } = useParams();
  return (
    <section>
      <h1>Región de interés (ROI)</h1>
      <p className="subtitulo">Estudio {id}</p>
      <p>
        Aquí irán el visor del corte T2 con la ROI superpuesta (mostrar u ocultar, opacidad y cambio
        de corte), las métricas Dice e IoU cuando se cargó una máscara de referencia, y el panel «¿Qué estoy viendo?» con el texto de docs/diseno/texto_roi.md.
      </p>
    </section>
  );
}
