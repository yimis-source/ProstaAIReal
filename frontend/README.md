# Frontend de Prosta-AI

Interfaz web (React 18 + Vite + react-router-dom 6) del proyecto académico Prosta-AI. Uso académico, no diagnóstico: todas las pantallas muestran el aviso de uso no diagnóstico.

## Requisitos

- Node.js 20 o superior y npm.
- La API corriendo en `http://localhost:8000` (rutas bajo `/api`).

## Instalar

```bash
cd frontend
npm install
```

## Desarrollo

```bash
npm run dev
```

Abre `http://localhost:5173`. Vite envía las peticiones a `/api` hacia `http://localhost:8000`. El indicador del encabezado consulta `GET /api/salud` y muestra si la API responde.

## Compilar

```bash
npm run build     # genera dist/
npm run preview   # sirve dist/ para revisarlo
```

## Rutas (ciclo 6)

| Ruta | Pantalla |
|---|---|
| `/` | CU00 Inicio |
| `/acceso` | CU01 Acceso básico |
| `/cargar` | CU02 Cargar estudio |
| `/estudios/:id/estado` | CU03 Estado del procesamiento |
| `/estudios/:id/roi` | CU04 ROI con panel «¿Qué estoy viendo?» |
