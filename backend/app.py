
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
import jwt

from functools import wraps

from flask import g

from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError
)

from datetime import timedelta

from flask import Flask, jsonify, request 
from flask_cors import CORS

from datetime import datetime, timezone

import os
from database.db import get_db_connection

from utils.auth import (
    verify_token,
    login_required,
    admin_required
)

from utils.logger import log_activity

from routes.auth_routes import auth_bp

from routes.device_routes import device_bp

from routes.user_routes import user_bp

from routes.log_routes import log_bp

from routes.dashboard_routes import dashboard_bp

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

    # CORS Configuration

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "http://localhost:5173"
        }
    }
)
    # Register Blueprints

app.register_blueprint(auth_bp)
app.register_blueprint(device_bp)
app.register_blueprint(user_bp)
app.register_blueprint(log_bp)
app.register_blueprint(dashboard_bp)

# JWT Configuration

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)


print(app.url_map)

   
if __name__ == '__main__':

    app.run(debug=True)
