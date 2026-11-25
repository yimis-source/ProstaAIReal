import { Link } from 'react-router-dom';

// CU00: pantalla de inicio
export default function Inicio() {
  return (
    <section>
      <h1>Bienvenido a Prosta-AI</h1>
      <p className="subtitulo">
        Herramienta académica que segmenta la próstata en imágenes de resonancia magnética T2 y
        muestra la región de interés (ROI) calculada por el modelo.
      </p>
      <p>
        Para empezar, ingresa con tu alias y carga un estudio NIfTI de prueba. Después podrás procesarlo y ver
        la ROI calculada.
      </p>
      <p className="acciones">
        <Link className="btn btn-primario" to="/cargar">Cargar estudio</Link>
        <Link className="btn" to="/acceso">Acceso</Link>
      </p>
    </section>
  );
}
