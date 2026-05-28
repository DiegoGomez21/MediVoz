from fastapi.testclient import TestClient


def test_health_endpoint_reports_service_status(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "medivoz-api"}
