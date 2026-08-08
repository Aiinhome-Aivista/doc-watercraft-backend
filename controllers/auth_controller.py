import jwt
import bcrypt
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
            SELECT id, username, role, full_name, password, is_active
            FROM users
            WHERE email=%s
        """, (data["email"],))

        user = cursor.fetchone()

        if not user:
            return jsonify({
                "status": "error",
                "message": "Invalid credentials"
            }), 401

        # Verify password hash
        stored_hash = user[4]
        if not bcrypt.checkpw(data["password"].encode('utf-8'), stored_hash.encode('utf-8') if isinstance(stored_hash, str) else stored_hash):
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

def change_password():
    data = request.get_json()

    if not data or not data.get("old_password") or not data.get("new_password"):
        return jsonify({
            "status": "error",
            "message": "Old and new password required"
        }), 400

    try:
        user_id = request.user["user_id"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # 🔹 Verify old password
        cursor.execute("SELECT password FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 400
        stored_hash = user[0]
        if not bcrypt.checkpw(data["old_password"].encode('utf-8'), stored_hash.encode('utf-8') if isinstance(stored_hash, str) else stored_hash):
            return jsonify({
                "status": "error",
                "message": "Old password incorrect"
            }), 400

        # 🔹 Update password with new hash
        new_hash = bcrypt.hashpw(data["new_password"].encode('utf-8'), bcrypt.gensalt())
        cursor.execute("""
            UPDATE users 
            SET password=%s 
            WHERE id=%s
        """, (new_hash, user_id))

        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Password changed successfully"
        }), 200

    except Exception as e:
        print(f"Error in change_password: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

    finally:
        if 'conn' in locals() and conn:
            conn.close()

def admin_change_user_password(user_id):
    data = request.get_json()

    if not data or not data.get("new_password"):
        return jsonify({
            "status": "error",
            "message": "New password required"
        }), 400

    try:
        # 🔹 Check role
        if request.user.get("role") != "admin":
            return jsonify({
                "status": "error",
                "message": "Only admin can change user password"
            }), 403

        conn = get_db_connection()
        cursor = conn.cursor()

        # 🔹 Check user exists
        cursor.execute("SELECT id FROM users WHERE id=%s", (user_id,))
        if not cursor.fetchone():
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404

        # 🔹 Update password
        new_hash = bcrypt.hashpw(data["new_password"].encode('utf-8'), bcrypt.gensalt())
        cursor.execute("""
                UPDATE users 
                SET password=%s 
                WHERE id=%s
            """, (new_hash, user_id))

        conn.commit()

        return jsonify({
            "status": "success",
            "message": "User password updated by admin"
        }), 200

    except Exception as e:
        print(f"Error in admin_change_user_password: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

    finally:
        if 'conn' in locals() and conn:
            conn.close()

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
        hashed_pw = bcrypt.hashpw(data.get("password").encode('utf-8'), bcrypt.gensalt())
        cursor.execute("""
            INSERT INTO users 
            (role, username, password, full_name, mobile, email, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            "user",
            data.get("username"),
            hashed_pw,
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
            '{}'   
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
        print(f"Error in register: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

    finally:
        if 'conn' in locals() and conn:
            conn.close()


def get_loggedin_user():
    try:
        user_id = request.user["user_id"]

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

    except Exception as e:
        print(f"Error in get_loggedin_user: {e}")
        return jsonify({
            "status": "error",
            "message": "Internal server error"
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


def update_access_rights(user_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No data provided"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        import json

        # 🔹 Convert dict → JSON string
        access_json = json.dumps(data)

        # 🔹 Check if record exists
        cursor.execute("""
            SELECT id FROM user_access_rights WHERE user_id=%s
        """, (user_id,))
        exists = cursor.fetchone()

        if exists:
            # 🔹 UPDATE
            cursor.execute("""
                UPDATE user_access_rights
                SET access_rights=%s
                WHERE user_id=%s
            """, (access_json, user_id))
        else:
            # 🔹 INSERT (if not exists)
            cursor.execute("""
                INSERT INTO user_access_rights (user_id, access_rights)
                VALUES (%s, %s)
            """, (user_id, access_json))

        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Access rights updated successfully",
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        conn.close()     


def get_access_rights(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT access_rights 
            FROM user_access_rights 
            WHERE user_id=%s
        """, (user_id,))

        result = cursor.fetchone()

        if not result:
            return jsonify({
                "status": "error",
                "message": "No access rights found"
            }), 404

        access_rights = result[0]

        # 🔹 Convert JSON string → dict if needed
        import json
        if isinstance(access_rights, str):
            access_rights = json.loads(access_rights)

        return jsonify({
            "status": "success",
            "data": {
                "user_id": user_id,
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


def delete_user(user_id):
    try:
        # 🔹 Check role
        if request.user.get("role") != "admin":
            return jsonify({
                "status": "error",
                "message": "Only admin can delete user"
            }), 403

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, username FROM users WHERE id=%s", (user_id,))
        user_to_delete = cursor.fetchone()
        if not user_to_delete:
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404

        # Delete the user from the users table.
        # Cascade deletes will handle user_access_rights.
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()

        return jsonify({
            "status": "success",
            "message": f"User {user_to_delete[1]} deleted successfully"
        }), 200

    except Exception as e:
        print(f"Error in delete_user: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

    finally:
        if 'conn' in locals() and conn:
            conn.close()           