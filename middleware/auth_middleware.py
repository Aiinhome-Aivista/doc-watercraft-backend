import jwt
from flask import request, jsonify, current_app


def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({
                "status": "error",
                "message": "Token is missing"
            }), 401

        try:
            # format: Bearer <token>
            token = token.split(" ")[1]

            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

            request.user = data  # attach user info

        except jwt.ExpiredSignatureError:
            return jsonify({
                "status": "error",
                "message": "Token expired"
            }), 401

        except Exception:
            return jsonify({
                "status": "error",
                "message": "Invalid token"
            }), 401

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper