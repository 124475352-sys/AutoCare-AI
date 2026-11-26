from database import find_vehicle, add_specification
from maintenance_data import list_tasks_for_vehicle

vehicle = find_vehicle(
    "Opel", "Astra", 2015, "1.3 CDTI (A13DTE)"
)

if vehicle:
    vehicle_id = vehicle[0]

    tasks = list_tasks_for_vehicle(vehicle_id)

    for task in tasks:
        if task["name"] == "Engine Oil Change":
            source = (
                "Opel Astra J Owner's Manual, MY2015, "
                "August 2014 edition, page 308 (A13DTE ecoFlex)."
            )

            add_specification(
                vehicle_id,
                task["id"],
                "Engine Oil Capacity (Including Filter)",
                "3.5",
                "L",
                source,
                verified=True
            )

            add_specification(
                vehicle_id,
                task["id"],
                "Oil Quantity Between MIN and MAX",
                "1.0",
                "L",
                source,
                verified=True
            )

            print("Verified specifications added!")
else:
    print("Vehicle not found.")