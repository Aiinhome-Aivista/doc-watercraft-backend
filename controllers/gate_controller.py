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
    gate_in_no = request.args.get("gate_in_no")
    vehicle_no = request.args.get("vehicle_no")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    sort_order = request.args.get("sort", "latest")

    # pagination
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        base_query = """
            FROM gate_entries ge
            LEFT JOIN party_masters pm ON pm.id = ge.party_id
            LEFT JOIN vehicle_master vm ON vm.id = ge.vehicle_id
            LEFT JOIN cargo_operations co ON co.id = (
                SELECT c2.id FROM cargo_operations c2 WHERE c2.gate_entry_id = ge.id ORDER BY c2.id DESC LIMIT 1
            )
            LEFT JOIN vessels v ON v.id = co.vessel_id
        """

        conditions = []
        params = []

        if vessel_id:
            conditions.append("co.vessel_id = %s")
            params.append(vessel_id)

        if vehicle_id:
            conditions.append("ge.vehicle_id = %s")
            params.append(vehicle_id)

        if party_id:
            conditions.append("ge.party_id = %s")
            params.append(party_id)

        if status:
            if status == "LOADING/UNLOADING" or status == "UNLOADING" or status == "LOADING":
                conditions.append("ge.status IN ('LOADING', 'UNLOADING')")
            else:
                conditions.append("ge.status = %s")
                params.append(status)

        if gate_in_no:
            conditions.append("ge.gate_in_no = %s")
            params.append(gate_in_no)

        if vehicle_no:
            conditions.append("vm.vehicle_no LIKE %s")
            params.append(f"%{vehicle_no}%")

        if start_date and end_date:
            conditions.append("DATE(ge.gate_in_datetime) BETWEEN %s AND %s")
            params.extend([start_date, end_date])
        elif start_date:
            conditions.append("DATE(ge.gate_in_datetime) >= %s")
            params.append(start_date)
        elif end_date:
            conditions.append("DATE(ge.gate_in_datetime) <= %s")
            params.append(end_date)

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        # total count
        count_query = "SELECT COUNT(*) " + base_query
        cursor.execute(count_query, tuple(params))
        total = cursor.fetchone()[0]

        # order clause
        order_clause = "ORDER BY ge.gate_in_datetime DESC"
        if sort_order == "oldest":
            order_clause = "ORDER BY ge.gate_in_datetime ASC"

        # data query
        data_query = f"""
            SELECT 
                ge.id,
                ge.gate_in_no,
                ge.gate_in_datetime,
                ge.party_id,
                ge.vehicle_id,
                ge.challan_invoice_no,
                ge.weighment_slip_no,
                ge.outside_payment_slip,
                ge.outside_gross_weight,
                ge.outside_tare_weight,
                ge.outside_net_weight,
                ge.own_weighbridge,
                ge.status,
                ge.direction,
                ge.gate_out_datetime,
                ge.driver_name,
                ge.driver_mob_no,
                ge.created_at,
                ge.updated_at,
                pm.party_name,
                pm.party_code,
                vm.vehicle_no,
                vm.transporter_name,
                v.id AS vessel_id,
                v.vessel_name,
                co.id AS cargo_operation_id,
                co.compressor_no
            {base_query}
            {order_clause}
            LIMIT %s OFFSET %s
        """

        data_params = list(params)
        data_params.extend([per_page, offset])
        cursor.execute(data_query, tuple(data_params))

        cols = [c[0] for c in cursor.description]
        rows = [_row(r, cols) for r in cursor.fetchall()]

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

# ---------- GET all unique gate-in numbers ----------
def get_gate_in_numbers():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT DISTINCT gate_in_no FROM gate_entries WHERE gate_in_no IS NOT NULL AND gate_in_no != '' ORDER BY gate_in_no DESC")
        rows = [r[0] for r in cursor.fetchall()]

        return jsonify({
            "success": True,
            "data": rows
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
            data["vehicle_id"],
            data["challan_invoice_no"],
            data.get("weighment_slip_no"),
            data.get("outside_payment_slip"),
            data.get("outside_gross_weight"),
            data.get("outside_tare_weight"),
            int(data.get("own_weighbridge", 0)),
            data["gate_in_datetime"],
            data.get("direction"),
            data.get("driver_name"),
            data.get("driver_mob_no")
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


# ---------- UPDATE gate entry ----------
def update_gate_entry(gate_id):
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update gate_entries columns
        query = """
            UPDATE gate_entries
            SET party_id = %s,
                vehicle_id = %s,
                challan_invoice_no = %s,
                weighment_slip_no = %s,
                outside_payment_slip = %s,
                outside_gross_weight = %s,
                outside_tare_weight = %s,
                own_weighbridge = %s,
                gate_in_datetime = %s,
                direction = %s,
                status = %s,
                gate_out_datetime = %s,
                driver_name = %s,
                driver_mob_no = %s,
                updated_at = NOW()
            WHERE id = %s
        """

        party_id = data.get("party_id")
        vehicle_id = data.get("vehicle_id")
        challan_invoice_no = data.get("challan_invoice_no")
        weighment_slip_no = data.get("weighment_slip_no")
        outside_payment_slip = data.get("outside_payment_slip")
        outside_gross_weight = data.get("outside_gross_weight")
        outside_tare_weight = data.get("outside_tare_weight")
        own_weighbridge = int(data.get("own_weighbridge", 0))
        gate_in_datetime = data.get("gate_in_datetime")
        direction = data.get("direction")
        status = data.get("status")
        gate_out_datetime = data.get("gate_out_datetime") or None
        driver_name = data.get("driver_name")
        driver_mob_no = data.get("driver_mob_no")

        cursor.execute(query, (
            party_id,
            vehicle_id,
            challan_invoice_no,
            weighment_slip_no,
            outside_payment_slip,
            outside_gross_weight,
            outside_tare_weight,
            own_weighbridge,
            gate_in_datetime,
            direction,
            status,
            gate_out_datetime,
            driver_name,
            driver_mob_no,
            gate_id
        ))

        # Handle Cargo Operation updates (vessel_id, compressor_no) if relevant
        vessel_id = data.get("vessel_id")
        compressor_no = data.get("compressor_no")

        if vessel_id is not None or compressor_no is not None:
            # Check if cargo operation exists
            cursor.execute("SELECT id FROM cargo_operations WHERE gate_entry_id = %s LIMIT 1", (gate_id,))
            op_row = cursor.fetchone()

            if op_row:
                op_id = op_row[0]
                cursor.execute("""
                    UPDATE cargo_operations
                    SET vessel_id = %s,
                        compressor_no = %s,
                        updated_at = NOW()
                    WHERE id = %s
                """, (vessel_id, compressor_no, op_id))
            else:
                if vessel_id:
                    op_type = "LOADING" if direction == "IMPORT" else "UNLOADING"
                    start_dt = gate_in_datetime or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("""
                        INSERT INTO cargo_operations (gate_entry_id, vessel_id, operation_type, start_datetime, compressor_no, remarks)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (gate_id, vessel_id, op_type, start_dt, compressor_no, ""))

        conn.commit()

        # Retrieve and return the updated row
        cursor.execute("""
            SELECT 
                ge.id,
                ge.gate_in_no,
                ge.gate_in_datetime,
                ge.party_id,
                ge.vehicle_id,
                ge.challan_invoice_no,
                ge.weighment_slip_no,
                ge.outside_payment_slip,
                ge.outside_gross_weight,
                ge.outside_tare_weight,
                ge.outside_net_weight,
                ge.own_weighbridge,
                ge.status,
                ge.direction,
                ge.gate_out_datetime,
                ge.driver_name,
                ge.driver_mob_no,
                ge.created_at,
                ge.updated_at,
                pm.party_name,
                pm.party_code,
                vm.vehicle_no,
                vm.transporter_name,
                v.id AS vessel_id,
                v.vessel_name,
                co.id AS cargo_operation_id,
                co.compressor_no
            FROM gate_entries ge
            LEFT JOIN party_masters pm ON pm.id = ge.party_id
            LEFT JOIN vehicle_master vm ON vm.id = ge.vehicle_id
            LEFT JOIN cargo_operations co ON co.id = (
                SELECT c2.id FROM cargo_operations c2 WHERE c2.gate_entry_id = ge.id ORDER BY c2.id DESC LIMIT 1
            )
            LEFT JOIN vessels v ON v.id = co.vessel_id
            WHERE ge.id = %s
        """, (gate_id,))

        row = cursor.fetchone()
        if row:
            cols = [c[0] for c in cursor.description]
            updated_data = _row(row, cols)
            return jsonify({
                "success": True,
                "message": "Gate entry updated successfully",
                "data": updated_data
            }), 200
        else:
            return jsonify({
                "success": True,
                "message": "Gate entry updated successfully",
                "data": None
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