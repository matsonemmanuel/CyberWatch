from database.db import get_db_connection
from datetime import datetime, timezone


# =====================================================
# GET ALERTS
# =====================================================

def get_alerts_service(
    severity=None,
    status=None
):
    """
    Retrieve security alerts.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    query = """
        SELECT
            id,
            log_id,
            device_id,
            title,
            message,
            severity,
            status,
            created_at
        FROM alerts
        WHERE 1 = 1
    """

    params = []


    # =================================================
    # FILTER BY SEVERITY
    # =================================================

    if severity:

        query += """
            AND severity = ?
        """

        params.append(severity)


    # =================================================
    # FILTER BY STATUS
    # =================================================

    if status:

        query += """
            AND status = ?
        """

        params.append(status)


    # =================================================
    # ORDER
    # =================================================

    query += """
        ORDER BY created_at DESC
    """


    cursor.execute(
        query,
        params
    )

    rows = cursor.fetchall()

    connection.close()


    alerts = []

    for row in rows:

        alerts.append({

            "id": row["id"],

            "log_id": row["log_id"],

            "device_id": row["device_id"],

            "title": row["title"],

            "message": row["message"],

            "severity": row["severity"],

            "status": row["status"],

            "created_at": row["created_at"]

        })


    return {
        "status": "success",
        "alerts": alerts,
        "total": len(alerts)
    }, 200


# =====================================================
# GET SINGLE ALERT
# =====================================================

def get_alert_service(alert_id):

    connection = get_db_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            id,
            log_id,
            device_id,
            title,
            message,
            severity,
            status,
            created_at
        FROM alerts
        WHERE id = ?
        """,
        (alert_id,)
    )


    row = cursor.fetchone()

    connection.close()


    if not row:

        return {
            "status": "error",
            "message": "Alert not found"
        }, 404


    alert = {

        "id": row["id"],

        "log_id": row["log_id"],

        "device_id": row["device_id"],

        "title": row["title"],

        "message": row["message"],

        "severity": row["severity"],

        "status": row["status"],

        "created_at": row["created_at"]

    }


    return {
        "status": "success",
        "data": alert
    }, 200


# =====================================================
# CREATE ALERT
# =====================================================

def create_alert_service(data):

    log_id = data.get("log_id")

    device_id = data.get("device_id")

    title = data.get("title")

    message = data.get("message")

    severity = data.get("severity")


    # =================================================
    # VALIDATION
    # =================================================

    if not log_id:

        return {
            "status": "error",
            "message": "log_id is required"
        }, 400


    if not title:

        return {
            "status": "error",
            "message": "Alert title is required"
        }, 400


    if not message:

        return {
            "status": "error",
            "message": "Alert message is required"
        }, 400


    if not severity:

        return {
            "status": "error",
            "message": "Alert severity is required"
        }, 400


    allowed_severities = [
        "low",
        "medium",
        "high",
        "critical"
    ]


    if severity not in allowed_severities:

        return {
            "status": "error",
            "message": "Invalid alert severity"
        }, 400


    connection = get_db_connection()

    cursor = connection.cursor()


    # =================================================
    # VERIFY LOG EXISTS
    # =================================================

    cursor.execute(
        """
        SELECT id
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
            "message": "Security log not found"
        }, 404


    # =================================================
    # CREATE ALERT
    # =================================================

    created_at = datetime.now(
        timezone.utc
    ).isoformat().replace(
        "+00:00",
        "Z"
    )


    cursor.execute(
        """
        INSERT INTO alerts (
            log_id,
            device_id,
            title,
            message,
            severity,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            log_id,
            device_id,
            title,
            message,
            severity,
            "active",
            created_at
        )
    )


    connection.commit()


    alert_id = cursor.lastrowid


    connection.close()


    return {
        "status": "success",
        "message": "Alert created successfully",
        "data": {
            "id": alert_id,
            "log_id": log_id,
            "device_id": device_id,
            "title": title,
            "message": message,
            "severity": severity,
            "status": "active",
            "created_at": created_at
        }
    }, 201


# =====================================================
# UPDATE ALERT STATUS
# =====================================================

def update_alert_status_service(
    alert_id,
    data
):

    new_status = data.get("status")


    if not new_status:

        return {
            "status": "error",
            "message": "Status is required"
        }, 400


    allowed_statuses = [
        "active",
        "acknowledged",
        "resolved"
    ]


    if new_status not in allowed_statuses:

        return {
            "status": "error",
            "message": "Invalid alert status"
        }, 400


    connection = get_db_connection()

    cursor = connection.cursor()


    # =================================================
    # FIND ALERT
    # =================================================

    cursor.execute(
        """
        SELECT *
        FROM alerts
        WHERE id = ?
        """,
        (alert_id,)
    )


    alert = cursor.fetchone()


    if not alert:

        connection.close()

        return {
            "status": "error",
            "message": "Alert not found"
        }, 404


    # =================================================
    # UPDATE STATUS
    # =================================================

    cursor.execute(
        """
        UPDATE alerts
        SET status = ?
        WHERE id = ?
        """,
        (
            new_status,
            alert_id
        )
    )


    connection.commit()


    # =================================================
    # GET UPDATED ALERT
    # =================================================

    cursor.execute(
        """
        SELECT *
        FROM alerts
        WHERE id = ?
        """,
        (alert_id,)
    )


    row = cursor.fetchone()


    connection.close()


    updated_alert = {

        "id": row["id"],

        "log_id": row["log_id"],

        "device_id": row["device_id"],

        "title": row["title"],

        "message": row["message"],

        "severity": row["severity"],

        "status": row["status"],

        "created_at": row["created_at"]

    }


    return {
        "status": "success",
        "message": "Alert status updated successfully",
        "data": updated_alert
    }, 200