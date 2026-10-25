"""Pruebas de la verificación de anonimización (tarea 1205)."""
import nibabel as nib
import numpy as np

from scripts.verificar_anonimizacion import informe, revisar


def _nifti(ruta, descrip=b""):
    img = nib.Nifti1Image(np.zeros((4, 4, 4), np.int16), np.eye(4))
    img.header["descrip"] = descrip
    ruta.parent.mkdir(parents=True, exist_ok=True)
    nib.save(img, str(ruta))


def test_datos_limpios_sin_hallazgos(tmp_path):
    _nifti(tmp_path / "Task05_Prostate" / "imagesTr" / "prostate_00.nii.gz")
    texto, aprobado = informe(revisar(tmp_path))
    assert aprobado, texto


def test_detecta_nombre_y_fecha_en_el_archivo(tmp_path):
    _nifti(tmp_path / "Task05_Prostate" / "imagesTr" / "juan_perez_20190311.nii.gz")
    res = revisar(tmp_path)["MSD Task05_Prostate"]
    assert res["nombres_no_neutros"] and res["fechas_en_nombres"]


def test_detecta_texto_en_cabecera_y_claves_mhd(tmp_path):
    _nifti(tmp_path / "Task05_Prostate" / "imagesTr" / "prostate_01.nii.gz", b"Paciente: Ana")
    mhd = tmp_path / "externos" / "promise12" / "training_data" / "Case00.mhd"
    mhd.parent.mkdir(parents=True)
    mhd.write_text("NDims = 3\nPatientName = ANA\n")
    res = revisar(tmp_path)
    assert "descrip = «Paciente: Ana»" in res["MSD Task05_Prostate"]["campos_nifti"]
    assert any("PatientName" in k for k in res["PROMISE12 (entrenamiento)"]["claves_mhd_extra"])
    assert not informe(res)[1]


def test_detecta_dicom_por_firma(tmp_path):
    dcm = tmp_path / "Task05_Prostate" / "imagesTr" / "001"
    dcm.parent.mkdir(parents=True)
    dcm.write_bytes(b"\0" * 128 + b"DICM" + b"\0" * 10)
    assert revisar(tmp_path)["MSD Task05_Prostate"]["dicom"]
