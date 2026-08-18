
from flask import (
    Blueprint,
    jsonify,
    request,
    g
)

from services.log_services import (
    get_logs_service,
    create_log_service,
    get_log_service,
    update_log_service,
    update_log_status_service,
    archive_log_service,
    get_log_history_service
)

from services.log_history_service import (
    get_log_history_service
)

from database.db import get_db_connection

from utils.auth import (
    login_required,
    admin_required
)

from utils.logger import log_activity

from datetime import (
    datetime,
    timezone
)

log_bp = Blueprint(
    "logs",
    __name__
)

     # Logs Endpoint


@log_bp.route('/api/v1/logs', methods=['GET'])
@login_required
def get_logs():

    severity = request.args.get("severity")
    status = request.args.get("status")
    archived = request.args.get("archived")
    search = request.args.get("search")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    result, status_code = get_logs_service(
        severity,
        status,
        archived,
        search,
        page,
        limit
    )

    return jsonify(result), status_code


    # POST METHOD

@log_bp.route('/api/v1/logs', methods=['POST'])
@login_required
def create_log():
    

        data = request.get_json()

        result, status_code = create_log_service(
            g.current_user["user_id"],
            g.current_user["username"],
            data
        )

        return jsonify(result), status_code

            
    # Retrieve Single Log By ID

    
@log_bp.route('/api/v1/logs/<int:log_id>', methods=['GET'])
@login_required
def get_single_log(log_id):

    result, status_code = get_log_service(log_id)

    return jsonify(result), status_code


    # Update Log By ID

@log_bp.route('/api/v1/logs/<int:log_id>', methods=['PUT'])
@login_required
def update_log(log_id):

    data = request.get_json()

    result, status_code = update_log_service(
        log_id,
        g.current_user["user_id"],
        g.current_user["username"],
        data
    )

    return jsonify(result), status_code

# Update Log Status By ID

@log_bp.route('/api/v1/logs/<int:log_id>/status', methods=['PATCH'])
@login_required
def update_status(log_id):

    data = request.get_json()

    result, status_code = update_log_status_service(
        log_id,
        g.current_user["user_id"],
        g.current_user["username"],
        data
    )

    return jsonify(result), status_code

# Archive Log By ID

@log_bp.route('/api/v1/logs/<int:log_id>/archive', methods=['PATCH'])
@admin_required
def archive_log(log_id):

    result, status_code = archive_log_service(
        log_id,
        g.current_user["user_id"],
        g.current_user["username"]
    )

    return jsonify(result), status_code

# =========================================================
# GET LOG HISTORY
# =========================================================

@log_bp.route('/api/v1/log-history', methods=['GET'])
@login_required
def get_log_history():

    result, status_code = get_log_history_service()

    return jsonify(result), status_code