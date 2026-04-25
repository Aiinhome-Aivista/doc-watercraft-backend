from flask import request, jsonify
from database.db_connection import get_db_connection
from datetime import datetime
import json


def _row(row, keys):
    d = dict(zip(keys, row))
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
    return d

def create_partymaster():
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc("sp_create_party", (
            data.get("party_name"),
            data.get("party_code"),
            data.get("address"),
            data.get("state"),
            data.get("country"),
            data.get("pincode"),
            json.dumps(data.get("mobiles")) if data.get("mobiles") else None,
            json.dumps(data.get("emails")) if data.get("emails") else None
        ))

        result = list(cursor.stored_results())[0]
        cols = [c[0] for c in result.description]

        return jsonify({
            "success": True,
            "data": _row(result.fetchone(), cols)
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        conn.close()


def get_partymasters():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.callproc("sp_get_parties")
    result = list(cursor.stored_results())[0]

    cols = [c[0] for c in result.description]
    data = [_row(r, cols) for r in result.fetchall()]

    conn.close()

    return jsonify({"success": True, "data": data}), 200

def get_partymaster(partymaster_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.callproc("sp_get_party", (partymaster_id,))
    result = list(cursor.stored_results())[0]

    row = result.fetchone()

    if not row:
        return jsonify({"success": False, "message": "Not found"}), 404

    cols = [c[0] for c in result.description]

    return jsonify({
        "success": True,
        "data": _row(row, cols)
    }), 200


def update_partymaster(partymaster_id):
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc("sp_update_party", (
            partymaster_id,
            data.get("party_name"),
            data.get("party_code"),
            data.get("address"),
            data.get("state"),
            data.get("country"),
            data.get("pincode"),
            json.dumps(data.get("mobiles")) if data.get("mobiles") else None,
            json.dumps(data.get("emails")) if data.get("emails") else None
        ))

        result = list(cursor.stored_results())[0]
        cols = [c[0] for c in result.description]

        return jsonify({
            "success": True,
            "data": _row(result.fetchone(), cols)
        })

    finally:
        conn.close()


def delete_partymaster(partymaster_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc("sp_delete_party", (partymaster_id,))
        conn.commit()

        return jsonify({
            "success": True,
            "message": "Deleted successfully"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    finally:
        conn.close()