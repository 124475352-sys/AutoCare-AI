from database import get_maintenance_tasks
from database import get_tasks_for_vehicle
from database import get_specifications

def list_maintenance_tasks():
    tasks = get_maintenance_tasks()

    return [
        {
            "id": task[0],
            "name": task[1],
            "description": task[2]
        }
        for task in tasks
    ]

def list_tasks_for_vehicle(vehicle_id):
    tasks = get_tasks_for_vehicle(vehicle_id)

    return [
        {
            "id": task[0],
            "name": task[1],
            "description": task[2]
        }
        for task in tasks
    ]

def list_specifications(vehicle_id, task_id):
    specifications = get_specifications(vehicle_id, task_id)

    return [
        {
            "name": spec[0],
            "value": spec[1],
            "unit": spec[2],
            "source": spec[3]
        }
        for spec in specifications
    ]

if __name__ == "__main__":
    tasks = list_maintenance_tasks()

    for task in tasks:
        print(task["name"])
        print(task["description"])
        print()