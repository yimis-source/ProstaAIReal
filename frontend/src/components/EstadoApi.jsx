import { useEffect, useState } from 'react';
import { consultarSalud } from '../api/cliente.js';

// Indicador pequeño: consulta /api/salud y muestra si la API responde
export default function EstadoApi() {
  const [estado, setEstado] = useState({ tipo: 'consultando', texto: 'Consultando API…' });

  useEffect(() => {
    let activo = true;
    consultarSalud()
      .then((d) => activo && setEstado({ tipo: 'ok', texto: `API disponible · v${d.version}` }))
      .catch((e) => activo && setEstado({ tipo: 'error', texto: `API sin respuesta: ${e.message}` }));
    return () => {
      activo = false;
    };
  }, []);

  return (
    <span className={`estado-api estado-api-${estado.tipo}`} role="status">
      <span className="punto" aria-hidden="true" />
      {estado.texto}
    </span>
  );
}
