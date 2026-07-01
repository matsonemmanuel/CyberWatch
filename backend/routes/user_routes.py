
from flask import (
    Blueprint,
    jsonify,
    request,
    g
)

from database.db import get_db_connection

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

    connection = get_db_connection()

    cursor = connection.cursor()

    # Optional search functionality for filtering users by username or email

    search = request.args.get(
        "search",
        ""
    )

    cursor.execute(
        """
        SELECT
            id,
            username,
            email,
            role,
            created_at
        FROM users
        WHERE
            username LIKE ?
            OR email LIKE ?
            OR role LIKE ?
        """,
        (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )
    )

    users = cursor.fetchall()

    connection.close()

    user_list = []

    for user in users:

        user_list.append({
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"]
        })

    return jsonify({
        "status": "success",
        "count": len(user_list),
        "data": user_list
    })

    # Get Single User By ID Endpoint

@user_bp.route('/api/v1/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            email,
            role,
            created_at
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    if not user:

        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404

    return jsonify({
        "status": "success",
        "data": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"]
        }
    }), 200

    # Update User Role Endpoint

@user_bp.route('/api/v1/users/<int:user_id>/role', methods=['PATCH'])
@admin_required
def update_user_role(user_id):

    data = request.get_json()

    role = data.get("role")

    # Validate role

    allowed_roles = [
        "admin",
        "analyst"
    ]

    if role not in allowed_roles:

        return jsonify({
            "status": "error",
            "message": "Invalid role"
        }), 400

    connection = get_db_connection()

    cursor = connection.cursor()

    # Check if user exists

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:

        connection.close()

        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404

    # Update role

    cursor.execute(
        """
        UPDATE users
        SET role = ?
        WHERE id = ?
        """,
        (
            role,
            user_id
        )
    )

    connection.commit()

    # Log the role change activity for auditing purposes

    log_activity(
        g.current_user["user_id"],
        g.current_user["username"],
        f"Changed user {user_id} role to {role}"
    )

    connection.close()

    return jsonify({
        "status": "success",
        "message": f"User role updated to {role}"
    }), 200