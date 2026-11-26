import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { cargarEstudio } from '../api/cliente.js';
import ErrorApi from '../components/ErrorApi.jsx';
import Pasos from '../components/Pasos.jsx';
import { esNifti, formatoTamano, MAX_ARCHIVO, validarCarga } from '../validacion.js';

const NOMBRES = { archivos: 'Imagen T2', referencia: 'Máscara de referencia' };

// Selector de un archivo NIfTI con zona para arrastrar
function SelectorArchivo({ id, titulo, ayuda, archivo, onCambio, opcional }) {
  const entrada = useRef(null);
  const [encima, setEncima] = useState(false);

  function soltar(e) {
    e.preventDefault();
    setEncima(false);
    const f = e.dataTransfer.files && e.dataTransfer.files[0];
    if (f) onCambio(f);
  }

  const problema = archivo && (!esNifti(archivo.name) ? 'Formato no admitido' : archivo.size > MAX_ARCHIVO ? 'Supera 50 MB' : '');

  return (
    <div className="selector">
      <div className={`zona${encima ? ' zona-encima' : ''}`} onDragOver={(e) => { e.preventDefault(); setEncima(true); }}
        onDragLeave={() => setEncima(false)} onDrop={soltar}>
        <p className="zona-titulo">{titulo}{opcional && <span className="etiqueta">Opcional</span>}</p>
        <p className="nota">{ayuda}</p>
        <input ref={entrada} id={id} type="file" accept=".nii,.gz" hidden
          onChange={(e) => { onCambio(e.target.files[0] || null); e.target.value = ''; }} />
        <button type="button" className="btn" onClick={() => entrada.current.click()}>
          {archivo ? 'Cambiar archivo' : 'Seleccionar archivo'}
        </button>
      </div>
      {archivo && (
        <div className={`archivo${problema ? ' archivo-error' : ''}`}>
          <div>
            <p className="archivo-nombre">{archivo.name}</p>
            <p className="nota">{formatoTamano(archivo.size)}{problema ? ` · ${problema}` : ' · Listo para enviar'}</p>
          </div>
          <button type="button" className="enlace" onClick={() => onCambio(null)} aria-label={`Quitar ${archivo.name}`}>Quitar</button>
        </div>
      )}
    </div>
  );
}

// CU02: carga de un estudio (imagen NIfTI y máscara de referencia opcional)
export default function Cargar() {
  const navegar = useNavigate();
  const [imagen, setImagen] = useState(null);
  const [referencia, setReferencia] = useState(null);
  const [error, setError] = useState(null);
  const [enviando, setEnviando] = useState(false);

  const total = (imagen ? imagen.size : 0) + (referencia ? referencia.size : 0);

  async function enviar(e) {
    e.preventDefault();
    setError(null);
    const problema = validarCarga(imagen, referencia);
    if (problema) return setError(problema);
    setEnviando(true);
    try {
      const estudio = await cargarEstudio(imagen, referencia);
      navegar(`/estudios/${estudio.id}/estado`);
    } catch (err) {
      setError(err);
      setEnviando(false);
    }
  }

  return (
    <section>
      <h1>Cargar estudio</h1>
      <p className="subtitulo">
        Sube una imagen T2 en formato NIfTI (.nii o .nii.gz). La API le asigna un código anónimo y no guarda el
        nombre original del archivo.
      </p>
      <Pasos actual={1} />

      <form className="carga" onSubmit={enviar} noValidate>
        <div className="carga-principal">
          <SelectorArchivo id="imagen" titulo="Imagen T2" archivo={imagen} onCambio={setImagen}
            ayuda="Un archivo NIfTI (.nii o .nii.gz) de hasta 50 MB." />
          <SelectorArchivo id="referencia" titulo="Máscara de referencia" opcional archivo={referencia} onCambio={setReferencia}
            ayuda="Si la cargas, al procesar se calculan Dice e IoU contra ella. NIfTI de hasta 50 MB." />
        </div>

        <aside className="carga-lado">
          <div className="tarjeta">
            <p className="tarjeta-titulo">Resumen del estudio</p>
            <dl className="resumen">
              <dt>Archivos</dt><dd>{[imagen, referencia].filter(Boolean).length}</dd>
              <dt>Tamaño total</dt><dd>{total ? formatoTamano(total) : '—'}</dd>
              <dt>Máximo del estudio</dt><dd>150 MB</dd>
            </dl>
          </div>
          <div className="tarjeta tarjeta-teal">
            <p className="tarjeta-titulo">Se eliminan los metadatos de texto o se rechaza el archivo</p>
            <p>Usa únicamente archivos de prueba sin datos personales. No incluyas nombres en los archivos.</p>
          </div>
        </aside>

        <div className="carga-pie">
          <ErrorApi error={error} nombres={NOMBRES} />
          <button className="btn btn-primario" disabled={enviando || !imagen}>
            {enviando ? 'Enviando…' : 'Cargar estudio'}
          </button>
        </div>
      </form>
    </section>
  );
}
