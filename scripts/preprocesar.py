"""Preprocesamiento de un volumen para el modelo (tarea 1305, RF-09).

Pasos (MONAI), en este orden:
  1. Orientación RAS.
  2. Remuestreo a vóxeles isotrópicos (por defecto 0,5 mm, interpolación bilineal).
  3. Escala de intensidad a [0, 1].
  4. Normalización (resta la media y divide por la desviación típica).

Los valores por defecto son los de la configuración de inferencia del modelo
preentrenado candidato (`prostate_mri_anatomy`, MONAI Model Zoo). La misma
preparación debe usarse en entrenamiento e inferencia; en el ciclo 3 pasa a
vivir en el paquete del pipeline.

Uso (desde la raíz del repositorio):
    python scripts/preprocesar.py datos/convertidos/msd_task05/prostate_00_t2.nii.gz salida.nii.gz
    python scripts/preprocesar.py ENTRADA SALIDA --espaciado 1.0 --sin-normalizar
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import nibabel as nib
import numpy as np
import torch
from monai.data import MetaTensor
from monai.transforms import Compose, EnsureTyped, NormalizeIntensityd, Orientationd, ScaleIntensityd, Spacingd


def transformaciones(espaciado: float = 0.5, normalizar: bool = True) -> Compose:
    pasos = [
        Orientationd(keys="imagen", axcodes="RAS"),
        Spacingd(keys="imagen", pixdim=(espaciado,) * 3, mode="bilinear"),
        ScaleIntensityd(keys="imagen", minv=0.0, maxv=1.0),
    ]
    if normalizar:
        pasos.append(NormalizeIntensityd(keys="imagen"))
    pasos.append(EnsureTyped(keys="imagen"))
    return Compose(pasos)


def preprocesar(entrada: Path, espaciado: float = 0.5, normalizar: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Devuelve (volumen preparado, afín del espacio preparado). Toma el canal 0 si el NIfTI es 4D."""
    img = nib.load(str(entrada))
    datos = np.asarray(img.dataobj, dtype=np.float32)
    if datos.ndim == 4:
        datos = datos[..., 0]
    tensor = MetaTensor(torch.from_numpy(datos[None]), affine=torch.as_tensor(img.affine))
    salida = transformaciones(espaciado, normalizar)({"imagen": tensor})["imagen"]
    return salida[0].numpy(), np.asarray(salida.affine)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada", type=Path)
    ap.add_argument("salida", type=Path)
    ap.add_argument("--espaciado", type=float, default=0.5)
    ap.add_argument("--sin-normalizar", action="store_true")
    args = ap.parse_args()
    t0 = time.perf_counter()
    vol, afin = preprocesar(args.entrada, args.espaciado, not args.sin_normalizar)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    nib.save(nib.Nifti1Image(vol.astype(np.float32), afin), str(args.salida))
    print(f"Forma preparada {vol.shape}, media {vol.mean():.3f}, desv. {vol.std():.3f}, "
          f"{time.perf_counter() - t0:.1f} s")


if __name__ == "__main__":
    main()
