


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


# Get Single Log Service

def get_log_service(log_id):
    """
    Retrieve a single security log by its ID.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
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

        LEFT JOIN devices
            ON logs.device_id = devices.id

        WHERE logs.id = ?
        """,
        (log_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if not row:

        return {
            "status": "error",
            "message": "Log not found"
        }, 404

    log = {
        "id": row["id"],
        "timestamp": row["timestamp"],
        "event": row["event"],
        "severity": row["severity"],
        "status": row["status"],
        "archived": bool(row["archived"]),
        "device": None
    }

    # If the device still exists, include its information.

    if row["device_id"] is not None:

        log["device"] = {
            "id": row["device_id"],
            "hostname": row["hostname"],
            "ip_address": row["ip_address"],
            "operating_system": row["operating_system"]
        }

    return {
        "status": "success",
        "data": log
    }, 200

# =========================================================
# UPDATE LOG SERVICE
# =========================================================

def update_log_service(
    log_id,
    current_user_id,
    current_username,
    data
):
    """
    Update an existing security log.

    Only severity can be changed.
    Incident/event and device are immutable.

    A reason/comment is required.

    Every change is recorded in log_history with:
        - log ID
        - user
        - field changed
        - old value
        - new value
        - reason
        - timestamp
    """

    severity = data.get("severity")
    comment = data.get("comment")


    # =====================================================
    # VALIDATE SEVERITY
    # =====================================================

    if not severity:

        return {
            "status": "error",
            "message": "Severity is required"
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


    # =====================================================
    # VALIDATE COMMENT / REASON
    # =====================================================

    if not comment or not comment.strip():

        return {
            "status": "error",
            "message": "Reason for editing this log is required"
        }, 400


    comment = comment.strip()


    # =====================================================
    # DATABASE CONNECTION
    # =====================================================

    connection = get_db_connection()

    cursor = connection.cursor()


    try:

        # =================================================
        # FIND LOG
        # =================================================

        cursor.execute(
            """
            SELECT *
            FROM logs
            WHERE id = ?
            """,
            (log_id,)
        )

        log = cursor.fetchone()


        if not log:

            return {
                "status": "error",
                "message": "Log not found"
            }, 404


        # =================================================
        # PREVENT ARCHIVED LOG MODIFICATION
        # =================================================

        if log["archived"]:

            return {
                "status": "error",
                "message": "Archived logs cannot be updated"
            }, 400


        # =================================================
        # GET OLD SEVERITY
        # =================================================

        old_severity = log["severity"]


        # =================================================
        # CHECK WHETHER ANYTHING ACTUALLY CHANGED
        # =================================================

        if old_severity == severity:

            return {
                "status": "error",
                "message": "No change was made to the severity"
            }, 400


        # =================================================
        # UPDATE ONLY SEVERITY
        # =================================================

        cursor.execute(
            """
            UPDATE logs
            SET severity = ?
            WHERE id = ?
            """,
            (
                severity,
                log_id
            )
        )


        # =================================================
        # RECORD CHANGE IN LOG HISTORY
        # =================================================

        cursor.execute(
            """
            INSERT INTO log_history (
                log_id,
                user_id,
                username,
                field_name,
                old_value,
                new_value,
                reason,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                log_id,
                current_user_id,
                current_username,
                "severity",
                old_severity,
                severity,
                comment,
                datetime.now(timezone.utc).isoformat()
            )
        )


        # =================================================
        # COMMIT BOTH CHANGES
        # =================================================

        connection.commit()


        # =================================================
        # GET UPDATED LOG
        # =================================================

        cursor.execute(
            """
            SELECT *
            FROM logs
            WHERE id = ?
            """,
            (log_id,)
        )

        row = cursor.fetchone()


        # =================================================
        # RECORD GENERAL ACTIVITY
        # =================================================

        log_activity(
            current_user_id,
            current_username,
            f"Updated log {log_id}: "
            f"severity changed from {old_severity} "
            f"to {severity}"
        )


        # =================================================
        # RETURN UPDATED LOG
        # =================================================

        updated_log = {

            "id": row["id"],

            "timestamp": row["timestamp"],

            "device_id": row["device_id"],

            "event": row["event"],

            "severity": row["severity"],

            "status": row["status"],

            "archived": bool(row["archived"])

        }


        return {

            "status": "success",

            "message": "Log updated successfully",

            "data": updated_log

        }, 200


    except Exception as error:

        # =================================================
        # ROLLBACK EVERYTHING IF SOMETHING FAILS
        # =================================================

        connection.rollback()


        print(
            "Error updating log:",
            error
        )


        return {

            "status": "error",

            "message": "Failed to update log"

        }, 500


    finally:

        connection.close()

    # status update service

def update_log_status_service(
    log_id,
    current_user_id,
    current_username,
    data
):
    """
    Update the status of a security log.
    """

    status = data.get("status")

    if not status:

        return {
            "status": "error",
            "message": "Status is required"
        }, 400

    allowed_statuses = [
        "open",
        "investigating",
        "resolved"
    ]

    if status not in allowed_statuses:

        return {
            "status": "error",
            "message": "Invalid status"
        }, 400

    connection = get_db_connection()

    cursor = connection.cursor()

    # Verify log exists

    cursor.execute(
        """
        SELECT *
        FROM logs
        WHERE id = ?
        """,
        (log_id,)
    )

    log = cursor.fetchone()

    if not log:

        connection.close()

        return {
            "status": "error",
            "message": "Log not found"
        }, 404

    # Archived logs cannot change

    if log["archived"]:

        connection.close()

        return {
            "status": "error",
            "message": "Archived logs cannot be modified"
        }, 400

    current_status = log["status"]

    # State transition rules

    allowed_transitions = {

        "open": [
            "investigating"
        ],

        "investigating": [
            "resolved"
        ],

        "resolved": []
    }

    if status not in allowed_transitions[current_status]:

        connection.close()

        return {
            "status": "error",
            "message": f"Cannot change status from '{current_status}' to '{status}'"
        }, 400

    # Update status

    cursor.execute(
        """
        UPDATE logs
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            log_id
        )
    )

    connection.commit()

    # Retrieve updated log

    cursor.execute(
        """
        SELECT *
        FROM logs
        WHERE id = ?
        """,
        (log_id,)
    )

    row = cursor.fetchone()

    # Audit activity

    log_activity(
        current_user_id,
        current_username,
        f"Updated log {log_id} status from {current_status} to {status}"
    )

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

    return {
        "status": "success",
        "message": "Status updated successfully",
        "data": updated_log
    }, 200


def archive_log_service(
    log_id,
    current_user_id,
    current_username
):
    """
    Archive a resolved security log.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    # Verify log exists
    cursor.execute(
        """
        SELECT *
        FROM logs
        WHERE id = ?
        """,
        (log_id,)
    )

    log = cursor.fetchone()

    if not log:

        connection.close()

        return {
            "status": "error",
            "message": "Log not found"
        }, 404

    # Prevent archiving twice
    if log["archived"]:

        connection.close()

        return {
            "status": "error",
            "message": "Log is already archived"
        }, 400

    # Only resolved logs may be archived
    if log["status"] != "resolved":

        connection.close()

        return {
            "status": "error",
            "message": "Only resolved incidents can be archived"
        }, 400

    # Archive log
    cursor.execute(
        """
        UPDATE logs
        SET archived = 1
        WHERE id = ?
        """,
        (log_id,)
    )

    connection.commit()

    # Retrieve updated log
    cursor.execute(
        """
        SELECT *
        FROM logs
        WHERE id = ?
        """,
        (log_id,)
    )

    row = cursor.fetchone()

    # Record audit activity
    log_activity(
        current_user_id,
        current_username,
        f"Archived log {log_id}"
    )

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

    return {
        "status": "success",
        "message": "Log archived successfully",
        "data": updated_log
    }, 200

    # =========================================================
# GET LOG HISTORY SERVICE
# =========================================================

def get_log_history_service():

    connection = get_db_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                log_id,
                user_id,
                username,
                field_name,
                old_value,
                new_value,
                reason,
                created_at
            FROM log_history
            ORDER BY created_at DESC
            """
        )

        rows = cursor.fetchall()

        history = []

        for row in rows:

            history.append({
                "id": row["id"],
                "log_id": row["log_id"],
                "user_id": row["user_id"],
                "username": row["username"],
                "field_name": row["field_name"],
                "old_value": row["old_value"],
                "new_value": row["new_value"],
                "reason": row["reason"],
                "created_at": row["created_at"]
            })

        return {
            "status": "success",
            "total_changes": len(history),
            "history": history
        }, 200

    except Exception as error:

        print(
            "Error loading log history:",
            error
        )

        return {
            "status": "error",
            "message": "Failed to load log history"
        }, 500

    finally:

        connection.close()