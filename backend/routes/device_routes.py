

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
@device_bp.route('/api/v1/devices', methods=["GET", "POST"])
@login_required
def register_device():

    # GET METHOD - Retrieve All Devices with Optional Pagination and Filtering

    if request.method == 'GET':
        connection = get_db_connection()

        cursor = connection.cursor()

        # Optional search functionality for filtering devices by hostname, IP address, or operating system

        search = request.args.get(
            "search",
            ""
        )

    # Pagination parameters

        cursor.execute(
            """
            SELECT *
            FROM devices
            WHERE
                hostname LIKE ?
                OR ip_address LIKE ?
                OR operating_system LIKE ?
                OR status LIKE ?
            """,
            (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            )
        )

        rows = cursor.fetchall()

        connection.close()

        devices = []

        for row in rows:

            devices.append({
                "id": row["id"],
                "hostname": row["hostname"],
                "ip_address": row["ip_address"],
                "operating_system": row["operating_system"],
                "status": row["status"],
                "registered_at": row["registered_at"]
            })

        return jsonify({
        "status": "success",
        "total_devices": len(devices),
        "devices": devices
    })

    data = request.get_json()

    hostname = data.get('hostname')
    ip_address = data.get('ip_address')
    operating_system = data.get('operating_system')
    status = data.get('status', 'active')

    if not hostname or not ip_address or not operating_system or not status:

        return jsonify({
            "status": "error",
            "message": "All fields are required"
        }), 400

    timestamp = datetime.now(
        timezone.utc
    ).isoformat().replace('+00:00', 'Z')

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        '''
        INSERT INTO devices
        (
            hostname,
            ip_address,
            operating_system,
            status,
            registered_at
        )
        VALUES (?, ?, ?, ?, ?)
        ''',
        (
            hostname,
            ip_address,
            operating_system,
            status,
            timestamp
        )
    )

    connection.commit()

    # Log the device registration activity for auditing purposes

    log_activity(
        g.current_user["user_id"],
        g.current_user["username"],
        f"Registered device {hostname}"
    )

    device_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "status": "success",
        "message": "Device registered successfully",
        "data": {
            "id": device_id,
            "hostname": hostname,
            "ip_address": ip_address,
            "operating_system": operating_system,
            "status": status,
            "registered_at": timestamp
        }
    }), 201

# Retrieve Single Device By ID
@device_bp.route('/api/v1/devices/<int:device_id>', methods=['GET'])
@login_required
def get_single_device(device_id):

    # Connect to the database and check if the device exists before retrieving details

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if not row:

        return jsonify({
            "status": "error",
            "message": "Device not found"
        }), 404

    device = {
        "id": row["id"],
        "hostname": row["hostname"],
        "ip_address": row["ip_address"],
        "operating_system": row["operating_system"],
        "status": row["status"],
        "registered_at": row["registered_at"]
    }

    return jsonify({
        "status": "success",
        "device": device
    })

    # Update Device Status
@device_bp.route('/api/v1/devices/<int:device_id>/status', methods=['PATCH'])
@login_required
def update_device_status(device_id):


    data = request.get_json()

    status = data.get('status')

    allowed_statuses = [
        'active',
        'offline',
        'maintenance',
        'disabled'
    ]

    if status not in allowed_statuses:

        return jsonify({
            "status": "error",
            "message": "Invalid device status"
        }), 400

    connection = get_db_connection()

    cursor = connection.cursor()

    # Check if device exists
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

    # Update status
    cursor.execute(
        """
        UPDATE devices
        SET status = ?
        WHERE id = ?
        """,
        (status, device_id)
    )

    connection.commit()

    # Retrieve updated device
    cursor.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    )

    updated_device = cursor.fetchone()

    connection.close()

    return jsonify({
        "status": "success",
        "message": "Device status updated successfully",
        "data": {
            "id": updated_device["id"],
            "hostname": updated_device["hostname"],
            "status": updated_device["status"]
        }
    })

    # Retrieve Logs for a Specific Device

@device_bp.route('/api/v1/devices/<int:device_id>/logs', methods=['GET'])
@login_required
def get_device_logs(device_id):

# Connect to the database and check if the device exists before retrieving logs


    connection = get_db_connection()

    cursor = connection.cursor()

    # Verify device exists
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

    # Retrieve device logs
    cursor.execute(
        """
        SELECT * FROM logs
        WHERE device_id = ?
        """,
        (device_id,)
    )

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
            "archived": bool(row["archived"])
        })

    return jsonify({
        "status": "success",
        "device_id": device_id,
        "total_logs": len(logs),
        "logs": logs
    })