
from flask import (
    Blueprint,
    jsonify
)

from database.db import get_db_connection

from utils.auth import (
    login_required
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

# Dashboard Statistics Endpoint
@dashboard_bp.route('/api/v1/dashboard/stats', methods=['GET'])
@login_required
def dashboard_stats():


    # Connect to the database and retrieve metrics for the dashboard

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