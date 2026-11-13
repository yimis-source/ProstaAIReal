# Arquitectura de datos (base de datos)

Describe cómo fluyen y se almacenan los datos de Prosta-AI y define el modelo de la base de datos PostgreSQL.

## Ficha

| Campo | Detalle |
|---|---|
| Paquete EDT | 1.3.2.5 |
| Fecha y versión | 22/10/2026 |
| Autores | Yeison Bolaños Ruiz, Juan David Riascos Erazo, Sergio Gabriel Meneses Silva, Yimis Buenaventura y Fernando José Angulo Núñez |
| Formato | PDF |

## Contenido principal

* **Flujo de datos:** recopilación (carga DICOM o NIfTI), validación (si no cumple, el archivo se rechaza y no se guarda), transformación, evaluación y registro.
* **Siete tablas:** usuario, estudio, archivo, modelo, trabajo, etapa de trabajo y resultado.
* **Relaciones:** un usuario carga varios estudios; un estudio tiene archivos y puede procesarse en varios trabajos; cada trabajo usa una versión del modelo, registra etapas y produce un resultado solo si se completa.
* **Privacidad:** las contraseñas se guardan solo como hash; imágenes, máscaras y pesos viven fuera de la base (solo ruta y hash), sin metadatos identificables.
* **Resultados:** Dice e IoU quedan nulos si no hay referencia.
* **Reglas físicas:** borrado en cascada al eliminar un estudio e índices por estado del trabajo y por usuario.
* **Implementación:** Ciclo 6 (actividad 1703), con verificación de cero datos personales en la actividad 1711.
* **Trazabilidad:** vincula las tablas con los requisitos 2.2, 3.5, 4.1, 4.2, 4.5, 4.7, 5.1 y 5.4 de la matriz.

## Documento original

* [Arquitectura de datos (PDF)](https://github.com/yimis-source/ProstaAIReal/blob/main/docs/docsf/1.3%20Ejecuci%C3%B3n/1.3.2.5%20Arquitectura%20de%20datos%20%28base%20de%20datos%29.pdf)
* [Resumen en Markdown del repositorio](https://github.com/yimis-source/ProstaAIReal/blob/main/docs/ejecucion/04_modelo_datos.md)
