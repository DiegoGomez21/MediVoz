# Mobile MediVoz

Aplicacion React Native con Expo para Android.

## Preparacion

```bash
npm install
```

## Ejecucion

```bash
npm start
```

Para abrir en emulador Android:

```bash
npm run android
```

## Configuracion de API

Copia `.env.example` si necesitas cambiar la URL del backend:

```text
EXPO_PUBLIC_API_URL=http://10.0.2.2:8000
```

- Emulador Android: `http://10.0.2.2:8000`.
- Telefono fisico: `http://IP_DEL_EQUIPO:8000` con FastAPI en `--host 0.0.0.0`.

## Estructura MVVM inicial

- `src/features/health/HealthScreen.jsx`: vista accesible.
- `src/features/health/useHealthViewModel.js`: estado de presentacion y acciones.
- `src/features/health/healthService.js`: contrato con la API.
- `src/api/client.js`: cliente HTTP compartido.

## Verificacion JavaScript

```bash
npm run check:js-only
npm run lint
```

`check:js-only` confirma que el frontend no conserva archivos, configuracion o dependencias directas de TypeScript.
