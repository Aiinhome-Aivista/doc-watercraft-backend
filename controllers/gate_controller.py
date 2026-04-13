from flask import request, jsonify
from database.db_connection import get_db_connection
from datetime import datetime


def _row(row, keys):
    d = dict(zip(keys, row))
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
    return d


# ---------- GET all gate entries ----------
def get_gate_entries():
    vessel_id = request.args.get("vessel_id")
    status = request.args.get("status")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = """
            SELECT ge.*, v.vessel_name, v.party_name, v.direction
            FROM gate_entries ge
            JOIN vessels v ON ge.vessel_id = v.id
            WHERE 1=1
        """
        params = []
        if vessel_id:
            sql += " AND ge.vessel_id = %s"
            params.append(vessel_id)
        if status:
            sql += " AND ge.status = %s"
            params.append(status)
        sql += " ORDER BY ge.gate_in_datetime DESC"
        cursor.execute(sql, params)
        cols = [c[0] for c in cursor.description]
        rows = [_row(r, cols) for r in cursor.fetchall()]
        return jsonify({"success": True, "data": rows}), 200
    finally:
        cursor.close()
        conn.close()


# ---------- CREATE gate entry ----------
def create_gate_entry():
    data = request.get_json()
    required = ["vessel_id", "consignor_name", "challan_invoice_no", "vehicle_no", "gate_in_datetime"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"success": False, "message": f"Missing: {', '.join(missing)}"}), 400

    own_wb = int(data.get("own_weighbridge", 0))
    initial_status = "PENDING_WBOUT" if own_wb else "PENDING_WBIN"

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO gate_entries
              (vessel_id, consignor_name, challan_invoice_no, vehicle_no,
               transporter_name, weighment_slip_no, own_weighbridge,
               gate_in_datetime, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data["vessel_id"], data["consignor_name"], data["challan_invoice_no"],
            data["vehicle_no"], data.get("transporter_name"), data.get("weighment_slip_no"),
            own_wb, data["gate_in_datetime"], initial_status
        ))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute("""
            SELECT ge.*, v.vessel_name, v.party_name, v.direction
            FROM gate_entries ge JOIN vessels v ON ge.vessel_id = v.id
            WHERE ge.id = %s
        """, (new_id,))
        cols = [c[0] for c in cursor.description]
        return jsonify({"success": True, "data": _row(cursor.fetchone(), cols), "message": "Gate entry created"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ---------- Gate Out ----------
def gate_out(gate_id):
    data = request.get_json()
    gate_out_dt = data.get("gate_out_datetime")
    if not gate_out_dt:
        return jsonify({"success": False, "message": "gate_out_datetime required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE gate_entries SET gate_out_datetime=%s, status='COMPLETED' WHERE id=%s",
                       (gate_out_dt, gate_id))
        conn.commit()
        return jsonify({"success": True, "message": "Gate-out recorded"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ---------- WBIN ----------
def create_wbin():
    data = request.get_json()
    required = ["gate_entry_id", "weighment_slip_no", "wbin_datetime"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"success": False, "message": f"Missing: {', '.join(missing)}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT status FROM gate_entries WHERE id = %s", (data["gate_entry_id"],))
        row = cursor.fetchone()
        if not row:
            return jsonify({"success": False, "message": "Gate entry not found"}), 404
        if row[0] != "PENDING_WBIN":
            return jsonify({"success": False, "message": f"Entry status is {row[0]}, not PENDING_WBIN"}), 400

        cursor.execute("""
            INSERT INTO wbin_records (gate_entry_id, weighment_slip_no, wbin_datetime, gross_weight, tare_weight)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            data["gate_entry_id"], data["weighment_slip_no"], data["wbin_datetime"],
            data.get("gross_weight"), data.get("tare_weight")
        ))
        cursor.execute("UPDATE gate_entries SET status='WBIN_DONE' WHERE id=%s", (data["gate_entry_id"],))
        conn.commit()
        return jsonify({"success": True, "message": "WBIN recorded"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ---------- Cargo Operation (Loading/Unloading) ----------
def create_cargo_operation():
    data = request.get_json()
    required = ["gate_entry_id", "operation_type", "start_datetime"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"success": False, "message": f"Missing: {', '.join(missing)}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO cargo_operations (gate_entry_id, operation_type, start_datetime, end_datetime, compressor_no, remarks)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            data["gate_entry_id"], data["operation_type"], data["start_datetime"],
            data.get("end_datetime"), data.get("compressor_no"), data.get("remarks")
        ))
        cursor.execute("UPDATE gate_entries SET status='UNLOADING' WHERE id=%s", (data["gate_entry_id"],))
        conn.commit()
        return jsonify({"success": True, "message": "Operation recorded"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ---------- WBOUT ----------
def create_wbout():
    data = request.get_json()
    required = ["gate_entry_id", "weighment_slip_no", "wbout_datetime"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"success": False, "message": f"Missing: {', '.join(missing)}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO wbout_records (gate_entry_id, weighment_slip_no, wbout_datetime, gross_weight, tare_weight)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            data["gate_entry_id"], data["weighment_slip_no"], data["wbout_datetime"],
            data.get("gross_weight"), data.get("tare_weight")
        ))
        cursor.execute("UPDATE gate_entries SET status='COMPLETED' WHERE id=%s", (data["gate_entry_id"],))
        conn.commit()
        return jsonify({"success": True, "message": "WBOUT recorded"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ---------- GET weighments for a gate entry ----------
def get_weighments(gate_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        result = {}
        cursor.execute("SELECT * FROM wbin_records WHERE gate_entry_id=%s", (gate_id,))
        cols = [c[0] for c in cursor.description]
        row = cursor.fetchone()
        result["wbin"] = _row(row, cols) if row else None

        cursor.execute("SELECT * FROM wbout_records WHERE gate_entry_id=%s", (gate_id,))
        cols = [c[0] for c in cursor.description]
        row = cursor.fetchone()
        result["wbout"] = _row(row, cols) if row else None

        cursor.execute("SELECT * FROM cargo_operations WHERE gate_entry_id=%s", (gate_id,))
        cols = [c[0] for c in cursor.description]
        result["operations"] = [_row(r, cols) for r in cursor.fetchall()]

        return jsonify({"success": True, "data": result}), 200
    finally:
        cursor.close()
        conn.close()
