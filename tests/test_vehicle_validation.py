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