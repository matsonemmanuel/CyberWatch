
from flask import (
    Blueprint,
    jsonify,
    request,
    g
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import jwt

from datetime import (
    datetime,
    timezone,
    timedelta
)

import os

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

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    #Password hashing for security
    hashed_password = generate_password_hash(password)

    if not username or not email or not password:

        return jsonify({
            "status": "error",
            "message": "All fields are required"
        }), 400

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

        return jsonify({
            "status": "error",
            "message": "Username already exists"
        }), 409

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

        return jsonify({
            "status": "error",
            "message": "Email already exists"
        }), 409

    #Generate timestamp for user registration
    timestamp = datetime.now(
    timezone.utc
    ).isoformat().replace('+00:00', 'Z')


    # Insert new user into the database
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
            'analyst',
            timestamp
        )
    )

    # Commit the changes to the database
    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "status": "success",
        "message": "User registered successfully",
        "data": {
            "id": user_id,
            "username": username,
            "email": email,
            "role": "analyst",
            "created_at": timestamp
        }
    }), 201

     # User Login Endpoint

@auth_bp.route('/api/v1/auth/login', methods=['POST'])
def login_user():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:

        return jsonify({
            "status": "error",
            "message": "Username and password are required"
        }), 400
    
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

    # Check if user exists
    if not user:

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Invalid username or password"
        }), 401


    # Check if the provided password matches the hashed password in the database

    if not check_password_hash(
        user["password"],
        password
    ):

        connection.close()

        return jsonify({
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

    # User found
    connection.close()

    return jsonify({
        "status": "success",
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
})

# Get Current User Endpoint

@auth_bp.route('/api/v1/auth/me', methods=['GET'])
@login_required
def get_current_user():

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (g.current_user["user_id"],)
    )

    user = cursor.fetchone()

    connection.close()

    return jsonify({
        "status": "success",
        "data": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"]
        }
    })


    # Logout Endpoint

@auth_bp.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout_user():


    # Log the logout activity for auditing purposes

    log_activity(
        g.current_user["user_id"],
        g.current_user["username"],
        "User logged out"
    )

    return jsonify({
        "status": "success",
        "message": "Logout successful"
    }), 200

    # Change Password Endpoint

@auth_bp.route('/api/v1/auth/change-password', methods=['PATCH'])
@login_required
def change_password():

    data = request.get_json()

    current_password = data.get(
        "current_password"
    )

    new_password = data.get(
        "new_password"
    )

    # Validate input

    if not current_password or not new_password:

        return jsonify({
            "status": "error",
            "message": "Current password and new password are required"
        }), 400

    # Database connection

    connection = get_db_connection()

    cursor = connection.cursor()

    # Retrieve current user

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (g.current_user["user_id"],)
    )

    user = cursor.fetchone()

    # Verify current password

    if not check_password_hash(
        user["password"],
        current_password
    ):

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Current password is incorrect"
        }), 401

    # Hash new password

    hashed_password = generate_password_hash(
        new_password
    )

    # Update password

    cursor.execute(
        """
        UPDATE users
        SET password = ?
        WHERE id = ?
        """,
        (
            hashed_password,
            g.current_user["user_id"]
        )
    )

    # Save changes

    connection.commit()

    # Log the password change activity for auditing purposes

    log_activity(
        g.current_user["user_id"],
        g.current_user["username"],
        "Password changed"
    )

    connection.close()

    return jsonify({
        "status": "success",
        "message": "Password changed successfully"
    }), 200