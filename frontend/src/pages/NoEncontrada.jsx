import { Link } from 'react-router-dom';

// Página para rutas que no existen
export default function NoEncontrada() {
  return (
    <section>
      <h1>Página no encontrada</h1>
      <p className="subtitulo">La dirección que abriste no existe en Prosta-AI.</p>
      <p><Link to="/">Volver al inicio</Link></p>
    </section>
  );
}
