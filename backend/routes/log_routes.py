
from flask import (
    Blueprint,
    jsonify,
    request,
    g
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
@log_bp.route('/api/v1/logs', methods=['GET', 'POST'])
@login_required
def logs():

    # GET METHOD
    if request.method == 'GET':

        severity = request.args.get('severity')
        status = request.args.get('status')
        archived = request.args.get('archived')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit

        print("Page:", page)
        print("Limit:", limit)
        print("Offset:", offset)

        print("Severity Filter:", severity)
        connection = get_db_connection()
        cursor = connection.cursor()
        # First, get the total count of logs for pagination

        count_cursor = connection.cursor()

    
        count_cursor.execute(
                """
                SELECT COUNT(*)
                FROM logs
                WHERE archived = 0
                """
            )

        total_logs = count_cursor.fetchone()[0]

        # Calculate total pages based on total logs and limit

        total_pages = (total_logs + limit - 1) // limit

        print("Total Logs:", total_logs)
        print("Total Pages:", total_pages)

        query = """
            SELECT
                logs.id,
                logs.timestamp,
                logs.event,
                logs.severity,
                logs.status,
                logs.archived,
                devices.id AS device_id,
                devices.hostname,
                devices.ip_address,
                devices.operating_system
            FROM logs
            INNER JOIN devices
            ON logs.device_id = devices.id
        """
        query += " WHERE 1=1"
        params = []

        if archived != 'true':

           query += " AND logs.archived = 0"

        if severity:
            query += " AND logs.severity = ?"
            params.append(severity)

        if status:
            query += " AND logs.status = ?"
            params.append(status)

    # Optional search functionality for filtering logs by event, severity, status, or device hostname

            if search:
                query += """
                    AND (
                        logs.event LIKE ?
                        OR logs.severity LIKE ?
                        OR logs.status LIKE ?
                        OR devices.hostname LIKE ?
                    )
                """

                params.extend([
                    f"%{search}%",
                    f"%{search}%",
                    f"%{search}%",
                    f"%{search}%"
                ])


        # Pagination   
        query += " LIMIT ? OFFSET ?"
        params.append(limit)
        params.append(offset)

        print("Final Query:", query)
        print("Parameters:", params)

        cursor.execute(query, params)

        rows = cursor.fetchall()

        connection.close()

        logs = []

        for row in rows:
            logs.append({
                "id": row["id"],
                "timestamp": row["timestamp"],
                "event": row["event"],
                "severity": row["severity"],
                "status": row["status"],
                "archived": bool(row["archived"]),
                "device": {
                    "id": row["device_id"],
                    "hostname": row["hostname"],
                    "ip_address": row["ip_address"],
                    "operating_system": row["operating_system"]
                }
            })

        return jsonify({
                "status": "success",

                "page": page,
                "limit": limit,

                "total_logs": total_logs,
                "total_pages": total_pages,

                "logs": logs
            })

    # POST METHOD
    elif request.method == 'POST':

        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Invalid JSON payload"
            }), 400

        device_id = data.get('device_id')
        event = data.get('event')
        severity = data.get('severity')

        if not device_id or not event or not severity:
            return jsonify({
                "status": "error",
                "message": "All fields are required"
            }), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM devices WHERE id = ?",
            (device_id,)
        )

        device = cursor.fetchone()

        if not device:
            connection.close()
            return jsonify({
                "status": "error",
                "message": "Device not found"
            }), 404

        allowed_severity = ['low', 'medium', 'high']

        if severity not in allowed_severity:
            connection.close()
            return jsonify({
                "status": "error",
                "message": "Invalid severity level"
            }), 400

        timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

        new_log = {
            "timestamp": timestamp,
            "device_id": device_id,
            "event": event,
            "severity": severity,
            "status": "open",
            "archived": False
        }

        cursor.execute(
            '''
            INSERT INTO logs
            (
                timestamp,
                device_id,
                event,
                severity,
                status,
                archived
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                timestamp,
                device_id,
                event,
                severity,
                'open',
                0
            )
        )


        connection.commit()
        new_log_id = cursor.lastrowid
        connection.close()

        new_log['id'] = new_log_id

        return jsonify({
            "status": "success",
            "message": "Log received successfully",
            "data": new_log
        }), 201
    
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