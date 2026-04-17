from flask import request, jsonify
from database.db_connection import get_db_connection
from datetime import datetime


def _row(row, keys):
    d = dict(zip(keys, row))
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
    return d

# ===============================
# 🔹 BUILD CONTEXT FROM DB
# ===============================
def build_context(vessel_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    context = {}

    try:
        # Vessel
        cursor.execute("SELECT * FROM vessels WHERE id=%s", (vessel_id,))
        cols = [c[0] for c in cursor.description]
        vessel = dict(zip(cols, cursor.fetchone()))

        context["survey_qty"] = vessel.get("survey_quantity") or 0
        context["berthing_time"] = vessel.get("berthing_datetime")
        context["unberthing_time"] = vessel.get("sailing_datetime")
        context["mooring_start"] = vessel.get("mooring_datetime")
        context["mooring_end"] = vessel.get("sailing_datetime")

        # Gatein Count
        cursor.execute("SELECT COUNT(*) FROM gate_entries WHERE vessel_id=%s", (vessel_id,))
        context["gatein_count"] = cursor.fetchone()[0]

        # WBIN Count
        cursor.execute("""
            SELECT COUNT(*) FROM cargo_operations co
            JOIN gate_entries g ON co.gate_entry_id = g.id
            WHERE g.vessel_id=%s AND co.operation_type='WBIN'
        """, (vessel_id,))
        context["wbin_count"] = cursor.fetchone()[0]

        # Vehicles for Parking
        cursor.execute("""
            SELECT gate_in_datetime, gate_out_datetime
            FROM gate_entries
            WHERE vessel_id=%s AND gate_out_datetime IS NOT NULL
        """, (vessel_id,))

        vehicles = []
        for r in cursor.fetchall():
            vehicles.append({
                "gatein": r[0],
                "gateout": r[1]
            })

        context["vehicles"] = vehicles

        return context

    finally:
        cursor.close()
        conn.close()


# ===============================
# 🔹 FETCH RATES
# ===============================
def fetch_rates(vessel_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, activity, formula, rate, gst_rate, min_qty, max_qty
        FROM rate_master
        WHERE vessel_id = %s
    """, (vessel_id,))

    cols = [c[0] for c in cursor.description]
    rows = [dict(zip(cols, r)) for r in cursor.fetchall()]

    cursor.close()
    conn.close()

    return rows


# ===============================
# 🔹 CALCULATE LOGIC
# ===============================
def calculate_amount(row, context):
    formula = row["formula"]
    rate = float(row["rate"])

    if formula == "Logic1":
        return context["survey_qty"] * rate

    elif formula == "Logic2":
        return context["gatein_count"] * rate

    elif formula == "Logic3":
        start = context["berthing_time"]
        end = context["unberthing_time"]

        hours = (end - start).total_seconds() / 3600
        days = hours / 24
        return days * rate

    elif formula == "Logic4":
        start = context["mooring_start"]
        end = context["mooring_end"]

        hours = (end - start).total_seconds() / 3600
        days = math.ceil(hours / 24)
        return days * rate

    elif formula == "Logic6":
        return context["wbin_count"] * rate

    elif formula == "Logic7":
        total_days = 0
        for v in context["vehicles"]:
            hrs = (v["gateout"] - v["gatein"]).total_seconds() / 3600
            charge = max(0, hrs - 24)
            days = math.ceil(charge / 24)
            total_days += days

        return total_days * rate

    return 0


# ===============================
# 🔹 MAIN API
# ===============================
def generate_bill():
    data = request.get_json()

    party_id = data.get("party_id")
    vessel_ids = data.get("vessel_ids")
    start_date = data.get("period_start")
    end_date = data.get("period_end")

    if not party_id or not vessel_ids:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        total_base = 0
        bill_details = []

        for vessel_id in vessel_ids:
            context = build_context(vessel_id)
            rates = fetch_rates(vessel_id)

            for r in rates:
                amount = calculate_amount(r, context)
                gst = amount * float(r["gst_rate"]) / 100

                total_base += amount

                bill_details.append({
                    "vessel_id": vessel_id,
                    "activity": r["activity"],
                    "qty": 1,
                    "rate": r["rate"],
                    "amount": amount,
                    "gst_rate": r["gst_rate"],
                    "gst_amount": gst
                })

        # Insert bill_main
        cursor.execute("""
            INSERT INTO bill_main
            (voucher_number, bill_date, party_id, period_start, period_end,
             bill_base_value, total_bill_value, created_at)
            VALUES (%s, CURDATE(), %s, %s, %s, %s, %s, NOW())
        """, (
            f"BILL-{datetime.now().timestamp()}",
            party_id,
            start_date,
            end_date,
            total_base,
            total_base
        ))

        bill_main_id = cursor.lastrowid

        # Insert bill_details
        for d in bill_details:
            cursor.execute("""
                INSERT INTO bill_details
                (bill_main_id, vessel_id, activity_name, qty, rate, amount, gst_rate, gst_amount)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                bill_main_id,
                d["vessel_id"],
                d["activity"],
                d["qty"],
                d["rate"],
                d["amount"],
                d["gst_rate"],
                d["gst_amount"]
            ))

        conn.commit()

        return jsonify({
            "success": True,
            "bill_id": bill_main_id,
            "total": total_base
        })

    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


def get_vessels_for_billing():
    data = request.get_json()

    party_id = data.get("party_id")
    start_date = data.get("period_start")
    end_date = data.get("period_end")

    if not party_id or not start_date or not end_date:
        return jsonify({
            "success": False,
            "message": "party_id, period_start, period_end required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                id AS vessel_id,
                vessel_auto_id,
                vessel_name,
                quantity,
                sailing_datetime
            FROM vessels
            WHERE party_id = %s
              AND status = 'COMPLETED'
              AND sailing_datetime IS NOT NULL
              AND DATE(sailing_datetime) BETWEEN %s AND %s
            ORDER BY sailing_datetime
        """, (party_id, start_date, end_date))

        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

        vessels = [_row(r, cols) for r in rows]

        return jsonify({
            "success": True,
            "data": vessels
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()