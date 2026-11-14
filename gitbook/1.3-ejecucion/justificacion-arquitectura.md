# Justificación de la arquitectura de software

Documenta las decisiones arquitectónicas según el estándar IEEE 1471 y el enfoque «Vistas y más allá» del SEI.

## Ficha

| Campo | Detalle |
|---|---|
| Paquete EDT | 1.3.2.4 |
| Fecha y versión | 24/10/2026 |
| Autores | Yeison Bolaños Ruiz, Juan David Riascos Erazo, Sergio Gabriel Meneses Silva, Yimis Buenaventura y Fernando José Angulo Núñez |
| Formato | PDF |

## Contenido principal

* **Complementa** la [arquitectura de software](arquitectura-de-software.md): referencia sus figuras y tablas sin repetirlas.
* **Vistas documentadas:** lógica de componentes y escenarios de casos de uso (prioridad 1), y despliegue mínimo viable (prioridad 2); la vista de ejecución se integra en la lógica y la de código se difiere al diseño técnico.
* **Identificación y decisiones:** tabla de identificación del documento y decisiones con sus razones y alternativas descartadas.
* **Decisiones registradas:** DEC-01 (identificación en el primer acceso, compatible con la ausencia de registro de cuentas) y DEC-02 (el procesamiento inicia con «Procesar»).
* **Observación abierta:** el SRS programa casi todas las pruebas funcionales en el Ciclo 6, pero el plan de calidad exige verificar flujo y privacidad en cada integración; se propone adelantar controles a los ciclos 2 y 3.
* **Uso de los requisitos:** emplea la numeración del SRS (RF, RU, RR, RB, RC, RN y RA).

## Documento original

* [Justificación de la arquitectura (PDF)](https://github.com/yimis-source/ProstaAIReal/tree/main/docs) — `docs/docsf/1.3 Ejecución/1.3.2.4 Arquitectura de software - Justificación.pdf`
* [Resumen en Markdown del repositorio](https://github.com/yimis-source/ProstaAIReal/tree/main/docs) — `docs/ejecucion/02_arquitectura.md`
