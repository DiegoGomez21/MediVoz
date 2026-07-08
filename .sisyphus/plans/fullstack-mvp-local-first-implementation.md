# MediVoz Fullstack MVP Local-First Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Do not create git commits unless the user explicitly requests commits.

**Goal:** Build a reviewable local-first mobile MVP that connects the Expo app to the existing FastAPI medication and reminder backend, then document the implemented process.

**Architecture:** Preserve the current backend module pattern (`router -> service -> repository -> models/schemas`) and the mobile MVVM-by-feature pattern (`Screen`, `useViewModel`, `service`). Implement vertical slices: navigation/API foundation, medications, reminders, today's reminders/mark-taken, then documentation/verification.

**Tech Stack:** FastAPI, SQLAlchemy, SQLite, pytest, Expo SDK 52, React Native 0.76, JavaScript-only React components, React Navigation native stack.

---

## Source Spec

- `.sisyphus/specs/fullstack-mvp-local-first-design.md`

## Non-Negotiable Constraints

- Keep the mobile app JavaScript-only. Do not create `.ts`, `.tsx`, or `tsconfig.json` files.
- Preserve `npm run check:js-only` as a required verification command.
- Do not use `as any`, `@ts-ignore`, or type-suppression patterns.
- Do not commit unless the user explicitly asks.
- Keep backend changes minimal; existing medication and reminder endpoints are the source of truth.
- Keep Spanish labels in the UI.

## Files to Create or Modify

### Mobile foundation

- Modify: `mobile/package.json` — add navigation dependencies through package manager commands, not manual JSON editing.
- Modify: `mobile/App.jsx` — replace single `HealthScreen` mount with app navigator.
- Create: `mobile/src/navigation/AppNavigator.jsx` — React Navigation v7 static native stack and screen registration.
- Create: `mobile/src/components/ScreenContainer.jsx` — shared safe-area container.
- Create: `mobile/src/components/PrimaryButton.jsx` — shared accessible primary button.
- Create: `mobile/src/components/TextField.jsx` — shared labeled text input.
- Create: `mobile/src/components/EmptyState.jsx` — shared empty/error state block.
- Modify: `mobile/src/theme/colors.js` — add neutral border/card colors if needed.
- Modify: `mobile/src/theme/spacing.js` — add `xs` and `xxl` if needed.

### Mobile API layer

- Modify: `mobile/src/api/client.js` — add `requestJson`, `postJson`, `patchJson`, `deleteJson`, and structured API errors.
- Create: `mobile/src/features/medications/medicationsService.js` — medication API contract.
- Create: `mobile/src/features/reminders/remindersService.js` — reminder API contract.

### Mobile medication feature

- Create: `mobile/src/features/medications/useMedicationsViewModel.js` — list/loading/form state and CRUD actions.
- Create: `mobile/src/features/medications/MedicationsScreen.jsx` — medication list and inline create/edit form.

### Mobile reminder feature

- Create: `mobile/src/features/reminders/useRemindersViewModel.js` — list/loading/form state and CRUD actions.
- Create: `mobile/src/features/reminders/RemindersScreen.jsx` — reminder list and inline create/edit form.
- Create: `mobile/src/features/reminders/useTodayRemindersViewModel.js` — today list and mark-taken action.
- Create: `mobile/src/features/reminders/TodayRemindersScreen.jsx` — active reminders and dose confirmation.

### Documentation

- Modify: `README.md` — mention new MVP flow and verification commands.
- Modify: `mobile/README.md` — document navigation, screens, API URL, and verification.
- Modify: `backend/README.md` — confirm endpoints used by mobile.
- Create: `docs/development/fullstack-mvp-process.md` — implementation notes, runbook, verification results, deferred scope.

---

## Task 1: Install Navigation Dependencies

**Files:**
- Modify: `mobile/package.json`
- Modify: `mobile/package-lock.json` if npm creates or updates it

- [ ] **Step 1: Install React Navigation packages**

Run:

```bash
cd mobile && npm install @react-navigation/native @react-navigation/native-stack
```

Expected: npm adds navigation packages to `dependencies`.

- [ ] **Step 2: Install Expo-compatible native dependencies**

Run:

```bash
cd mobile && npx expo install react-native-screens react-native-safe-area-context
```

Expected: Expo installs versions compatible with SDK 52.

- [ ] **Step 3: Verify package scripts still work**

Run:

```bash
cd mobile && npm run check:js-only
```

Expected: PASS, with no TypeScript files/config/dependencies reported.

---

## Task 2: Expand Shared Mobile Theme and Components

**Files:**
- Modify: `mobile/src/theme/colors.js`
- Modify: `mobile/src/theme/spacing.js`
- Create: `mobile/src/components/ScreenContainer.jsx`
- Create: `mobile/src/components/PrimaryButton.jsx`
- Create: `mobile/src/components/TextField.jsx`
- Create: `mobile/src/components/EmptyState.jsx`

- [ ] **Step 1: Extend theme tokens**

Modify `mobile/src/theme/colors.js` to include these keys while preserving existing ones:

```javascript
export const colors = {
  background: "#F4FAF8",
  border: "#D0D5DD",
  card: "#FFFFFF",
  danger: "#B42318",
  mutedText: "#475467",
  onPrimary: "#FFFFFF",
  primary: "#147D73",
  primaryMuted: "#E0F2F1",
  success: "#027A48",
  successBackground: "#D1FADF",
  text: "#102A43",
  warning: "#DC6803",
  warningBackground: "#FEF0C7"
};
```

Modify `mobile/src/theme/spacing.js` to:

```javascript
export const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 20,
  xl: 28,
  xxl: 40
};
```

- [ ] **Step 2: Create `ScreenContainer`**

Create `mobile/src/components/ScreenContainer.jsx`:

```javascript
import { SafeAreaView, ScrollView, StyleSheet, View } from "react-native";

import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

export function ScreenContainer({ children, scroll = true }) {
  if (!scroll) {
    return (
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.content}>{children}</View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
        {children}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: colors.background
  },
  content: {
    flexGrow: 1,
    gap: spacing.lg,
    padding: spacing.xl
  }
});
```

- [ ] **Step 3: Create `PrimaryButton`**

Create `mobile/src/components/PrimaryButton.jsx`:

```javascript
import { Pressable, StyleSheet, Text } from "react-native";

import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

export function PrimaryButton({ label, onPress, disabled = false, accessibilityLabel }) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={accessibilityLabel ?? label}
      disabled={disabled}
      onPress={onPress}
      style={({ pressed }) => [
        styles.button,
        disabled ? styles.disabled : null,
        pressed && !disabled ? styles.pressed : null
      ]}
    >
      <Text style={styles.text}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    alignItems: "center",
    backgroundColor: colors.primary,
    borderRadius: 18,
    justifyContent: "center",
    minHeight: 56,
    paddingHorizontal: spacing.lg
  },
  disabled: {
    opacity: 0.45
  },
  pressed: {
    opacity: 0.8
  },
  text: {
    color: colors.onPrimary,
    fontSize: 18,
    fontWeight: "800"
  }
});
```

- [ ] **Step 4: Create `TextField`**

Create `mobile/src/components/TextField.jsx`:

```javascript
import { StyleSheet, Text, TextInput, View } from "react-native";

import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

export function TextField({ label, value, onChangeText, placeholder, keyboardType = "default" }) {
  return (
    <View style={styles.group}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        accessibilityLabel={label}
        keyboardType={keyboardType}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor={colors.mutedText}
        style={styles.input}
        value={value}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  group: {
    gap: spacing.sm
  },
  input: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderRadius: 14,
    borderWidth: 1,
    color: colors.text,
    fontSize: 18,
    minHeight: 54,
    paddingHorizontal: spacing.md
  },
  label: {
    color: colors.text,
    fontSize: 16,
    fontWeight: "700"
  }
});
```

- [ ] **Step 5: Create `EmptyState`**

Create `mobile/src/components/EmptyState.jsx`:

```javascript
import { StyleSheet, Text, View } from "react-native";

import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

export function EmptyState({ title, description }) {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.description}>{description}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderRadius: 20,
    borderWidth: 1,
    gap: spacing.sm,
    padding: spacing.lg
  },
  description: {
    color: colors.mutedText,
    fontSize: 16,
    lineHeight: 24
  },
  title: {
    color: colors.text,
    fontSize: 20,
    fontWeight: "800"
  }
});
```

- [ ] **Step 6: Verify shared components lint**

Run:

```bash
cd mobile && npm run lint
```

Expected: PASS.

---

## Task 3: Add Navigation Shell

**Files:**
- Create: `mobile/src/navigation/AppNavigator.jsx`
- Modify: `mobile/App.jsx`

- [ ] **Step 1: Create navigator**

Create `mobile/src/navigation/AppNavigator.jsx`:

```javascript
import { createStaticNavigation } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { HealthScreen } from "../features/health/HealthScreen";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

function HomeScreen({ navigation }) {
  return (
    <View style={styles.home}>
      <Text style={styles.kicker}>MediVoz MVP</Text>
      <Text style={styles.title}>Gestion de medicamentos</Text>
      <Text style={styles.description}>Administra medicamentos y recordatorios conectados al backend FastAPI.</Text>

      <View style={styles.actions}>
        <HomeLink label="Estado tecnico" onPress={() => navigation.navigate("Health")} />
        <HomeLink label="Medicamentos" onPress={() => navigation.navigate("Medications")} />
        <HomeLink label="Recordatorios" onPress={() => navigation.navigate("Reminders")} />
        <HomeLink label="Recordatorios de hoy" onPress={() => navigation.navigate("TodayReminders")} />
      </View>
    </View>
  );
}

function HomeLink({ label, onPress }) {
  return (
    <Pressable accessibilityRole="button" accessibilityLabel={label} onPress={onPress} style={styles.link}>
      <Text style={styles.linkText}>{label}</Text>
    </Pressable>
  );
}

function PlaceholderScreen({ title }) {
  return (
    <View style={styles.home}>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.description}>Esta pantalla se implementa en la siguiente tarea del plan.</Text>
    </View>
  );
}

const RootStack = createNativeStackNavigator({
  initialRouteName: "Home",
  screens: {
    Home: {
      screen: HomeScreen,
      options: { title: "Inicio" }
    },
    Health: {
      screen: HealthScreen,
      options: { title: "Estado tecnico" }
    },
    Medications: {
      screen: () => <PlaceholderScreen title="Medicamentos" />,
      options: { title: "Medicamentos" }
    },
    Reminders: {
      screen: () => <PlaceholderScreen title="Recordatorios" />,
      options: { title: "Recordatorios" }
    },
    TodayReminders: {
      screen: () => <PlaceholderScreen title="Recordatorios de hoy" />,
      options: { title: "Hoy" }
    }
  }
});

export const AppNavigator = createStaticNavigation(RootStack);

const styles = StyleSheet.create({
  actions: {
    gap: spacing.md
  },
  description: {
    color: colors.mutedText,
    fontSize: 18,
    lineHeight: 28
  },
  home: {
    flex: 1,
    gap: spacing.lg,
    justifyContent: "center",
    padding: spacing.xl,
    backgroundColor: colors.background
  },
  kicker: {
    color: colors.primary,
    fontSize: 18,
    fontWeight: "700"
  },
  link: {
    backgroundColor: colors.primary,
    borderRadius: 18,
    minHeight: 56,
    justifyContent: "center",
    paddingHorizontal: spacing.lg
  },
  linkText: {
    color: colors.onPrimary,
    fontSize: 18,
    fontWeight: "800",
    textAlign: "center"
  },
  title: {
    color: colors.text,
    fontSize: 32,
    fontWeight: "800",
    lineHeight: 38
  }
});
```

- [ ] **Step 2: Wire navigator in app root**

Modify `mobile/App.jsx`:

```javascript
import { StatusBar } from "expo-status-bar";

import { AppNavigator } from "./src/navigation/AppNavigator";

export default function App() {
  return (
    <>
      <AppNavigator />
      <StatusBar style="dark" />
    </>
  );
}
```

- [ ] **Step 3: Verify app shell**

Run:

```bash
cd mobile && npm run lint && npm run check:js-only
```

Expected: both commands PASS.

---

## Task 4: Expand API Client for Mutations

**Files:**
- Modify: `mobile/src/api/client.js`

- [ ] **Step 1: Replace API client with structured request helpers**

Modify `mobile/src/api/client.js`:

```javascript
const DEFAULT_API_URL = "http://10.0.2.2:8000";

export const API_URL = process.env.EXPO_PUBLIC_API_URL ?? DEFAULT_API_URL;

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function requestJson(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      Accept: "application/json",
      ...(options.body ? { "Content-Type": "application/json" } : null),
      ...options.headers
    },
    ...options
  });

  if (!response.ok) {
    throw new ApiError(`API request failed with status ${response.status}`, response.status);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export function getJson(path) {
  return requestJson(path);
}

export function postJson(path, body) {
  return requestJson(path, {
    method: "POST",
    body: JSON.stringify(body)
  });
}

export function patchJson(path, body) {
  return requestJson(path, {
    method: "PATCH",
    body: JSON.stringify(body)
  });
}

export function deleteJson(path) {
  return requestJson(path, {
    method: "DELETE"
  });
}
```

- [ ] **Step 2: Verify health service compatibility**

Run:

```bash
cd mobile && npm run lint && npm run check:js-only
```

Expected: both commands PASS and `healthService.js` still imports `getJson` successfully.

---

## Task 5: Implement Medication Service and ViewModel

**Files:**
- Create: `mobile/src/features/medications/medicationsService.js`
- Create: `mobile/src/features/medications/useMedicationsViewModel.js`

- [ ] **Step 1: Create medication API service**

Create `mobile/src/features/medications/medicationsService.js`:

```javascript
import { deleteJson, getJson, patchJson, postJson } from "../../api/client";

export function listMedications() {
  return getJson("/medications");
}

export function createMedication(payload) {
  return postJson("/medications", payload);
}

export function updateMedication(medicationId, payload) {
  return patchJson(`/medications/${medicationId}`, payload);
}

export function deleteMedication(medicationId) {
  return deleteJson(`/medications/${medicationId}`);
}
```

- [ ] **Step 2: Create medication ViewModel**

Create `mobile/src/features/medications/useMedicationsViewModel.js`:

```javascript
import { useCallback, useEffect, useState } from "react";

import { createMedication, deleteMedication, listMedications, updateMedication } from "./medicationsService";

const EMPTY_FORM = {
  name: "",
  dose_label: ""
};

export function useMedicationsViewModel() {
  const [medications, setMedications] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [editingId, setEditingId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  const loadMedications = useCallback(async () => {
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const nextMedications = await listMedications();
      setMedications(nextMedications);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "No fue posible cargar medicamentos.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadMedications();
  }, [loadMedications]);

  const updateField = useCallback((field, value) => {
    setForm((current) => ({ ...current, [field]: value }));
  }, []);

  const resetForm = useCallback(() => {
    setForm(EMPTY_FORM);
    setEditingId(null);
  }, []);

  const startEditing = useCallback((medication) => {
    setEditingId(medication.id);
    setForm({ name: medication.name, dose_label: medication.dose_label });
  }, []);

  const saveMedication = useCallback(async () => {
    const name = form.name.trim();
    const doseLabel = form.dose_label.trim();

    if (!name || !doseLabel) {
      setErrorMessage("Nombre y dosis son obligatorios.");
      return;
    }

    setIsSaving(true);
    setErrorMessage(null);

    try {
      const payload = { name, dose_label: doseLabel };
      if (editingId) {
        await updateMedication(editingId, payload);
      } else {
        await createMedication(payload);
      }
      resetForm();
      await loadMedications();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "No fue posible guardar el medicamento.");
    } finally {
      setIsSaving(false);
    }
  }, [editingId, form.dose_label, form.name, loadMedications, resetForm]);

  const removeMedication = useCallback(async (medicationId) => {
    setErrorMessage(null);

    try {
      await deleteMedication(medicationId);
      await loadMedications();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "No fue posible eliminar el medicamento.");
    }
  }, [loadMedications]);

  return {
    editingId,
    errorMessage,
    form,
    isLoading,
    isSaving,
    medications,
    loadMedications,
    removeMedication,
    resetForm,
    saveMedication,
    startEditing,
    updateField
  };
}
```

- [ ] **Step 3: Verify medication logic lint**

Run:

```bash
cd mobile && npm run lint
```

Expected: PASS.

---

## Task 6: Implement Medication Screen

**Files:**
- Create: `mobile/src/features/medications/MedicationsScreen.jsx`
- Modify: `mobile/src/navigation/AppNavigator.jsx`

- [ ] **Step 1: Create medication screen**

Create `mobile/src/features/medications/MedicationsScreen.jsx`:

```javascript
import { Pressable, StyleSheet, Text, View } from "react-native";

import { EmptyState } from "../../components/EmptyState";
import { PrimaryButton } from "../../components/PrimaryButton";
import { ScreenContainer } from "../../components/ScreenContainer";
import { TextField } from "../../components/TextField";
import { colors } from "../../theme/colors";
import { spacing } from "../../theme/spacing";
import { useMedicationsViewModel } from "./useMedicationsViewModel";

export function MedicationsScreen() {
  const viewModel = useMedicationsViewModel();

  return (
    <ScreenContainer>
      <View style={styles.header}>
        <Text style={styles.title}>Medicamentos</Text>
        <Text style={styles.description}>Registra los medicamentos que usaran los recordatorios.</Text>
      </View>

      <View style={styles.formCard}>
        <Text style={styles.sectionTitle}>{viewModel.editingId ? "Editar medicamento" : "Nuevo medicamento"}</Text>
        <TextField
          label="Nombre del medicamento"
          onChangeText={(value) => viewModel.updateField("name", value)}
          placeholder="Ej. Losartan"
          value={viewModel.form.name}
        />
        <TextField
          label="Dosis"
          onChangeText={(value) => viewModel.updateField("dose_label", value)}
          placeholder="Ej. 50 mg"
          value={viewModel.form.dose_label}
        />
        {viewModel.errorMessage ? <Text style={styles.errorText}>{viewModel.errorMessage}</Text> : null}
        <PrimaryButton
          disabled={viewModel.isSaving}
          label={viewModel.isSaving ? "Guardando..." : "Guardar medicamento"}
          onPress={viewModel.saveMedication}
        />
        {viewModel.editingId ? (
          <Pressable accessibilityRole="button" accessibilityLabel="Cancelar edicion" onPress={viewModel.resetForm}>
            <Text style={styles.secondaryAction}>Cancelar edicion</Text>
          </Pressable>
        ) : null}
      </View>

      {viewModel.isLoading ? <EmptyState title="Cargando" description="Consultando medicamentos registrados." /> : null}

      {!viewModel.isLoading && viewModel.medications.length === 0 ? (
        <EmptyState title="Sin medicamentos" description="Agrega el primer medicamento para crear recordatorios." />
      ) : null}

      <View style={styles.list}>
        {viewModel.medications.map((medication) => (
          <View key={medication.id} style={styles.card}>
            <View style={styles.cardText}>
              <Text style={styles.cardTitle}>{medication.name}</Text>
              <Text style={styles.cardDescription}>{medication.dose_label}</Text>
            </View>
            <View style={styles.cardActions}>
              <Pressable accessibilityRole="button" accessibilityLabel={`Editar ${medication.name}`} onPress={() => viewModel.startEditing(medication)}>
                <Text style={styles.actionText}>Editar</Text>
              </Pressable>
              <Pressable accessibilityRole="button" accessibilityLabel={`Eliminar ${medication.name}`} onPress={() => viewModel.removeMedication(medication.id)}>
                <Text style={styles.dangerText}>Eliminar</Text>
              </Pressable>
            </View>
          </View>
        ))}
      </View>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  actionText: {
    color: colors.primary,
    fontSize: 16,
    fontWeight: "800"
  },
  card: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderRadius: 20,
    borderWidth: 1,
    gap: spacing.md,
    padding: spacing.lg
  },
  cardActions: {
    flexDirection: "row",
    gap: spacing.lg
  },
  cardDescription: {
    color: colors.mutedText,
    fontSize: 16
  },
  cardText: {
    gap: spacing.xs
  },
  cardTitle: {
    color: colors.text,
    fontSize: 20,
    fontWeight: "800"
  },
  dangerText: {
    color: colors.danger,
    fontSize: 16,
    fontWeight: "800"
  },
  description: {
    color: colors.mutedText,
    fontSize: 18,
    lineHeight: 26
  },
  errorText: {
    color: colors.danger,
    fontSize: 16,
    fontWeight: "700"
  },
  formCard: {
    backgroundColor: colors.card,
    borderRadius: 24,
    gap: spacing.md,
    padding: spacing.lg
  },
  header: {
    gap: spacing.sm
  },
  list: {
    gap: spacing.md
  },
  secondaryAction: {
    color: colors.primary,
    fontSize: 16,
    fontWeight: "700",
    textAlign: "center"
  },
  sectionTitle: {
    color: colors.text,
    fontSize: 22,
    fontWeight: "800"
  },
  title: {
    color: colors.text,
    fontSize: 32,
    fontWeight: "800"
  }
});
```

- [ ] **Step 2: Register medication screen in navigator**

In `mobile/src/navigation/AppNavigator.jsx`, import and use the real screen:

```javascript
import { MedicationsScreen } from "../features/medications/MedicationsScreen";
```

Replace the placeholder `Medications` entry in the static stack with:

```javascript
Medications: {
  screen: MedicationsScreen,
  options: { title: "Medicamentos" }
}
```

- [ ] **Step 3: Verify medication screen**

Run:

```bash
cd mobile && npm run lint && npm run check:js-only
```

Expected: both commands PASS.

---

## Task 7: Implement Reminder Services and ViewModels

**Files:**
- Create: `mobile/src/features/reminders/remindersService.js`
- Create: `mobile/src/features/reminders/useRemindersViewModel.js`
- Create: `mobile/src/features/reminders/useTodayRemindersViewModel.js`

- [ ] **Step 1: Create reminder API service**

Create `mobile/src/features/reminders/remindersService.js`:

```javascript
import { deleteJson, getJson, patchJson, postJson } from "../../api/client";

export function listReminders() {
  return getJson("/reminders");
}

export function listTodayReminders() {
  return getJson("/reminders/today");
}

export function createReminder(payload) {
  return postJson("/reminders", payload);
}

export function updateReminder(reminderId, payload) {
  return patchJson(`/reminders/${reminderId}`, payload);
}

export function deleteReminder(reminderId) {
  return deleteJson(`/reminders/${reminderId}`);
}

export function markReminderTaken(reminderId) {
  return postJson(`/reminders/${reminderId}/taken`, {});
}
```

- [ ] **Step 2: Create reminder CRUD ViewModel**

Create `mobile/src/features/reminders/useRemindersViewModel.js`:

```javascript
import { useCallback, useEffect, useState } from "react";

import { listMedications } from "../medications/medicationsService";
import { createReminder, deleteReminder, listReminders, updateReminder } from "./remindersService";

const EMPTY_FORM = {
  medication_id: "",
  time_of_day: "08:00",
  is_active: true
};

export function useRemindersViewModel() {
  const [reminders, setReminders] = useState([]);
  const [medications, setMedications] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [editingId, setEditingId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  const loadData = useCallback(async () => {
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const [nextMedications, nextReminders] = await Promise.all([listMedications(), listReminders()]);
      setMedications(nextMedications);
      setReminders(nextReminders);
      if (!form.medication_id && nextMedications.length > 0) {
        setForm((current) => ({ ...current, medication_id: String(nextMedications[0].id) }));
      }
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "No fue posible cargar recordatorios.");
    } finally {
      setIsLoading(false);
    }
  }, [form.medication_id]);

  useEffect(() => {
    void loadData();
  }, [loadData]);

  const updateField = useCallback((field, value) => {
    setForm((current) => ({ ...current, [field]: value }));
  }, []);

  const resetForm = useCallback(() => {
    setForm((current) => ({ ...EMPTY_FORM, medication_id: current.medication_id }));
    setEditingId(null);
  }, []);

  const startEditing = useCallback((reminder) => {
    setEditingId(reminder.id);
    setForm({
      medication_id: String(reminder.medication_id),
      time_of_day: reminder.time_of_day,
      is_active: reminder.is_active
    });
  }, []);

  const saveReminder = useCallback(async () => {
    const medicationId = Number(form.medication_id);
    const timeOfDay = form.time_of_day.trim();

    if (!medicationId || !timeOfDay) {
      setErrorMessage("Selecciona medicamento y hora.");
      return;
    }

    setIsSaving(true);
    setErrorMessage(null);

    try {
      const payload = { medication_id: medicationId, time_of_day: timeOfDay, is_active: form.is_active };
      if (editingId) {
        await updateReminder(editingId, payload);
      } else {
        await createReminder(payload);
      }
      resetForm();
      await loadData();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "No fue posible guardar el recordatorio.");
    } finally {
      setIsSaving(false);
    }
  }, [editingId, form.is_active, form.medication_id, form.time_of_day, loadData, resetForm]);

  const removeReminder = useCallback(async (reminderId) => {
    setErrorMessage(null);

    try {
      await deleteReminder(reminderId);
      await loadData();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "No fue posible eliminar el recordatorio.");
    }
  }, [loadData]);

  return {
    editingId,
    errorMessage,
    form,
    isLoading,
    isSaving,
    medications,
    reminders,
    removeReminder,
    resetForm,
    saveReminder,
    startEditing,
    updateField
  };
}
```

- [ ] **Step 3: Create today's reminders ViewModel**

Create `mobile/src/features/reminders/useTodayRemindersViewModel.js`:

```javascript
import { useCallback, useEffect, useState } from "react";

import { listTodayReminders, markReminderTaken } from "./remindersService";

export function useTodayRemindersViewModel() {
  const [reminders, setReminders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const loadTodayReminders = useCallback(async () => {
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const nextReminders = await listTodayReminders();
      setReminders(nextReminders);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "No fue posible cargar recordatorios de hoy.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadTodayReminders();
  }, [loadTodayReminders]);

  const markTaken = useCallback(async (reminder) => {
    setIsSaving(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      await markReminderTaken(reminder.id);
      setSuccessMessage(`${reminder.medication.name} marcado como tomado.`);
      await loadTodayReminders();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "No fue posible confirmar la dosis.");
    } finally {
      setIsSaving(false);
    }
  }, [loadTodayReminders]);

  return {
    errorMessage,
    isLoading,
    isSaving,
    reminders,
    successMessage,
    loadTodayReminders,
    markTaken
  };
}
```

- [ ] **Step 4: Verify reminder logic lint**

Run:

```bash
cd mobile && npm run lint
```

Expected: PASS.

---

## Task 8: Implement Reminder Screens

**Files:**
- Create: `mobile/src/features/reminders/RemindersScreen.jsx`
- Create: `mobile/src/features/reminders/TodayRemindersScreen.jsx`
- Modify: `mobile/src/navigation/AppNavigator.jsx`

- [ ] **Step 1: Create reminder CRUD screen**

Create `mobile/src/features/reminders/RemindersScreen.jsx`:

```javascript
import { Pressable, StyleSheet, Switch, Text, View } from "react-native";

import { EmptyState } from "../../components/EmptyState";
import { PrimaryButton } from "../../components/PrimaryButton";
import { ScreenContainer } from "../../components/ScreenContainer";
import { TextField } from "../../components/TextField";
import { colors } from "../../theme/colors";
import { spacing } from "../../theme/spacing";
import { useRemindersViewModel } from "./useRemindersViewModel";

export function RemindersScreen() {
  const viewModel = useRemindersViewModel();

  return (
    <ScreenContainer>
      <View style={styles.header}>
        <Text style={styles.title}>Recordatorios</Text>
        <Text style={styles.description}>Programa horarios asociados a medicamentos registrados.</Text>
      </View>

      <View style={styles.formCard}>
        <Text style={styles.sectionTitle}>{viewModel.editingId ? "Editar recordatorio" : "Nuevo recordatorio"}</Text>
        {viewModel.medications.length > 0 ? (
          <Text style={styles.helperText}>
            Medicamentos disponibles: {viewModel.medications.map((medication) => `${medication.id} - ${medication.name} (${medication.dose_label})`).join(", ")}
          </Text>
        ) : (
          <Text style={styles.helperText}>Primero crea un medicamento para asociarlo al recordatorio.</Text>
        )}
        <TextField
          keyboardType="numeric"
          label="ID del medicamento"
          onChangeText={(value) => viewModel.updateField("medication_id", value)}
          placeholder="Ej. 1"
          value={viewModel.form.medication_id}
        />
        <TextField
          label="Hora"
          onChangeText={(value) => viewModel.updateField("time_of_day", value)}
          placeholder="08:00"
          value={viewModel.form.time_of_day}
        />
        <View style={styles.switchRow}>
          <Text style={styles.switchLabel}>Recordatorio activo</Text>
          <Switch
            accessibilityLabel="Recordatorio activo"
            onValueChange={(value) => viewModel.updateField("is_active", value)}
            value={viewModel.form.is_active}
          />
        </View>
        {viewModel.errorMessage ? <Text style={styles.errorText}>{viewModel.errorMessage}</Text> : null}
        <PrimaryButton
          disabled={viewModel.isSaving || viewModel.medications.length === 0}
          label={viewModel.isSaving ? "Guardando..." : "Guardar recordatorio"}
          onPress={viewModel.saveReminder}
        />
        {viewModel.editingId ? (
          <Pressable accessibilityRole="button" accessibilityLabel="Cancelar edicion" onPress={viewModel.resetForm}>
            <Text style={styles.secondaryAction}>Cancelar edicion</Text>
          </Pressable>
        ) : null}
      </View>

      {viewModel.isLoading ? <EmptyState title="Cargando" description="Consultando recordatorios registrados." /> : null}

      {!viewModel.isLoading && viewModel.reminders.length === 0 ? (
        <EmptyState title="Sin recordatorios" description="Agrega un horario para un medicamento registrado." />
      ) : null}

      <View style={styles.list}>
        {viewModel.reminders.map((reminder) => (
          <View key={reminder.id} style={styles.card}>
            <View style={styles.cardText}>
              <Text style={styles.time}>{reminder.time_of_day}</Text>
              <Text style={styles.cardTitle}>{reminder.medication.name}</Text>
              <Text style={styles.cardDescription}>{reminder.medication.dose_label}</Text>
              <Text style={reminder.is_active ? styles.activeText : styles.inactiveText}>
                {reminder.is_active ? "Activo" : "Inactivo"}
              </Text>
            </View>
            <View style={styles.cardActions}>
              <Pressable accessibilityRole="button" accessibilityLabel={`Editar recordatorio ${reminder.id}`} onPress={() => viewModel.startEditing(reminder)}>
                <Text style={styles.actionText}>Editar</Text>
              </Pressable>
              <Pressable accessibilityRole="button" accessibilityLabel={`Eliminar recordatorio ${reminder.id}`} onPress={() => viewModel.removeReminder(reminder.id)}>
                <Text style={styles.dangerText}>Eliminar</Text>
              </Pressable>
            </View>
          </View>
        ))}
      </View>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  actionText: {
    color: colors.primary,
    fontSize: 16,
    fontWeight: "800"
  },
  activeText: {
    color: colors.success,
    fontSize: 16,
    fontWeight: "800"
  },
  card: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderRadius: 20,
    borderWidth: 1,
    gap: spacing.md,
    padding: spacing.lg
  },
  cardActions: {
    flexDirection: "row",
    gap: spacing.lg
  },
  cardDescription: {
    color: colors.mutedText,
    fontSize: 16
  },
  cardText: {
    gap: spacing.xs
  },
  cardTitle: {
    color: colors.text,
    fontSize: 20,
    fontWeight: "800"
  },
  dangerText: {
    color: colors.danger,
    fontSize: 16,
    fontWeight: "800"
  },
  description: {
    color: colors.mutedText,
    fontSize: 18,
    lineHeight: 26
  },
  errorText: {
    color: colors.danger,
    fontSize: 16,
    fontWeight: "700"
  },
  formCard: {
    backgroundColor: colors.card,
    borderRadius: 24,
    gap: spacing.md,
    padding: spacing.lg
  },
  header: {
    gap: spacing.sm
  },
  helperText: {
    color: colors.mutedText,
    fontSize: 15,
    lineHeight: 22
  },
  inactiveText: {
    color: colors.warning,
    fontSize: 16,
    fontWeight: "800"
  },
  list: {
    gap: spacing.md
  },
  secondaryAction: {
    color: colors.primary,
    fontSize: 16,
    fontWeight: "700",
    textAlign: "center"
  },
  sectionTitle: {
    color: colors.text,
    fontSize: 22,
    fontWeight: "800"
  },
  switchLabel: {
    color: colors.text,
    fontSize: 16,
    fontWeight: "700"
  },
  switchRow: {
    alignItems: "center",
    flexDirection: "row",
    justifyContent: "space-between"
  },
  time: {
    color: colors.primary,
    fontSize: 26,
    fontWeight: "900"
  },
  title: {
    color: colors.text,
    fontSize: 32,
    fontWeight: "800"
  }
});
```

- [ ] **Step 2: Create today's reminders screen**

Create `mobile/src/features/reminders/TodayRemindersScreen.jsx`:

```javascript
import { StyleSheet, Text, View } from "react-native";

import { EmptyState } from "../../components/EmptyState";
import { PrimaryButton } from "../../components/PrimaryButton";
import { ScreenContainer } from "../../components/ScreenContainer";
import { colors } from "../../theme/colors";
import { spacing } from "../../theme/spacing";
import { useTodayRemindersViewModel } from "./useTodayRemindersViewModel";

export function TodayRemindersScreen() {
  const viewModel = useTodayRemindersViewModel();

  return (
    <ScreenContainer>
      <View style={styles.header}>
        <Text style={styles.title}>Recordatorios de hoy</Text>
        <Text style={styles.description}>Confirma las dosis tomadas durante el dia.</Text>
      </View>

      {viewModel.errorMessage ? <Text style={styles.errorText}>{viewModel.errorMessage}</Text> : null}
      {viewModel.successMessage ? <Text style={styles.successText}>{viewModel.successMessage}</Text> : null}

      {viewModel.isLoading ? <EmptyState title="Cargando" description="Consultando recordatorios activos." /> : null}

      {!viewModel.isLoading && viewModel.reminders.length === 0 ? (
        <EmptyState title="Sin recordatorios activos" description="Crea un recordatorio activo para verlo aqui." />
      ) : null}

      <View style={styles.list}>
        {viewModel.reminders.map((reminder) => (
          <View key={reminder.id} style={styles.card}>
            <Text style={styles.time}>{reminder.time_of_day}</Text>
            <Text style={styles.cardTitle}>{reminder.medication.name}</Text>
            <Text style={styles.cardDescription}>{reminder.medication.dose_label}</Text>
            <PrimaryButton
              disabled={viewModel.isSaving}
              label="Marcar como tomado"
              onPress={() => viewModel.markTaken(reminder)}
            />
          </View>
        ))}
      </View>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderRadius: 20,
    borderWidth: 1,
    gap: spacing.sm,
    padding: spacing.lg
  },
  cardDescription: {
    color: colors.mutedText,
    fontSize: 16
  },
  cardTitle: {
    color: colors.text,
    fontSize: 22,
    fontWeight: "800"
  },
  description: {
    color: colors.mutedText,
    fontSize: 18,
    lineHeight: 26
  },
  errorText: {
    color: colors.danger,
    fontSize: 16,
    fontWeight: "700"
  },
  header: {
    gap: spacing.sm
  },
  list: {
    gap: spacing.md
  },
  successText: {
    color: colors.success,
    fontSize: 16,
    fontWeight: "700"
  },
  time: {
    color: colors.primary,
    fontSize: 28,
    fontWeight: "900"
  },
  title: {
    color: colors.text,
    fontSize: 32,
    fontWeight: "800"
  }
});
```

- [ ] **Step 3: Register reminder screens**

In `mobile/src/navigation/AppNavigator.jsx`, import:

```javascript
import { RemindersScreen } from "../features/reminders/RemindersScreen";
import { TodayRemindersScreen } from "../features/reminders/TodayRemindersScreen";
```

Replace reminder placeholders in the static stack with:

```javascript
Reminders: {
  screen: RemindersScreen,
  options: { title: "Recordatorios" }
},
TodayReminders: {
  screen: TodayRemindersScreen,
  options: { title: "Hoy" }
}
```

- [ ] **Step 4: Verify reminder screens**

Run:

```bash
cd mobile && npm run lint && npm run check:js-only
```

Expected: both commands PASS.

---

## Task 9: Run Backend Compatibility Verification

**Files:**
- No planned code changes unless tests expose a real backend/mobile contract issue.

- [ ] **Step 1: Run backend tests**

Run:

```bash
cd backend && pytest -v
```

Expected: all tests PASS.

- [ ] **Step 2: If backend tests fail, fix the root cause**

Only edit backend files if the failure is caused by current implementation defects. Preserve existing endpoint contracts:

- `POST /medications` accepts `{ "name": string, "dose_label": string }`.
- `PATCH /medications/{id}` accepts partial `name` and `dose_label`.
- `POST /reminders` accepts `{ "medication_id": number, "time_of_day": "HH:MM", "is_active": boolean }`.
- `PATCH /reminders/{id}` accepts partial `medication_id`, `time_of_day`, and `is_active`.
- `POST /reminders/{id}/taken` returns a dose log.

Re-run:

```bash
cd backend && pytest -v
```

Expected: all tests PASS.

---

## Task 10: Manual End-to-End QA

**Files:**
- No planned source edits unless QA exposes a defect.

- [ ] **Step 1: Start backend**

Run in one terminal:

```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Expected: FastAPI starts on port 8000.

- [ ] **Step 2: Start mobile**

Run in another terminal:

```bash
cd mobile && npm start
```

Expected: Expo starts without Metro errors.

- [ ] **Step 3: Execute QA flow**

In Android emulator or Expo target:

1. Open app.
2. Navigate to `Estado tecnico` and verify backend connected.
3. Navigate to `Medicamentos`.
4. Create medication `Losartan`, dose `50 mg`.
5. Edit it to `Losartan potasico`, dose `50 mg`.
6. Navigate to `Recordatorios`.
7. Create reminder for that medication at `08:00`.
8. Navigate to `Recordatorios de hoy`.
9. Confirm the medication appears.
10. Tap `Marcar como tomado`.
11. Verify a success message appears.

Expected: every step succeeds without app crash.

---

## Task 11: Documentation Update

**Files:**
- Modify: `README.md`
- Modify: `mobile/README.md`
- Modify: `backend/README.md`
- Create: `docs/development/fullstack-mvp-process.md`

- [ ] **Step 1: Update root README**

Add a section summarizing implemented MVP flows:

```markdown
## MVP local-first implementado

El MVP conecta la app Expo con la API FastAPI para:

- Verificar conectividad con `GET /health`.
- Crear, listar, editar y eliminar medicamentos.
- Crear, listar, editar y eliminar recordatorios.
- Ver recordatorios activos del dia.
- Marcar una dosis como tomada.

Verificacion principal:

```bash
cd backend && pytest -v
cd ../mobile && npm run lint
npm run check:js-only
```
```

- [ ] **Step 2: Update mobile README**

Add a section listing screens:

```markdown
## Pantallas MVP

- Inicio: navegacion principal.
- Estado tecnico: valida conexion con FastAPI.
- Medicamentos: CRUD de medicamentos.
- Recordatorios: CRUD de horarios asociados a medicamentos.
- Recordatorios de hoy: lista recordatorios activos y permite marcar dosis tomada.
```

- [ ] **Step 3: Update backend README**

Add a short note:

```markdown
## Uso desde la app movil

La app movil consume los endpoints de salud, medicamentos y recordatorios documentados arriba. Para emulador Android, ejecutar FastAPI con `--host 0.0.0.0` y configurar `EXPO_PUBLIC_API_URL=http://10.0.2.2:8000`.
```

- [ ] **Step 4: Create process documentation**

Create `docs/development/fullstack-mvp-process.md`:

```markdown
# Fullstack MVP Process

## Alcance implementado

El MVP local-first prioriza flujos visibles y verificables sobre el backend existente: medicamentos, recordatorios, recordatorios del dia y confirmacion de dosis tomada.

## Decisiones

- Se preservo FastAPI modular por feature en backend.
- Se preservo Expo JavaScript sin TypeScript.
- Se implemento navegacion y MVVM por feature en mobile.
- Se difirio autenticacion, sincronizacion, voz, inventario, reportes y notificaciones de sistema.

## Ejecucion local

Backend:

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Mobile:

```bash
cd mobile
npm start
```

## Verificacion

```bash
cd backend && pytest -v
cd mobile && npm run lint
cd mobile && npm run check:js-only
```

## QA manual

1. Abrir la app.
2. Validar estado tecnico.
3. Crear medicamento.
4. Crear recordatorio.
5. Ver recordatorio del dia.
6. Marcar dosis como tomada.

## Trabajo diferido

- Autenticacion y multi-paciente.
- Inventario.
- Sintomas y reportes.
- Voz y NLP.
- Notificaciones confiables en segundo plano.
- CI/CD.
```

- [ ] **Step 5: Verify documentation changes**

Run from repository root:

```bash
git diff -- README.md mobile/README.md backend/README.md docs/development/fullstack-mvp-process.md
git diff --check
```

Expected:

- The first command shows the new root README section `MVP local-first implementado`.
- The first command shows the new mobile README section `Pantallas MVP`.
- The first command shows the new backend README section `Uso desde la app movil`.
- The first command shows the new file `docs/development/fullstack-mvp-process.md` with sections `Alcance implementado`, `Decisiones`, `Ejecucion local`, `Verificacion`, `QA manual`, and `Trabajo diferido`.
- `git diff --check` exits with status 0 and prints no whitespace errors.

---

## Task 12: Final Verification

**Files:**
- All modified files.

- [ ] **Step 1: Run LSP diagnostics where available**

Run diagnostics on modified mobile JS files and documentation paths if the environment supports it.

Expected: no blocking diagnostics.

- [ ] **Step 2: Run backend tests**

```bash
cd backend && pytest -v
```

Expected: PASS.

- [ ] **Step 3: Run mobile lint**

```bash
cd mobile && npm run lint
```

Expected: PASS.

- [ ] **Step 4: Run JavaScript-only verification**

```bash
cd mobile && npm run check:js-only
```

Expected: PASS.

- [ ] **Step 5: Inspect git diff without committing**

```bash
git status --short
git diff --stat
```

Expected: changes match this plan and no secrets, generated DB files, `.expo`, `node_modules`, or build artifacts are staged or included.

---

## Self-Review

### Spec Coverage

- Navigation shell: Task 3.
- Medication CRUD from mobile: Tasks 4, 5, 6.
- Reminder CRUD from mobile: Tasks 4, 7, 8.
- Today's reminders and mark taken: Tasks 7, 8, 10.
- Accessibility and Spanish UI: Tasks 2, 3, 6, 8.
- Documentation: Task 11.
- Verification: Tasks 9, 10, 12.

### Placeholder Scan

This plan intentionally avoids placeholder markers and defines concrete file paths, commands, code blocks, and expected outcomes. Task 8 now includes complete code for `RemindersScreen.jsx` instead of relying on visual inference from another screen.

### Type and Contract Consistency

- Medication payloads use backend schema fields `name` and `dose_label`.
- Reminder payloads use backend schema fields `medication_id`, `time_of_day`, and `is_active`.
- Navigation route names are consistent: `Home`, `Health`, `Medications`, `Reminders`, `TodayReminders`.
- API helper names are consistent: `getJson`, `postJson`, `patchJson`, `deleteJson`.
