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

    if not data or not data.get("party_name"):
        return jsonify({
            "status": "error",
            "message": "party_name is required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO party_masters 
            (party_name, party_code, address, state, country, pincode, mobiles, emails)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data.get("party_name"),
            data.get("party_code"),
            data.get("address"),
            data.get("state"),
            data.get("country"),
            data.get("pincode"),
            json.dumps(data.get("mobiles")) if data.get("mobiles") else None,
            json.dumps(data.get("emails")) if data.get("emails") else None
        ))

        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Party Master created successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        conn.close()


def get_partymasters():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM party_masters")
    rows = cursor.fetchall()
    keys = [desc[0] for desc in cursor.description]
    partymasters = [_row(row, keys) for row in rows]
    conn.close()
    return jsonify({
        "status": "success",
        "data": partymasters
    }), 200


def get_partymaster(partymaster_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM party_masters WHERE id = %s", (partymaster_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return jsonify({
            "status": "error",
            "message": "Party Master not found"
        }), 404
    keys = [desc[0] for desc in cursor.description]
    partymaster = _row(row, keys)
    conn.close()
    return jsonify({
        "status": "success",
        "data": partymaster
    }), 200


def update_partymaster(partymaster_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No data provided"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        fields = []
        values = []

        if "party_name" in data:
            fields.append("party_name=%s")
            values.append(data["party_name"])

        if "party_code" in data:
            fields.append("party_code=%s")
            values.append(data["party_code"])

        if "address" in data:
            fields.append("address=%s")
            values.append(data["address"])

        if "state" in data:
            fields.append("state=%s")
            values.append(data["state"])

        if "country" in data:
            fields.append("country=%s")
            values.append(data["country"])

        if "pincode" in data:
            fields.append("pincode=%s")
            values.append(data["pincode"])

        if "mobiles" in data:
            fields.append("mobiles=%s")
            values.append(json.dumps(data["mobiles"]))

        if "emails" in data:
            fields.append("emails=%s")
            values.append(json.dumps(data["emails"]))

        if not fields:
            return jsonify({
                "status": "error",
                "message": "No fields to update"
            }), 400

        values.append(partymaster_id)

        query = f"UPDATE party_masters SET {', '.join(fields)} WHERE id=%s"
        cursor.execute(query, values)

        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Party Master updated successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        conn.close()


def delete_partymaster(partymaster_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM party_masters WHERE id=%s", (partymaster_id,))
        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Party Master deleted successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        conn.close() 
