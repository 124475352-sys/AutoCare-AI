from database import find_vehicle
from database import get_all_vehicles

def get_vehicle_id(make, model, year, engine):
    vehicle = find_vehicle(make, model, year, engine)

    if vehicle is None:
        return None

    return vehicle[0]

def validate_vehicle(make, model, year, engine):
    vehicle = find_vehicle(make, model, year, engine)

    return vehicle is not None

def list_supported_vehicles():
    vehicles = get_all_vehicles()

    return [
        {
            "make": vehicle[0],
            "model": vehicle[1],
            "year": vehicle[2],
            "engine": vehicle[3]
        }
        for vehicle in vehicles
    ]

if __name__ == "__main__":
    print(
        "Vehicle supported:",
        validate_vehicle("Opel", "Astra", 2015, "1.3 CDTI")
    )

    print(
        "Vehicle supported:",
        validate_vehicle("Ferrari", "Astra", 2015, "1.3 CDTI")
    )
