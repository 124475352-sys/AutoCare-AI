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


def test_duplicate_maintenance_task(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DB_NAME", str(tmp_path / "test.db")
    )

    database.create_database()

    database.add_maintenance_task(
        "Engine Oil Change", "Replace engine oil"
    )

    database.add_maintenance_task(
        "Engine Oil Change", "Replace engine oil"
    )

    tasks = database.get_maintenance_tasks()

    assert len(tasks) == 1


def test_duplicate_vehicle_task_link(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DB_NAME", str(tmp_path / "test.db")
    )

    database.create_database()

    database.add_vehicle("Opel", "Astra", 2015, "1.3 CDTI")

    vehicle_id = database.find_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI"
    )[0]

    database.add_maintenance_task(
        "Engine Oil Change", "Replace engine oil"
    )

    task_id = database.get_maintenance_tasks()[0][0]

    database.link_vehicle_task(vehicle_id, task_id)
    database.link_vehicle_task(vehicle_id, task_id)

    tasks = database.get_tasks_for_vehicle(vehicle_id)

    assert len(tasks) == 1


def test_empty_vehicle_database(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DB_NAME", str(tmp_path / "test.db")
    )

    database.create_database()

    assert database.get_all_vehicles() == []


def test_empty_maintenance_database(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DB_NAME", str(tmp_path / "test.db")
    )

    database.create_database()

    assert database.get_maintenance_tasks() == []


def test_update_existing_specification(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DB_NAME", str(tmp_path / "test.db")
    )

    database.create_database()

    database.add_vehicle("Opel", "Astra", 2015, "1.3 CDTI")

    vehicle_id = database.find_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI"
    )[0]

    database.add_maintenance_task(
        "Engine Oil Change", "Replace engine oil"
    )

    task_id = database.get_maintenance_tasks()[0][0]

    database.link_vehicle_task(vehicle_id, task_id)

    database.add_specification(
        vehicle_id, task_id, "Test Capacity",
        "100", "units", "Test Source", verified=True
    )

    database.add_specification(
        vehicle_id, task_id, "Test Capacity",
        "200", "units", "Updated Source", verified=True
    )

    specifications = database.get_specifications(
        vehicle_id, task_id
    )

    assert len(specifications) == 1
    assert specifications[0][1] == "200"
    assert specifications[0][3] == "Updated Source"


def test_unverified_specification_excluded(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DB_NAME", str(tmp_path / "test.db")
    )

    database.create_database()

    database.add_vehicle("Opel", "Astra", 2015, "1.3 CDTI")

    vehicle_id = database.find_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI"
    )[0]

    database.add_maintenance_task(
        "Engine Oil Change", "Replace engine oil"
    )

    task_id = database.get_maintenance_tasks()[0][0]

    database.link_vehicle_task(vehicle_id, task_id)

    database.add_specification(
        vehicle_id, task_id, "Test Capacity",
        "100", "units", "Test Source", verified=True
    )

    database.add_specification(
        vehicle_id, task_id, "Test Capacity",
        "100", "units", "Test Source", verified=False
    )

    assert database.get_specifications(
        vehicle_id, task_id
    ) == []


def test_update_engine_name(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DB_NAME", str(tmp_path / "test.db")
    )

    database.create_database()

    database.add_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI"
    )

    database.update_engine_name()

    assert database.find_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI"
    ) is None

    assert database.find_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI (A13DTE)"
    ) is not None


def test_engine_update_preserves_other_vehicles(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DB_NAME", str(tmp_path / "test.db")
    )

    database.create_database()

    database.add_vehicle(
        "Opel", "Astra", 2014, "1.3 CDTI"
    )

    database.update_engine_name()

    assert database.find_vehicle(
        "Opel", "Astra", 2014, "1.3 CDTI"
    ) is not None