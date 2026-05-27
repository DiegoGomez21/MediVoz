import { StatusBar } from "expo-status-bar";

import { HealthScreen } from "./src/features/health/HealthScreen";

export default function App() {
  return (
    <>
      <HealthScreen />
      <StatusBar style="dark" />
    </>
  );
}
