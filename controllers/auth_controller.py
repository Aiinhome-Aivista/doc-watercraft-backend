import jwt
from datetime import datetime, timedelta
from flask import request, jsonify, current_app
from database.db_connection import get_db_connection


# def login():
#     data = request.get_json()

#     if not data or not data.get("username") or not data.get("password"):
#         return jsonify({
#             "status": "error",
#             "message": "Username and password required"
#         }), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         cursor.execute("""
#             SELECT id, username, role, full_name, is_active
#             FROM users
#             WHERE username=%s AND password=%s
#         """, (data["username"], data["password"]))

#         user = cursor.fetchone()

#         if not user:
#             return jsonify({
#                 "status": "error",
#                 "message": "Invalid credentials"
#             }), 401

#         if not user[4]:
#             return jsonify({
#                 "status": "error",
#                 "message": "User inactive"
#             }), 403

#         user_id = user[0]

#         # permissions
#         cursor.execute("SELECT * FROM user_permissions WHERE user_id=%s", (user_id,))
#         perm = cursor.fetchone()
#         perm_keys = [desc[0] for desc in cursor.description] if perm else []
#         perm_data = dict(zip(perm_keys, perm)) if perm else {}

#         # 🔐 CREATE TOKEN
#         token = jwt.encode({
#             "user_id": user_id,
#             "username": user[1],
#             "role": user[2],
#             "exp": datetime.utcnow() + timedelta(hours=8)  # token expiry
#         }, current_app.config['SECRET_KEY'], algorithm="HS256")

#         return jsonify({
#             "status": "success",
#             "token": token,
#             "data": {
#                 "id": user_id,
#                 "username": user[1],
#                 "role": user[2],
#                 "full_name": user[3],
#                 "permissions": perm_data
#             }
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

#     finally:
#         conn.close()
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({
            "status": "error",
            "message": "Username and password required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id,email, role,username, full_name, is_active
            FROM users
            WHERE email=%s AND password=%s
        """, (data["email"], data["password"]))

        user = cursor.fetchone()

        if not user:
            return jsonify({
                "status": "error",
                "message": "Invalid credentials"
            }), 401

        if not user[4]:
            return jsonify({
                "status": "error",
                "message": "User inactive"
            }), 403

        user_id = user[0]

        

        # 🔐 CREATE TOKEN
        token = jwt.encode({
            "user_id": user_id,
            "email": user[1],
            "role": user[2],
            "exp": datetime.utcnow() + timedelta(hours=8)  # token expiry
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            "status": "success",
            "token": token,
            "data": {
                "id": user_id,
                "email": user[1],
                "role": user[2],
                "full_name": user[4]
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        conn.close()


def register():
    data = request.get_json()

    # 🔹 Basic validation
    if not data or not data.get("password") or not data.get("email"):
        return jsonify({
            "status": "error",
            "message": "username, password and role are required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 🔹 Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username=%s", (data["username"],))
        if cursor.fetchone():
            return jsonify({
                "status": "error",
                "message": "Username already exists"
            }), 400

        # 🔹 Insert user
        query = """
            INSERT INTO users 
            (role, username, password, full_name, mobile, email, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            "user",
            data.get("username"),
            data.get("password"),   
            data.get("full_name"),
            data.get("mobile"),
            data.get("email"),
            data.get("is_active", True)
        ))

        conn.commit()
        user_id = cursor.lastrowid

        return jsonify({
            "status": "success",
            "message": "User registered successfully",
            "data": {
                "id": user_id,
                "username": data.get("username"),
                "email": data.get("email"),
                "full_name": data.get("full_name")
            }
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        conn.close()        