# Diseño del visor de la ROI, versión final

| Campo | Valor |
|---|---|
| Tarea | 1502 |
| Responsable | Sergio Gabriel Meneses Silva (Diseñador) |
| Fecha | 09/11/2026 (versión 1 del 07/11/2026) |
| Versión | 2.0 |

Uso académico y experimental; el visor no es una herramienta diagnóstica. Referencia visual: `docs/ejecucion/assets/pantallas/cu04_roi.svg` (pantalla de ROI del CU04).

## 1. Propósito

Mostrar la ROI (región de interés: la próstata segmentada por el modelo) sobre un corte axial de la imagen T2, y poder exportar esa imagen siempre con el aviso experimental (RF-15).

## 2. Superposición de la ROI

| Elemento | Decisión |
|---|---|
| Color de la ROI | verde azulado `#2dd4bf` |
| Alfa de la máscara | 0,45 |
| Opacidad | ajustable con un deslizador; por defecto 0,45 |
| Base | corte axial en gris, normalizado entre percentiles 1 y 99 |
| Corte inicial | el de mayor área de ROI; sin ROI, el central |

Estos valores son los que implementa `backend/prosta_ai/pipeline/visualizacion.py` (`COLOR_ROI`, `ALFA_ROI`).

## 3. Vista con y sin ROI

Dos paneles lado a lado con el mismo corte, zoom y posición: imagen sola a la izquierda, imagen con ROI a la derecha, sincronizados.

## 4. Controles de corte y zoom (ciclo 6)

- Corte: deslizador y flechas del teclado, con «Corte N de M».
- Zoom: botones + y −, Ctrl + rueda, botón «Ajustar», arrastrar para desplazar.
- Opacidad 0–100 % y interruptor para mostrar u ocultar la ROI.
En el ciclo 4 solo se genera la imagen estática exportada (`scripts/generar_roi.py`).

## 5. Contraste y accesibilidad

- No depender solo del color: existe la vista sin ROI y el interruptor.
- Controles con teclado, foco visible y etiquetas de texto.
- Texto blanco sobre fondo casi negro (`#141414` en la banda del aviso).
- Controles de al menos 40 px.
- Sin imágenes de pacientes en documentación ni ejemplos.

## 6. Aviso experimental en la imagen exportada

- **Ubicación:** banda inferior, impresa **dentro de la propia imagen** (no como etiqueta HTML ni metadato), para que acompañe a la imagen si se copia o se envía.
- **Texto:** el de `AVISO_EXPERIMENTAL` en `backend/prosta_ai/constantes.py`, sin modificarlo:
  «Resultado experimental con fines académicos. No es un diagnóstico ni sustituye la valoración de un profesional de la salud.»
- **Ancho mínimo:** 512 px; si el corte es más estrecho, se amplía con un factor entero antes de añadir la banda.
- **Fuente:** DejaVu Sans (incluida en `backend/prosta_ai/recursos/`) por sus tildes y eñes; tamaño proporcional al ancho (mínimo 12 px), texto blanco sobre fondo `#141414`, con salto de línea para que no se corte.
- Toda imagen exportada pasa por `renderizador_exportacion()`, de modo que no se puede exportar sin el aviso.

## 7. Boceto de la composición (imagen exportada)

```
+--------------------------------------------------+  ^
|                                                  |  |
|            corte axial, escala de grises         |  |
|                                                  |  | imagen
|              .-~~~~~~~~-.                        |  | (>= 512 px
|             /  ROI verde \   <- #2dd4bf, alfa    |  |  de ancho)
|             \  azulado   /      0,45             |  |
|              `-.______.-'                        |  |
|                                                  |  |
+--------------------------------------------------+  v
| Resultado experimental con fines académicos. No  |  ^ banda del aviso
| es un diagnóstico ni sustituye la valoración de  |  | (#141414, texto
| un profesional de la salud.                      |  v  blanco)
+--------------------------------------------------+
```

Pantalla del visor (ciclo 6), según `cu04_roi.svg`: la imagen con ROI a la izquierda; a la derecha los controles y el panel «¿Qué estoy viendo?» (`docs/diseno/texto_roi.md`); el aviso visible en la pantalla y también impreso en lo que se exporta.
