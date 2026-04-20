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

        params = []

        if status_filter:
            base_query += " WHERE v.status = %s"
            params.append(status_filter)

        # total count
        count_query = "SELECT COUNT(*) " + base_query
        cursor.execute(count_query, tuple(params))
        total = cursor.fetchone()[0]

        # data query
        data_query = """
            SELECT v.*, p.party_name
        """ + base_query + """
            ORDER BY v.created_at DESC
            LIMIT %s OFFSET %s
        """

        params.extend([per_page, offset])
        cursor.execute(data_query, tuple(params))

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

    finally:
        cursor.close()
        conn.close()

# ---------- GET single vessel ----------
def get_vessel(vessel_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                v.*,
                p.party_name AS party_name
            FROM party_masters p
            JOIN vessels v ON v.party_id = p.id
            WHERE v.id = %s
        """, (vessel_id,))

        cols = [c[0] for c in cursor.description]
        row = cursor.fetchone()

        if not row:
            return jsonify({
                "success": False,
                "message": "Vessel not found"
            }), 404

        return jsonify({
            "success": True,
            "data": _vessel_row(row, cols)
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
