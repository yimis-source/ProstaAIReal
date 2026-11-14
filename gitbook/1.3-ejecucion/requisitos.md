# Requisitos funcionales y no funcionales (ISO/IEC/IEEE 29148)

Especificación de requisitos de software (SRS) del Entregable 1: define qué debe hacer Prosta-AI y bajo qué condiciones, con prioridad y método de verificación.

## Ficha

| Campo | Detalle |
|---|---|
| Paquete EDT | 1.3.1.1 |
| Fecha y versión | Octubre de 2026, versión 1.0 (sujeta a aprobación del propietario en el hito H002) |
| Autores | Yimis Buenaventura, Juan David Riascos Erazo, Sergio Gabriel Meneses Silva, Yeison Bolaños Ruiz y Fernando José Angulo Núñez |
| Formato | PDF |

## Contenido principal

* **Alcance del documento:** 39 requisitos con ID único, prioridad MoSCoW, origen en la matriz de trazabilidad, caso de uso y método de verificación (prueba, inspección, demostración o análisis).
* **Funcionales (RF-01 a RF-24):** acceso básico, carga y validación de estudios (máximo 50 MB por archivo y 150 MB por estudio), eliminación de metadatos identificables, flujo automático, segmentación 3D, ROI superpuesta, aviso experimental, panel de explicación, registro y consulta de estudios, asistente opcional y métricas Dice e IoU.
* **No funcionales:** usabilidad (RU-01), rendimiento de 2 minutos o menos por estudio (RR-01), base de datos sin datos personales (RB-01 y RB-02), restricciones de diseño (RC-01 a RC-06), normas (RN-01 a RN-03) y atributos de reproducibilidad y trazabilidad (RA-01 y RA-02).
* **Formatos admitidos:** DICOM y NIfTI.
* **Decisiones vigentes:** no hay registro de cuentas; quien entra por primera vez confirma una contraseña con su alias; el procesamiento comienza al pulsar «Procesar»; Google Colab se usa solo para entrenar y probar durante el desarrollo.
* **Exclusiones (Won't):** uso clínico, validación médica, datos de pacientes reales, certificación sanitaria, agentes autónomos, producción de alta disponibilidad y aplicación móvil.
* **Trazabilidad:** cada necesidad N1 a N8 del Acta se relaciona con sus requisitos (por ejemplo, N4 con RF-15, RF-16, RF-17 y RN-02).
* **Relación con otros documentos:** [casos de uso](casos-de-uso.md), [matriz de trazabilidad](matriz-de-trazabilidad.md) y [arquitectura de software](arquitectura-de-software.md).
* **Dos numeraciones:** la matriz usa 1.1 a 6.5 y el SRS usa RF, RU, RR, RB, RC, RN y RA.

## Documento original

* [SRS, requisitos (PDF)](https://github.com/yimis-source/ProstaAIReal/tree/main/docs) — `docs/docsf/1.3 Ejecución/1.3.1.1 Requerimientos funcionales y no funcionales (ISO 29148).pdf`
* [Resumen en Markdown del repositorio](https://github.com/yimis-source/ProstaAIReal/tree/main/docs) — `docs/ejecucion/01_requisitos.md`
