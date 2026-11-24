import { NavLink, Outlet } from 'react-router-dom';
import Aviso from './Aviso.jsx';
import EstadoApi from './EstadoAPI.jsx';

const ENLACES = [
  ['/', 'Inicio'],
  ['/acceso', 'Acceso'],
  ['/cargar', 'Cargar estudio'],
];

// Marco común: encabezado con navegación, contenido y aviso fijo
export default function Layout() {
  return (
    <div className="marco">
      <header className="cabecera">
        <NavLink to="/" className="logo">Prosta-AI</NavLink>
        <nav aria-label="Principal">
          <ul className="menu">
            {ENLACES.map(([ruta, texto]) => (
              <li key={ruta}>
                <NavLink to={ruta} end={ruta === '/'}>{texto}</NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <EstadoApi />
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
