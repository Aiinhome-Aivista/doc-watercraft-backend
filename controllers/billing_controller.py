from flask import request, jsonify, send_file, Response, url_for
from database.db_connection import get_db_connection
from datetime import datetime, timedelta
from decimal import Decimal
import math
from utils.pdf_generator import generate_invoice_pdf
import os


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
            "bill_main_id": bill_main_id,
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



def get_bill_data(bill_main_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 🔹 Bill Main + Party
        cursor.execute("""
            SELECT 
                bm.voucher_number,
                bm.bill_base_value,
                bm.cgst,
                bm.sgst,
                bm.total_bill_value,
                bm.period_start,
                bm.period_end,
                p.party_name
            FROM bill_main bm
            JOIN party_masters p ON bm.party_id = p.id
            WHERE bm.id = %s
        """, (bill_main_id,))

        bm = cursor.fetchone()

        if not bm:
            return None

        # 🔹 Bill Details + Vessel Name
        cursor.execute("""
            SELECT 
                bd.vessel_id,
                v.vessel_name,
                bd.activity_name,
                bd.qty,
                bd.rate,
                bd.amount,
                bd.gst_rate,
                bd.gst_amount
            FROM bill_details bd
            JOIN vessels v ON bd.vessel_id = v.id
            WHERE bd.bill_main_id = %s
        """, (bill_main_id,))

        rows = cursor.fetchall()

        details = []
        for r in rows:
            details.append({
                "vessel_id": r[0],
                "vessel_name": r[1],
                "activity": r[2],
                "qty": float(r[3]),
                "rate": float(r[4]),
                "amount": float(r[5]),
                "gst_rate": float(r[6]),
                "gst_amount": float(r[7])
            })

        return {
            "voucher_number": bm["voucher_number"],
            "total_base": float(bm[1]),
            "cgst": float(bm[2]),
            "sgst": float(bm[3]),
            "total_gst": float(bm[2]) + float(bm[3]),
            "total_bill": float(bm[4]),
            "period_start": str(bm[5]),
            "period_end": str(bm[6]),
            "party_name": bm[7],
            "details": details
        }

    finally:
        cursor.close()
        conn.close()     



def pdf_bill_generator():
    data = request.get_json()

    party_id = data.get("party_id")
    vessel_ids = data.get("vessel_ids") or []
    start_date = data.get("period_start")
    end_date = data.get("period_end")

    if not party_id or not vessel_ids:
        return jsonify({
            "success": False,
            "message": "party_id and vessel_ids required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 🔹 Validate all vessels belong to same party
        placeholders = ','.join(['%s'] * len(vessel_ids))

        query = f"""
            SELECT COUNT(DISTINCT party_id)
            FROM vessels
            WHERE id IN ({placeholders})
        """

        cursor.execute(query, vessel_ids)

        if cursor.fetchone()[0] > 1:
            return jsonify({
                "success": False,
                "message": "Selected vessels belong to different parties"
            }), 400

        # 🔹 Get party name
        cursor.execute("SELECT party_name FROM party_masters WHERE id=%s", (party_id,))
        p = cursor.fetchone()
        party_name = p[0] if p else ""

        total_base = Decimal(0)
        total_gst = Decimal(0)
        details = []

        # 🔹 Loop selected vessels only
        for vessel_id in vessel_ids:

            context = build_context(vessel_id)
            rates = fetch_rates(vessel_id)
            context["all_rates"] = rates

            processed_logic5 = False
            processed_activities = set()

            for r in rates:
                activity = r["activity"]
                formula = r["formula"]

                if formula != "Logic5":
                    if activity in processed_activities:
                        continue
                    processed_activities.add(activity)

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

                # 🔹 Get vessel name
                cursor.execute("SELECT vessel_name FROM vessels WHERE id=%s", (vessel_id,))
                vn = cursor.fetchone()
                vessel_name = vn[0] if vn else f"Vessel {vessel_id}"

                details.append({
                    "vessel_id": vessel_id,
                    "vessel_name": vessel_name,
                    "activity": activity,
                    "qty": float(qty),
                    "rate": float(final_rate),
                    "amount": float(amount),
                    "gst_rate": float(gst_rate),
                    "gst_amount": float(gst)
                })

        if not details:
            return jsonify({
                "success": False,
                "message": "No billable data found"
            }), 400

        # 🔹 Build PDF data (no DB)
        result = {
            "voucher_number": f"INVOICE-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "party_name": party_name,
            "period_start": start_date,
            "period_end": end_date,
            "total_base": float(total_base),
            "cgst": float(total_gst / 2),
            "sgst": float(total_gst / 2),
            "total_bill": float(total_base + total_gst),
            "details": details
        }

        # 🔥 File path (cross-platform)
        folder = "generated_pdfs"
        os.makedirs(folder, exist_ok=True)

        file_path = os.path.join(folder, f"{result['voucher_number']}.pdf")

        # 🔹 Generate PDF
        generate_invoice_pdf(result, file_path)

        # 🔹 Return a downloadable link instead of streaming the PDF here
        download_url = url_for("download_pdf_bill", filename=f"{result['voucher_number']}.pdf", _external=True)

        return jsonify({
            "success": True,
            "message": "PDF generated successfully",
            "voucher_number": result["voucher_number"],
            "download_url": download_url,
            "file_name": f"{result['voucher_number']}.pdf",
        }), 200

    except Exception as e:
        print("PDF ERROR:", str(e))
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


def download_bill_pdf(filename):
    folder = "generated_pdfs"
    file_path = os.path.join(folder, filename)

    if not os.path.exists(file_path):
        return jsonify({
            "success": False,
            "message": "PDF file not found"
        }), 404

    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )


def get_all_bills():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                bm.id,
                bm.voucher_number,
                bm.bill_date,
                pm.party_name,
                bm.period_start,
                bm.period_end,
                bm.narration,
                bm.bill_base_value,
                bm.cgst,
                bm.sgst,
                bm.igst,
                bm.round_off,
                bm.total_bill_value,
                bm.created_at
            FROM bill_main bm
            LEFT JOIN party_masters pm ON bm.party_id = pm.id
            ORDER BY bm.created_at DESC
        """)

        cols = [
            "id", "voucher_number", "bill_date", "party_name",
            "period_start", "period_end", "narration", "bill_base_value",
            "cgst", "sgst", "igst", "round_off", "total_bill_value", "created_at"
        ]
        
        rows = cursor.fetchall()
        bills = []
        for r in rows:
            d = dict(zip(cols, r))
            for k, v in d.items():
                if isinstance(v, datetime):
                    d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
                elif hasattr(v, 'strftime'): # handles date objects like bill_date
                    d[k] = v.strftime("%Y-%m-%d")
                elif isinstance(v, Decimal):
                    d[k] = float(v)
            
            # Fetch details for this bill
            cursor.execute("""
                SELECT 
                    bd.activity_name, bd.amount, bd.gst_amount, bd.gst_rate, bd.qty, bd.rate, bd.remarks, bd.vessel_id, v.vessel_name
                FROM bill_details bd
                LEFT JOIN vessels v ON bd.vessel_id = v.id
                WHERE bd.bill_main_id = %s
            """, (d["id"],))
            
            detail_cols = ["activity", "amount", "gst_amount", "gst_rate", "qty", "rate", "remarks", "vessel_id", "vessel_name"]
            detail_rows = cursor.fetchall()
            details = []
            for dr in detail_rows:
                dd = dict(zip(detail_cols, dr))
                for dk, dv in dd.items():
                    if isinstance(dv, Decimal):
                        dd[dk] = float(dv)
                    elif dv is None and dk in ["remarks", "vessel_name"]:
                        dd[dk] = ""
                details.append(dd)
            
            d["details"] = details
            bills.append(d)

        return jsonify({
            "success": True,
            "data": bills
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()



def update_bill(bill_id):
    data = request.get_json()

    narration = data.get("narration", "")
    bill_base_value = data.get("bill_base_value")
    cgst = data.get("cgst")
    sgst = data.get("sgst")
    igst = data.get("igst")
    round_off = data.get("round_off")
    total_bill_value = data.get("total_bill_value")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM bill_main WHERE id = %s", (bill_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Bill not found"}), 404

        cursor.execute("""
            UPDATE bill_main
            SET narration = %s,
                bill_base_value = %s,
                cgst = %s,
                sgst = %s,
                igst = %s,
                round_off = %s,
                total_bill_value = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (
            narration,
            float(bill_base_value) if bill_base_value is not None else 0.0,
            float(cgst) if cgst is not None else 0.0,
            float(sgst) if sgst is not None else 0.0,
            float(igst) if igst is not None else 0.0,
            float(round_off) if round_off is not None else 0.0,
            float(total_bill_value) if total_bill_value is not None else 0.0,
            bill_id
        ))

        conn.commit()
        return jsonify({"success": True, "message": "Bill updated successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


def delete_bill(bill_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM bill_main WHERE id = %s", (bill_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Bill not found"}), 404

        # Delete details first
        cursor.execute("DELETE FROM bill_details WHERE bill_main_id = %s", (bill_id,))
        
        # Delete main bill
        cursor.execute("DELETE FROM bill_main WHERE id = %s", (bill_id,))

        conn.commit()
        return jsonify({"success": True, "message": "Bill deleted successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()




