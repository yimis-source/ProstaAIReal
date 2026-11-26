import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listarEstudios } from '../api/historial.js';
import ErrorApi from '../components/ErrorApi.jsx';
import { useAuth } from '../auth/AuthContext.jsx';
import './MisEstudios.css';

const FECHA = new Intl.DateTimeFormat('es-CO', { dateStyle: 'medium', timeStyle: 'short' });
const METRICA = new Intl.NumberFormat('es-CO', { minimumFractionDigits: 3, maximumFractionDigits: 3 });

const fecha = (iso) => (iso ? FECHA.format(new Date(iso)) : '—');
const metrica = (valor) => (valor === null || valor === undefined ? '—' : METRICA.format(valor));

// CU05 (RF-19): historial de los estudios del usuario, del más reciente al más antiguo
export default function MisEstudios() {
  const { cerrar } = useAuth();
  const [estudios, setEstudios] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let activo = true;
    listarEstudios()
      .then((lista) => activo && setEstudios(lista))
      .catch((e) => {
        if (!activo) return;
        // Token vencido o no válido: igual que el resto de pantallas, se vuelve a /acceso
        if (e.estado === 401) cerrar('Tu sesión terminó. Vuelve a ingresar.');
        else setError(e);
      });
    return () => {
      activo = false;
    };
  }, [cerrar]);

  const vacio = estudios !== null && estudios.length === 0;

  return (
    <section>
      <div className="historial-cabecera">
        <div>
          <h1>Mis estudios</h1>
          <p className="subtitulo">Consulta tus estudios de prueba y vuelve al estado de cada uno.</p>
        </div>
        {!vacio && <Link className="btn btn-primario" to="/cargar">Cargar estudio</Link>}
      </div>
      <ErrorApi error={error} />
      {estudios === null && !error && <p className="nota" role="status">Consultando tus estudios…</p>}

      {vacio && (
        <div className="tarjeta historial-vacio">
          <h2>Aún no hay estudios</h2>
          <p>Carga tu primer estudio de prueba para recorrer el flujo de procesamiento y ver la ROI calculada.</p>
          <p className="acciones">
            <Link className="btn btn-primario" to="/cargar">Cargar estudio</Link>
          </p>
          <p className="nota">Solo archivos NIfTI de prueba, sin datos personales.</p>
        </div>
      )}

      {estudios && estudios.length > 0 && (
        <>
          <p className="nota">
            {estudios.length === 1 ? '1 estudio' : `${estudios.length} estudios`} · más recientes primero
          </p>
          <div className="tarjeta historial-tabla">
            <table>
              <thead>
                <tr>
                  <th scope="col">Código anónimo</th>
                  <th scope="col">Formato</th>
                  <th scope="col">Fecha de carga</th>
                  <th scope="col">Estado</th>
                  <th scope="col">Dice</th>
                  <th scope="col"><span className="oculto">Acción</span></th>
                </tr>
              </thead>
              <tbody>
                {estudios.map((e) => (
                  <tr key={e.id}>
                    <td className="historial-codigo">{e.codigo}</td>
                    <td>{e.formato}</td>
                    <td>{fecha(e.fecha_carga)}</td>
                    <td><span className="etiqueta historial-estado">{e.estado}</span></td>
                    <td>{metrica(e.dice)}</td>
                    <td>
                      <Link to={`/estudios/${e.id}/estado`} aria-label={`Ver estado de ${e.codigo}`}>Ver estado</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="nota">«—» en Dice indica que el estudio aún no tiene resultado o que se cargó sin máscara de referencia.</p>
        </>
      )}
    </section>
  );
}
