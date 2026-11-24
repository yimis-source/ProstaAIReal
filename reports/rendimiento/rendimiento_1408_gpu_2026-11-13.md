# Tiempo y memoria de la inferencia en GPU (tareas 1408 y 1602) — 2026-11-13

Uso académico y experimental. Mide la ruta de inferencia del ciclo 3 con un estudio representativo, esta vez en GPU, para cerrar lo que quedó pendiente de la tarea 1408.

## Condiciones

- Estudio: `prostate_13` de MSD Task05 (canal T2), forma (320, 320, 20), espaciado (0.625, 0.625, 3.6) mm; volumen preparado a 0,5 mm: (400, 400, 138).
- Modelo: `prostate_mri_anatomy` 0.3.6, ventana deslizante 96³, lote 4, solape 0,5.
- Dispositivo: cuda; GPU: Tesla T4 (15 360 MiB, controlador 580.82.07). CPU: Intel(R) Xeon(R) CPU @ 2.00GHz; 1 hilo de torch; RAM 12.7 GB; Linux 6.6.159+ (Google Colab).
- Software: Python 3.13.16, torch 2.5.1+cu121 (CUDA 12.1), MONAI 1.4.0, numpy 1.26.4.
- Versión del código medida: `f36fd8f` (cierre del ciclo 4), con `python scripts/medir_rendimiento.py --caso prostate_13 --repeticiones 3 --dispositivo cuda`.
- Repeticiones: 3. La primera incluye la carga de los pesos (arranque en frío).
- Memoria: pico de memoria residente (RSS) del proceso medido con `resource.getrusage`.

## Resultados por repetición (segundos)

| Rep. | lectura y control de calidad | preparación | inferencia | rejilla original | Total | Pico RSS (MB) |
|---|---:|---:|---:|---:|---:|---:|
| 1 (en frío) | 0.05 | 2.67 | 4.05 | 0.16 | **6.93** | 2644 |
| 2 | 0.06 | 2.57 | 2.34 | 0.11 | **5.09** | 3201 |
| 3 | 0.04 | 2.46 | 2.33 | 0.10 | **4.94** | 3243 |

## Resumen

- Memoria del proceso tras importar librerías y construir el pipeline: 1417 MB; pico durante la medición: 3243 MB.
- Tiempo medio por estudio con el modelo ya cargado: 5.0 s (inferencia: 2.3 s).
- Repetición más lenta (de todas, incluida la de arranque en frío): 6.9 s.
- RR-01 (≤ 120 s por estudio): **se cumple** con margen de 113 s sobre la repetición más lenta.

## GPU

- GPU: Tesla T4.
- Con el modelo ya cargado, la inferencia pasa de 13.0 s en CPU (informe del 07/11/2026) a 2.3 s en GPU. La preparación (unos 2.5 s) se hace en CPU en los dos casos, así que ahora es casi la mitad del tiempo total.
- Los tiempos de esta medición **no son comparables** con los de CPU: cambian el equipo, el procesador (Xeon de Colab con 1 hilo frente a Ryzen 5 5600G con 6 hilos) y la memoria. Solo sirven para ver el orden de magnitud y comprobar RR-01 en cada equipo.
- **Memoria de la GPU: no medida en esta corrida.** La versión `f36fd8f` del script solo medía la memoria del proceso (RSS) y escribía «No disponible» en esta sección aunque se midiera en GPU. Con la corrección de la tarea 1602, el script escribe este informe como `rendimiento_1408_gpu_<fecha>.md`, pone el nombre de la GPU y agrega la columna «Pico GPU (MB)» (`torch.cuda.max_memory_allocated`). Para tener esa cifra hay que repetir la medición en Colab con la celda de la guía del ciclo 5.

## Limitaciones

- Un solo estudio y un solo equipo; los tiempos cambian con el tamaño del volumen y el hardware.
- La GPU de Colab gratuita no está garantizada: el tipo de GPU y su disponibilidad cambian entre sesiones.
- No incluye la carga del archivo por la web ni guardar resultados (eso se mide en el ciclo 6).
