from flask import request, jsonify
from database.db_connection import get_db_connection
from datetime import datetime
from decimal import Decimal
import math


# ===============================
# 🔹 BUILD CONTEXT FROM DB
# ===============================
def build_context(vessel_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    context = {}

    try:
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
        context["gatein_count"] = cursor.fetchone()[0] or 0

        # WBIN Count
        cursor.execute("""
            SELECT COUNT(*) FROM cargo_operations co
            JOIN gate_entries g ON co.gate_entry_id = g.id
            WHERE g.vessel_id=%s AND co.operation_type='WBIN'
        """, (vessel_id,))
        context["wbin_count"] = cursor.fetchone()[0] or 0

        # Vehicles
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
    rate = Decimal(row["rate"])

    # ---------------- Logic 1 ----------------
    if formula == "Logic1":
        return Decimal(context["survey_qty"]) * rate

    # ---------------- Logic 2 ----------------
    elif formula == "Logic2":
        return Decimal(context["gatein_count"]) * rate

    # ---------------- Logic 3 (Berthing) ----------------
    elif formula == "Logic3":
        start = context["berthing_time"]
        end = context["unberthing_time"]

        if not start or not end:
            return Decimal(0)

        hours = Decimal((end - start).total_seconds()) / Decimal(3600)
        days = math.ceil(hours / Decimal(24))   # rounded

        return Decimal(days) * rate

    # ---------------- Logic 4 (Mooring) ----------------
    elif formula == "Logic4":
        start = context["mooring_start"]
        end = context["mooring_end"]

        if not start or not end:
            return Decimal(0)

        hours = Decimal((end - start).total_seconds()) / Decimal(3600)
        days = math.ceil(hours / Decimal(24))

        return Decimal(days) * rate

    # ---------------- Logic 6 ----------------
    elif formula == "Logic6":
        return Decimal(context["wbin_count"]) * rate

    # ---------------- Logic 7 (Parking) ----------------
    elif formula == "Logic7":
        total_days = Decimal(0)

        for v in context["vehicles"]:
            if not v["gatein"] or not v["gateout"]:
                continue

            hrs = Decimal((v["gateout"] - v["gatein"]).total_seconds()) / Decimal(3600)
            charge = max(Decimal(0), hrs - Decimal(24))
            days = math.ceil(charge / Decimal(24))
            total_days += Decimal(days)

        return total_days * rate

    return Decimal(0)


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
        total_base = Decimal(0)
        total_gst = Decimal(0)
        bill_details = []

        for vessel_id in vessel_ids:
            context = build_context(vessel_id)
            rates = fetch_rates(vessel_id)

            for r in rates:
                amount = calculate_amount(r, context)

                gst_rate = Decimal(r["gst_rate"])
                gst = (amount * gst_rate) / Decimal(100)

                total_base += amount
                total_gst += gst

                bill_details.append({
                    "vessel_id": vessel_id,
                    "activity": r["activity"],
                    "qty": 1,
                    "rate": float(r["rate"]),
                    "amount": float(amount),
                    "gst_rate": float(r["gst_rate"]),
                    "gst_amount": float(gst)
                })

        total_bill_value = total_base + total_gst

        # 🔹 Insert bill_main
        cursor.execute("""
            INSERT INTO bill_main
            (voucher_number, bill_date, party_id, period_start, period_end,
             bill_base_value, cgst, sgst, igst, total_bill_value, created_at)
            VALUES (%s, CURDATE(), %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, (
            f"BILL-{datetime.now().timestamp()}",
            party_id,
            start_date,
            end_date,
            float(total_base),
            0, 0, float(total_gst),  # simple IGST (can split later)
            float(total_bill_value)
        ))

        bill_main_id = cursor.lastrowid

        # 🔹 Insert bill_details
        for d in bill_details:
            cursor.execute("""
                INSERT INTO bill_details
                (bill_main_id, vessel_id, activity_name, qty, rate, amount, gst_rate, gst_amount)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                bill_main_id,
                d["vessel_id"],
                d["activity"],
                float(d["qty"]),
                float(d["rate"]),
                float(d["amount"]),
                float(d["gst_rate"]),
                float(d["gst_amount"])
            ))

        conn.commit()

        return jsonify({
            "success": True,
            "bill_id": bill_main_id,
            "base": float(total_base),
            "gst": float(total_gst),
            "total": float(total_bill_value)
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