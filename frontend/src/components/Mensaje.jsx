// Mensaje de error, éxito o información; los errores se anuncian a los lectores de pantalla
export default function Mensaje({ tipo = 'error', children }) {
  if (!children) return null;
  return (
    <div className={`mensaje mensaje-${tipo}`} role={tipo === 'error' ? 'alert' : 'status'}>
      {children}
    </div>
  );
}
