import re

from werkzeug.security import check_password_hash

from werkzeug.security import generate_password_hash

from config.constants import ALLOWED_USER_ROLES

from datetime import (
    datetime,
    timezone,
    timedelta
)

import jwt
import os

from dotenv import load_dotenv

from database.db import get_db_connection

from utils.logger import log_activity

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        60
    )
)

def login_service(data):
    """
    Responsibility:
        Authenticate a CyberWatch user and generate a JWT access token.

    Business Rules:
        • Username and password are required.
        • User must be registered.
        • Password must match the stored password hash.
        • Successful login must be recorded in the audit log.
        • Failed login attempts must be recorded in the audit log.

    Returns:
        JSON response containing the JWT access token and authenticated
        user's basic information.
    """

    username = data.get("username")

    password = data.get("password")

    # Validate required fields

    if not username or not password:

        return {
            "status": "error",
            "message": "Username and password are required"
        }, 400

    connection = get_db_connection()

    cursor = connection.cursor()

    # Retrieve the user by username

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    # Business Rule:
    # User must be registered

    if not user:

        log_activity(
            None,
            username,
            "Failed login (invalid username)"
        )

        connection.close()

        return {
            "status": "error",
            "message": "Invalid username or password"
        }, 401

    # Business Rule:
    # Password must match

    if not check_password_hash(
        user["password"],
        password
    ):

        log_activity(
            user["id"],
            user["username"],
            "Failed login (incorrect password)"
        )

        connection.close()

        return {
            "status": "error",
            "message": "Invalid username or password"
        }, 401

    # Generate JWT access token

    expiration_time = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "user_id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "exp": expiration_time
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm="HS256"
    )

    # Record successful authentication

    log_activity(
        user["id"],
        user["username"],
        "User logged in"
    )

    connection.close()

    return {
        "status": "success",
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    }, 200

    #Register a new CyberWatch user


def register_service(
    current_user_id,
    current_username,
    data
):
    """
    Responsibility:
        Register a new CyberWatch user.

    Business Rules:
        • Only authenticated administrators may register users.
        • Username is required.
        • Email is required.
        • Password is required.
        • Role is required.
        • Username must be unique.
        • Email must be unique.
        • Email format must be valid.
        • Password must be securely hashed.
        • Registration must be recorded in the audit log.

    Returns:
        JSON response containing the newly created user.
    """

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    # Validate required fields

    if not username or not email or not password or not role:

        return {
            "status": "error",
            "message": "Username, email, password and role are required"
        }, 400

    # Validate email format
    email_pattern = (
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    if not re.match(email_pattern, email):

        return {
            "status": "error",
            "message": "Invalid email format"
        }, 400

    # Validate allowed roles

    ALLOWED_USER_ROLES

    if role not in ALLOWED_USER_ROLES:

        return {
            "status": "error",
            "message": "Invalid user role"
        }, 400

    # Securely hash the password

    hashed_password = generate_password_hash(password)

    connection = get_db_connection()

    cursor = connection.cursor()

    # Check whether the username already exists

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        connection.close()

        return {
            "status": "error",
            "message": "Username already exists"
        }, 409

    # Check whether the email already exists
    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    existing_email = cursor.fetchone()

    if existing_email:

        connection.close()

        return {
            "status": "error",
            "message": "Email already exists"
        }, 409

    timestamp = (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )

    # Register the new user

    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            email,
            password,
            role,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            username,
            email,
            hashed_password,
            role,
            timestamp
        )
    )

    connection.commit()

    user_id = cursor.lastrowid

    # Record the registration activity

    log_activity(
        current_user_id,
        current_username,
        f"Registered new user '{username}' with role '{role}'"
    )

    connection.close()

    return {
        "status": "success",
        "message": "User registered successfully",
        "data": {
            "id": user_id,
            "username": username,
            "email": email,
            "role": role,
            "created_at": timestamp
        }
    }, 201

# Retrieve the currently authenticated user's details

def get_current_user_service(user_id):
    """
    Responsibility:
        Retrieve the profile information of the currently authenticated user.

    Business Rules:
        • User must be authenticated.
        • User must exist.
        • Password hash must never be returned.
        • This operation does not modify the system state.
        • No audit log is required.

    Returns:
        JSON response containing the authenticated user's profile information.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    # Retrieve the authenticated user's profile
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

    # Business Rule:
    # User must exist
    if not user:

        connection.close()

        return {
            "status": "error",
            "message": "User not found"
        }, 404

    connection.close()

    return {
        "status": "success",
        "message": "User profile retrieved successfully",
        "data": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"]
        }
    }, 200



    # Log out the current user


def logout_service(user_id, username):
    """
    Responsibility:
        Log out the authenticated user and record the logout activity.

    Business Rules:
        • User must already be authenticated.
        • Logout activity must be recorded in the audit log.
        • No system data is modified.
        • JWT invalidation is handled on the client side by removing
          the stored access token.

    Returns:
        JSON response confirming a successful logout.
    """

    # Record the logout activity for auditing purposes
    log_activity(
        user_id,
        username,
        "User logged out"
    )

    return {
        "status": "success",
        "message": "Logout successful"
    }, 200

  # Change the password of the authenticated user

def change_password_service(
    user_id,
    username,
    data
):
    """
    Responsibility:
        Update the password of the currently authenticated user.

    Business Rules:
        • User must already be authenticated.
        • Current password is required.
        • New password is required.
        • User must exist.
        • Current password must match the stored password.
        • New password must be different from the current password.
        • New password must be securely hashed.
        • Password change must be recorded in the audit log.

    Returns:
        JSON response confirming the password change.
    """

    current_password = data.get("current_password")
    new_password = data.get("new_password")

    # Validate required fields
    if not current_password or not new_password:

        return {
            "status": "error",
            "message": "Current password and new password are required"
        }, 400

    # Business Rule:
    # New password must be different from the current password
    if current_password == new_password:

        return {
            "status": "error",
            "message": "New password must be different from the current password"
        }, 400

    connection = get_db_connection()

    cursor = connection.cursor()

    # Retrieve the authenticated user's password
    cursor.execute(
        """
        SELECT
            id,
            password
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    # Business Rule:
    # User must exist
    if not user:

        connection.close()

        return {
            "status": "error",
            "message": "User not found"
        }, 404

    # Business Rule:
    # Current password must match
    if not check_password_hash(
        user["password"],
        current_password
    ):

        connection.close()

        return {
            "status": "error",
            "message": "Current password is incorrect"
        }, 401

    # Securely hash the new password
    hashed_password = generate_password_hash(
        new_password
    )

    # Update the password
    cursor.execute(
        """
        UPDATE users
        SET password = ?
        WHERE id = ?
        """,
        (
            hashed_password,
            user_id
        )
    )

    connection.commit()

    # Record the password change for auditing purposes
    log_activity(
        user_id,
        username,
        "Password changed"
    )

    connection.close()

    return {
        "status": "success",
        "message": "Password changed successfully"
    }, 200