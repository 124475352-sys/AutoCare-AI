from ai_guide import MockAIGuide


def test_generate_guide():
    ai = MockAIGuide()

    vehicle = {
        "make": "Opel",
        "model": "Astra",
        "year": 2015,
        "engine": "1.3 CDTI"
    }

    task = {
        "name": "Engine Oil Change",
        "description": "Replacing engine oil."
    }

    guide = ai.generate_guide(vehicle, task, {})

    assert "Opel Astra" in guide
    assert "2015" in guide
    assert "1.3 CDTI" in guide
    assert "Engine Oil Change" in guide


def test_missing_specifications():
    ai = MockAIGuide()

    vehicle = {
        "make": "Opel",
        "model": "Astra",
        "year": 2015,
        "engine": "1.3 CDTI"
    }

    task = {
        "name": "Engine Oil Change",
        "description": "Replacing engine oil."
    }

    guide = ai.generate_guide(vehicle, task, {})

    assert "have not yet been verified" in guide
    assert "official vehicle service manual" in guide


def test_guide_contains_safety_precautions():
    vehicle = {
        "make": "Opel",
        "model": "Astra",
        "year": 2015,
        "engine": "1.3 CDTI (A13DTE)"
    }

    task = {
        "name": "Engine Oil Change",
        "description": "Replace engine oil"
    }

    guide = MockAIGuide().generate_guide(vehicle, task, [])

    assert "Safety Precautions" in guide
    assert "protective equipment" in guide
    assert "safely secured" in guide


def test_guide_identifies_mock_implementation():
    vehicle = {
        "make": "Opel",
        "model": "Astra",
        "year": 2015,
        "engine": "1.3 CDTI (A13DTE)"
    }

    task = {
        "name": "Air Filter Replacement",
        "description": "Replace air filter"
    }

    guide = MockAIGuide().generate_guide(vehicle, task, [])

    assert "mock AI component" in guide
    assert "not a complete repair procedure" in guide


def test_guide_with_verified_specifications():
    vehicle = {
        "make": "Opel",
        "model": "Astra",
        "year": 2015,
        "engine": "1.3 CDTI (A13DTE)"
    }

    task = {
        "name": "Engine Oil Change",
        "description": "Replace engine oil"
    }

    specifications = [
        {
            "name": "Test Capacity",
            "value": "100",
            "unit": "units",
            "source": "Test Source"
        }
    ]

    guide = MockAIGuide().generate_guide(
        vehicle, task, specifications
    )

    assert "verified technical specifications" in guide
    assert "have not yet been verified" not in guide
    assert "100 units" not in guide