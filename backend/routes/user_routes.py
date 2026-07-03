
from re import search

from flask import (
    Blueprint,
    jsonify,
    request,
    g
)

from database.db import get_db_connection

from services.user_services import (
    get_users_service,
    get_user_service,
    update_user_role_service
)

from utils.auth import (
    admin_required
)

from utils.logger import log_activity

user_bp = Blueprint(
    "users",
    __name__
)


    #USER MANAGEMENT ENDPOINTS

    # Get All Users Endpoint

@user_bp.route('/api/v1/users', methods=['GET'])
@admin_required
def get_users():
    search = request.args.get("search", "")

    result, status_code = get_users_service(search)

    return jsonify(result), status_code


    # Get Single User By ID Endpoint

@user_bp.route('/api/v1/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):

    result, status_code = get_user_service(user_id)

    return jsonify(result), status_code


    # Update User Role Endpoint

@user_bp.route('/api/v1/users/<int:user_id>/role', methods=['PATCH'])
@admin_required
def update_user_role(user_id):

    data = request.get_json()

    result, status_code = update_user_role_service(
        user_id,
        g.current_user["user_id"],
        g.current_user["username"],
        data
    )

    return jsonify(result), status_code