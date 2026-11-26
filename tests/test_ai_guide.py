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