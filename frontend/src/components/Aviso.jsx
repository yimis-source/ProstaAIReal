import { AVISO_EXPERIMENTAL } from '../constantes.js';

// Aviso de uso no diagnóstico, fijo en todas las pantallas (RF-15, RF-16)
export default function Aviso() {
  return (
    <div className="aviso" role="note">
      <span className="aviso-icono" aria-hidden="true">i</span>
      <p>{AVISO_EXPERIMENTAL}</p>
    </div>
  );
}
