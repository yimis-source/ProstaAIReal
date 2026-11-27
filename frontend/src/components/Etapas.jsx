import { ETAPAS, capitalizar, formatearSegundos } from '../constantes.js';

const DESCRIPCIONES = {
  'control de calidad': 'Integridad del volumen y de sus metadatos.',
  preparación: 'Mismas transformaciones que usa el modelo.',
  segmentación: 'Máscara 3D con el modelo experimental.',
  ROI: 'Máscara en la rejilla de la imagen original.',
  evaluación: 'Dice e IoU si se cargó una máscara de referencia.',
};
const ICONOS = { pendiente: '○', 'en proceso': '…', completado: '✓', fallido: '✕' };

// Las 5 etapas en su orden fijo, con estado y duración; una etapa que no llegó se muestra pendiente
export default function Etapas({ etapas = [] }) {
  const porNombre = Object.fromEntries(etapas.map((e) => [e.nombre, e]));
  return (
    <ol className="etapas" aria-label="Etapas del procesamiento">
      {ETAPAS.map((nombre) => {
        const e = porNombre[nombre] || { estado: 'pendiente', duracion_s: null };
        return (
          <li key={nombre} className={`etapa etapa-${e.estado.replace(' ', '-')}`}>
            <span className="etapa-icono" aria-hidden="true">{ICONOS[e.estado] || '○'}</span>
            <div className="etapa-info">
              <span className="etapa-nombre">{capitalizar(nombre)}</span>
              <span className="etapa-desc">{DESCRIPCIONES[nombre]}</span>
            </div>
            <div className="etapa-lado">
              <span className="etapa-tiempo">{formatearSegundos(e.duracion_s)}</span>
              <span className="etapa-estado">{capitalizar(e.estado)}</span>
            </div>
          </li>
        );
      })}
    </ol>
  );
}
