# Backend MediVoz

API FastAPI para el MVP de MediVoz.

## Preparacion

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
```

En entornos donde falte `ensurepip` o el paquete del sistema `python3.12-venv`, se puede crear el entorno con `uv`:

```bash
uv venv .venv
. .venv/bin/activate
uv pip install -r requirements-dev.txt
```

## Ejecucion

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Pruebas

```bash
pytest
```

## Endpoint inicial

- `GET /health`: verifica que la API esta disponible para la app Expo.

## Endpoints Sprint 1

Medicamentos:

- `POST /medications`
- `GET /medications`
- `GET /medications/{medication_id}`
- `PATCH /medications/{medication_id}`
- `DELETE /medications/{medication_id}`

Recordatorios/alarmas basicas:

- `POST /reminders`
- `GET /reminders`
- `GET /reminders/today`
- `GET /reminders/{reminder_id}`
- `PATCH /reminders/{reminder_id}`
- `DELETE /reminders/{reminder_id}`
- `POST /reminders/{reminder_id}/taken`

La persistencia usa SQLite con SQLAlchemy. Por defecto la API crea `medivoz.db` en el directorio desde el que se ejecuta `uvicorn`.
