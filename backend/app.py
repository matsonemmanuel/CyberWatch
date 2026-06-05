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

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM logs")

        rows = cursor.fetchall()

        connection.close()

        logs = []

        for row in rows:

            logs.append({
                "id": row["id"],
                "timestamp": row["timestamp"],
                "device": row["device"],
                "event": row["event"],
                "severity": row["severity"],
                "status": row["status"],
                "archived": bool(row["archived"])
            })

        return jsonify({
            "status": "success",
            "total_logs": len(logs),
            "logs": logs
        })
    # POST METHOD
    elif request.method == 'POST':

        # Receive JSON Data
        data = request.get_json()

        # Extract Values
        device = data.get('device')
        event = data.get('event')
        severity = data.get('severity')

        # Validate Missing Fields
        if not device or not event or not severity:

            return jsonify({
                "status": "error",
                "message": "All fields are required"
            }), 400

        # Allowed Severity Levels
        allowed_severity = ['low', 'medium', 'high']

        # Validate Severity
        if severity not in allowed_severity:

            return jsonify({
                "status": "error",
                "message": "Invalid severity level"
            }), 400

        # Generate Unique Log ID
    

        # Generate UTC Timestamp
        timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

        # Create Log Object
        new_log = {
            "timestamp": timestamp,
            "device": device,
            "event": event,
            "severity": severity,
            "status": "open",
            "archived": False
        }

        # Save Log To Database
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO logs
            (timestamp, device, event, severity, status, archived)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                timestamp,
                device,
                event,
                severity,
                'open',
                0
            )
        )

        connection.commit()
        new_log_id = cursor.lastrowid
        connection.close()

        # Add Database Generated ID
        new_log['id'] = new_log_id

        # Keep Temporary Memory Storage
        logs_storage.append(new_log)

        # Success Response
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
            "device": row["device"],
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

    device = data.get('device')
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
        SET device = ?, event = ?, severity = ?
        WHERE id = ?
        ''',
        (
            device,
            event,
            severity,
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
        "device": row["device"],
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
        "device": row["device"],
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
        "device": updated_row["device"],
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
@app.route('/api/v1/devices', methods=['GET'])
def devices():

    return jsonify({
        "status": "success",
        "message": "Devices retrieved successfully"
    })


if __name__ == '__main__':
    app.run(debug=True)