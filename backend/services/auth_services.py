
from werkzeug.security import check_password_hash

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
    Authenticate a user and return login details.
    """

    username = data.get("username")
    password = data.get("password")

    if not username or not password:

        return {
            "status": "error",
            "message": "Username and password are required"
        }, 400
    
     # Connect to database
    connection = get_db_connection()

    cursor = connection.cursor()

    # Find user by username in the database
    cursor.execute(
        """
        SELECT * FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    # Check if the provided password matches the hashed password in the database

    if not check_password_hash(
        user["password"],
        password
    ):

        connection.close()

        return({
            "status": "error",
            "message": "Invalid username or password"
        }), 401

        # Generate JWT token for authenticated user

    expiration_time = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
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

    # Add audit log here

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

    # Register a new user

from werkzeug.security import generate_password_hash

def register_service(data):
    """
    Register a new CyberWatch user.
    """

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:

        return {
            "status": "error",
            "message": "All fields are required"
        }, 400
    
    #Password hashing for security

    hashed_password = generate_password_hash(password)

    # Database connection
    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if username already exists
    cursor.execute(
        """
        SELECT * FROM users
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

    # Check if email already exists
    cursor.execute(
        """
        SELECT * FROM users
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
    
    
    timestamp = datetime.now(
    timezone.utc
).isoformat().replace('+00:00', 'Z')
    
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
        "analyst",
        timestamp
    )
)
    
    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return {
        "status": "success",
        "message": "User registered successfully",
        "data": {
            "id": user_id,
            "username": username,
            "email": email,
            "role": "analyst",
            "created_at": timestamp
        }
    }, 201

# Retrieve the currently authenticated user's details

def get_current_user_service(user_id):
    """
    Retrieve the currently authenticated user's details.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:

      return {
          "status": "error",
          "message": "User not found"
      }, 404

    connection.close()

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

    # Log out the current user


def logout_service(user_id, username):
    """
    Log out the current user.
    """

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

def change_password_service(user_id, username, data):
    """
    Change the password of the authenticated user.
    """

    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not current_password or not new_password:

        return {
            "status": "error",
            "message": "Current password and new password are required"
        }, 400

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    if not check_password_hash(
    user["password"],
    current_password
):

      connection.close()

      return {
          "status": "error",
          "message": "Current password is incorrect"
      }, 401
    
    hashed_password = generate_password_hash(
    new_password
)
    
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