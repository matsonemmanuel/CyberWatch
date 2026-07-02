
from flask import (
    Blueprint,
    jsonify,
    request,
    g
)



import os

from services.auth_services import (
    login_service,
    register_service,
    get_current_user_service,
    logout_service,
    change_password_service
)

from dotenv import load_dotenv

from database.db import get_db_connection

from utils.auth import (
    login_required
)

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        60
    )
)

from utils.logger import log_activity


auth_bp = Blueprint(
    "auth",
    __name__
)

# Home Endpoint
@auth_bp.route('/api/v1/')
def home():

    return jsonify({
        "status": "success",
        "message": "CyberWatch API Version 1 Running Successfully"
    })

# Health Check Endpoint

@auth_bp.route('/api/v1/health', methods=['GET'])
def health_check():

    return jsonify({
        "status": "success",
        "message": "CyberWatch API is running"
    }), 200


   #AUTHENTICATION ENDPOINTS

  # User Registration Endpoint

@auth_bp.route('/api/v1/auth/register', methods=['POST'])
def register_user():

    data = request.get_json()

    result, status_code = register_service(data)

    return jsonify(result), status_code

     # User Login Endpoint

@auth_bp.route('/api/v1/auth/login', methods=['POST'])
def login_user():

    data = request.get_json()

    result, status_code = login_service(data)

    return jsonify(result), status_code

# Get Current User Endpoint

@auth_bp.route('/api/v1/auth/me', methods=['GET'])
@login_required
def get_current_user():

    result, status_code = get_current_user_service(
        g.current_user["user_id"]
    )

    return jsonify(result), status_code


    # Logout Endpoint

@auth_bp.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout_user():

    result, status_code = logout_service(
        g.current_user["user_id"],
        g.current_user["username"]
    )

    return jsonify(result), status_code

    # Change Password Endpoint

@auth_bp.route('/api/v1/auth/change-password', methods=['PATCH'])
@login_required
def change_password():

    data = request.get_json()

    result, status_code = change_password_service(
        g.current_user["user_id"],
        g.current_user["username"],
        data
    )

    return jsonify(result), status_code