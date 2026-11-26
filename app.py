from flask import Flask, request
from vehicle_validation import validate_vehicle
from vehicle_validation import get_vehicle_id
from maintenance_data import list_tasks_for_vehicle
from ai_guide import MockAIGuide
from flask import render_template
from vehicle_validation import list_supported_vehicles
from maintenance_data import list_specifications
app = Flask(__name__)


@app.route("/")
def home():
    vehicles = list_supported_vehicles()

    return render_template(
        "index.html",
        vehicles=vehicles
    )

@app.route("/check-vehicle", methods=["POST"])
def check_vehicle():
    make = request.form["make"].strip()
    model = request.form["model"].strip()
    engine = request.form["engine"].strip()

    try:
        year = int(request.form["year"])
    except ValueError:
        return "Invalid vehicle year.", 400

    if not validate_vehicle(make, model, year, engine):
        return "<h2>Vehicle not supported.</h2><a href='/'>Back</a>"

    vehicle_id = get_vehicle_id(make, model, year, engine)

    if vehicle_id is None:
        return "Vehicle not supported.", 400

    tasks = list_tasks_for_vehicle(vehicle_id)

    if not tasks:
        return """
            <h2>No maintenance tasks available for this vehicle.</h2>
            <a href="/">Back</a>
        """

    return render_template(
        "tasks.html",
        make=make,
        model=model,
        year=year,
        engine=engine,
        tasks=tasks
    )

@app.route("/maintenance-guide", methods=["POST"])
def maintenance_guide():
    make = request.form.get("make", "").strip()
    model = request.form.get("model", "").strip()
    engine = request.form.get("engine", "").strip()
    task_id = request.form.get("task_id", "")

    try:
        year = int(request.form.get("year", ""))
        task_id = int(task_id)
    except ValueError:
        return "Invalid vehicle or task details.", 400

    if not validate_vehicle(make, model, year, engine):
        return "Vehicle not supported.", 400

    vehicle_id = get_vehicle_id(make, model, year, engine)

    if vehicle_id is None:
        return "Vehicle not supported.", 400

    tasks = list_tasks_for_vehicle(vehicle_id)

    selected_task = next(
        (task for task in tasks if task["id"] == task_id),
        None
    )

    if selected_task is None:
        return "Maintenance task not found.", 404

    vehicle_details = {
        "make": make,
        "model": model,
        "year": year,
        "engine": engine
    }

    specifications = list_specifications(vehicle_id, task_id)

    ai = MockAIGuide()

    guide_text = ai.generate_guide(
        vehicle_details,
        selected_task,
        specifications
    )

    return render_template(
        "guide.html",
        make=make,
        model=model,
        year=year,
        engine=engine,
        task_name=selected_task["name"],
        guide=guide_text,
        specifications=specifications
    )
if __name__ == "__main__":
    app.run(debug=True)