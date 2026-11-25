import { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registrarAlExpirar, sesion } from '../api/cliente.js';

const AuthContext = createContext(null);

export function useAuth() {
  const valor = useContext(AuthContext);
  if (!valor) throw new Error('useAuth debe usarse dentro de <AuthProvider>.');
  return valor;
}

// Sesión académica: token y alias en sessionStorage (se borran al cerrar la pestaña)
export function AuthProvider({ children }) {
  const navegar = useNavigate();
  const [alias, setAlias] = useState(sesion.alias());
  const [aviso, setAviso] = useState('');

  const iniciar = useCallback((token, nombre) => {
    sesion.guardar(token, nombre);
    setAlias(nombre);
    setAviso('');
  }, []);

  const cerrar = useCallback(
    (mensaje = '') => {
      sesion.borrar();
      setAlias(null);
      setAviso(mensaje);
      navegar('/acceso');
    },
    [navegar]
  );

  // Un 401 con sesión abierta cierra la sesión y lleva a /acceso
  useEffect(() => {
    registrarAlExpirar(() => cerrar('Tu sesión terminó. Vuelve a ingresar.'));
  }, [cerrar]);

  return (
    <AuthContext.Provider value={{ alias, aviso, iniciar, cerrar }}>{children}</AuthContext.Provider>
  );
}
