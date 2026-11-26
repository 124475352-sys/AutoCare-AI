from maintenance_data import list_tasks_for_vehicle
import pytest

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

from maintenance_data import (
    list_maintenance_tasks,
    list_specifications
)


def test_list_all_maintenance_tasks(monkeypatch):
    monkeypatch.setattr(
        "maintenance_data.get_maintenance_tasks",
        lambda: [
            (1, "Engine Oil Change", "Replace engine oil"),
            (2, "Air Filter Replacement", "Replace air filter")
        ]
    )

    tasks = list_maintenance_tasks()

    assert len(tasks) == 2
    assert tasks[0]["id"] == 1
    assert tasks[0]["name"] == "Engine Oil Change"
    assert tasks[1]["name"] == "Air Filter Replacement"


def test_empty_maintenance_tasks(monkeypatch):
    monkeypatch.setattr(
        "maintenance_data.get_maintenance_tasks",
        lambda: []
    )

    assert list_maintenance_tasks() == []


def test_list_specifications(monkeypatch):
    monkeypatch.setattr(
        "maintenance_data.get_specifications",
        lambda vehicle_id, task_id: [
            ("Test Capacity", "3.5", "L", "Test Source")
        ]
    )

    specifications = list_specifications(1, 1)

    assert len(specifications) == 1
    assert specifications[0]["name"] == "Test Capacity"
    assert specifications[0]["value"] == "3.5"
    assert specifications[0]["unit"] == "L"
    assert specifications[0]["source"] == "Test Source"


def test_no_specifications_available(monkeypatch):
    monkeypatch.setattr(
        "maintenance_data.get_specifications",
        lambda vehicle_id, task_id: []
    )

    assert list_specifications(1, 1) == []