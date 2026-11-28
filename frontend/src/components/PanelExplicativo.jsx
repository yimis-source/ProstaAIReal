import { formatearSegundos } from '../constantes.js';

// Dice e IoU con coma decimal; null cuando el estudio no trae máscara de referencia (contrato 4.8)
const metrica = (v) => (v === null || v === undefined ? null : v.toFixed(3).replace('.', ','));

// Panel «¿Qué estoy viendo?» (RF-17), textos de docs/diseno/texto_roi.md, sección 1
export default function PanelExplicativo({ resultado }) {
  const dice = metrica(resultado.dice);
  const iou = metrica(resultado.iou);
  const conReferencia = dice !== null || iou !== null;
  const { modelo } = resultado;

  return (
    <aside className="tarjeta panel" aria-labelledby="t-panel">
      <h2 id="t-panel">¿Qué estoy viendo?</h2>

      <dl className="resumen panel-datos">
        <dt>Dice</dt>
        <dd>{dice ?? 'sin máscara de referencia'}</dd>
        <dt>IoU</dt>
        <dd>{iou ?? 'sin máscara de referencia'}</dd>
        <dt>Modelo</dt>
        <dd>{modelo ? `${modelo.nombre} (${modelo.version})` : '—'}</dd>
        <dt>Tiempo total</dt>
        <dd>{formatearSegundos(resultado.tiempo_total_s)}</dd>
      </dl>

      <h3>Qué muestra la ROI</h3>
      <p>
        La zona verde azulada es la región de interés (ROI): el contorno que el modelo calculó para la próstata en
        este corte de la imagen T2. Es una marca generada por un programa para que veas qué región delimitó; no
        interpreta la imagen ni dice nada sobre el estado de la persona. Puedes ver la imagen con y sin la ROI y
        cambiar su opacidad.
      </p>

      <h3>Qué significan Dice e IoU</h3>
      <p>
        Son dos números entre 0 y 1 que comparan la ROI del modelo con una referencia dibujada a mano en datos
        públicos de prueba. Valen 1 si coinciden del todo y 0 si no se solapan.
      </p>
      <ul>
        <li>Dice: el doble del solapamiento dividido entre la suma de las dos áreas.</li>
        <li>IoU: el solapamiento dividido entre el área de la unión de ambas.</li>
      </ul>
      <p>
        Solo se calculan cuando hay una referencia; con una imagen propia sin referencia no se muestran.
        {!conReferencia && ' Este estudio se cargó sin máscara de referencia.'}
      </p>
      <p className="nota">
        En los 5 casos de prueba el Dice medio fue 0,8925 ± 0,0340 y el IoU medio 0,8071 ± 0,0534 (informe del
        19/11/2026). Son cifras del conjunto público de prueba, no de tus datos.
      </p>

      <h3>Límites que debes conocer</h3>
      <ul>
        <li>
          Solo se evaluó con 5 casos de prueba; con tan pocos casos la media es poco estable (el más bajo fue
          prostate_28, Dice 0,8320).
        </li>
        <li>
          Cambio de dominio: el modelo se entrenó con otros datos (Prostate158) y los casos de prueba (MSD Task05)
          tienen otra resolución y protocolo, con cortes gruesos de 4 mm.
        </li>
        <li>Los cortes gruesos hacen que los bordes de la base y el ápex sean menos precisos.</li>
        <li>
          Posible sesgo del modelo preentrenado: la documentación no menciona los datos de Task05, pero no se puede
          garantizar que no se hayan usado en su entrenamiento; si así fuera, las cifras estarían sobreestimadas.
        </li>
        <li>
          Al ampliar a los 32 casos, el Dice medio baja a 0,8736 ± 0,1222 porque prostate_07 tiene Dice 0,2255: el
          modelo marcó una región falsa cerca del borde del campo de visión. Ese caso muestra que la ROI puede fallar.
        </li>
        <li>Uso académico: no hay validación clínica ni externa.</li>
      </ul>
    </aside>
  );
}
