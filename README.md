# MediVoz

MediVoz es el MVP de una aplicación móvil para gestión de medicamentos con interfaz accesible, recordatorios, inventario y asistencia por voz en fases posteriores.

## Estructura

- `backend/`: API FastAPI, persistencia SQLite y pruebas automatizadas.
- `mobile/`: app React Native con Expo en JavaScript y estructura MVVM.
- `docs/`: guías técnicas y decisiones de arquitectura.

## Guía de instalación y ejecución

Backend:

```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Si `python3 -m venv` falla por falta de `ensurepip`/`python3.12-venv`, usa `uv`:

```bash
cd backend
uv venv .venv
. .venv/bin/activate
uv pip install -r requirements-dev.txt
pytest -v
```

Mobile:

```bash
cd mobile
npm install
npm start
```

Para emulador Android, usa `EXPO_PUBLIC_API_URL=http://10.0.2.2:8000`. Para teléfono físico, usa la IP LAN del equipo que ejecuta el backend.
