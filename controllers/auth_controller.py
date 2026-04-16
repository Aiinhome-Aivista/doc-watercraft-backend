import jwt
from datetime import datetime, timedelta
from flask import request, jsonify, current_app
from database.db_connection import get_db_connection


def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({
            "status": "error",
            "message": "Email and password required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 🔹 Get user
        cursor.execute("""
            SELECT id, username, role, full_name,is_active
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

        # 🔹 Get access rights (JSON)
        cursor.execute("""
            SELECT access_rights 
            FROM user_access_rights 
            WHERE user_id=%s
        """, (user_id,))

        perm = cursor.fetchone()

        # Convert JSON (MySQL returns string sometimes)
        access_rights = perm[0] if perm else {}

        # If string → convert to dict
        if isinstance(access_rights, str):
            import json
            access_rights = json.loads(access_rights)

        # 🔐 CREATE TOKEN
        token = jwt.encode({
            "user_id": user_id,
            "username": user[1],
            "role": user[2],
            "exp": datetime.utcnow() + timedelta(hours=8)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            "status": "success",
            "token": token,
            "data": {
                "id": user_id,
                "username": user[1],
                "role": user[2],
                "full_name": user[3],
                "access_rights": access_rights
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        conn.close()

# def login():
#     data = request.get_json()

#     if not data or not data.get("email") or not data.get("password"):
#         return jsonify({
#             "status": "error",
#             "message": "Username and password required"
#         }), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         cursor.execute("""
#             SELECT id,email, role,username, full_name, is_active
#             FROM users
#             WHERE email=%s AND password=%s
#         """, (data["email"], data["password"]))

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

        

#         # 🔐 CREATE TOKEN
#         token = jwt.encode({
#             "user_id": user_id,
#             "email": user[1],
#             "role": user[2],
#             "exp": datetime.utcnow() + timedelta(hours=8)  # token expiry
#         }, current_app.config['SECRET_KEY'], algorithm="HS256")

#         return jsonify({
#             "status": "success",
#             "token": token,
#             "data": {
#                 "id": user_id,
#                 "email": user[1],
#                 "role": user[2],
#                 "full_name": user[4]
#             }
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

#     finally:
#         conn.close()


def register():
    data = request.get_json()

    # 🔹 Validation
    if not data or not data.get("username") or not data.get("password") or not data.get("email"):
        return jsonify({
            "status": "error",
            "message": "username, password and email are required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 🔹 Check username
        cursor.execute("SELECT id FROM users WHERE username=%s", (data["username"],))
        if cursor.fetchone():
            return jsonify({
                "status": "error",
                "message": "Username already exists"
            }), 400

        # 🔹 Insert user
        cursor.execute("""
            INSERT INTO users 
            (role, username, password, full_name, mobile, email, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            "user",
            data.get("username"),
            data.get("password"),
            data.get("full_name"),
            data.get("mobile"),
            data.get("email"),
            data.get("is_active", True)
        ))

        user_id = cursor.lastrowid

        # 🔹 Insert NULL permissions (empty JSON)
        cursor.execute("""
            INSERT INTO user_access_rights (user_id, access_rights)
            VALUES (%s, %s)
        """, (
            user_id,
            None   # or '{}' if you prefer empty JSON
        ))

        conn.commit()

        return jsonify({
            "status": "success",
            "message": "User registered successfully",
            "data": {
                "id": user_id,
                "username": data.get("username"),
                "email": data.get("email"),
                "full_name": data.get("full_name"),
                "access_rights": None
            }
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        conn.close()


def get_loggedin_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({
            "status": "error",
            "message": "Token missing"
        }), 401

    try:
        # 🔐 Extract token (Bearer TOKEN)
        token = auth_header.split(" ")[1]

        # 🔓 Decode token
        decoded = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=["HS256"]
        )

        user_id = decoded["user_id"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # 🔹 Fetch user from DB
        cursor.execute("""
            SELECT id, username, role, full_name, mobile, email, is_active
            FROM users
            WHERE id=%s
        """, (user_id,))

        user = cursor.fetchone()

        if not user:
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404

        return jsonify({
            "status": "success",
            "data": {
                "id": user[0],
                "username": user[1],
                "role": user[2],
                "full_name": user[3],
                "mobile": user[4],
                "email": user[5],
                "is_active": user[6]
            }
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({
            "status": "error",
            "message": "Token expired"
        }), 401

    except jwt.InvalidTokenError:
        return jsonify({
            "status": "error",
            "message": "Invalid token"
        }), 401

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, username, role, full_name, mobile, email, is_active
            FROM users
        """)

        users = cursor.fetchall()

        # Convert to list of dict
        user_list = []
        for user in users:
            user_list.append({
                "id": user[0],
                "username": user[1],
                "role": user[2],
                "full_name": user[3],
                "mobile": user[4],
                "email": user[5],
                "is_active": user[6]
            })

        return jsonify({
            "status": "success",
            "data": user_list
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        conn.close()