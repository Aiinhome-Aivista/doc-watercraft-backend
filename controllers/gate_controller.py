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
            SELECT ge.*, v.vessel_name, v.party_id, v.direction,co.compressor_no,co.id as cargo_operation_id
            FROM gate_entries ge
            JOIN vessels v ON ge.vessel_id = v.id
            LEFT JOIN cargo_operations co 
            ON co.gate_entry_id = ge.id
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
            SELECT ge.*, v.vessel_name, v.party_id, v.direction
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
        # Get gate entry + vessel direction
        cursor.execute("""
            SELECT ge.status, v.direction
            FROM gate_entries ge
            JOIN vessels v ON ge.vessel_id = v.id
            WHERE ge.id = %s
        """, (data["gate_entry_id"],))

        row = cursor.fetchone()

        if not row:
            return jsonify({"success": False, "message": "Gate entry not found"}), 404

        status, direction = row

        if status != "PENDING_WBIN":
            return jsonify({
                "success": False,
                "message": f"Entry status is {status}, not PENDING_WBIN"
            }), 400

        # Apply condition
        gross_weight = None
        tare_weight = None

        if direction == "EXPORT":
            gross_weight = data.get("gross_weight")
            if not gross_weight:
                return jsonify({"success": False, "message": "gross_weight required for EXPORT"}), 400

        elif direction == "IMPORT":
            tare_weight = data.get("tare_weight")
            if not tare_weight:
                return jsonify({"success": False, "message": "tare_weight required for IMPORT"}), 400

        # Insert WBIN
        cursor.execute("""
            INSERT INTO wbin_records 
            (gate_entry_id, weighment_slip_no, wbin_datetime, gross_weight, tare_weight)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            data["gate_entry_id"],
            data["weighment_slip_no"],
            data["wbin_datetime"],
            gross_weight,
            tare_weight
        ))

        # Update status
        cursor.execute("""
            UPDATE gate_entries 
            SET status='WBIN_DONE' 
            WHERE id=%s
        """, (data["gate_entry_id"],))

        conn.commit()

        return jsonify({
            "success": True,
            "message": f"WBIN recorded for {direction}"
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# ---------- Cargo Operation (Loading/Unloading) ----------
def get_cargo_operation(operation_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, gate_entry_id, operation_type,
                   start_datetime, end_datetime,
                   compressor_no, remarks, created_at
            FROM cargo_operations
            WHERE id = %s
        """, (operation_id,))

        row = cursor.fetchone()

        if not row:
            return jsonify({
                "success": False,
                "message": "Cargo operation not found"
            }), 404

        cols = [c[0] for c in cursor.description]
        data = dict(zip(cols, row))

        return jsonify({
            "success": True,
            "data": data
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

def create_cargo_operation():
    data = request.get_json()

    required = ["gate_entry_id", "operation_type"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"success": False, "message": f"Missing: {', '.join(missing)}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        start_dt = data.get("start_datetime") or None
        end_dt = data.get("end_datetime") or None

        # ✅ Insert
        cursor.execute("""
            INSERT INTO cargo_operations 
            (gate_entry_id, operation_type, start_datetime, end_datetime, compressor_no, remarks)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            data["gate_entry_id"],
            data["operation_type"],
            start_dt,
            end_dt,
            data.get("compressor_no"),
            data.get("remarks")
        ))

        # ✅ STATUS LOGIC FIX
        if start_dt and not end_dt:
            # Operation started
            new_status = "UNLOADING"

        elif end_dt:
            # Operation completed
            new_status = "PENDING_WBOUT"

        else:
            new_status = None  # no change

        # ✅ Only update if needed
        if new_status:
            cursor.execute("""
                UPDATE gate_entries 
                SET status=%s 
                WHERE id=%s
            """, (new_status, data["gate_entry_id"]))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Operation created (status handled correctly)"
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

def update_cargo_operation(operation_id):
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)

    try:
        fields = []
        values = []

        # Track if end_datetime is updated
        end_updated = False

        if "start_datetime" in data:
            fields.append("start_datetime=%s")
            values.append(data["start_datetime"])

        if "end_datetime" in data:
            fields.append("end_datetime=%s")
            values.append(data["end_datetime"])
            end_updated = True 

        if "compressor_no" in data:
            fields.append("compressor_no=%s")
            values.append(data["compressor_no"])

        if "remarks" in data:
            fields.append("remarks=%s")
            values.append(data["remarks"])

        if not fields:
            return jsonify({"success": False, "message": "Nothing to update"}), 400

        # 🔹 Update cargo operation
        query = f"""
            UPDATE cargo_operations 
            SET {', '.join(fields)} 
            WHERE id=%s
        """
        values.append(operation_id)

        cursor.execute(query, tuple(values))

        # 🔥 If end_datetime updated → change status
        if end_updated:
            cursor.execute("""
                UPDATE gate_entries 
                SET status='PENDING_WBOUT'
                WHERE id = (
                    SELECT gate_entry_id 
                    FROM cargo_operations 
                    WHERE id = %s
                )
            """, (operation_id,))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Operation updated successfully"
        })

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
        cursor.execute("UPDATE gate_entries SET status='GATE_OUT' WHERE id=%s", (data["gate_entry_id"],))
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
