// CU02: carga de un estudio
export default function Cargar() {
  return (
    <section>
      <h1>Cargar estudio</h1>
      <p className="subtitulo">Sube una imagen T2 en formato NIfTI (.nii o .nii.gz) o elige una muestra de prueba.</p>
      <p>
        Aquí irán la zona para arrastrar el archivo, la validación del formato y del tamaño, y el
        botón «Procesar» que envía el estudio a la API.
      </p>
    </section>
  );
}
