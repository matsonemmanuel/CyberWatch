
from multiprocessing import connection

from flask import jsonify

from database.db import get_db_connection

from datetime import (
    datetime,
    timezone
)

from utils.logger import log_activity

def get_logs_service(
    severity,
    status,
    archived,
    search,
    page,
    limit
):
    """
    Retrieve logs with filtering, searching and pagination.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    count_cursor = connection.cursor()

    count_cursor.execute(
        """
        SELECT COUNT(*)
        FROM logs
        WHERE archived = 0
        """
    )

    total_logs = count_cursor.fetchone()[0]

    total_pages = (total_logs + limit - 1) // limit

    offset = (page - 1) * limit

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

    query += " LIMIT ? OFFSET ?"

    params.append(limit)

    params.append(offset)

    print(query)
    print(params)

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

    return {
        "status": "success",
        "page": page,
        "limit": limit,
        "total_logs": total_logs,
        "total_pages": total_pages,
        "logs": logs
    }, 200
    
def create_log_service(
    current_user_id,
    current_username,
    data
):
    """
    Create a new security log.
    """

    event = data.get("event")
    severity = data.get("severity")
    device_id = data.get("device_id")
    status = data.get("status", "open")

    if not event or not severity or not device_id:

        return {
            "status": "error",
            "message": "All required fields must be provided."
        }, 400
    
    allowed_severity = [
        "low",
        "medium",
        "high"
    ]

    if severity not in allowed_severity:

        return {
            "status": "error",
            "message": "Invalid severity level"
        }, 400

    connection = get_db_connection()

    cursor = connection.cursor()

    timestamp = datetime.now(
        timezone.utc
    ).isoformat().replace("+00:00", "Z")

    new_log = {
        "timestamp": timestamp,
        "device_id": device_id,
        "event": event,
        "severity": severity,
        "status": "open",
        "archived": False
    }

    cursor.execute(
        """
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
        """,
        (
            timestamp,
            device_id,
            event,
            severity,
            "open",
            0
        )
    )

    connection.commit()

    new_log_id = cursor.lastrowid

    log_activity(
        current_user_id,
        current_username,
        f"Created security log for device {device_id}"
    )

    connection.close()

    new_log["id"] = new_log_id

    return {
        "status": "success",
        "message": "Log received successfully",
        "data": new_log
    }, 201


    
