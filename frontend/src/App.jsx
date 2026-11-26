import { Route, Routes } from 'react-router-dom';
import Layout from './components/Layout.jsx';
import RutaProtegida from './components/RutaProtegida.jsx';
import Inicio from './pages/Inicio.jsx';
import Acceso from './pages/Acceso.jsx';
import Cargar from './pages/Cargar.jsx';
import Estado from './pages/Estado.jsx';
import MisEstudios from './pages/MisEstudios.jsx';
import Roi from './pages/Roi.jsx';
import NoEncontrada from './pages/NoEncontrada.jsx';

// Rutas del ciclo 6: CU00 a CU05. Cargar y los estudios piden sesión.
export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Inicio />} />
        <Route path="/acceso" element={<Acceso />} />
        <Route element={<RutaProtegida />}>
          <Route path="/cargar" element={<Cargar />} />
          <Route path="/estudios" element={<MisEstudios />} />
          <Route path="/estudios/:id/estado" element={<Estado />} />
          <Route path="/estudios/:id/roi" element={<Roi />} />
        </Route>
        <Route path="*" element={<NoEncontrada />} />
      </Route>
    </Routes>
  );
}
