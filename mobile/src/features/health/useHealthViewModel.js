import { useCallback, useEffect, useState } from "react";

import { API_URL } from "../../api/client";
import { getHealthStatus } from "./healthService";

export function useHealthViewModel() {
  const [connectionState, setConnectionState] = useState("checking");
  const [serviceName, setServiceName] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  const checkConnection = useCallback(async () => {
    setConnectionState("checking");
    setErrorMessage(null);

    try {
      const health = await getHealthStatus();
      setServiceName(health.service);
      setConnectionState("connected");
    } catch (error) {
      setServiceName(null);
      setConnectionState("error");
      setErrorMessage(error instanceof Error ? error.message : "No fue posible conectar con la API.");
    }
  }, []);

  useEffect(() => {
    void checkConnection();
  }, [checkConnection]);

  return {
    apiUrl: API_URL,
    connectionState,
    errorMessage,
    isChecking: connectionState === "checking",
    isConnected: connectionState === "connected",
    serviceName,
    checkConnection
  };
}
