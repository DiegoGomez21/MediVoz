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
