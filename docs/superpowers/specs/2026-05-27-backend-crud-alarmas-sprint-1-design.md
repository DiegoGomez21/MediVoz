# Backend CRUD de alarmas Sprint 1 - Diseno

## Objetivo

Implementar el backend FastAPI del Sprint 1 minimo de MediVoz para registrar medicamentos, crear recordatorios/alarmas basicas y confirmar tomas. El alcance responde al MVP descrito en el trabajo de grado: planificacion del suministro de medicamentos, recordatorios y seguimiento terapeutico inicial.

## Contexto verificado

- El proyecto es MediVoz, una aplicacion movil Expo + FastAPI + SQLite orientada a pacientes y cuidadores.
- El backend actual solo expone `GET /health`.
- La documentacion existente define que el backend FastAPI se organizara por modulos funcionales.
- La documentacion previa de Sprint 1 propone las entidades `Medication`, `Reminder` y `DoseLog`.
- El usuario aprobo el alcance `Sprint 1 minimo` y eligio SQLAlchemy para persistencia.

## Alcance aprobado

Incluido:

- CRUD de medicamentos.
- CRUD de recordatorios/alarmas basicas.
- Consulta de recordatorios del dia.
- Registro de toma realizada.
- Persistencia en SQLite usando SQLAlchemy.
- Pruebas automatizadas con `pytest` y `TestClient`.

Fuera de alcance para este sprint:

- Autenticacion.
- Multiples pacientes complejos.
- Inventario de medicamentos.
- Voz STT/TTS o NLP.
- Configuracion avanzada de alarmas: sonido, voz, vibracion, repeticion por dias o segundo plano.
- Reportes.

## Alternativas consideradas

### SQLite sin ORM

Ventajas: menos dependencias y estructura mas simple.

Riesgos: mas codigo manual para relaciones, pruebas y evolucion futura.

### SQLAlchemy

Ventajas: relaciones explicitas, integridad referencial, sesiones por request y mejor base para ampliar el MVP.

Riesgos: agrega dependencia y requiere una estructura minima de base de datos.

Decision: usar SQLAlchemy porque el usuario lo prefirio y el dominio crecera hacia inventario, pacientes y reportes.

### Memoria temporal

Ventajas: prototipo rapido.

Riesgos: los datos se pierden al reiniciar y no cumple bien la persistencia esperada del MVP.

## Arquitectura

El backend mantendra FastAPI modular:

- `app/main.py`: configura la app, CORS, creacion inicial de tablas e inclusion de routers.
- `app/database.py`: engine SQLAlchemy, `SessionLocal`, base declarativa y dependencia de sesion.
- `app/modules/medications/`: router, schemas, service y repository para medicamentos.
- `app/modules/reminders/`: router, schemas, service y repository para recordatorios y tomas.

El modulo `health` se mantiene intacto.

## Modelo de datos

`Medication`:

- `id`: entero autoincremental.
- `name`: nombre del medicamento.
- `dose_label`: etiqueta de dosis visible para el usuario, por ejemplo `500 mg`.
- `created_at`: fecha de creacion.
- `updated_at`: fecha de ultima actualizacion.

`Reminder`:

- `id`: entero autoincremental.
- `medication_id`: referencia a `Medication`.
- `time_of_day`: hora en formato `HH:MM`.
- `is_active`: indica si el recordatorio esta activo.
- `created_at`: fecha de creacion.
- `updated_at`: fecha de ultima actualizacion.

`DoseLog`:

- `id`: entero autoincremental.
- `reminder_id`: referencia a `Reminder`.
- `status`: estado de la toma. En Sprint 1 solo se usara `taken`.
- `taken_at`: fecha y hora en que se confirma la toma.
- `created_at`: fecha de creacion.

## Contratos HTTP

Medicamentos:

- `POST /medications`: crea un medicamento.
- `GET /medications`: lista medicamentos.
- `GET /medications/{medication_id}`: obtiene un medicamento.
- `PATCH /medications/{medication_id}`: actualiza parcialmente un medicamento.
- `DELETE /medications/{medication_id}`: elimina un medicamento.

Recordatorios:

- `POST /reminders`: crea un recordatorio asociado a un medicamento existente.
- `GET /reminders`: lista recordatorios.
- `GET /reminders/today`: lista recordatorios activos del dia, ordenados por hora.
- `GET /reminders/{reminder_id}`: obtiene un recordatorio.
- `PATCH /reminders/{reminder_id}`: actualiza parcialmente un recordatorio.
- `DELETE /reminders/{reminder_id}`: elimina un recordatorio.
- `POST /reminders/{reminder_id}/taken`: registra una toma realizada.

## Reglas de negocio

- `name` y `dose_label` no pueden estar vacios.
- `time_of_day` debe cumplir formato `HH:MM` de 24 horas.
- Un recordatorio solo puede crearse para un medicamento existente.
- Registrar una toma requiere que el recordatorio exista.
- `GET /reminders/today` retorna los recordatorios activos; no calcula recurrencias avanzadas porque estan fuera de alcance.
- El borrado sera fisico para mantener el MVP simple.

## Manejo de errores

- `404 Not Found`: medicamento o recordatorio inexistente.
- `400 Bad Request`: hora invalida, campos vacios o relacion invalida.
- Las respuestas usaran los mecanismos estandar de `HTTPException` de FastAPI.

## Flujo principal

1. La app movil crea un medicamento con nombre y dosis.
2. La app crea un recordatorio asociado al medicamento.
3. La app consulta `/reminders/today` para mostrar la proxima toma.
4. El usuario confirma la toma desde la app.
5. La app llama `POST /reminders/{reminder_id}/taken`.
6. El backend crea un `DoseLog` con estado `taken`.

## Pruebas

Se ampliara la suite con pruebas de integracion HTTP usando `pytest` y `TestClient`.

Casos minimos:

- `GET /health` sigue funcionando.
- CRUD completo de medicamentos.
- CRUD completo de recordatorios.
- No se puede crear un recordatorio con medicamento inexistente.
- No se puede crear o actualizar un recordatorio con `time_of_day` invalido.
- `GET /reminders/today` retorna recordatorios activos ordenados por hora.
- `POST /reminders/{reminder_id}/taken` crea un registro de toma.

Las pruebas deben usar una base SQLite temporal para evitar contaminar datos locales.

## Criterios de aceptacion

- La API arranca con FastAPI y crea las tablas necesarias en SQLite.
- Los endpoints de medicamentos y recordatorios responden con JSON validado por schemas.
- Los errores principales devuelven codigos HTTP esperados.
- La suite `pytest` pasa completa.
- El README del backend queda actualizado si se agregan dependencias o comandos relevantes.

## Revision interna

- No quedan marcadores incompletos ni decisiones abiertas.
- El alcance esta limitado al Sprint 1 minimo aprobado.
- La eleccion de SQLAlchemy es consistente con la preferencia del usuario.
- El diseno no introduce inventario, voz, pacientes multiples ni configuracion avanzada de alarmas.
- Los contratos HTTP coinciden con la documentacion previa de Sprint 1 y agregan CRUD completo solicitado para el backend.
