from app import app
import database
import pytest

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


@pytest.mark.parametrize("invalid_year", [
    "abc",
    "",
    "2015.5",
    "unknown",
    "!"
])
def test_invalid_vehicle_year(invalid_year):
    client = app.test_client()

    response = client.post("/check-vehicle", data={
        "make": "Opel",
        "model": "Astra",
        "year": invalid_year,
        "engine": "1.3 CDTI (A13DTE)"
    })

    assert response.status_code == 400


@pytest.mark.parametrize("invalid_task", [
    "abc",
    "",
    "1.5",
    "unknown",
    "!"
])
def test_invalid_maintenance_task_id(invalid_task):
    client = app.test_client()

    response = client.post("/maintenance-guide", data={
        "make": "Opel",
        "model": "Astra",
        "year": "2015",
        "engine": "1.3 CDTI (A13DTE)",
        "task_id": invalid_task
    })

    assert response.status_code == 400


def test_unsupported_vehicle_guide(monkeypatch):
    monkeypatch.setattr(
        "app.validate_vehicle",
        lambda *args: False
    )

    client = app.test_client()

    response = client.post("/maintenance-guide", data={
        "make": "BMW",
        "model": "320d",
        "year": "2020",
        "engine": "2.0 Diesel",
        "task_id": "1"
    })

    assert response.status_code == 400
    assert b"Vehicle not supported" in response.data


@pytest.mark.parametrize("task_id", [
    "999",
    "-1",
    "0"
])
def test_unavailable_maintenance_task(monkeypatch, task_id):
    monkeypatch.setattr(
        "app.validate_vehicle",
        lambda *args: True
    )

    monkeypatch.setattr(
        "app.get_vehicle_id",
        lambda *args: (1,)
    )

    monkeypatch.setattr(
        "app.list_tasks_for_vehicle",
        lambda *args: [
            {
                "id": 1,
                "name": "Engine Oil Change",
                "description": "Replace engine oil"
            }
        ]
    )

    client = app.test_client()

    response = client.post("/maintenance-guide", data={
        "make": "Opel",
        "model": "Astra",
        "year": "2015",
        "engine": "1.3 CDTI (A13DTE)",
        "task_id": task_id
    })

    assert response.status_code == 404


def test_vehicle_id_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.validate_vehicle", lambda *args: True
    )

    monkeypatch.setattr(
        "app.get_vehicle_id", lambda *args: None
    )

    client = app.test_client()

    response = client.post("/check-vehicle", data={
        "make": "Opel",
        "model": "Astra",
        "year": "2015",
        "engine": "1.3 CDTI (A13DTE)"
    })

    assert response.status_code == 400
    assert b"Vehicle not supported" in response.data


def test_vehicle_has_no_maintenance_tasks(monkeypatch):
    monkeypatch.setattr(
        "app.validate_vehicle", lambda *args: True
    )

    monkeypatch.setattr(
        "app.get_vehicle_id", lambda *args: 1
    )

    monkeypatch.setattr(
        "app.list_tasks_for_vehicle", lambda *args: []
    )

    client = app.test_client()

    response = client.post("/check-vehicle", data={
        "make": "Opel",
        "model": "Astra",
        "year": "2015",
        "engine": "1.3 CDTI (A13DTE)"
    })

    assert response.status_code == 200
    assert b"No maintenance tasks available" in response.data


def test_guide_vehicle_id_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.validate_vehicle", lambda *args: True
    )

    monkeypatch.setattr(
        "app.get_vehicle_id", lambda *args: None
    )

    client = app.test_client()

    response = client.post("/maintenance-guide", data={
        "make": "Opel",
        "model": "Astra",
        "year": "2015",
        "engine": "1.3 CDTI (A13DTE)",
        "task_id": "1"
    })

    assert response.status_code == 400
    assert b"Vehicle not supported" in response.data