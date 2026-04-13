from flask import request, jsonify
from database.db_connection import get_db_connection
from datetime import datetime


def _vessel_row(row, keys):
    d = dict(zip(keys, row))
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
    return d


# ---------- GET all vessels ----------
def get_vessels():
    status_filter = request.args.get("status")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if status_filter:
            cursor.execute("SELECT * FROM vessels WHERE status = %s ORDER BY created_at DESC", (status_filter,))
        else:
            cursor.execute("SELECT * FROM vessels ORDER BY created_at DESC")
        cols = [c[0] for c in cursor.description]
        rows = [_vessel_row(r, cols) for r in cursor.fetchall()]
        return jsonify({"success": True, "data": rows}), 200
    finally:
        cursor.close()
        conn.close()


# ---------- GET single vessel ----------
def get_vessel(vessel_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM vessels WHERE id = %s", (vessel_id,))
        cols = [c[0] for c in cursor.description]
        row = cursor.fetchone()
        if not row:
            return jsonify({"success": False, "message": "Vessel not found"}), 404
        return jsonify({"success": True, "data": _vessel_row(row, cols)}), 200
    finally:
        cursor.close()
        conn.close()


# ---------- CREATE vessel ----------
def create_vessel():
    data = request.get_json()
    required = ["vessel_name", "party_name", "cargo_type", "quantity", "direction", "expected_date"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"success": False, "message": f"Missing fields: {', '.join(missing)}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO vessels (vessel_name, party_name, cargo_type, quantity, direction, expected_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data["vessel_name"], data["party_name"], data["cargo_type"],
            data["quantity"], data["direction"], data["expected_date"]
        ))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM vessels WHERE id = %s", (new_id,))
        cols = [c[0] for c in cursor.description]
        row = cursor.fetchone()
        return jsonify({"success": True, "data": _vessel_row(row, cols), "message": "Vessel created"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ---------- BERTH vessel ----------
def berth_vessel(vessel_id):
    data = request.get_json()
    berthing_datetime = data.get("berthing_datetime")
    if not berthing_datetime:
        return jsonify({"success": False, "message": "berthing_datetime is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT status FROM vessels WHERE id = %s", (vessel_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"success": False, "message": "Vessel not found"}), 404
        if row[0] != "PLANNED":
            return jsonify({"success": False, "message": f"Vessel already in status: {row[0]}"}), 400

        cursor.execute(
            "UPDATE vessels SET status='BERTHED', berthing_datetime=%s WHERE id=%s",
            (berthing_datetime, vessel_id)
        )
        conn.commit()
        return jsonify({"success": True, "message": "Vessel berthed successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ---------- MOOR vessel ----------
def moor_vessel(vessel_id):
    data = request.get_json()
    mooring_datetime = data.get("mooring_datetime")
    if not mooring_datetime:
        return jsonify({"success": False, "message": "mooring_datetime is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT status FROM vessels WHERE id = %s", (vessel_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"success": False, "message": "Vessel not found"}), 404
        if row[0] != "BERTHED":
            return jsonify({"success": False, "message": f"Vessel must be BERTHED first, current: {row[0]}"}), 400

        cursor.execute(
            "UPDATE vessels SET status='MOORED', mooring_datetime=%s WHERE id=%s",
            (mooring_datetime, vessel_id)
        )
        conn.commit()
        return jsonify({"success": True, "message": "Vessel moored successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ---------- SURVEY vessel ----------
def survey_vessel(vessel_id):
    data = request.get_json()
    survey_quantity = data.get("survey_quantity")
    survey_datetime = data.get("survey_datetime")
    if not survey_quantity or not survey_datetime:
        return jsonify({"success": False, "message": "survey_quantity and survey_datetime are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT status FROM vessels WHERE id = %s", (vessel_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"success": False, "message": "Vessel not found"}), 404

        cursor.execute(
            "UPDATE vessels SET survey_quantity=%s, survey_datetime=%s WHERE id=%s",
            (survey_quantity, survey_datetime, vessel_id)
        )
        conn.commit()
        return jsonify({"success": True, "message": "Survey recorded"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ---------- UNBERTH / Complete vessel ----------
def unberth_vessel(vessel_id):
    data = request.get_json()
    sailing_datetime = data.get("sailing_datetime")
    if not sailing_datetime:
        return jsonify({"success": False, "message": "sailing_datetime is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT status FROM vessels WHERE id = %s", (vessel_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"success": False, "message": "Vessel not found"}), 404
        if row[0] not in ("BERTHED", "MOORED"):
            return jsonify({"success": False, "message": f"Cannot unberth vessel in status: {row[0]}"}), 400

        cursor.execute(
            "UPDATE vessels SET status='COMPLETED', sailing_datetime=%s WHERE id=%s",
            (sailing_datetime, vessel_id)
        )
        conn.commit()
        return jsonify({"success": True, "message": "Vessel unberthed and completed"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ---------- GET billing for vessel ----------
def get_vessel_billing(vessel_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM v_vessel_billing WHERE vessel_id = %s", (vessel_id,))
        cols = [c[0] for c in cursor.description]
        row = cursor.fetchone()
        if not row:
            return jsonify({"success": False, "message": "No billing data found"}), 404
        return jsonify({"success": True, "data": _vessel_row(row, cols)}), 200
    finally:
        cursor.close()
        conn.close()


# ---------- GET all billing (MIS report) ----------
def get_mis_report():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM v_vessel_billing ORDER BY vessel_id DESC")
        cols = [c[0] for c in cursor.description]
        rows = [_vessel_row(r, cols) for r in cursor.fetchall()]
        return jsonify({"success": True, "data": rows}), 200
    finally:
        cursor.close()
        conn.close()
