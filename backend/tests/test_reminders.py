from fastapi.testclient import TestClient


def create_medication(client: TestClient, name: str = "Metformina") -> dict:
    response = client.post("/medications", json={"name": name, "dose_label": "500 mg"})
    assert response.status_code == 201
    return response.json()


def test_create_and_list_reminders(client: TestClient):
    medication = create_medication(client)

    create_response = client.post(
        "/reminders",
        json={"medication_id": medication["id"], "time_of_day": "08:30", "is_active": True},
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] == 1
    assert created["medication_id"] == medication["id"]
    assert created["time_of_day"] == "08:30"
    assert created["is_active"] is True
    assert created["medication"]["name"] == "Metformina"

    list_response = client.get("/reminders")

    assert list_response.status_code == 200
    assert list_response.json() == [created]


def test_get_patch_and_delete_reminder(client: TestClient):
    medication = create_medication(client, name="Losartan")
    create_response = client.post(
        "/reminders",
        json={"medication_id": medication["id"], "time_of_day": "07:00"},
    )
    assert create_response.status_code == 201
    reminder = create_response.json()

    get_response = client.get(f"/reminders/{reminder['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["time_of_day"] == "07:00"

    patch_response = client.patch(
        f"/reminders/{reminder['id']}",
        json={"time_of_day": "09:15", "is_active": False},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["time_of_day"] == "09:15"
    assert patch_response.json()["is_active"] is False

    delete_response = client.delete(f"/reminders/{reminder['id']}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/reminders/{reminder['id']}")
    assert missing_response.status_code == 404


def test_reminder_requires_existing_medication(client: TestClient):
    response = client.post(
        "/reminders",
        json={"medication_id": 999, "time_of_day": "08:00"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Medication does not exist"


def test_reminder_rejects_invalid_time(client: TestClient):
    medication = create_medication(client)

    response = client.post(
        "/reminders",
        json={"medication_id": medication["id"], "time_of_day": "25:90"},
    )

    assert response.status_code == 400
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert detail[0]["loc"] == ["body", "time_of_day"]


def test_today_reminders_returns_active_reminders_ordered_by_time(client: TestClient):
    medication = create_medication(client)

    client.post("/reminders", json={"medication_id": medication["id"], "time_of_day": "18:00"})
    client.post("/reminders", json={"medication_id": medication["id"], "time_of_day": "08:00"})
    client.post(
        "/reminders",
        json={"medication_id": medication["id"], "time_of_day": "06:00", "is_active": False},
    )

    response = client.get("/reminders/today")

    assert response.status_code == 200
    assert [item["time_of_day"] for item in response.json()] == ["08:00", "18:00"]


def test_mark_reminder_taken_creates_dose_log(client: TestClient):
    medication = create_medication(client)
    reminder_response = client.post(
        "/reminders",
        json={"medication_id": medication["id"], "time_of_day": "08:00"},
    )
    assert reminder_response.status_code == 201
    reminder = reminder_response.json()

    response = client.post(f"/reminders/{reminder['id']}/taken")

    assert response.status_code == 201
    dose_log = response.json()
    assert dose_log["reminder_id"] == reminder["id"]
    assert dose_log["status"] == "taken"
    assert "taken_at" in dose_log
    assert "created_at" in dose_log
