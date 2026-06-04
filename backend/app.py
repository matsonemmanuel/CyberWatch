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

# Temporary In-Memory Storage
logs_storage = []


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
        archived = request.args.get('archived')

        filtered_logs = []

        for log in logs_storage:

            # Hide archived logs by default
            if archived != 'true' and log['archived']:
                continue

            if severity and log['severity'] != severity:
                continue

            filtered_logs.append(log)

        return jsonify({
            "status": "success",
            "total_logs": len(filtered_logs),
            "logs": filtered_logs
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

    for log in logs_storage:

        if log['id'] == log_id:

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

    allowed_severity = ['low', 'medium', 'high']

    for log in logs_storage:

        if log['id'] == log_id:

            # Validate Severity If Provided
            if 'severity' in data:

                if data['severity'] not in allowed_severity:

                    return jsonify({
                        "status": "error",
                        "message": "Invalid severity level"
                    }), 400

            # Update Fields
            log['device'] = data.get('device', log['device'])
            log['event'] = data.get('event', log['event'])
            log['severity'] = data.get('severity', log['severity'])

            return jsonify({
                "status": "success",
                "message": "Log updated successfully",
                "data": log
            })

    return jsonify({
        "status": "error",
        "message": "Log not found"
    }), 404

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

    for log in logs_storage:

        if log['id'] == log_id:

            log['status'] = status

            return jsonify({
                "status": "success",
                "message": "Status updated successfully",
                "data": log
            })

    return jsonify({
        "status": "error",
        "message": "Log not found"
    }), 404


@app.route('/api/v1/logs/<int:log_id>/archive', methods=['PATCH'])
def archive_log(log_id):

    for log in logs_storage:

        if log['id'] == log_id:

            # Only resolved incidents can be archived
            if log['status'] != 'resolved':

                return jsonify({
                    "status": "error",
                    "message": "Only resolved incidents can be archived"
                }), 400

            log['archived'] = True

            return jsonify({
                "status": "success",
                "message": "Log archived successfully",
                "data": log
            })

    return jsonify({
        "status": "error",
        "message": "Log not found"
    }), 404

# Devices Endpoint
@app.route('/api/v1/devices', methods=['GET'])
def devices():

    return jsonify({
        "status": "success",
        "message": "Devices retrieved successfully"
    })


if __name__ == '__main__':
    app.run(debug=True)