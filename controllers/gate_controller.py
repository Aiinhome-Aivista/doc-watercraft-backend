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
    vehicle_id = request.args.get("vehicle_id") 
    party_id = request.args.get("party_id")       
    status = request.args.get("status")

    # pagination
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc(
            "sp_get_gate_entries",
            (
                int(vessel_id) if vessel_id else None,
                status if status else None,
                per_page,
                offset
            )
        )

        result_sets = list(cursor.stored_results())

        # ✅ COUNT
        count_result = result_sets[0].fetchone()
        total = count_result[0] if count_result else 0

        # ✅ DATA
        data_result = result_sets[1]
        cols = [c[0] for c in data_result.description]
        rows = [_row(r, cols) for r in data_result.fetchall()]

        # ✅ OPTIONAL FILTERS (post-filtering if needed)
        if vehicle_id:
            rows = [r for r in rows if r.get("vehicle_id") == int(vehicle_id)]

        if party_id:
            rows = [r for r in rows if r.get("party_id") == int(party_id)]

        return jsonify({
            "success": True,
            "data": rows,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": (total + per_page - 1) // per_page
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()
# ---------- CREATE gate entry ----------
def create_gate_entry():
    data = request.get_json()

    # ✅ Updated required fields
    required = ["party_id", "challan_invoice_no", "vehicle_id", "gate_in_datetime"]
    missing = [f for f in required if not data.get(f)]

    if missing:
        return jsonify({
            "success": False,
            "message": f"Missing: {', '.join(missing)}"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # ✅ Call updated stored procedure
        cursor.callproc("sp_create_gate_entry", (
            data["party_id"],
            data["challan_invoice_no"],
            data["vehicle_id"],
            data["gate_in_datetime"],
            data.get("weighment_slip_no"),
            data.get("outside_payment_slip"),
            data.get("outside_weight"),   # ✅ NEW
            int(data.get("own_weighbridge", 0)),
            data.get("direction")
        ))

        result = list(cursor.stored_results())[0]

        cols = [c[0] for c in result.description]
        row = result.fetchone()

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Gate entry created successfully",
            "data": _row(row, cols)
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()
# ---------- Gate Out ----------
def gate_out(gate_id):
    data = request.get_json()
    gate_out_dt = data.get("gate_out_datetime")

    if not gate_out_dt:
        return jsonify({
            "success": False,
            "message": "gate_out_datetime required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc("sp_gate_out", (
            gate_id,
            gate_out_dt
        ))

        result = list(cursor.stored_results())[0]

        cols = [c[0] for c in result.description]
        row = result.fetchone()

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Gate-out recorded successfully",
            "data": _row(row, cols)
        }), 200

    except Exception as e:
        conn.rollback()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()

# ---------- WBIN ----------
def create_wbin():
    data = request.get_json()

    required = ["gate_entry_id", "weighment_slip_no", "wbin_datetime"]
    missing = [f for f in required if not data.get(f)]

    if missing:
        return jsonify({
            "success": False,
            "message": f"Missing: {', '.join(missing)}"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc("sp_create_wbin", (
            data["gate_entry_id"],
            data["weighment_slip_no"],
            data["wbin_datetime"],
            data.get("gross_weight"),
            data.get("tare_weight")
        ))

        result = list(cursor.stored_results())[0]

        cols = [c[0] for c in result.description]
        row = result.fetchone()

        conn.commit()

        return jsonify({
            "success": True,
            "message": "WBIN recorded successfully",
            "data": _row(row, cols)
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()

# ---------- Cargo Operation (Loading/Unloading) ----------
def get_cargo_operation(operation_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc("sp_get_cargo_operation", (operation_id,))
        result = list(cursor.stored_results())[0]

        row = result.fetchone()

        if not row:
            return jsonify({
                "success": False,
                "message": "Cargo operation not found"
            }), 404

        cols = [c[0] for c in result.description]
        data = _row(row, cols)

        return jsonify({
            "success": True,
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()


def create_cargo_operation():
    data = request.get_json()

    required = ["gate_entry_id", "vessel_id", "operation_type"]
    missing = [f for f in required if not data.get(f)]

    if missing:
        return jsonify({
            "success": False,
            "message": f"Missing: {', '.join(missing)}"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc("sp_create_cargo_operation", (
            data["gate_entry_id"],
            data["vessel_id"],
            data["operation_type"],
            data.get("start_datetime"),
            data.get("end_datetime"),
            data.get("compressor_no"),
            data.get("remarks")
        ))

        result = list(cursor.stored_results())[0]

        cols = [c[0] for c in result.description]
        row = result.fetchone()

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Cargo operation created successfully",
            "data": _row(row, cols)
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()


def update_cargo_operation(operation_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data provided"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc("sp_update_cargo_operation", (
            operation_id,
            data.get("start_datetime"),
            data.get("end_datetime"),
            data.get("compressor_no"),
            data.get("remarks")
        ))

        result = list(cursor.stored_results())[0]

        row = result.fetchone()
        cols = [c[0] for c in result.description]

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Operation updated successfully",
            "data": _row(row, cols)
        }), 200

    except Exception as e:
        conn.rollback()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()       

# ---------- WBOUT ----------
def create_wbout():
    data = request.get_json()

    required = ["gate_entry_id", "weighment_slip_no", "wbout_datetime"]
    missing = [f for f in required if not data.get(f)]

    if missing:
        return jsonify({
            "success": False,
            "message": f"Missing: {', '.join(missing)}"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc("sp_create_wbout", (
            data["gate_entry_id"],
            data["weighment_slip_no"],
            data["wbout_datetime"],
            data.get("gross_weight"),
            data.get("tare_weight")
        ))

        result = list(cursor.stored_results())[0]

        cols = [c[0] for c in result.description]
        row = result.fetchone()

        conn.commit()

        return jsonify({
            "success": True,
            "message": "WBOUT recorded successfully",
            "data": _row(row, cols)
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()

# ---------- GET weighments for a gate entry ----------
def get_weighments(gate_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc("sp_get_weighments", (gate_id,))
        results = list(cursor.stored_results())

        # ======================
        # WBIN
        # ======================
        wbin_res = results[0]
        wbin_row = wbin_res.fetchone()
        wbin_cols = [c[0] for c in wbin_res.description]
        wbin = _row(wbin_row, wbin_cols) if wbin_row else None

        # ======================
        # WBOUT
        # ======================
        wbout_res = results[1]
        wbout_row = wbout_res.fetchone()
        wbout_cols = [c[0] for c in wbout_res.description]
        wbout = _row(wbout_row, wbout_cols) if wbout_row else None

        # ======================
        # OPERATIONS
        # ======================
        op_res = results[2]
        op_cols = [c[0] for c in op_res.description]
        operations = [_row(r, op_cols) for r in op_res.fetchall()]

        return jsonify({
            "success": True,
            "data": {
                "wbin": wbin,
                "wbout": wbout,
                "operations": operations
            }
        }), 200

    finally:
        cursor.close()
        conn.close()