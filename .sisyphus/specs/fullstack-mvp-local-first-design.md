# MediVoz Fullstack MVP Local-First Design

Date: 2026-06-12
Status: approved-by-inference for planning

## 1. Context

The repository already contains a working FastAPI backend for health checks, medications, reminders, today's reminders, and dose confirmation. The mobile Expo frontend is JavaScript-only and currently renders only the backend health screen. Documentation exists for MVVM, Android setup, prior backend Sprint 1 work, and a broader thesis/product vision, but many thesis deliverables and most mobile screens remain missing.

This design converts the broad request to "write backend and frontend code and document the process" into a bounded MVP that can be implemented safely and reviewed incrementally.

## 2. Product Goal

Build a demoable local-first MediVoz MVP for medication management that lets a user:

1. Open the mobile app and navigate between core areas.
2. Create, view, edit, and delete medications.
3. Create, view, edit, and delete medication reminders.
4. See today's reminders.
5. Mark a reminder as taken.
6. Read basic process/API documentation for the implemented flow.

The MVP prioritizes visible thesis/demo value by connecting mobile screens to the backend modules that already exist.

## 3. Chosen Approach

Use vertical slices with mobile-first integration over the existing backend.

### Considered Options

1. **Mobile-first over existing backend**
   - Pros: fastest demo value, reuses implemented API, reduces backend churn.
   - Cons: leaves larger product modules such as inventory, voice, and reports for later.

2. **Backend-first expansion**
   - Pros: grows domain coverage before UI.
   - Cons: creates unused endpoints and delays a reviewable app experience.

3. **Vertical slices, recommended**
   - Pros: each milestone is testable end-to-end, preserves existing architecture, and avoids disconnected work.
   - Cons: requires careful sequencing and small integration checks after each slice.

The chosen approach is option 3 with initial emphasis on option 1.

## 4. Scope

### In Scope

- Mobile navigation shell.
- Medication list/create/edit/delete screens.
- Reminder list/create/edit/delete screens.
- Today's reminders screen.
- Dose confirmation action.
- Mobile API client expanded beyond `getJson` to support mutations.
- Accessible reusable UI primitives needed by the MVP.
- Backend compatibility fixes if mobile integration reveals small API issues.
- Documentation of API usage, run commands, verification, and implementation process.

### Out of Scope for This MVP

- Account-based authentication and cross-device sync.
- Multi-patient caregiver workflows.
- Production-grade notifications that must fire with the app killed or phone locked.
- Full voice assistant / NLP / STT / TTS implementation.
- CUM/INVIMA live catalog integration.
- Inventory, symptoms, and reports beyond navigation placeholders if useful.
- CI/CD pipeline unless implementation time remains after core MVP verification.

## 5. Architecture

### Backend

Keep the current FastAPI modular pattern:

```text
backend/app/modules/<feature>/
  router.py      -> HTTP endpoints
  service.py     -> business rules and HTTPException mapping
  repository.py  -> database operations
  models.py      -> SQLAlchemy models
  schemas.py     -> Pydantic request/response contracts
```

No broad backend rewrite is required for the MVP. Existing modules should remain the source of truth for medication and reminder behavior.

### Mobile

Keep the JavaScript-only Expo MVVM feature pattern:

```text
mobile/src/features/<feature>/
  <Feature>Screen.jsx
  use<Feature>ViewModel.js
  <feature>Service.js
```

Add navigation at the app root and build feature screens around hooks that call service functions. Avoid TypeScript files and preserve `npm run check:js-only`.

## 6. Data Flow

1. User opens app.
2. App renders navigation shell instead of only `HealthScreen`.
3. Feature screen calls its ViewModel hook.
4. ViewModel calls a feature service.
5. Service calls the shared API client.
6. API client calls FastAPI backend using `EXPO_PUBLIC_API_URL`.
7. Backend router delegates to service/repository/database.
8. Response returns to ViewModel, which updates loading/error/success state.

## 7. Error Handling

- Mobile screens show loading, empty, success, and error states.
- API client throws structured errors with HTTP status and readable messages.
- Form validation catches required fields and obvious invalid values before calling the backend.
- Backend validation remains authoritative for time format, blank medication fields, missing resources, and invalid medication references.

## 8. Accessibility and UX

- Use large touch targets and readable text sizes.
- Keep Spanish labels because the project context and user base are Spanish-speaking.
- Prefer simple forms and clear primary actions.
- Expose `accessibilityLabel` on interactive controls.
- Avoid visual complexity until the functional flow is working.

## 9. Documentation

Create or update documentation covering:

- How to run backend and mobile locally.
- API endpoints used by the mobile app.
- Implemented user flows.
- Verification commands and results.
- Deferred features and rationale.

Documentation should be factual and tied to implemented code, not aspirational.

## 10. Verification Strategy

Required checks after implementation:

```bash
cd backend && pytest -v
cd mobile && npm run lint
cd mobile && npm run check:js-only
```

Manual/agent QA should also run backend and Expo, then exercise:

- App opens successfully.
- Health screen still works.
- Medication CRUD works from mobile.
- Reminder CRUD works from mobile.
- Today's reminders displays active reminders.
- Mark taken creates a dose log successfully.

## 11. Implementation Milestones

1. Mobile API client and navigation shell.
2. Medication mobile vertical slice.
3. Reminder mobile vertical slice.
4. Today's reminders and mark-taken flow.
5. Documentation and verification pass.

Each milestone should keep the app runnable and avoid broad speculative rewrites.

## 12. Risks and Mitigations

- **Risk:** Navigation dependency choice may add setup friction.
  - **Mitigation:** Use the simplest Expo-compatible option and verify immediately after installation.
- **Risk:** Backend API shape may not perfectly match form needs.
  - **Mitigation:** Make small compatible backend adjustments only when required by mobile integration.
- **Risk:** Mobile has no tests today.
  - **Mitigation:** Start with lint, JS-only checks, and manual/agent flow verification; add automated tests later if stable.
- **Risk:** Reminder behavior can become complex quickly.
  - **Mitigation:** MVP only manages scheduled reminder records and taken confirmation; device notifications are deferred.

## 13. Acceptance Criteria

- Backend tests pass.
- Mobile lint passes.
- JavaScript-only verification passes.
- Mobile app has navigation beyond health check.
- User can complete medication CRUD from the app.
- User can complete reminder CRUD from the app.
- User can view today's reminders and mark a reminder as taken.
- Documentation describes what was implemented, how to run it, and what remains deferred.
