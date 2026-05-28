from fastapi.testclient import TestClient


def test_create_and_list_medications(client: TestClient):
    create_response = client.post(
        "/medications",
        json={"name": "Metformina", "dose_label": "500 mg"},
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] == 1
    assert created["name"] == "Metformina"
    assert created["dose_label"] == "500 mg"
    assert "created_at" in created
    assert "updated_at" in created

    list_response = client.get("/medications")

    assert list_response.status_code == 200
    assert list_response.json() == [created]


def test_get_patch_and_delete_medication(client: TestClient):
    create_response = client.post(
        "/medications",
        json={"name": "Losartan", "dose_label": "50 mg"},
    )
    assert create_response.status_code == 201
    medication = create_response.json()

    get_response = client.get(f"/medications/{medication['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Losartan"

    patch_response = client.patch(
        f"/medications/{medication['id']}",
        json={"dose_label": "100 mg"},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["dose_label"] == "100 mg"

    delete_response = client.delete(f"/medications/{medication['id']}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/medications/{medication['id']}")
    assert missing_response.status_code == 404


def test_medication_rejects_blank_fields(client: TestClient):
    response = client.post(
        "/medications",
        json={"name": "   ", "dose_label": "500 mg"},
    )

    assert response.status_code == 400
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert detail[0]["loc"] == ["body", "name"]
