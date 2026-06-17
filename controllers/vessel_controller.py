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
# def get_vessels():
#     status_filter = request.args.get("status")

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         if status_filter:
#             cursor.execute("""
#                 SELECT 
#                     v.*,
#                     p.party_name
#                 FROM vessels v
#                 LEFT JOIN party_masters p ON v.party_id = p.id
#                 WHERE v.status = %s
#                 ORDER BY v.created_at DESC
#             """, (status_filter,))
#         else:
#             cursor.execute("""
#                 SELECT 
#                     v.*,
#                     p.party_name
#                 FROM vessels v
#                 LEFT JOIN party_masters p ON v.party_id = p.id
#                 ORDER BY v.created_at DESC
#             """)

#         cols = [c[0] for c in cursor.description]
#         rows = [_vessel_row(r, cols) for r in cursor.fetchall()]

#         return jsonify({
#             "success": True,
#             "data": rows
#         }), 200

#     finally:
#         cursor.close()
#         conn.close()
def get_vessels():
    status_filter = request.args.get("status")
    vessel_name = request.args.get("vessel_name")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    sort_order = request.args.get("sort", "latest")

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        base_query = """
            FROM vessels v
            LEFT JOIN party_masters p ON v.party_id = p.id
        """

        conditions = []
        params = []

        if status_filter:
            conditions.append("v.status = %s")
            params.append(status_filter)

        if vessel_name:
            conditions.append("v.vessel_name = %s")
            params.append(vessel_name)

        if start_date and end_date:
            conditions.append("( (DATE(v.created_at) BETWEEN %s AND %s) OR (DATE(v.berthing_datetime) BETWEEN %s AND %s) )")
            params.extend([start_date, end_date, start_date, end_date])
        elif start_date:
            conditions.append("(DATE(v.created_at) >= %s OR DATE(v.berthing_datetime) >= %s)")
            params.extend([start_date, start_date])
        elif end_date:
            conditions.append("(DATE(v.created_at) <= %s OR DATE(v.berthing_datetime) <= %s)")
            params.extend([end_date, end_date])

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        # total count
        count_query = "SELECT COUNT(*) " + base_query
        cursor.execute(count_query, tuple(params))
        total = cursor.fetchone()[0]

        # order clause
        order_clause = "ORDER BY v.created_at DESC"
        if sort_order == "oldest":
            order_clause = "ORDER BY v.created_at ASC"

        # data query
        data_query = f"""
            SELECT v.*, p.party_name
            {base_query}
            {order_clause}
            LIMIT %s OFFSET %s
        """

        data_params = list(params)
        data_params.extend([per_page, offset])
        cursor.execute(data_query, tuple(data_params))

        cols = [c[0] for c in cursor.description]
        rows = [_vessel_row(r, cols) for r in cursor.fetchall()]

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

# ---------- GET all unique vessel names ----------
def get_vessel_names():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT DISTINCT vessel_name FROM vessels WHERE vessel_name IS NOT NULL AND vessel_name != '' ORDER BY vessel_name")
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


# ---------- GET single vessel ----------
def get_vessel(vessel_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 🔹 Get vessel + party
        cursor.execute("""
            SELECT 
                v.*,
                p.party_name AS party_name
            FROM party_masters p
            JOIN vessels v ON v.party_id = p.id
            WHERE v.id = %s
        """, (vessel_id,))

        vessel_cols = [c[0] for c in cursor.description]
        vessel_row = cursor.fetchone()

        if not vessel_row:
            return jsonify({
                "success": False,
                "message": "Vessel not found"
            }), 404

        vessel_data = _vessel_row(vessel_row, vessel_cols)

        # 🔹 Get rates (assuming rate_master has vessel_id FK)
        cursor.execute("""
            SELECT *
            FROM rate_master
            WHERE vessel_id = %s
        """, (vessel_id,))

        rate_cols = [c[0] for c in cursor.description]
        rate_rows = cursor.fetchall()

        rates = [
            dict(zip(rate_cols, row))
            for row in rate_rows
        ]

        # 🔹 Final response
        return jsonify({
            "success": True,
            "data": {
                "vessel": vessel_data,
                "rates": rates
            }
        }), 200

    finally:
        cursor.close()
        conn.close()

# ---------- CREATE vessel ----------
# def create_vessel():
#     data = request.get_json()
#     required = ["vessel_name", "party_id", "cargo_type", "quantity", "direction", "expected_date"]
#     missing = [f for f in required if not data.get(f)]
#     if missing:
#         return jsonify({"success": False, "message": f"Missing fields: {', '.join(missing)}"}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute("""
#             INSERT INTO vessels (vessel_name, party_id, cargo_type, quantity, direction, expected_date)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (
#             data["vessel_name"], data["party_id"], data["cargo_type"],
#             data["quantity"], data["direction"], data["expected_date"]
#         ))
#         conn.commit()
#         new_id = cursor.lastrowid
#         cursor.execute("SELECT * FROM vessels WHERE id = %s", (new_id,))
#         cols = [c[0] for c in cursor.description]
#         row = cursor.fetchone()
#         return jsonify({"success": True, "data": _vessel_row(row, cols), "message": "Vessel created"}), 201
#     except Exception as e:
#         conn.rollback()
#         return jsonify({"success": False, "message": str(e)}), 500
#     finally:
#         cursor.close()
#         conn.close()
def create_vessel():
    data = request.get_json()

    required = ["vessel_name", "party_id", "cargo_type", "quantity", "direction", "expected_date"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"success": False, "message": f"Missing fields: {', '.join(missing)}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Insert Vessel
        cursor.execute("""
            INSERT INTO vessels (vessel_name, party_id, cargo_type, quantity, direction, expected_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data["vessel_name"],
            data["party_id"],
            data["cargo_type"],
            data["quantity"],
            data["direction"],
            data["expected_date"]
        ))

        vessel_id = cursor.lastrowid

        # 2️⃣ Insert Rates from Payload
        rates = data.get("rates", [])

        for r in rates:
            cursor.execute("""
                INSERT INTO rate_master
                (vessel_id, activity, formula, rate, gst_rate, min_qty, max_qty, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """, (
                vessel_id,
                r.get("activity"),
                r.get("formula"),
                r.get("rate"),
                r.get("gst_rate"),
                r.get("min_qty"),
                r.get("max_qty")
            ))

        conn.commit()

        # 3️⃣ Return Data
        cursor.execute("SELECT * FROM vessels WHERE id = %s", (vessel_id,))
        cols = [c[0] for c in cursor.description]
        row = cursor.fetchone()

        return jsonify({
            "success": True,
            "data": _vessel_row(row, cols),
            "message": "Vessel + rates saved"
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# ---------- UPDATE vessel ----------
def update_vessel(vessel_id):
    data = request.get_json()

    required = ["vessel_name", "party_id", "cargo_type", "quantity", "direction"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"success": False, "message": f"Missing fields: {', '.join(missing)}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Update Vessel
        cursor.execute("""
            UPDATE vessels
            SET vessel_name=%s,
                party_id=%s,
                cargo_type=%s,
                quantity=%s,
                direction=%s,
                status=%s,
                updated_at=NOW()
            WHERE id=%s
        """, (
            data["vessel_name"],
            data["party_id"],
            data["cargo_type"],
            data["quantity"],
            data["direction"],
            data["status"],
            vessel_id
        ))

        conn.commit()

        # 4️⃣ Return Updated Data
        cursor.execute("SELECT * FROM vessels WHERE id = %s", (vessel_id,))
        cols = [c[0] for c in cursor.description]
        row = cursor.fetchone()

        return jsonify({
            "success": True,
            "data": _vessel_row(row, cols),
            "message": "Vessel updated successfully"
        }), 200

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


# ---------- Rate Master -----------------
def get_rates_by_vessel(vessel_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, vessel_id, activity, formula, rate, gst_rate, min_qty, max_qty, created_at
            FROM rate_master
            WHERE vessel_id = %s
        """, (vessel_id,))

        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

        if not rows:
            return jsonify({
                "success": False,
                "message": "No rates found for this vessel"
            }), 404

        data = [dict(zip(cols, r)) for r in rows]

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


def update_rate(vessel_id, rate_id):
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Check if record exists
        cursor.execute("""
            SELECT id FROM rate_master 
            WHERE id = %s AND vessel_id = %s
        """, (rate_id, vessel_id))

        if not cursor.fetchone():
            return jsonify({
                "success": False,
                "message": "Rate not found for this vessel"
            }), 404

        # 2️⃣ Build dynamic update query
        fields = []
        values = []

        allowed_fields = [
            "activity", "formula", "rate",
            "gst_rate", "min_qty", "max_qty"
        ]

        for field in allowed_fields:
            if field in data:
                fields.append(f"{field} = %s")
                values.append(data[field])

        if not fields:
            return jsonify({
                "success": False,
                "message": "No fields to update"
            }), 400

        values.append(rate_id)
        values.append(vessel_id)

        query = f"""
            UPDATE rate_master
            SET {', '.join(fields)}
            WHERE id = %s AND vessel_id = %s
        """

        cursor.execute(query, tuple(values))
        conn.commit()

        # 3️⃣ Return updated row
        cursor.execute("""
            SELECT * FROM rate_master
            WHERE id = %s AND vessel_id = %s
        """, (rate_id, vessel_id))

        cols = [c[0] for c in cursor.description]
        updated = dict(zip(cols, cursor.fetchone()))

        return jsonify({
            "success": True,
            "data": updated,
            "message": "Rate updated successfully"
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


# ---------- GET Daily Vehicle Movement Report ----------
def get_vehicle_movement_report():
    vessel_id = request.args.get("vessel_id")
    party_id = request.args.get("party_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date is None and end_date is None:
        today = datetime.now().strftime("%Y-%m-%d")
        start_date = today
        end_date = today

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
            LEFT JOIN wbin_records wbi ON wbi.gate_entry_id = ge.id
            LEFT JOIN wbout_records wbo ON wbo.gate_entry_id = ge.id
        """

        conditions = []
        params = []

        if vessel_id:
            conditions.append("co.vessel_id = %s")
            params.append(vessel_id)

        if party_id:
            conditions.append("ge.party_id = %s")
            params.append(party_id)

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

        data_query = f"""
            SELECT 
                pm.party_name,
                ge.gate_in_datetime,
                ge.challan_invoice_no,
                vm.vehicle_no,
                vm.transporter_name,
                ge.driver_name,
                ge.driver_mob_no,
                ge.outside_payment_slip,
                ge.outside_gross_weight,
                ge.outside_tare_weight,
                ge.outside_net_weight,
                wbi.wbin_datetime,
                wbi.gross_weight AS wbin_gross_weight,
                wbi.tare_weight AS wbin_tare_weight,
                wbo.wbout_datetime,
                wbo.gross_weight AS wbout_gross_weight,
                wbo.tare_weight AS wbout_tare_weight,
                ge.gate_out_datetime,
                co.start_datetime AS cargo_start_datetime,
                co.compressor_no,
                co.end_datetime AS cargo_end_datetime,
                v.vessel_name,
                v.berthing_datetime,
                v.sailing_datetime,
                v.survey_quantity
            {base_query}
            ORDER BY ge.gate_in_datetime ASC
        """

        cursor.execute(data_query, tuple(params))
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

        data = []
        for row in rows:
            d = dict(zip(cols, row))
            
            # Extract weighbridge raw weights
            wbin_gross = d.get("wbin_gross_weight")
            wbin_tare = d.get("wbin_tare_weight")
            wbout_gross = d.get("wbout_gross_weight")
            wbout_tare = d.get("wbout_tare_weight")
            outside_net = d.get("outside_net_weight")
            
            # 1. Own Gross Weight
            own_gross = wbin_gross if wbin_gross is not None else wbout_gross
            # 2. Own Tare Weight
            own_tare = wbin_tare if wbin_tare is not None else wbout_tare
            
            # Own net weight dynamic calculation
            net_val = None
            try:
                if wbin_gross is not None and wbout_tare is not None:
                    net_val = abs(float(wbin_gross) - float(wbout_tare))
                elif wbout_gross is not None and wbin_tare is not None:
                    net_val = abs(float(wbout_gross) - float(wbin_tare))
            except (ValueError, TypeError):
                net_val = None

            if net_val is not None:
                d["net_weight"] = round(net_val, 3)
            else:
                if wbin_gross is None and wbin_tare is None and wbout_gross is None and wbout_tare is None:
                    try:
                        d["net_weight"] = round(float(outside_net), 3) if outside_net is not None else None
                    except (ValueError, TypeError):
                        d["net_weight"] = outside_net
                else:
                    d["net_weight"] = None

            # Own gross and tare for display
            try:
                d["gross_weight"] = round(float(own_gross), 3) if own_gross is not None else None
            except (ValueError, TypeError):
                d["gross_weight"] = own_gross

            try:
                d["tare_weight"] = round(float(own_tare), 3) if own_tare is not None else None
            except (ValueError, TypeError):
                d["tare_weight"] = own_tare

            # Calculate Waiting Hour 24 (rounded to nearest integer)
            gate_in = d.get("gate_in_datetime")
            gate_out = d.get("gate_out_datetime")
            waiting_hours = None
            if isinstance(gate_in, datetime) and isinstance(gate_out, datetime):
                diff = gate_out - gate_in
                waiting_hours = round(diff.total_seconds() / 3600.0)
            d["waiting_hours"] = waiting_hours

            # Format datetimes to strings for JSON serialization
            for k, v in d.items():
                if isinstance(v, datetime):
                    d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
                    
            data.append(d)

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

