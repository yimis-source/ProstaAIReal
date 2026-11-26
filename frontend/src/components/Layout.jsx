import { NavLink, Outlet } from 'react-router-dom';
import Aviso from './Aviso.jsx';
import EstadoApi from './EstadoApi.jsx';
import { useAuth } from '../auth/AuthContext.jsx';

const ENLACES = [
  ['/', 'Inicio'],
  ['/acceso', 'Acceso'],
  ['/cargar', 'Cargar estudio'],
  ['/estudios', 'Mis estudios'],
];

// Marco común: encabezado con navegación, contenido y aviso fijo
export default function Layout() {
  const { alias, cerrar } = useAuth();
  return (
    <div className="marco">
      <header className="cabecera">
        <NavLink to="/" className="logo">Prosta-AI</NavLink>
        <nav aria-label="Principal">
          <ul className="menu">
            {ENLACES.map(([ruta, texto]) => (
              <li key={ruta}>
                <NavLink to={ruta} end={ruta === '/' || ruta === '/estudios'}>{texto}</NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <EstadoApi />
        {alias && (
          <span className="sesion">
            Sesión: <strong>{alias}</strong>
            <button type="button" className="enlace" onClick={() => cerrar()}>Cerrar sesión</button>
          </span>
        )}
      </header>
      <main id="principal">
        <Outlet />
      </main>
      <footer className="pie">
        <Aviso />
      </footer>
    </div>
  );
}
