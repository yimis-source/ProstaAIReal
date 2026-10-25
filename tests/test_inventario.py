"""Pruebas del inventario de datos (tarea 1204)."""
import hashlib

from scripts.inventario_datos import contar_casos, inventariar, sha256, tipo_archivo


def test_sha256_coincide_con_hashlib(tmp_path):
    ruta = tmp_path / "x.nii.gz"
    ruta.write_bytes(b"prosta-ai" * 1000)
    assert sha256(ruta) == hashlib.sha256(b"prosta-ai" * 1000).hexdigest()


def test_tipos_de_archivo():
    assert tipo_archivo("prostate_00.nii.gz") == "imagen"
    assert tipo_archivo("Case00.mhd") == "imagen"
    assert tipo_archivo("dataset.json") == "metadatos"
    assert tipo_archivo("a.py") == "no esperado"


def test_msd_solo_cuenta_con_mascara_los_casos_con_imagen_y_etiqueta(tmp_path):
    base = tmp_path / "Task05_Prostate"
    for carpeta, casos in (("imagesTr", ["prostate_00", "prostate_01"]), ("labelsTr", ["prostate_00"]),
                           ("imagesTs", ["prostate_03"])):
        (base / carpeta).mkdir(parents=True)
        for c in casos:
            (base / carpeta / f"{c}.nii.gz").write_bytes(c.encode())
    filas, resumen = inventariar(tmp_path)
    r = resumen["MSD Task05_Prostate"]
    assert contar_casos("MSD Task05_Prostate", r["casos"]).startswith("1 con máscara")
    assert all(f["sha256"] for f in filas)


def test_archivo_no_esperado_se_lista_sin_hash(tmp_path):
    base = tmp_path / "externos" / "promise12" / "training_data"
    base.mkdir(parents=True)
    (base / "Case00.mhd").write_text("NDims = 3\n")
    (base / "a.py").write_text("print('no se ejecuta')\n")
    filas, resumen = inventariar(tmp_path)
    assert resumen["PROMISE12 (entrenamiento)"]["no_esperados"] == ["a.py"]
    assert [f["sha256"] for f in filas if f["tipo"] == "no esperado"] == [""]
