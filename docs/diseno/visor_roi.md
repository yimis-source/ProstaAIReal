# Diseño del visor de la ROI, versión 1

| Campo | Valor |
|---|---|
| Tarea | 1502 |
| Responsable | Sergio Gabriel Meneses Silva (Diseñador) |
| Fecha | 07/11/2026 |
| Versión | 1.0 (la versión final es la del 09/11/2026) |

Uso académico y experimental; el visor no es una herramienta diagnóstica.

## 1. Propósito

Mostrar la ROI (región de interés: la próstata segmentada por el modelo) sobre un corte axial de la imagen T2 para que el usuario vea qué marcó el modelo. Parte del caso de uso CU04 (ROI).

## 2. Superposición de la ROI

| Elemento | Decisión |
|---|---|
| Color de la ROI | verde azulado `#2dd4bf` |
| Alfa de la máscara | 0,45 |
| Opacidad | ajustable por el usuario con un deslizador (0 % = solo imagen, 100 % = ROI opaca); el valor por defecto es el alfa 0,45 |
| Base | corte axial en escala de grises, normalizado entre los percentiles 1 y 99 |
| Corte inicial | el de mayor área de ROI; sin ROI, el central |

Se eligió el verde azulado porque no se confunde con los grises de la imagen ni con el rojo y amarillo que suelen sugerir alarma.

## 3. Vista con y sin ROI

Dos paneles lado a lado con el mismo corte, el mismo zoom y la misma posición: a la izquierda la imagen sola; a la derecha la imagen con la ROI. Al mover el corte o el zoom, ambos se mueven juntos. Esto permite comparar sin que la ROI tape la anatomía.

## 4. Controles de corte y zoom (se implementan en el ciclo 6)

- **Corte:** deslizador y flechas del teclado (arriba/abajo) con el número de corte visible («Corte 12 de 20»).
- **Zoom:** botones + y −, rueda del ratón con Ctrl y botón «Ajustar» para volver al encuadre completo; desplazamiento arrastrando.
- **Opacidad:** deslizador de 0 a 100 %.
- **Mostrar/ocultar ROI:** interruptor.
En el ciclo 4 solo se genera una imagen estática del corte; los controles son diseño para el ciclo 6.

## 5. Contraste y accesibilidad

- La ROI no es el único canal: el modo con y sin ROI evita depender solo del color.
- Controles operables con teclado, con foco visible y etiquetas de texto.
- Texto del visor con contraste suficiente sobre fondo oscuro (blanco sobre casi negro).
- Tamaños de control tocables (al menos 40 px).
- No se usan imágenes de pacientes en el diseño ni en los ejemplos de la documentación.

## 6. Pendiente en la versión final

La ubicación del aviso experimental y el boceto de la composición se definen el 09/11/2026.
