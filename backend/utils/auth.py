
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

from datetime import datetime
from datetime import timezone

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")




# Token Verification Function
def verify_token():

    auth_header = request.headers.get("Authorization")

    print("\n========== AUTH DEBUG ==========")
    print("Authorization Header:", auth_header)

    if not auth_header:

        print("No Authorization header received.")

        return None, (
            jsonify({
                "status": "error",
                "message": "Authorization token is missing"
            }),
            401
        )

    if not auth_header.startswith("Bearer "):

        print("Authorization header format is invalid.")

        return None, (
            jsonify({
                "status": "error",
                "message": "Invalid authorization format"
            }),
            401
        )

    token = auth_header.split(" ")[1]

    print("JWT Token:", token)

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=["HS256"]
        )

        print("Decoded Payload:", payload)

        return payload, None

    except ExpiredSignatureError:

        print("ERROR: Token has expired.")

        return None, (
            jsonify({
                "status": "error",
                "message": "Token has expired"
            }),
            401
        )

    except ExpiredSignatureError:

            print("Current UTC:", datetime.now(timezone.utc))
            print("Token expired.")

            return None, (
                jsonify({
                    "status": "error",
                    "message": "Token has expired"
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