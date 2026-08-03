from flask import request, jsonify
from database.db_connection import get_db_connection
from datetime import datetime
import json


def _row(row, keys):
    if not row:
        return None
    d = dict(zip(keys, row))
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(v, str) and (k in ["mobiles", "emails"]):
            try:
                d[k] = json.loads(v)
            except Exception:
                pass
    return d


def create_partymaster():
    data = request.get_json()
    if not data or not data.get("party_name"):
        return jsonify({"success": False, "message": "Party name is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    mobiles_json = json.dumps(data.get("mobiles")) if data.get("mobiles") else None
    emails_json = json.dumps(data.get("emails")) if data.get("emails") else None

    try:
        # Try stored procedure first
        try:
            cursor.callproc("sp_create_party", (
                data.get("party_name"),
                data.get("party_code"),
                data.get("address"),
                data.get("state"),
                data.get("country"),
                data.get("pincode"),
                mobiles_json,
                emails_json,
                data.get("pan_number"),
                data.get("gst_number")
            ))
            result = list(cursor.stored_results())[0]
            cols = [c[0] for c in result.description]
            row = result.fetchone()
            conn.commit()
            return jsonify({"success": True, "data": _row(row, cols)}), 201
        except Exception as proc_err:
            # Fallback to direct SQL INSERT if procedure doesn't exist
            sql = """
                INSERT INTO party_masters 
                (party_name, party_code, address, state, country, pincode, mobiles, emails, pan_number, gst_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data.get("party_name"),
                data.get("party_code"),
                data.get("address"),
                data.get("state"),
                data.get("country"),
                data.get("pincode"),
                mobiles_json,
                emails_json,
                data.get("pan_number"),
                data.get("gst_number")
            ))
            conn.commit()
            new_id = cursor.lastrowid

            cursor.execute("SELECT * FROM party_masters WHERE id = %s", (new_id,))
            cols = [c[0] for c in cursor.description]
            row = cursor.fetchone()
            return jsonify({"success": True, "data": _row(row, cols)}), 201

    except Exception as e:
        conn.rollback()
        err_msg = str(e)
        if "Duplicate entry" in err_msg and "party_code" in err_msg:
            err_msg = "Party code already exists. Please use a unique party code."
        return jsonify({"success": False, "message": err_msg}), 500

    finally:
        cursor.close()
        conn.close()


def get_partymasters():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        try:
            cursor.callproc("sp_get_parties")
            result = list(cursor.stored_results())[0]
            cols = [c[0] for c in result.description]
            rows = result.fetchall()
        except Exception:
            cursor.execute("SELECT * FROM party_masters ORDER BY id DESC")
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()

        data = [_row(r, cols) for r in rows]
        return jsonify({"success": True, "data": data}), 200

    finally:
        cursor.close()
        conn.close()


def get_partymaster(partymaster_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        try:
            cursor.callproc("sp_get_party", (partymaster_id,))
            result = list(cursor.stored_results())[0]
            row = result.fetchone()
            cols = [c[0] for c in result.description] if result else []
        except Exception:
            cursor.execute("SELECT * FROM party_masters WHERE id = %s", (partymaster_id,))
            row = cursor.fetchone()
            cols = [c[0] for c in cursor.description] if row else []

        if not row:
            return jsonify({"success": False, "message": "Party master not found"}), 404

        return jsonify({"success": True, "data": _row(row, cols)}), 200

    finally:
        cursor.close()
        conn.close()


def update_partymaster(partymaster_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    mobiles_json = json.dumps(data.get("mobiles")) if data.get("mobiles") else None
    emails_json = json.dumps(data.get("emails")) if data.get("emails") else None

    try:
        try:
            cursor.callproc("sp_update_party", (
                partymaster_id,
                data.get("party_name"),
                data.get("party_code"),
                data.get("address"),
                data.get("state"),
                data.get("country"),
                data.get("pincode"),
                mobiles_json,
                emails_json,
                data.get("pan_number"),
                data.get("gst_number")
            ))
            result = list(cursor.stored_results())[0]
            cols = [c[0] for c in result.description]
            row = result.fetchone()
            conn.commit()
            return jsonify({"success": True, "data": _row(row, cols)})
        except Exception:
            sql = """
                UPDATE party_masters SET
                    party_name = %s,
                    party_code = %s,
                    address = %s,
                    state = %s,
                    country = %s,
                    pincode = %s,
                    mobiles = %s,
                    emails = %s,
                    pan_number = %s,
                    gst_number = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                data.get("party_name"),
                data.get("party_code"),
                data.get("address"),
                data.get("state"),
                data.get("country"),
                data.get("pincode"),
                mobiles_json,
                emails_json,
                data.get("pan_number"),
                data.get("gst_number"),
                partymaster_id
            ))
            conn.commit()

            cursor.execute("SELECT * FROM party_masters WHERE id = %s", (partymaster_id,))
            cols = [c[0] for c in cursor.description]
            row = cursor.fetchone()
            return jsonify({"success": True, "data": _row(row, cols)})

    except Exception as e:
        conn.rollback()
        err_msg = str(e)
        if "Duplicate entry" in err_msg and "party_code" in err_msg:
            err_msg = "Party code already exists. Please use a unique party code."
        return jsonify({"success": False, "message": err_msg}), 500

    finally:
        cursor.close()
        conn.close()


def delete_partymaster(partymaster_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        try:
            cursor.callproc("sp_delete_party", (partymaster_id,))
            conn.commit()
        except Exception:
            cursor.execute("DELETE FROM party_masters WHERE id = %s", (partymaster_id,))
            conn.commit()

        return jsonify({"success": True, "message": "Deleted successfully"})

    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 400

    finally:
        cursor.close()
        conn.close()