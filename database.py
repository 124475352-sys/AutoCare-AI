import sqlite3

DB_NAME = "autocare.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            engine TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_tasks
        (
            id
            INTEGER
            PRIMARY
            KEY
            AUTOINCREMENT,
            name
            TEXT
            NOT
            NULL
            UNIQUE,
            description
            TEXT
            NOT
            NULL
        )
    """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS vehicle_tasks
                   (
                       vehicle_id
                       INTEGER
                       NOT
                       NULL,
                       task_id
                       INTEGER
                       NOT
                       NULL,
                       PRIMARY
                       KEY
                   (
                       vehicle_id,
                       task_id
                   ),
                       FOREIGN KEY
                   (
                       vehicle_id
                   ) REFERENCES vehicles
                   (
                       id
                   ),
                       FOREIGN KEY
                   (
                       task_id
                   ) REFERENCES maintenance_tasks
                   (
                       id
                   )
                       )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS specifications
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       vehicle_id
                       INTEGER
                       NOT
                       NULL,
                       task_id
                       INTEGER
                       NOT
                       NULL,
                       name
                       TEXT
                       NOT
                       NULL,
                       value
                       TEXT
                       NOT
                       NULL,
                       unit
                       TEXT,
                       source
                       TEXT
                       NOT
                       NULL,
                       verified
                       INTEGER
                       NOT
                       NULL
                       DEFAULT
                       0,
                       FOREIGN
                       KEY
                   (
                       vehicle_id
                   ) REFERENCES vehicles
                   (
                       id
                   ),
                       FOREIGN KEY
                   (
                       task_id
                   ) REFERENCES maintenance_tasks
                   (
                       id
                   ),
                       UNIQUE
                   (
                       vehicle_id,
                       task_id,
                       name
                   )
                       )
                   """)

    conn.commit()
    conn.close()

def add_vehicle(make, model, year, engine):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vehicles (make, model, year, engine)
        VALUES (?, ?, ?, ?)
    """, (make, model, year, engine))

    conn.commit()
    conn.close()

def find_vehicle(make, model, year, engine):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM vehicles
        WHERE LOWER(make) = LOWER(?)
        AND LOWER(model) = LOWER(?)
        AND year = ?
        AND LOWER(engine) = LOWER(?)
    """, (make, model, year, engine))

    vehicle = cursor.fetchone()
    conn.close()

    return vehicle

def add_maintenance_task(name, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO maintenance_tasks (name, description)
        VALUES (?, ?)
    """, (name, description))

    conn.commit()
    conn.close()
def get_maintenance_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, description
        FROM maintenance_tasks
        ORDER BY name
    """)

    tasks = cursor.fetchall()
    conn.close()

    return tasks

def link_vehicle_task(vehicle_id, task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO vehicle_tasks (vehicle_id, task_id)
        VALUES (?, ?)
    """, (vehicle_id, task_id))

    conn.commit()
    conn.close()

def get_tasks_for_vehicle(vehicle_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.id, t.name, t.description
        FROM maintenance_tasks t
        JOIN vehicle_tasks vt ON t.id = vt.task_id
        WHERE vt.vehicle_id = ?
        ORDER BY t.name
    """, (vehicle_id,))

    tasks = cursor.fetchall()
    conn.close()

    return tasks

def get_all_vehicles():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT make, model, year, engine
        FROM vehicles
        ORDER BY make, model, year, engine
    """)

    vehicles = cursor.fetchall()
    conn.close()

    return vehicles

def get_specifications(vehicle_id, task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, value, unit, source
        FROM specifications
        WHERE vehicle_id = ?
        AND task_id = ?
        AND verified = 1
        ORDER BY name
    """, (vehicle_id, task_id))

    specifications = cursor.fetchall()
    conn.close()

    return specifications

def add_specification(vehicle_id, task_id, name,
                      value, unit, source, verified=False):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO specifications
        (vehicle_id, task_id, name, value, unit, source, verified)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(vehicle_id, task_id, name)
        DO UPDATE SET
            value = excluded.value,
            unit = excluded.unit,
            source = excluded.source,
            verified = excluded.verified
    """, (
        vehicle_id, task_id, name,
        value, unit, source, int(verified)
    ))

    conn.commit()
    conn.close()

def update_engine_name():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE vehicles
        SET engine = ?
        WHERE make = ?
        AND model = ?
        AND year = ?
        AND engine = ?
    """, (
        "1.3 CDTI (A13DTE)",
        "Opel",
        "Astra",
        2015,
        "1.3 CDTI"
    ))

    conn.commit()
    conn.close()

if __name__ == "__main__":

    create_database()

    vehicle = find_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI (A13DTE)"
    )

    if vehicle is None:
        add_vehicle(
            "Opel", "Astra", 2015, "1.3 CDTI (A13DTE)"
        )

    add_maintenance_task(
        "Engine Oil Change",
        "Replacing the engine oil and oil filter."
    )

    add_maintenance_task(
        "Air Filter Replacement",
        "Replacing the engine air filter."
    )

    vehicle = find_vehicle(
        "Opel", "Astra", 2015, "1.3 CDTI (A13DTE)"
    )

    vehicle_id = vehicle[0]

    for task in get_maintenance_tasks():
        if task[1] in [
            "Engine Oil Change",
            "Air Filter Replacement"
        ]:
            link_vehicle_task(vehicle_id, task[0])

    print("Database setup complete!")