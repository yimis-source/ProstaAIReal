import Mensaje from './Mensaje.jsx';

// Muestra el `detalle` de la API tal cual y, en un 422 de validación, los `campos` que fallaron
export default function ErrorApi({ error, nombres = {} }) {
  if (!error) return null;
  if (typeof error === 'string') return <Mensaje>{error}</Mensaje>;
  const campos = error.campos || [];
  return (
    <Mensaje>
      {error.message}
      {campos.length > 0 && (
        <ul>
          {campos.map((c) => (
            <li key={c}>Revisa el campo: {nombres[c] || c}</li>
          ))}
        </ul>
      )}
    </Mensaje>
  );
}
