from flask import request, jsonify
from database.db_connection import get_db_connection
from datetime import datetime


def _row(row, keys):
    d = dict(zip(keys, row))
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
    return d



# CREATE Vehicle
def create_vehicle():
    data = request.json
    vehicle_no = data.get("vehicle_no")
    transporter_name = data.get("transporter_name")
    active = data.get("active", 1)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO vehicle_master (vehicle_no, transporter_name, active)
            VALUES (%s, %s, %s)
        """, (vehicle_no, transporter_name, active))
        conn.commit()

        return jsonify({"message": "Vehicle created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()


# READ All Vehicles
def get_vehicles():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, vehicle_no, transporter_name, active FROM vehicle_master")
    rows = cursor.fetchall()

    columns = ["id", "vehicle_no", "transporter_name", "active"]
    data = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return jsonify(data)


# READ Single Vehicle
def get_vehicle(vehicle_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, vehicle_no, transporter_name, active
        FROM vehicle_master
        WHERE id = %s
    """, (vehicle_id,))
    
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        columns = ["id", "vehicle_no", "transporter_name", "active"]
        return jsonify(dict(zip(columns, row)))
    else:
        return jsonify({"message": "Vehicle not found"}), 404


# UPDATE Vehicle
def update_vehicle(vehicle_id):
    data = request.json
    vehicle_no = data.get("vehicle_no")
    transporter_name = data.get("transporter_name")
    active = data.get("active")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE vehicle_master
            SET vehicle_no = %s,
                transporter_name = %s,
                active = %s
            WHERE id = %s
        """, (vehicle_no, transporter_name, active, vehicle_id))

        conn.commit()
        return jsonify({"message": "Vehicle updated successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()


# DELETE Vehicle
def delete_vehicle(vehicle_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM vehicle_master WHERE id = %s", (vehicle_id,))
        conn.commit()
        return jsonify({"message": "Vehicle deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()


def toggle_vehicle_status(vehicle_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Get current status
        cursor.execute("SELECT active FROM vehicle_master WHERE id = %s", (vehicle_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"message": "Vehicle not found"}), 404

        current_status = row[0]
        new_status = 0 if current_status == 1 else 1

        # Update status
        cursor.execute("""
            UPDATE vehicle_master
            SET active = %s
            WHERE id = %s
        """, (new_status, vehicle_id))

        conn.commit()

        return jsonify({
            "message": "Vehicle status toggled successfully",
            "vehicle_id": vehicle_id,
            "new_status": new_status
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()

