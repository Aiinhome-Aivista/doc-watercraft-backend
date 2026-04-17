from flask import request, jsonify
from database.db_connection import get_db_connection
from datetime import datetime


def _row(row, keys):
    d = dict(zip(keys, row))
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
    return d

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