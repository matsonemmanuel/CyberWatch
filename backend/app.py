
from flask import Flask, jsonify, request 
from datetime import datetime, timezone
import sqlite3
import os

app = Flask(__name__)

# Database Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(
    BASE_DIR,
    '..',
    'database',
    'cyberwatch.db'
)

print("Database Path:", DATABASE_PATH)

def get_db_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection



# Home Endpoint
@app.route('/api/v1/')
def home():

    return jsonify({
        "status": "success",
        "message": "CyberWatch API Version 1 Running Successfully"
    })


# Logs Endpoint
@app.route('/api/v1/logs', methods=['GET', 'POST'])
def logs():

    # GET METHOD
    if request.method == 'GET':

        severity = request.args.get('severity')
        status = request.args.get('status')
        archived = request.args.get('archived')
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
@app.route('/api/v1/logs/<int:log_id>', methods=['GET'])
def get_single_log(log_id):

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
@app.route('/api/v1/logs/<int:log_id>', methods=['PUT'])
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

@app.route('/api/v1/logs/<int:log_id>/status', methods=['PATCH'])
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
@app.route('/api/v1/logs/<int:log_id>/archive', methods=['PATCH'])
def archive_log(log_id):

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

# Devices Endpoint
@app.route('/api/v1/devices', methods=(["GET", "POST"]))
def register_device():

    if request.method == 'GET':
        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM devices"
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

    if not hostname or not ip_address or not operating_system:

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
            registered_at
        )
        VALUES (?, ?, ?, ?)
        ''',
        (
            hostname,
            ip_address,
            operating_system,
            timestamp
        )
    )

    connection.commit()

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
            "status": "active",
            "registered_at": timestamp
        }
    }), 201

# Retrieve Single Device By ID
@app.route('/api/v1/devices/<int:device_id>', methods=['GET'])
def get_single_device(device_id):

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
@app.route('/api/v1/devices/<int:device_id>/status', methods=['PATCH'])
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

@app.route('/api/v1/devices/<int:device_id>/logs', methods=['GET'])
def get_device_logs(device_id):

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

# Dashboard Statistics Endpoint
@app.route('/api/v1/dashboard/stats', methods=['GET'])
def dashboard_stats():

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM devices"
    )

#Device metrics for dashboard
    total_devices = cursor.fetchone()[0]

    cursor.execute(
    "SELECT COUNT(*) FROM logs"
)

#Logs metrics for pagination
    total_logs = cursor.fetchone()[0]

#Open incidents metrics for dashboard
    cursor.execute(
    """
    SELECT COUNT(*)
    FROM logs
    WHERE status = 'open'
    """
)

    open_incidents = cursor.fetchone()[0]

    cursor.execute(
    """
    SELECT COUNT(*)
    FROM logs
    WHERE status = 'investigating'
    """
)

#Incidents that are currently being investigated for dashboard
    investigating_incidents = cursor.fetchone()[0]

    cursor.execute(
    """
    SELECT COUNT(*)
    FROM logs
    WHERE status = 'resolved'
    """
)

#Incidents that have been resolved for dashboard
    resolved_incidents = cursor.fetchone()[0]

    cursor.execute(
    """
    SELECT COUNT(*)
    FROM logs
    WHERE archived = 1
    """
)


#Incidents that have been archived for dashboard
    archived_incidents = cursor.fetchone()[0]

    cursor.execute(
    """
    SELECT COUNT(*)
    FROM logs
    WHERE severity = 'high'
    """
)


#Incidents that have a high severity for dashboard
    high_severity_incidents = cursor.fetchone()[0]

    connection.close()

    return jsonify({
    "status": "success",
    "total_devices": total_devices,
    "total_logs": total_logs,
    "open_incidents": open_incidents,
    "investigating_incidents": investigating_incidents,
    "resolved_incidents": resolved_incidents,
    "archived_incidents": archived_incidents,
    "high_severity_incidents": high_severity_incidents
})

print(app.url_map)

# User Registration Endpoint

@app.route('/api/v1/auth/register', methods=['POST'])
def register_user():

    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

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
            password,
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
if __name__ == '__main__':
    app.run(debug=True)