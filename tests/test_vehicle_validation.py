from vehicle_validation import validate_vehicle


def test_supported_vehicle(monkeypatch):
    monkeypatch.setattr(
        "vehicle_validation.find_vehicle",
        lambda *args: (1,)
    )

    assert validate_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI"
    ) is True


def test_unsupported_vehicle(monkeypatch):
    monkeypatch.setattr(
        "vehicle_validation.find_vehicle",
        lambda *args: None
    )

    assert validate_vehicle(
        "Ferrari", "488", 2018, "3.9 V8"
    ) is False


from vehicle_validation import list_supported_vehicles


def test_list_supported_vehicles(monkeypatch):
    monkeypatch.setattr(
        "vehicle_validation.get_all_vehicles",
        lambda: [
            ("Opel", "Astra", 2015, "1.3 CDTI (A13DTE)"),
            ("Ford", "Focus", 2015, "1.6 TDCi")
        ]
    )

    vehicles = list_supported_vehicles()

    assert len(vehicles) == 2
    assert vehicles[0]["make"] == "Opel"
    assert vehicles[0]["model"] == "Astra"
    assert vehicles[0]["year"] == 2015
    assert vehicles[0]["engine"] == "1.3 CDTI (A13DTE)"
    assert vehicles[1]["make"] == "Ford"


def test_empty_supported_vehicles(monkeypatch):
    monkeypatch.setattr(
        "vehicle_validation.get_all_vehicles",
        lambda: []
    )

    assert list_supported_vehicles() == []