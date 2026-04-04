# Aplicación Móvil para Gestión de Medicamentos — Funcionalidades y Prompt UXPilot

---

## 1. Resumen del Proyecto

Aplicación móvil con interfaces **vocal, táctil y gráfica** basada en **procesamiento de lenguaje natural (PLN)**, orientada a la planificación del suministro y la gestión del inventario de medicamentos en entornos domiciliarios para **pacientes y cuidadores**.

- **Arquitectura:** MVVM (Model–View–ViewModel)
- **Stack:** React Native (Expo) + FastAPI (Python) + SQLite + Google STT/TTS APIs
- **SO objetivo:** Android
- **Público:** Adultos mayores, pacientes crónicos y sus cuidadores domiciliarios

---

## 2. Sugerencias de Nombre para la App

| # | Nombre | Concepto |
|---|--------|----------|
| 1 | **MediVoz** | Medicamento + Voz — directo, memorable y refleja la interacción por voz |
| 2 | **CuidaMed** | Cuidar + Medicamento — enfatiza el rol del cuidador |
| 3 | **DosiVoz** | Dosis + Voz — conciso, alusivo a la funcionalidad principal |
| 4 | **VitalDosis** | Vital + Dosis — evoca importancia y salud |
| 5 | **MediHogar** | Medicamento + Hogar — destaca el entorno domiciliario |
| 6 | **FarmaCuida** | Farma + Cuida — farmacéutico + cuidado |
| 7 | **VozSalud** | Voz + Salud — simple y descriptivo |
| 8 | **MediAsiste** | Medicamento + Asistente — refleja el asistente virtual |
| 9 | **RemediApp** | Remedio + App — nombre amigable y fácil de recordar |
| 10 | **CuidaFarma** | Cuida + Farma — cuidado farmacológico |

> **Recomendación:** *MediVoz* o *DosiVoz* — son cortos, memorables, reflejan la diferenciación por voz y son fáciles de pronunciar para adultos mayores.

---

## 3. Módulos y Funcionalidades del MVP

### 3.1 Módulo de Registro de Usuarios/Pacientes
- Crear perfiles de pacientes (nombre, edad, condiciones médicas)
- Soporte para múltiples pacientes (un cuidador gestiona varios)
- Selección del rol: **paciente** o **cuidador**
- Configuración de preferencias de interacción (voz, táctil, gráfica)

### 3.2 Módulo de Registro de Tratamientos
- Registrar tratamientos farmacológicos con detalle
- Búsqueda de medicamentos por el catálogo **CUM (INVIMA)**: nombre comercial, principio activo, concentración, forma farmacéutica, vía de administración, presentación, laboratorio
- Autocompletado inteligente en la búsqueda de medicamentos
- Asociar medicamentos a pacientes específicos
- Registrar dosis, frecuencia, horarios y duración del tratamiento

### 3.3 Módulo de Planificación y Recordatorios
- Generar horarios personalizados de medicación
- Vista de calendario/agenda con la planificación diaria y semanal
- Sistema de **recordatorios y alarmas** configurables (sonido, vibración, voz)
- Confirmación de toma de medicamento (botón o voz)
- Registro automático de adherencia (tomó / no tomó / pospuso)
- Recordatorios recurrentes y ajustables

### 3.4 Módulo de Seguimiento Terapéutico
- Registro de **síntomas y efectos adversos** durante la ingesta
- Historial cronológico de tomas y eventos
- Indicadores visuales de adherencia (porcentaje de cumplimiento)
- Detección de dosis omitidas con alertas

### 3.5 Módulo de Gestión de Inventario
- Registrar existencias de medicamentos disponibles en el domicilio
- Control de cantidades actuales (stock)
- **Alertas de niveles críticos** cuando el inventario es bajo
- **Recordatorios de reclamación o compra** en farmacias
- Descuento automático del stock al confirmar toma de medicamento
- Historial de consumo del inventario

### 3.6 Módulo de Reportes
- Generación automática de reportes de:
  - Consumo de medicamentos
  - Adherencia terapéutica (frecuencia de toma, cumplimiento de recordatorios)
  - Estado del inventario
  - Registro de síntomas y efectos adversos
- Exportación/visualización del reporte para compartir con profesionales de salud

### 3.7 Módulo de Interacción por Voz (NLP)
- **Speech-to-Text (STT):** entrada de datos por micrófono
- **Text-to-Speech (TTS):** salida de audio (recordatorios, confirmaciones, lectura de información)
- **Procesamiento de Lenguaje Natural:** interpretación de instrucciones verbales
  - Reconocimiento de **intents** (intenciones): registrar toma, consultar inventario, programar recordatorio, etc.
  - Extracción de **entities** (entidades): nombre de medicamento, hora, cantidad, etc.
- Comandos de voz como: *"Registrar que tomé el ibuprofeno"*, *"¿Cuántas pastillas de metformina me quedan?"*, *"Programar recordatorio a las 8 de la mañana"*
- Confirmación auditiva de acciones realizadas

### 3.8 Módulo de Accesibilidad
- Tipografías grandes y legibles
- Botones amplios con áreas de toque generosas
- Contrastes de color adecuados (WCAG)
- Flujos de navegación simplificados y guiados
- Retroalimentación auditiva y visual simultánea
- Modo de alto contraste / tamaño de texto ajustable
- Navegación reducida (mínima cantidad de toques para completar tareas)

---

## 4. Pantallas Principales Identificadas

| # | Pantalla | Descripción |
|---|----------|-------------|
| 1 | **Splash / Onboarding** | Bienvenida, selección de rol (paciente/cuidador), configuración de preferencia de interacción |
| 2 | **Login / Registro** | Registro de cuenta y autenticación |
| 3 | **Home / Dashboard** | Resumen del día: próximos medicamentos, alertas de inventario, acceso rápido al asistente de voz |
| 4 | **Perfil del Paciente** | Datos del paciente, condiciones médicas, lista de tratamientos activos |
| 5 | **Registro de Tratamiento** | Formulario con búsqueda CUM, dosis, frecuencia, horarios |
| 6 | **Calendario / Planificación** | Vista diaria/semanal de medicación programada |
| 7 | **Recordatorio Activo** | Pantalla de alarma: nombre del medicamento, dosis, botones "Tomé" / "Posponer" / confirmar por voz |
| 8 | **Inventario** | Lista de medicamentos en stock, cantidades, alertas de nivel crítico |
| 9 | **Registrar Síntomas** | Formulario de síntomas/efectos adversos con opción de voz |
| 10 | **Reportes** | Gráficas de adherencia, historial de consumo, exportar reporte |
| 11 | **Asistente de Voz** | Pantalla con micrófono activo, transcripción en tiempo real y respuesta del sistema |
| 12 | **Configuración** | Ajustes de accesibilidad, notificaciones, tamaño de texto, modo de interacción |

---

## 5. Prompt para UXPilot — Generación de Mockup

A continuación se presenta el prompt optimizado para generar el diseño de interfaz en **UXPilot**. Puedes usarlo completo o dividirlo por pantallas según lo necesites.

---

### Prompt Completo (Aplicación Completa)

```
Design a complete mobile app UI/UX for Android called "MediVoz" — a medication management and home inventory control app for elderly patients and caregivers. The app uses voice, touch, and graphical interfaces with NLP-based voice assistant.

DESIGN PRINCIPLES:
- Accessibility-first: designed for elderly users and people with low digital literacy
- Large, legible fonts (minimum 16sp body text, 24sp+ headings)
- Big touch targets (minimum 48dp buttons, preferably 56dp+)
- High contrast colors (WCAG AA compliant)
- Simple, guided navigation flows with minimal steps
- Calming healthcare color palette: soft blues, whites, light greens, with orange/red for alerts
- Rounded corners, friendly icons, clear visual hierarchy
- Bottom navigation bar with max 4-5 tabs
- Persistent floating microphone button for voice interaction on every screen

SCREENS TO DESIGN:

1. ONBOARDING (3 slides):
   - Slide 1: Welcome illustration showing an elderly person using phone with voice waves
   - Slide 2: Feature highlight — medication reminders with clock icon
   - Slide 3: Feature highlight — inventory control with checklist icon
   - Role selection: two large cards "Soy Paciente" and "Soy Cuidador" with icons
   - Interaction preference: "¿Cómo prefieres usar la app?" → Voice / Touch / Both

2. LOGIN/REGISTER:
   - Clean form with large input fields
   - Options: email/password or phone number
   - "Registrar con voz" alternative button with microphone icon
   - Large "Iniciar Sesión" / "Registrarse" buttons

3. HOME / DASHBOARD:
   - Top greeting: "Buenos días, [Nombre] 👋" with current date
   - Card: "Próximo medicamento" showing medication name, dose, time remaining with countdown
   - Card: "Adherencia de hoy" with circular progress indicator (e.g., 3/5 tomas)
   - Card: "Alertas de inventario" showing medications running low with warning icon
   - Quick action buttons: "Registrar toma", "Ver calendario", "Añadir medicamento"
   - Floating mic button at bottom-right with pulsing animation indicator
   - Bottom nav: Inicio, Calendario, Inventario, Reportes, Perfil

4. PATIENT PROFILE:
   - Avatar/photo, name, age
   - Medical conditions tags/chips
   - List of active treatments with medication icons
   - "Agregar tratamiento" button
   - If caregiver role: horizontal scrollable patient selector at top

5. TREATMENT REGISTRATION (multi-step form):
   - Step 1: Search medication from CUM database with autocomplete search bar (name or active ingredient)
   - Step 2: Dose configuration — amount, unit, route of administration
   - Step 3: Schedule — frequency (every X hours, specific times), start/end date
   - Step 4: Review and confirm
   - Each step has voice input alternative — microphone icon beside each field
   - Progress indicator at top showing current step

6. CALENDAR / PLANNING VIEW:
   - Weekly calendar strip at top (selectable days)
   - Timeline view below showing medication schedule with time slots
   - Each medication entry: pill icon, name, dose, time, status (pending/taken/missed)
   - Color coding: green=taken, yellow=pending, red=missed
   - Tap to mark as taken or see details

7. ACTIVE REMINDER (alarm screen):
   - Full-screen overlay with soft blue background
   - Large medication name and dose in center
   - Pill illustration or icon
   - "Es hora de tomar: Metformina 500mg"
   - Three large buttons: "✓ Ya la tomé" (green), "⏰ Recordar en 15 min" (yellow), "✕ Omitir" (red)
   - Voice prompt text: "Diga 'tomé' para confirmar"
   - Subtle animation/pulse to draw attention

8. INVENTORY SCREEN:
   - Search bar at top
   - List of medications with: icon, name, current stock number, visual bar indicator
   - Color-coded bars: green (sufficient), yellow (getting low), red (critical)
   - Each item expandable to show: last purchase date, estimated days remaining
   - "Agregar medicamento al inventario" floating action button
   - Alert banner at top if any medication is at critical level: "⚠ 3 medicamentos con stock bajo"

9. SYMPTOM REGISTRATION:
   - Date and time (auto-filled, editable)
   - Associated medication selector (dropdown or voice)
   - Symptom type: selectable chips (Dolor de cabeza, Náuseas, Mareo, Fatiga, Otro...)
   - Severity scale: visual slider or emoji scale (😊 Leve → 😐 Moderado → 😟 Severo)
   - Notes text area with microphone icon for voice input
   - "Guardar" button

10. REPORTS SCREEN:
    - Date range selector at top
    - Adherence chart: circular/donut chart showing overall compliance percentage
    - Bar chart: daily medication intake over the past week/month
    - Inventory consumption trend line chart
    - Symptom frequency summary
    - "Exportar Reporte" button (PDF/share)
    - Cards with key metrics: "Adherencia: 87%", "Dosis omitidas: 4", "Stock crítico: 2"

11. VOICE ASSISTANT SCREEN:
    - Large central microphone button with animated sound waves when listening
    - Real-time transcription text area showing what the user is saying
    - System response area below with both text and speaker icon (for TTS playback)
    - Suggested commands as chips: "Registrar toma", "¿Qué medicamento sigue?", "Estado del inventario"
    - Conversation history showing user commands and assistant responses
    - Visual state indicators: "Escuchando...", "Procesando...", "Listo"

12. SETTINGS:
    - Accessibility section: text size slider, high contrast toggle, voice speed control
    - Notifications: enable/disable, sound selection, vibration toggle
    - Interaction mode: Voice preferred / Touch preferred / Both
    - Language settings
    - Account management
    - Help / Tutorial replay

GENERAL STYLE:
- Use a clean, modern healthcare aesthetic
- Primary color: #2196F3 (calming blue)
- Secondary: #4CAF50 (green for positive/success)
- Warning: #FF9800 (orange)
- Error/Critical: #F44336 (red)
- Background: #F5F7FA (light gray)
- Surface: #FFFFFF
- Text: #212121 (primary), #757575 (secondary)
- All icons should be filled style, not outline, for better visibility
- Card-based layout with subtle shadows
- Consistent 16dp padding and 8dp spacing grid

Generate all screens as a cohesive mobile app design system for Android, optimized for accessibility and elderly users.
```

---

### Prompts Individuales por Pantalla (Alternativa)

Si prefieres generar pantalla por pantalla en UXPilot, aquí tienes prompts individuales:

#### Onboarding
```
Design a 3-step mobile onboarding flow for a healthcare medication management app called "MediVoz". Accessibility-first design for elderly users. Large fonts (24sp+), high contrast, calming blue and white palette. Slide 1: Welcome with illustration of elderly person using phone with voice waves. Slide 2: Medication reminders feature with clock icon. Slide 3: Inventory control with checklist. Final screen: role selection with two large cards "Soy Paciente" and "Soy Cuidador". Android mobile format.
```

#### Dashboard
```
Design a home dashboard screen for "MediVoz" medication management Android app. Accessible design for elderly: large fonts, high contrast, big buttons. Top greeting "Buenos días, María" with date. Cards showing: next medication with countdown timer, today's adherence circular progress (3/5), low inventory alerts with warning icons. Quick action buttons at bottom. Floating microphone button bottom-right. Bottom navigation bar: Inicio, Calendario, Inventario, Reportes, Perfil. Healthcare color palette: blue primary, green success, orange warning.
```

#### Calendario
```
Design a medication calendar/schedule screen for "MediVoz" Android app. Accessible for elderly users with large fonts and high contrast. Weekly day selector strip at top. Below: vertical timeline showing scheduled medications with time slots. Each entry shows pill icon, medication name, dose, and time. Color coded status: green=taken, yellow=pending, red=missed. Tap to mark as taken. Bottom nav bar. Floating mic button. Clean healthcare aesthetic with blue and white.
```

#### Inventario
```
Design a medication inventory management screen for "MediVoz" Android app. Accessible design for elderly. Search bar at top. List of medications showing: name, stock quantity, visual progress bar (green=sufficient, yellow=low, red=critical). Alert banner at top "3 medicamentos con stock bajo". Each item expandable for details. Floating action button to add new medication. Bottom nav and floating mic button. Healthcare color palette.
```

#### Asistente de Voz
```
Design a voice assistant screen for "MediVoz" medication management Android app. Accessible for elderly users. Large central microphone button with animated sound wave rings. Real-time transcription area showing user's speech. Below: system response with text and speaker icon. Suggested command chips: "Registrar toma", "¿Qué sigue?", "Estado inventario". State indicators: "Escuchando...", "Procesando...", "Listo". Conversation history. Clean, calming healthcare design. Blue and white palette.
```

#### Recordatorio Activo (Alarma)
```
Design a full-screen medication reminder/alarm overlay for "MediVoz" Android app. Accessibility-focused for elderly. Soft blue gradient background. Large centered text "Es hora de tomar: Metformina 500mg" with pill illustration. Three large buttons stacked vertically: "Ya la tomé" (green), "Recordar en 15 min" (yellow), "Omitir" (red). Voice prompt text "Diga 'tomé' para confirmar". Subtle pulse animation effect. Very large typography and buttons.
```

---

## 6. Flujo de Navegación Principal

```
Onboarding → Login/Registro
       ↓
   Dashboard (Home)
    ├── Calendario / Planificación
    ├── Inventario de Medicamentos
    ├── Reportes y Estadísticas
    ├── Perfil del Paciente
    │     └── Registro de Tratamiento (multi-step)
    ├── Registrar Síntomas
    ├── Asistente de Voz (desde botón flotante en cualquier pantalla)
    └── Configuración / Accesibilidad
```

---

## 7. Notas para el Diseño

- El **botón de micrófono flotante** debe estar presente en **todas las pantallas** como punto de acceso rápido al asistente de voz.
- Cada campo de formulario debe tener un **ícono de micrófono** para permitir entrada por voz individual.
- Los **recordatorios/alarmas** deben funcionar incluso con la pantalla bloqueada.
- La navegación principal usa **bottom tab bar** con máximo 5 ítems e íconos grandes.
- Priorizar el **flujo de confirmación de toma de medicamento** — debe completarse en máximo 2 toques o 1 comando de voz.
