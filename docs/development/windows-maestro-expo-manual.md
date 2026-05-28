# Manual Windows Para Expo Go, Maestro Y MediVoz Mobile

Este documento sirve como guia de traspaso para configurar la interfaz mobile de MediVoz en otro equipo Windows y para que el siguiente agente no repita los mismos diagnosticos.

## Objetivo

Levantar la app mobile Expo en Android Emulator, automatizarla con Maestro/MCP y distinguir rapidamente si un fallo viene del codigo, de Metro/Expo, del backend o del canal ADB/Maestro.

## Hallazgos De La Sesion

1. El appId de Expo Go usado por Maestro es `host.exp.exponent`.
2. El proyecto mobile esta en `mobile/`.
3. La app esperada muestra el texto `MediVoz MVP`.
4. Metro usa normalmente el puerto `8081`.
5. Para Android Emulator, el backend del host debe apuntarse como `http://10.0.2.2:8000`.
6. El backend FastAPI corre en `backend/` con `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`.
7. Se encontro un error real de Metro: `Unable to resolve module ./index`.
8. La causa del error de Metro era que faltaba el entrypoint `mobile/index.js`.
9. La correccion aplicada fue crear `mobile/index.js` con `registerRootComponent(App)`.
10. Despues de la correccion, el bundle Android respondio `HTTP 200` y `npm run check:js-only` paso.
11. El fallo restante fue ambiental: ADB/Maestro devolvio `protocol fault (couldn't read status): Connection reset by peer` y Maestro devolvio `UNAVAILABLE: End of stream or IOException`.
12. La causa probable del fallo restante es un canal ADB roto entre Windows/WSL/emulador, no un error confirmado del codigo mobile.

## Recomendacion Principal

Configurar todo el circuito mobile en el mismo lado del sistema operativo.

Ruta recomendada: Windows nativo para Android Studio, ADB, Expo, Node, backend y Maestro/MCP.

Ruta a evitar si es posible: emulador en Windows, agente en WSL y ADB reenviado con proxy. Esa combinacion fue la que produjo errores de canal ADB durante la sesion.

Este manual asume Expo Go. Si mas adelante se usa dev build o APK standalone, el `appId` de Maestro dejara de ser `host.exp.exponent` y pasara a ser el package Android de la app, actualmente `com.medivoz.app` en `mobile/app.json`.

## Prerrequisitos En Windows

Instalar en Windows nativo y verificar desde PowerShell, no desde WSL:

```powershell
where.exe git
where.exe node
where.exe npm
git --version
node --version
npm --version
py --version
```

Versiones recomendadas:

```text
Node.js LTS 20 o superior
npm incluido con Node LTS
Python 3.12 o compatible
Java 17 o superior para Maestro
Android Studio actual con SDK Platform Tools
Maestro CLI actual
```

Instalar Android Studio y, desde SDK Manager, asegurar:

```text
Android SDK Platform Tools
Android Emulator
Una imagen de sistema Android para el AVD
```

Agregar al `PATH` de Windows si no estan disponibles:

```text
%LOCALAPPDATA%\Android\Sdk\platform-tools
%LOCALAPPDATA%\Android\Sdk\emulator
```

Verificar ADB:

```powershell
where.exe adb
adb version
adb devices
```

## Instalar Maestro CLI En Windows

Maestro necesita Java 17 o superior.

```powershell
java -version
```

Instalacion recomendada por la documentacion oficial:

1. Descargar `maestro.zip` desde `https://github.com/mobile-dev-inc/maestro/releases/latest/download/maestro.zip`.
2. Extraerlo en una ruta estable, por ejemplo `C:\maestro`.
3. Agregar `C:\maestro\bin` al `PATH`.
4. Reiniciar la terminal.

Verificar:

```powershell
maestro --help
```

## Configurar Maestro MCP

Maestro MCP corre como servidor local `stdio`. La configuracion exacta depende del agente, pero la forma base es:

```json
{
  "mcpServers": {
    "maestro": {
      "command": "maestro",
      "args": ["mcp"]
    }
  }
}
```

Si `maestro` no esta en `PATH`, usar la ruta completa del binario.

Para Claude Desktop en Windows, el archivo suele estar en:

```text
%APPDATA%\Claude\claude_desktop_config.json
```

En ese caso conviene declarar tambien `JAVA_HOME`, porque Claude Desktop puede iniciar con un entorno minimo:

```json
{
  "mcpServers": {
    "maestro": {
      "command": "C:\\maestro\\bin\\maestro.bat",
      "args": ["mcp"],
      "env": {
        "JAVA_HOME": "C:\\Program Files\\Java\\jdk-17"
      }
    }
  }
}
```

Despues de cambiar la configuracion MCP, reiniciar el agente. La verificacion minima es que el tool `maestro_list_devices` devuelva `emulator-5554` conectado o el id real del dispositivo.

## Instalacion Del Proyecto

Clonar o ubicar el repo en una ruta Windows, por ejemplo:

```powershell
cd C:\dev
git clone <URL_DEL_REPO> tg_aplication
cd tg_aplication
git status --short
```

Si el repo ya existe, confirmar que no se esta dentro de WSL:

```powershell
pwd
where.exe adb
where.exe node
```

Desde la raiz del repo:

```powershell
cd mobile
npm ci
npm run check:js-only
npm run lint
```

Si `npm ci` falla por diferencias de lockfile, revisar primero `mobile/package-lock.json`. En esta sesion el archivo ya aparecia modificado antes de tocarlo, asi que no revertir cambios ajenos sin confirmacion.

## Verificar El Entrypoint Expo

Antes de levantar Expo, verificar que exista:

```powershell
Test-Path .\mobile\index.js
```

El contenido esperado es:

```js
import { registerRootComponent } from "expo";

import App from "./App";

registerRootComponent(App);
```

Si este archivo falta, Metro puede fallar con:

```text
Unable to resolve module ./index
```

Aunque `mobile/package.json` declare `"main": "expo/AppEntry.js"`, en esta sesion Metro resolvio el bundle Android como `./index`. Mantener `mobile/index.js` es una correccion estandar y compatible con Expo porque registra el mismo `App.jsx` como componente raiz.

## Levantar Backend

Desde la raiz del repo:

```powershell
cd backend
py -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Si `requirements-dev.txt` no esta disponible en el entorno clonado, usar temporalmente:

```powershell
pip install -r requirements.txt
```

Verificar salud del backend:

```powershell
curl.exe http://127.0.0.1:8000/health
```

La app mobile usa por defecto `http://10.0.2.2:8000` para que el emulador Android pueda llegar al backend del host.

## Levantar Android Emulator

Desde Android Studio:

1. Abrir Device Manager.
2. Crear o iniciar un AVD.
3. Esperar hasta que Android termine de arrancar.

Validar desde PowerShell:

```powershell
adb kill-server
taskkill /F /IM adb.exe
adb start-server
adb devices
```

Resultado esperado:

```text
emulator-5554    device
```

Si aparece `offline`, reiniciar el AVD y volver a ejecutar `adb kill-server` y `adb start-server`.

Verificar si Expo Go esta instalado:

```powershell
adb shell pm list packages | findstr host.exp.exponent
```

Si no aparece, usar un AVD con Play Store e instalar Expo Go desde Play Store, o ejecutar `npx expo start --android` para que Expo CLI intente instalarlo automaticamente.

## Levantar Expo

Opcion recomendada, una sola terminal desde `mobile/`:

```powershell
npx expo start --android --clear
```

Opcion alternativa, tambien desde `mobile/`:

```powershell
npx expo start --clear
```

Cuando aparezca el menu de Expo, presionar `a` para abrir Android. No ejecutar dos servidores Expo para el mismo proyecto.

Si Expo indica que el puerto `8081` ya esta ocupado por la misma app, no iniciar otro servidor. Usar el servidor existente o cerrar el proceso viejo.

Para encontrar el proceso en Windows:

```powershell
netstat -ano | findstr :8081
```

Para cerrarlo si esta obsoleto:

```powershell
taskkill /PID <PID> /F
```

## Verificar Metro Antes De Maestro

Esta verificacion separa errores de bundle de errores de Maestro/ADB.

Con Expo corriendo:

```powershell
curl.exe -o NUL -w "%{http_code}" "http://127.0.0.1:8081/index.bundle?platform=android&dev=true&minify=false"
```

Resultado esperado:

```text
200
```

Si devuelve JSON con `Unable to resolve module ./index`, revisar `mobile/index.js`.

Si devuelve otro error de Metro, resolverlo antes de probar Maestro. Maestro no puede validar una app cuyo bundle no compila.

Tambien se puede verificar la conectividad del emulador hacia el backend:

```powershell
adb shell am start -a android.intent.action.VIEW -d http://10.0.2.2:8000/health
```

Si el navegador del emulador no puede abrir esa URL, el problema esta en backend, firewall o red, no en la UI React Native.

## Flujos Maestro/MCP

Primero validar que Expo Go abre:

```yaml
appId: host.exp.exponent
---
- launchApp
- waitForAnimationToEnd
- assertVisible: Expo Go
```

Luego abrir el proyecto Expo por deep link:

```yaml
appId: host.exp.exponent
---
- openLink: exp://10.0.2.2:8081
- waitForAnimationToEnd
- assertVisible: MediVoz MVP
```

Si el texto todavia no aparece, inspeccionar si Expo Go esta mostrando una pantalla de carga, error de bundle o error de red.

## Diagnostico Por Capas

Usar este orden para no mezclar causas:

1. `npm run check:js-only` y `npm run lint` fallan: problema de codigo mobile.
2. `curl.exe ... index.bundle` no devuelve `200`: problema de Metro/Expo/entrypoint.
3. Bundle devuelve `200`, pero la UI muestra `Backend no disponible`: problema de backend, URL o red.
4. Bundle devuelve `200`, pero Maestro no puede inspeccionar pantalla: problema de ADB/Maestro/emulador.
5. `adb devices` no muestra `device`: problema de Android SDK, ADB o AVD.

## Errores Conocidos Y Correcciones

### Metro: Unable To Resolve Module ./index

Sintoma:

```text
Unable to resolve module ./index from .../mobile/.
```

Causa probable:

```text
Falta mobile/index.js o Expo esta resolviendo un entrypoint diferente al esperado.
```

Correccion:

```js
import { registerRootComponent } from "expo";

import App from "./App";

registerRootComponent(App);
```

Verificacion:

```powershell
curl.exe -o NUL -w "%{http_code}" "http://127.0.0.1:8081/index.bundle?platform=android&dev=true&minify=false"
```

Debe responder `200`.

### ADB: protocol fault Connection Reset By Peer

Sintoma:

```text
adb: failed to check server version: protocol fault (couldn't read status): Connection reset by peer
```

Causa probable:

```text
Servidor ADB roto, conflicto entre adb.exe y adb en WSL, proxy ADB caido o AVD en estado inconsistente.
```

Correccion recomendada en Windows nativo:

```powershell
adb kill-server
taskkill /F /IM adb.exe
adb start-server
adb devices
```

Si sigue fallando:

1. Cerrar el AVD desde Android Studio.
2. Cerrar Android Studio.
3. Abrir Android Studio de nuevo.
4. Iniciar el AVD.
5. Ejecutar `adb devices`.

Si se insiste en usar WSL con emulador Windows, verificar que el proxy ADB apunte al host correcto. En esta sesion se uso un proxy similar a:

```bash
python3 ~/.local/bin/adb-server-proxy 5037 172.20.112.1 5037
```

Pero esta ruta no fue estable. Preferir Windows nativo para el flujo completo.

### Maestro: UNAVAILABLE End Of Stream Or IOException

Sintoma:

```text
io.grpc.StatusRuntimeException: UNAVAILABLE: End of stream or IOException
```

Causa probable:

```text
Maestro no puede leer la jerarquia de pantalla porque ADB o el driver Android esta cortando la conexion.
```

Correccion:

1. Confirmar `adb devices`.
2. Confirmar que el AVD esta desbloqueado y visible.
3. Reiniciar ADB.
4. Reiniciar el AVD si Maestro sigue sin inspeccionar.
5. Reintentar el YAML minimo de `assertVisible: Expo Go`.

### UI: Backend No Disponible

Sintoma:

```text
Backend no disponible
```

Causa probable:

```text
FastAPI no esta corriendo, el puerto 8000 no esta accesible o la URL del mobile no apunta a 10.0.2.2 desde el emulador.
```

Correccion:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
curl.exe http://127.0.0.1:8000/health
```

Si Windows Firewall pregunta por permisos de Python, permitir acceso en redes privadas.

## Checklist Para El Siguiente Agente

Ejecutar en este orden:

```powershell
git status --short
cd mobile
npm ci
npm run check:js-only
npm run lint
Test-Path .\index.js
npx expo start --android --clear
```

Con Expo ya levantado:

```powershell
curl.exe -o NUL -w "%{http_code}" "http://127.0.0.1:8081/index.bundle?platform=android&dev=true&minify=false"
adb devices
```

Luego usar MCP Maestro:

```yaml
appId: host.exp.exponent
---
- launchApp
- waitForAnimationToEnd
- assertVisible: Expo Go
```

Y despues:

```yaml
appId: host.exp.exponent
---
- openLink: exp://10.0.2.2:8081
- waitForAnimationToEnd
- assertVisible: MediVoz MVP
```

## Regla De Oro

No corregir a ciegas la app si Metro ya responde `200` y las verificaciones JS pasan. En ese caso, los errores de Maestro como timeout, `UNAVAILABLE` o `protocol fault` casi siempre pertenecen a ADB, al emulador o al puente Windows/WSL.

## Cambios De Worktree Observados

Durante esta sesion habia cambios no relacionados en el worktree. No revertirlos sin confirmacion del usuario.

Cambio relevante hecho para mobile:

```text
mobile/index.js
```

Ese archivo es necesario para evitar el error de Metro `Unable to resolve module ./index`.
