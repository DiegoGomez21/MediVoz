# Configuracion Android Para MediVoz

## Dos rutas de prueba

### Expo Go

Expo Go permite abrir la app rapido en un telefono Android escaneando el QR de `npm start`. Es la ruta mas sencilla para validar interfaz, textos, accesibilidad visual y consumo del backend cuando el telefono y el equipo estan en la misma red.

Usa esta URL para el backend cuando pruebes en telefono fisico:

```text
EXPO_PUBLIC_API_URL=http://IP_DEL_EQUIPO:8000
```

Ejecuta FastAPI escuchando en todas las interfaces:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Android Studio y emulador

Android Studio con un Android Virtual Device es la ruta recomendada para pruebas reproducibles con agentes. Permite verificar comandos como `adb devices`, automatizar evidencia y evitar depender de un telefono fisico.

Requisitos:

- JDK 17 o superior disponible en `java -version`.
- Android Studio instalado.
- Android SDK Platform Tools instalado.
- Un AVD creado desde Device Manager.
- `adb` y `emulator` disponibles en `PATH`.

Usa esta URL para que el emulador acceda al backend del host:

```text
EXPO_PUBLIC_API_URL=http://10.0.2.2:8000
```

## Verificacion esperada

```bash
java -version
adb version
emulator -version
adb devices
```

En el entorno actual, Node y Python estan disponibles, pero Java, `adb` y `emulator` no aparecen en `PATH`. Esa instalacion queda como prerrequisito local antes de ejecutar QA Android completo desde OpenCode.

## Nota sobre Python en WSL

Si `python3 -m venv .venv` falla con un mensaje sobre `ensurepip`, instala el paquete del sistema `python3.12-venv` o usa `uv` para crear el entorno del backend:

```bash
cd backend
uv venv .venv
. .venv/bin/activate
uv pip install -r requirements-dev.txt
pytest -v
```
