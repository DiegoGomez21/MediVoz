import { getJson } from "../../api/client";

export function getHealthStatus() {
  return getJson("/health");
}
