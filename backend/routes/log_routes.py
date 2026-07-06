
from flask import (
    Blueprint,
    jsonify,
    request,
    g
)

from services.log_services import (
    get_logs_service,
    create_log_service
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

    # Connect to the database and check if the log exists before retrieving details

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM logs WHERE id = ?",
        (log_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row:

        log = {
            "id": row["id"],
            "timestamp": row["timestamp"],
            "device_id": row["device_id"],
            "event": row["event"],
            "severity": row["severity"],
            "status": row["status"],
            "archived": bool(row["archived"])
        }

        return jsonify({
            "status": "success",
            "log": log
        })

    return jsonify({
        "status": "error",
        "message": "Log not found"
    }), 404


    # Update Log By ID
@log_bp.route('/api/v1/logs/<int:log_id>', methods=['PUT'])
@login_required
def update_log(log_id):

    data = request.get_json()

    device_id = data.get('device_id')
    event = data.get('event')
    severity = data.get('severity')

    allowed_severity = ['low', 'medium', 'high']

    if severity not in allowed_severity:

        return jsonify({
            "status": "error",
            "message": "Invalid severity level"
        }), 400

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        '''
        UPDATE logs
        SET device_id = ?, event = ?, severity = ?
        WHERE id = ?
        ''',
        (
            (
                device_id,
                event,
                severity,
                log_id
            )
        )
    )

    connection.commit()

    if cursor.rowcount == 0:

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Log not found"
        }), 404

    cursor.execute(
        "SELECT * FROM logs WHERE id = ?",
        (log_id,)
    )

    row = cursor.fetchone()

    connection.close()

    updated_log = {
        "id": row["id"],
        "timestamp": row["timestamp"],
        "device_id": row["device_id"],
        "event": row["event"],
        "severity": row["severity"],
        "status": row["status"],
        "archived": bool(row["archived"])
    }

    return jsonify({
        "status": "success",
        "message": "Log updated successfully",
        "data": updated_log
    })

# Update Log Status By ID
@log_bp.route('/api/v1/logs/<int:log_id>/status', methods=['PATCH'])
@login_required
def update_status(log_id):


    data = request.get_json()

    status = data.get('status')

    allowed_statuses = [
        'open',
        'investigating',
        'resolved'
    ]

    if status not in allowed_statuses:

        return jsonify({
            "status": "error",
            "message": "Invalid status"
        }), 400

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        '''
        UPDATE logs
        SET status = ?
        WHERE id = ?
        ''',
        (
            status,
            log_id
        )
    )

    connection.commit()

    if cursor.rowcount == 0:

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Log not found"
        }), 404

    cursor.execute(
        "SELECT * FROM logs WHERE id = ?",
        (log_id,)
    )

    row = cursor.fetchone()

    connection.close()

    updated_log = {
        "id": row["id"],
        "timestamp": row["timestamp"],
        "device_id": row["device_id"],
        "event": row["event"],
        "severity": row["severity"],
        "status": row["status"],
        "archived": bool(row["archived"])
    }

    return jsonify({
        "status": "success",
        "message": "Status updated successfully",
        "data": updated_log
    })

# Archive Log By ID
@log_bp.route('/api/v1/logs/<int:log_id>/archive', methods=['PATCH'])
@admin_required
def archive_log(log_id):

    # Connect to the database and check if the log exists and is resolved before archiving

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM logs WHERE id = ?",
        (log_id,)
    )

    row = cursor.fetchone()

    if not row:

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Log not found"
        }), 404

    if row["status"] != "resolved":

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Only resolved incidents can be archived"
        }), 400

    cursor.execute(
        '''
        UPDATE logs
        SET archived = 1
        WHERE id = ?
        ''',
        (log_id,)
    )

    connection.commit()

    # Log the archiving activity for auditing purposes

    log_activity(
        g.current_user["user_id"],
        g.current_user["username"],
        f"Archived log {log_id}"
    )

    cursor.execute(
        "SELECT * FROM logs WHERE id = ?",
        (log_id,)
    )

    updated_row = cursor.fetchone()

    connection.close()

    updated_log = {
        "id": updated_row["id"],
        "timestamp": updated_row["timestamp"],
        "device_id": updated_row["device_id"],
        "event": updated_row["event"],
        "severity": updated_row["severity"],
        "status": updated_row["status"],
        "archived": bool(updated_row["archived"])
    }


    return jsonify({
        "status": "success",
        "message": "Log archived successfully",
        "data": updated_log
    })