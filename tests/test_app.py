from app import app
import database

def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"AutoCare AI" in response.data


def test_supported_vehicle(monkeypatch):
    monkeypatch.setattr(
        "app.validate_vehicle", lambda *args: True
    )

    monkeypatch.setattr(
        "app.get_vehicle_id", lambda *args: 1
    )

    monkeypatch.setattr(
        "app.list_tasks_for_vehicle",
        lambda vehicle_id: [
            {
                "id": 1,
                "name": "Engine Oil Change",
                "description": "Replacing engine oil."
            }
        ]
    )

    client = app.test_client()

    response = client.post("/check-vehicle", data={
        "make": "Opel",
        "model": "Astra",
        "year": "2015",
        "engine": "1.3 CDTI"
    })

    assert response.status_code == 200
    assert b"Engine Oil Change" in response.data


def test_unsupported_vehicle(monkeypatch):
    monkeypatch.setattr(
        "app.get_vehicle_id", lambda *args: 1
    )

    client = app.test_client()

    response = client.post("/check-vehicle", data={
        "make": "Ferrari",
        "model": "488",
        "year": "2018",
        "engine": "3.9 V8"
    })

    assert b"Vehicle not supported" in response.data

def test_complete_maintenance_journey(tmp_path, monkeypatch):

    monkeypatch.setattr(
        database, "DB_NAME",
        str(tmp_path / "integration.db")
    )

    database.create_database()

    database.add_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI"
    )

    vehicle_id = database.find_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI"
    )[0]

    database.add_maintenance_task(
        "Engine Oil Change",
        "Replacing engine oil."
    )

    task_id = database.get_maintenance_tasks()[0][0]

    database.link_vehicle_task(vehicle_id, task_id)

    database.add_specification(
        vehicle_id, task_id,
        "Synthetic Verified Specification",
        "100", "units",
        "Integration test source",
        verified=True
    )

    database.add_specification(
        vehicle_id, task_id,
        "Synthetic Unverified Specification",
        "200", "units",
        "Integration test source",
        verified=False
    )

    client = app.test_client()

    vehicle_details = {
        "make": "Opel",
        "model": "Astra",
        "year": "2015",
        "engine": "1.3 CDTI"
    }

    response = client.post(
        "/check-vehicle",
        data=vehicle_details
    )

    assert response.status_code == 200
    assert b"Engine Oil Change" in response.data

    response = client.post(
        "/maintenance-guide",
        data={
            **vehicle_details,
            "task_id": task_id
        }
    )

    assert response.status_code == 200
    assert b"Synthetic Verified Specification" in response.data
    assert b"Synthetic Unverified Specification" not in response.data
    assert b"Maintenance Overview" in response.data