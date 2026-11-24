import { Route, Routes } from 'react-router-dom';
import Inicio from './pages/Inicio.jsx';
import Acceso from './pages/Acceso.jsx';
import Cargar from './pages/Cargar.jsx';
import Estado from './pages/Estado.jsx';
import Roi from './pages/Roi.jsx';
import NoEncontrada from './pages/NoEncontrada.jsx';

// Rutas del ciclo 6: CU00 a CU04
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Inicio />} />
      <Route path="/acceso" element={<Acceso />} />
      <Route path="/cargar" element={<Cargar />} />
      <Route path="/estudios/:id/estado" element={<Estado />} />
      <Route path="/estudios/:id/roi" element={<Roi />} />
      <Route path="*" element={<NoEncontrada />} />
    </Routes>
  );
}
