import { useState } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { acceder, verificarAlias } from '../api/cliente.js';
import { useAuth } from '../auth/AuthContext.jsx';
import ErrorApi from '../components/ErrorApi.jsx';
import Mensaje from '../components/Mensaje.jsx';

// Mismo patrón que la API (contrato 4.2)
const PATRON_ALIAS = /^[A-Za-z0-9_.-]{3,30}$/;
const NOMBRES = { alias: 'Usuario (alias)', contrasena: 'Contraseña', confirmacion: 'Verificar contraseña' };

function CampoClave({ id, etiqueta, valor, onCambio, placeholder, autoComplete, autoFocus }) {
  const [visible, setVisible] = useState(false);
  return (
    <div className="campo">
      <label htmlFor={id}>{etiqueta}</label>
      <div className="campo-caja">
        <input id={id} type={visible ? 'text' : 'password'} value={valor} placeholder={placeholder}
          onChange={(e) => onCambio(e.target.value)} autoComplete={autoComplete} autoFocus={autoFocus} />
        <button type="button" className="campo-ojo" onClick={() => setVisible(!visible)}
          aria-label={visible ? 'Ocultar contraseña' : 'Mostrar contraseña'}>
          {visible ? 'Ocultar' : 'Mostrar'}
        </button>
      </div>
    </div>
  );
}

// CU01: alias -> si existe pide contraseña; si no, crea la cuenta con contraseña y confirmación
export default function Acceso() {
  const { alias: aliasSesion, aviso, iniciar } = useAuth();
  const navegar = useNavigate();
  const ubicacion = useLocation();
  const destino = (ubicacion.state && ubicacion.state.desde) || '/cargar';
  const [paso, setPaso] = useState('alias'); // alias | contrasena | primera
  const [alias, setAlias] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [confirmacion, setConfirmacion] = useState('');
  const [error, setError] = useState(null);
  const [enviando, setEnviando] = useState(false);

  if (aliasSesion) return <Navigate to={destino} replace />;

  async function continuar(e) {
    e.preventDefault();
    setError(null);
    const limpio = alias.trim();
    if (!PATRON_ALIAS.test(limpio)) {
      setError('El alias debe tener de 3 a 30 caracteres: letras sin tilde, números, punto, guion o guion bajo.');
      return;
    }
    setEnviando(true);
    try {
      const { existe } = await verificarAlias(limpio);
      setAlias(limpio);
      setPaso(existe ? 'contrasena' : 'primera');
    } catch (err) {
      setError(err);
    } finally {
      setEnviando(false);
    }
  }

  async function entrar(e) {
    e.preventDefault();
    setError(null);
    if (paso === 'primera') {
      if (contrasena.length < 8) return setError('La contraseña debe tener al menos 8 caracteres.');
      if (contrasena !== confirmacion) return setError('La contraseña y su confirmación no coinciden.');
    } else if (!contrasena) {
      return setError('Escribe tu contraseña.');
    }
    setEnviando(true);
    try {
      const r = await acceder(alias, contrasena, paso === 'primera' ? confirmacion : undefined);
      iniciar(r.token, r.alias);
      navegar(destino, { replace: true });
    } catch (err) {
      setError(err);
    } finally {
      setEnviando(false);
    }
  }

  function cambiarAlias() {
    setPaso('alias');
    setError(null);
    setContrasena('');
    setConfirmacion('');
  }

  const coinciden = paso === 'primera' && confirmacion && contrasena === confirmacion;
  const textoBoton = enviando
    ? 'Un momento…'
    : paso === 'alias' ? 'Continuar' : paso === 'primera' ? 'Acceder por primera vez' : 'Acceder';

  return (
    <section className="acceso">
      <form className="tarjeta acceso-form" onSubmit={paso === 'alias' ? continuar : entrar} noValidate>
        <h1>Accede a Prosta-AI</h1>
        <p className="subtitulo">Escribe tu alias académico para continuar al espacio de trabajo.</p>
        <Mensaje tipo="info">{aviso}</Mensaje>

        <div className="campo">
          <label htmlFor="alias">Usuario (alias)</label>
          <div className="campo-caja">
            <input id="alias" value={alias} onChange={(e) => setAlias(e.target.value)} placeholder="Tu alias académico"
              autoComplete="username" autoFocus readOnly={paso !== 'alias'} />
          </div>
        </div>

        {paso !== 'alias' && (
          <>
            <button type="button" className="enlace" onClick={cambiarAlias}>Cambiar alias</button>
            {paso === 'primera' && (
              <p className="nota">Este alias es nuevo. Elige una contraseña de al menos 8 caracteres.</p>
            )}
            <CampoClave id="contrasena" etiqueta="Contraseña" valor={contrasena} onCambio={setContrasena}
              placeholder="Tu contraseña" autoComplete={paso === 'primera' ? 'new-password' : 'current-password'} autoFocus />
          </>
        )}
        {paso === 'primera' && (
          <>
            <CampoClave id="confirmacion" etiqueta="Verificar contraseña" valor={confirmacion} onCambio={setConfirmacion}
              placeholder="Ingresa nuevamente tu contraseña" autoComplete="new-password" />
            {coinciden && <Mensaje tipo="ok">Las contraseñas coinciden.</Mensaje>}
          </>
        )}

        <ErrorApi error={error} nombres={NOMBRES} />
        <button className="btn btn-primario btn-ancho" disabled={enviando}>{textoBoton}</button>
        <p className="nota">
          Utiliza únicamente archivos de prueba sin datos personales. No se piden nombre, correo ni otros
          datos personales.
        </p>
      </form>
    </section>
  );
}
