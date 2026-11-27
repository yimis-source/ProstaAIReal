import { useEffect, useState } from 'react';
import { obtenerCorte } from '../api/cliente.js';

// Pide un PNG del corte con el token (contrato 4.9) y lo deja como URL local para el <img>
function useCapa(idTrabajo, indice, capa) {
  const [url, setUrl] = useState(null);
  const [fallo, setFallo] = useState(false);
  useEffect(() => {
    let activo = true;
    setFallo(false);
    obtenerCorte(idTrabajo, indice, capa)
      .then((blob) => {
        if (!activo) return;
        setUrl(URL.createObjectURL(blob));
      })
      .catch(() => activo && setFallo(true));
    return () => {
      activo = false;
    };
  }, [idTrabajo, indice, capa]);
  return { url, fallo };
}

// Visor del CU04 (RF-13, RF-14): capa `imagen` y, encima, la capa `mascara` con la ROI.
// El interruptor «Mostrar ROI» solo oculta o muestra la capa ya descargada.
export default function Visor({ idTrabajo, cortes }) {
  const [indice, setIndice] = useState(Math.floor(cortes / 2));
  const [mostrarRoi, setMostrarRoi] = useState(true);
  const [opacidad, setOpacidad] = useState(0.45);
  const imagen = useCapa(idTrabajo, indice, 'imagen');
  const mascara = useCapa(idTrabajo, indice, 'mascara');

  return (
    <figure className="visor tarjeta">
      <div className="visor-lienzo">
        {imagen.url && <img src={imagen.url} alt={`Corte axial ${indice + 1} de ${cortes}`} />}
        {mascara.url && (
          <img className="visor-capa" src={mascara.url} alt="" hidden={!mostrarRoi} style={{ opacity: opacidad }} />
        )}
        {!imagen.url && !imagen.fallo && <p className="visor-nota" role="status">Cargando corte…</p>}
        {(imagen.fallo || mascara.fallo) && <p className="visor-nota" role="alert">No se pudo cargar el corte.</p>}
      </div>
      <figcaption className="visor-controles">
        <div className="control">
          <label htmlFor="corte">Corte {indice + 1} de {cortes}</label>
          <input
            id="corte"
            type="range"
            min="0"
            max={cortes - 1}
            value={indice}
            onChange={(e) => setIndice(Number(e.target.value))}
          />
        </div>
        <div className="control control-fila">
          <input
            id="mostrar-roi"
            type="checkbox"
            role="switch"
            checked={mostrarRoi}
            onChange={(e) => setMostrarRoi(e.target.checked)}
          />
          <label htmlFor="mostrar-roi">Mostrar ROI</label>
        </div>
        <div className="control">
          <label htmlFor="opacidad">Opacidad de la ROI: {Math.round(opacidad * 100)} %</label>
          <input
            id="opacidad"
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={opacidad}
            disabled={!mostrarRoi}
            onChange={(e) => setOpacidad(Number(e.target.value))}
          />
        </div>
      </figcaption>
    </figure>
  );
}
