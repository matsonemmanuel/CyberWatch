
from multiprocessing.dummy import connection

from database.db import get_db_connection

from utils.logger import log_activity

def get_users_service(search):
    """
    Retrieve all users with optional search filtering.
    """

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

    return {
        "status": "success",
        "count": len(user_list),
        "data": user_list
    }, 200

def get_user_service(user_id):
    """
    Retrieve a single user by ID.
    """

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

      return {
          "status": "error",
          "message": "User not found"
      }, 404
    
    return {
        "status": "success",
        "data": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"]
        }
    }, 200

def update_user_role_service(
    user_id,
    current_user_id,
    current_username,
    data
):
    """
    Update the role of a user.
    """

    role = data.get("role")

    allowed_roles = [
        "admin",
        "analyst"
    ]

    if role not in allowed_roles:

        return {
            "status": "error",
            "message": "Invalid role"
        }, 400

    connection = get_db_connection()

    cursor = connection.cursor()

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

    log_activity(
        current_user_id,
        current_username,
        f"Changed user {user_id} role to {role}"
    )

    connection.close()

    return {
        "status": "success",
        "message": f"User role updated to {role}"
    }, 200

