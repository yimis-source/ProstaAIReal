import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext.jsx';

// Pantallas que piden sesión: sin alias se va a /acceso y, al ingresar, se vuelve a la ruta pedida
export default function RutaProtegida() {
  const { alias } = useAuth();
  const ubicacion = useLocation();
  if (!alias) return <Navigate to="/acceso" replace state={{ desde: ubicacion.pathname }} />;
  return <Outlet />;
}
