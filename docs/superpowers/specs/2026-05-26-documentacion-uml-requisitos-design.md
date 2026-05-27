# Documentacion UML, requisitos e historias de usuario - Diseno

## Objetivo

Crear una base documental para MediVoz que permita avanzar en requisitos, historias de usuario, arquitectura y diagramas UML sin desconectar la documentacion del codigo, ClickUp ni los sprints del MVP.

## Decision de enfoque

El enfoque recomendado es usar Markdown versionable en Git como fuente principal de verdad, apoyado por Obsidian como entorno de navegacion y Excalidraw como herramienta complementaria para diagramas visuales.

La documentacion formal debe vivir en `docs/` porque ya es el espacio del proyecto para guias tecnicas, arquitectura y decisiones. Obsidian puede abrir esa carpeta como vault sin duplicar contenido. Mermaid debe ser la primera opcion para UML y diagramas tecnicos porque queda dentro de archivos Markdown revisables por humanos y agentes. Excalidraw se reserva para bocetos, explicaciones visuales, presentaciones o diagramas que necesiten libertad grafica.

## Alternativas consideradas

### Solo Obsidian + Mermaid

Ventajas: simple, versionable, facil de revisar en Git, compatible con agentes y suficiente para UML inicial.

Riesgos: menos comodo para diagramas altamente visuales o presentaciones.

### Obsidian + Excalidraw como fuente principal

Ventajas: excelente experiencia visual y edicion manual fluida.

Riesgos: peor trazabilidad textual, mas dificil de automatizar y revisar en diffs.

### PlantUML + Markdown

Ventajas: UML mas formal y expresivo.

Riesgos: agrega dependencia de Java/PlantUML y complejidad de instalacion. Java todavia no esta disponible en el entorno actual.

## Estructura documental propuesta

```text
docs/
  product/
    vision.md
    stakeholders.md
    glossary.md
  requirements/
    functional-requirements.md
    non-functional-requirements.md
    user-stories.md
    acceptance-criteria.md
  architecture/
    context.md
    containers.md
    components.md
    data-model.md
    mvvm.md
    decisions/
  diagrams/
    uml/
      use-case.md
      class-domain.md
      sequence-reminder.md
      activity-reminder.md
      component-architecture.md
    excalidraw/
  sprints/
    sprint-0.md
    sprint-1-reminder.md
```

## Diagramas UML iniciales

### Casos de uso

Debe mostrar actores y capacidades principales: paciente, cuidador, registro de medicamento, programacion de recordatorio, confirmacion de toma, consulta de inventario, seguimiento terapeutico y uso de voz.

### Modelo de dominio

Debe iniciar con el alcance de Sprint 1: `Medication`, `Reminder` y `DoseLog`. Luego puede ampliarse con `Patient`, `Caregiver`, `InventoryItem`, `VoiceCommand` y entidades de reportes.

### Secuencia del recordatorio basico

Debe representar el flujo app movil -> FastAPI -> SQLite -> respuesta al movil, incluyendo el registro de medicamento, consulta del proximo recordatorio y marcado de toma.

### Actividad de confirmacion de toma

Debe mostrar el proceso desde recibir/ver recordatorio hasta confirmar, omitir o registrar estado de la toma.

### Componentes de arquitectura MVVM

Debe explicar como se conectan vistas Expo, hooks ViewModel, servicios API, routers FastAPI, servicios de dominio y repositorios SQLite.

## Historias de usuario y requisitos

Cada historia debe tener una plantilla consistente:

- Epica.
- Actor.
- Historia: como [actor], quiero [accion], para [beneficio].
- Criterios de aceptacion.
- Reglas de negocio.
- Pantalla asociada.
- Endpoint asociado, si aplica.
- Diagrama relacionado.
- Validacion esperada.
- Relacion con tarea de ClickUp.

## Flujo de trabajo recomendado

1. Definir o actualizar vision, stakeholders y glosario.
2. Escribir requisitos funcionales y no funcionales.
3. Convertir requisitos priorizados en historias de usuario.
4. Crear diagramas UML que expliquen las historias del sprint actual.
5. Vincular cada historia con ClickUp, endpoints, pantallas y pruebas.
6. Implementar solo despues de tener historia, criterios y validacion clara.

## Configuracion esperada

Obsidian debe abrir la carpeta del repositorio o la carpeta `docs/` como vault. No se requiere mover el proyecto fuera de Git.

Plugins recomendados de Obsidian:

- Excalidraw, para bocetos y diagramas visuales.
- Mermaid Tools o soporte Mermaid nativo, para previsualizar diagramas en Markdown.
- Dataview, opcional, para consultar historias y requisitos mediante metadatos.
- Templates, para insertar plantillas de historias y decisiones.

## Fuera de alcance inicial

- No migrar todo a PlantUML en la primera iteracion.
- No crear un sistema documental separado fuera de `docs/`.
- No reemplazar ClickUp; la documentacion debe complementarlo.
- No generar diagramas de todos los modulos futuros antes de cerrar el flujo Sprint 1.

## Criterios de aceptacion del sistema documental

- Existe una estructura clara en `docs/` para producto, requisitos, arquitectura, diagramas y sprints.
- Las historias de usuario tienen plantilla reutilizable.
- Los diagramas UML iniciales existen como Markdown con Mermaid.
- Excalidraw queda reservado para bocetos visuales dentro de `docs/diagrams/excalidraw/`.
- La documentacion de Sprint 1 conecta historia, modelo, endpoints, pantallas y validacion.
- El flujo es usable por el usuario en Obsidian y por agentes mediante archivos Markdown versionables.

## Revision interna

La especificacion no introduce dependencias obligatorias nuevas para empezar. La unica herramienta externa recomendada para edicion visual es Obsidian con plugins, mientras que los archivos Markdown siguen siendo editables desde cualquier editor. La decision mantiene coherencia con el plan del trabajo de grado: requisitos, historias de usuario, arquitectura MVVM, Scrum/ClickUp y avance incremental del MVP.
