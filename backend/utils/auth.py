
import os

from dotenv import load_dotenv

from functools import wraps

from flask import (
    request,
    jsonify,
    g
)

import jwt

from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError
)

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")




# Token Verification Function
def verify_token():

    auth_header = request.headers.get("Authorization")

    if not auth_header:

        return None, (
            jsonify({
                "status": "error",
                "message": "Authorization token is missing"
            }),
            401
        )

    if not auth_header.startswith("Bearer "):

        return None, (
            jsonify({
                "status": "error",
                "message": "Invalid authorization format"
            }),
            401
        )

    token = auth_header.split(" ")[1]

    # Verify the JWT token

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload, None

    except ExpiredSignatureError:

        return None, (
            jsonify({
                "status": "error",
                "message": "Token has expired"
            }),
            401
        )

    except InvalidTokenError:

        return None, (
            jsonify({
                "status": "error",
                "message": "Invalid token"
            }),
            401
        )
    
    # Decorator to Require Login for Certain Endpoints

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        payload, error = verify_token()

        if error:
            return error
        
        g.current_user = payload

        return f(*args, **kwargs)

    return decorated_function

    # Decorator to Require Admin Role for Certain Endpoints

def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        payload, error = verify_token()

        if error:
            return error

        g.current_user = payload

        if payload["role"] != "admin":

            return jsonify({
                "status": "error",
                "message": "Access denied"
            }), 403

        return f(*args, **kwargs)

    return decorated_function