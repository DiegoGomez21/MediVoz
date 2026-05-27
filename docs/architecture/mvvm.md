# MVVM En MediVoz

La documentacion inicial menciona MVVM como patron de arquitectura para la app. Si aparece el termino MVVC en conversaciones, se tratara como referencia informal al mismo objetivo: separar vista, estado de presentacion y acceso a datos.

## Frontend React Native

- Vista: componentes `.jsx` que renderizan interfaz accesible y delegan la logica.
- ViewModel: hooks como `useHealthViewModel` que exponen estado, acciones y mensajes para la vista.
- Modelo/servicios: clientes API y tipos de datos que conocen el contrato con FastAPI.

## Backend FastAPI

La API se organizara por modulos funcionales. Cada modulo puede contener router, esquemas, servicios y repositorios cuando el flujo lo necesite. Sprint 0 solo incluye el modulo `health`; Sprint 1 agregara medicamentos y recordatorios.
