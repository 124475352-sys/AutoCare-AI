from maintenance_data import list_tasks_for_vehicle


def test_vehicle_maintenance_tasks(monkeypatch):
    monkeypatch.setattr(
        "maintenance_data.get_tasks_for_vehicle",
        lambda vehicle_id: [
            (1, "Engine Oil Change", "Replacing engine oil."),
            (2, "Air Filter Replacement", "Replacing air filter.")
        ]
    )

    tasks = list_tasks_for_vehicle(1)

    assert len(tasks) == 2
    assert tasks[0]["name"] == "Engine Oil Change"
    assert tasks[1]["name"] == "Air Filter Replacement"


def test_vehicle_with_no_tasks(monkeypatch):
    monkeypatch.setattr(
        "maintenance_data.get_tasks_for_vehicle",
        lambda vehicle_id: []
    )

    tasks = list_tasks_for_vehicle(999)

    assert tasks == []