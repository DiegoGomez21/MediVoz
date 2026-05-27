import { Pressable, SafeAreaView, StyleSheet, Text, View } from "react-native";

import { colors } from "../../theme/colors";
import { spacing } from "../../theme/spacing";
import { useHealthViewModel } from "./useHealthViewModel";

export function HealthScreen() {
  const viewModel = useHealthViewModel();

  const statusText = viewModel.isChecking
    ? "Verificando conexion con el backend..."
    : viewModel.isConnected
      ? `Conectado a ${viewModel.serviceName}`
      : "Backend no disponible";

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <Text style={styles.kicker}>MediVoz MVP</Text>
        <Text style={styles.title}>Base tecnica lista para Android</Text>
        <Text style={styles.description}>
          Esta pantalla valida que la app React Native Expo puede comunicarse con FastAPI antes de iniciar el flujo de recordatorio basico.
        </Text>

        <View style={[styles.statusCard, viewModel.isConnected ? styles.connected : styles.pending]}>
          <Text style={styles.statusLabel}>Estado del backend</Text>
          <Text style={styles.statusText}>{statusText}</Text>
          <Text style={styles.apiUrl}>{viewModel.apiUrl}</Text>
          {viewModel.errorMessage ? <Text style={styles.errorText}>{viewModel.errorMessage}</Text> : null}
        </View>

        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Volver a verificar conexion con el backend"
          onPress={viewModel.checkConnection}
          style={({ pressed }) => [styles.button, pressed ? styles.buttonPressed : null]}
        >
          <Text style={styles.buttonText}>Verificar de nuevo</Text>
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: colors.background
  },
  container: {
    flex: 1,
    justifyContent: "center",
    padding: spacing.xl,
    gap: spacing.lg
  },
  kicker: {
    color: colors.primary,
    fontSize: 18,
    fontWeight: "700",
    letterSpacing: 0.5
  },
  title: {
    color: colors.text,
    fontSize: 34,
    fontWeight: "800",
    lineHeight: 40
  },
  description: {
    color: colors.mutedText,
    fontSize: 20,
    lineHeight: 30
  },
  statusCard: {
    borderRadius: 24,
    borderWidth: 2,
    padding: spacing.lg,
    gap: spacing.sm
  },
  connected: {
    backgroundColor: colors.successBackground,
    borderColor: colors.success
  },
  pending: {
    backgroundColor: colors.warningBackground,
    borderColor: colors.warning
  },
  statusLabel: {
    color: colors.mutedText,
    fontSize: 16,
    fontWeight: "700",
    textTransform: "uppercase"
  },
  statusText: {
    color: colors.text,
    fontSize: 24,
    fontWeight: "800"
  },
  apiUrl: {
    color: colors.mutedText,
    fontSize: 16
  },
  errorText: {
    color: colors.danger,
    fontSize: 16,
    fontWeight: "700"
  },
  button: {
    alignItems: "center",
    backgroundColor: colors.primary,
    borderRadius: 18,
    minHeight: 56,
    justifyContent: "center",
    paddingHorizontal: spacing.lg
  },
  buttonPressed: {
    opacity: 0.8
  },
  buttonText: {
    color: colors.onPrimary,
    fontSize: 20,
    fontWeight: "800"
  }
});
