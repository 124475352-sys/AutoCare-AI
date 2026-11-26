import database


def test_add_and_find_vehicle(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DB_NAME",
        str(tmp_path / "test.db")
    )

    database.create_database()

    database.add_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI"
    )

    vehicle = database.find_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI"
    )

    assert vehicle is not None


def test_case_insensitive_search(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DB_NAME",
        str(tmp_path / "test.db")
    )

    database.create_database()

    database.add_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI"
    )

    vehicle = database.find_vehicle(
        "opel", "astra", 2015, "1.3 cdti"
    )

    assert vehicle is not None


def test_vehicle_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DB_NAME",
        str(tmp_path / "test.db")
    )

    database.create_database()

    vehicle = database.find_vehicle(
        "Ferrari", "488", 2018, "3.9 V8"
    )

    assert vehicle is None

def test_only_verified_specifications(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DB_NAME",
        str(tmp_path / "test.db")
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
        "Test Specification A", "100", "units",
        "Synthetic test source",
        verified=True
    )

    database.add_specification(
        vehicle_id, task_id,
        "Test Specification B", "200", "units",
        "Synthetic test source",
        verified=False
    )

    specifications = database.get_specifications(
        vehicle_id, task_id
    )

    assert len(specifications) == 1
    assert specifications[0][0] == "Test Specification A"