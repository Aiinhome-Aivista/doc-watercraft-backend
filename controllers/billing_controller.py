from flask import request, jsonify
from database.db_connection import get_db_connection
from datetime import datetime, timedelta
from decimal import Decimal
import math


# ===============================
# 🔹 HELPERS
# ===============================
def ceil(x):
    return math.ceil(float(x))


def _row(row, keys):
    d = dict(zip(keys, row))
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
    return d


def adjust_berthing_start(dt):
    if dt.hour >= 6:
        return dt.replace(hour=6, minute=0, second=0, microsecond=0)
    else:
        return (dt - timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)


def adjust_berthing_end(dt):
    if dt.hour >= 6:
        return (dt + timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)
    else:
        return dt.replace(hour=6, minute=0, second=0, microsecond=0)


# ===============================
# 🔹 BUILD CONTEXT
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

        # Gate count
        cursor.execute("""
            SELECT COUNT(DISTINCT g.id)
            FROM cargo_operations co
            JOIN gate_entries g ON co.gate_entry_id = g.id
            WHERE co.vessel_id = %s
        """, (vessel_id,))
        context["gatein_count"] = cursor.fetchone()[0] or 0

        # WBIN count
        cursor.execute("""
            SELECT COUNT(*)
            FROM cargo_operations co
            JOIN wbin_records w ON co.gate_entry_id = w.gate_entry_id
            WHERE co.vessel_id = %s
        """, (vessel_id,))
        context["wbin_count"] = cursor.fetchone()[0] or 0

        # Vehicles
        cursor.execute("""
            SELECT g.gate_in_datetime, g.gate_out_datetime
            FROM cargo_operations co
            JOIN gate_entries g ON co.gate_entry_id = g.id
            WHERE co.vessel_id = %s
            AND g.gate_out_datetime IS NOT NULL
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

    qty = Decimal(0)
    amount = Decimal(0)
    final_rate = rate

    if formula == "Logic1":
        qty = Decimal(context["survey_qty"])
        amount = qty * rate

    elif formula == "Logic2":
        qty = Decimal(context["gatein_count"])
        amount = qty * rate

    elif formula == "Logic3":
        start = context["berthing_time"]
        end = context["unberthing_time"]

        if not start or not end:
            return Decimal(0), Decimal(0), rate

        A1 = adjust_berthing_start(start)
        A2 = adjust_berthing_end(end)

        days = ceil((A2 - A1).total_seconds() / 86400)
        qty = Decimal(days)
        amount = qty * rate

    elif formula == "Logic4":
        start = context["mooring_start"]
        end = context["mooring_end"]

        if not start or not end:
            return Decimal(0), Decimal(0), rate

        hours = (end - start).total_seconds() / 3600
        slabs = ceil(hours / 8)

        qty = Decimal(slabs)
        amount = qty * rate

    elif formula == "Logic5":
        start = context["mooring_start"]
        end = context["mooring_end"]

        if not start or not end:
            return Decimal(0), Decimal(0), rate

        hours = (end - start).total_seconds() / 3600
        days = ceil(hours / 24)

        vessel_qty = Decimal(context["survey_qty"])

        slabs = [
            r for r in context.get("all_rates", [])
            if r["activity"] == row["activity"] and r["formula"] == "Logic5"
        ]

        slab_rate = rate

        for slab in slabs:
            min_q = Decimal(slab["min_qty"] or 0)
            max_q = Decimal(slab["max_qty"] or 999999999)

            if min_q <= vessel_qty <= max_q:
                slab_rate = Decimal(slab["rate"])
                break

        final_rate = slab_rate
        qty = Decimal(days)
        amount = qty * slab_rate

    elif formula == "Logic6":
        qty = Decimal(context["wbin_count"])
        amount = qty * rate

    elif formula == "Logic7":
        total_days = Decimal(0)

        for v in context["vehicles"]:
            hrs = (v["gateout"] - v["gatein"]).total_seconds() / 3600
            charge = max(0, hrs - 24)
            days = ceil(charge / 24)
            total_days += Decimal(days)

        qty = total_days
        amount = qty * rate

    return qty, amount, final_rate


# ===============================
# 🔹 MAIN API (FIXED DUPLICATES)
# ===============================
def generate_bill():
    data = request.get_json()

    party_id = data.get("party_id")
    vessel_id = data.get("vessel_id")
    start_date = data.get("period_start")
    end_date = data.get("period_end")

    if not party_id or not vessel_id:
        return jsonify({"success": False, "message": "party_id and vessel_id required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        total_base = Decimal(0)
        total_gst = Decimal(0)
        bill_details = []

        context = build_context(vessel_id)
        rates = fetch_rates(vessel_id)
        context["all_rates"] = rates

        processed_logic5 = False
        processed_activities = set()   # 🔥 FIX

        for r in rates:
            activity = r["activity"]
            formula = r["formula"]

            # 🚨 Skip duplicate activities (except Logic5)
            if formula != "Logic5":
                if activity in processed_activities:
                    continue
                processed_activities.add(activity)

            # Logic5 handled once
            if formula == "Logic5":
                if processed_logic5:
                    continue
                processed_logic5 = True

            qty, amount, final_rate = calculate_amount(r, context)

            if qty == 0 or amount == 0:
                continue

            gst_rate = Decimal(r["gst_rate"])
            gst = (amount * gst_rate) / Decimal(100)

            total_base += amount
            total_gst += gst

            bill_details.append({
                "vessel_id": vessel_id,
                "activity": activity,
                "qty": float(qty),
                "rate": float(final_rate),
                "amount": float(amount),
                "gst_rate": float(gst_rate),
                "gst_amount": float(gst),
                "remarks": ""
            })

        total_bill_value = total_base + total_gst

        cgst = total_gst / 2
        sgst = total_gst / 2
        igst = Decimal(0)
        round_off = Decimal(0)

        voucher_number = f"BILL-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        cursor.execute("""
            INSERT INTO bill_main (
                voucher_number, bill_date, party_id, period_start, period_end,
                narration, bill_base_value, cgst, sgst, igst, round_off,
                total_bill_value, created_at
            )
            VALUES (%s, CURDATE(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, (
            voucher_number,
            party_id,
            start_date,
            end_date,
            "",
            float(total_base),
            float(cgst),
            float(sgst),
            float(igst),
            float(round_off),
            float(total_bill_value)
        ))

        bill_main_id = cursor.lastrowid

        for d in bill_details:
            cursor.execute("""
                INSERT INTO bill_details (
                    bill_main_id, vessel_id, activity_name,
                    qty, rate, amount, remarks,
                    gst_rate, gst_amount, created_at
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
            """, (
                bill_main_id,
                d["vessel_id"],
                d["activity"],
                d["qty"],
                d["rate"],
                d["amount"],
                d["remarks"],
                d["gst_rate"],
                d["gst_amount"]
            ))

        conn.commit()

        return jsonify({
            "success": True,
            "voucher_number": voucher_number,
            "total_base": float(total_base),
            "total_gst": float(total_gst),
            "total_bill": float(total_bill_value),
            "details": bill_details
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