

from flask import (
    Blueprint,
    jsonify,
    request,
    g
)

from database.db import get_db_connection

from utils.auth import (
    login_required
)

from services.device_services import (
    register_device_service,
    get_devices_service,
    get_device_service,
    update_device_status_service,
    get_device_logs_service
)

from utils.logger import log_activity

from datetime import (
    datetime,
    timezone
)

device_bp = Blueprint(
    "devices",
    __name__
)

# Devices Endpoint

@device_bp.route('/api/v1/devices', methods=['GET'])
@login_required
def get_devices():

    search = request.args.get("search", "")

    result, status_code = get_devices_service(search)

    return jsonify(result), status_code



    # POST code.

@device_bp.route('/api/v1/devices', methods=['POST'])
@login_required
def register_device():

    data = request.get_json()

    result, status_code = register_device_service(
        g.current_user["user_id"],
        g.current_user["username"],
        data
    )

    return jsonify(result), status_code



    # Retrieve Single Device By ID
@device_bp.route('/api/v1/devices/<int:device_id>', methods=['GET'])
@login_required
def get_single_device(device_id):

    result, status_code = get_device_service(device_id)

    return jsonify(result), status_code



    # Update Device Status
@device_bp.route('/api/v1/devices/<int:device_id>/status', methods=['PATCH'])
@login_required
def update_device_status(device_id):

    data = request.get_json()

    result, status_code = update_device_status_service(
        device_id,
        data
    )

    return jsonify(result), status_code



    # Retrieve Logs for a Specific Device

@device_bp.route('/api/v1/devices/<int:device_id>/logs', methods=['GET'])
@login_required
def get_device_logs(device_id):

    result, status_code = get_device_logs_service(device_id)

    return jsonify(result), status_code