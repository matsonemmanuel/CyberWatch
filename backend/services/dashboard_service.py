

from ..db import get_db_connection


def get_dashboard_stats_service():
    """
    Retrieve dashboard statistics.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    queries = {

        "total_devices":
            "SELECT COUNT(*) FROM devices",

        "total_logs":
            "SELECT COUNT(*) FROM logs",

        "open_incidents":
            "SELECT COUNT(*) FROM logs WHERE status = 'open'",

        "investigating_incidents":
            "SELECT COUNT(*) FROM logs WHERE status = 'investigating'",

        "resolved_incidents":
            "SELECT COUNT(*) FROM logs WHERE status = 'resolved'",

        "archived_incidents":
            "SELECT COUNT(*) FROM logs WHERE archived = 1",

        "high_severity_incidents":
            "SELECT COUNT(*) FROM logs WHERE severity = 'high'"
    }

    stats = {}

    for key, query in queries.items():

        cursor.execute(query)

        stats[key] = cursor.fetchone()[0]

    connection.close()

    return {
        "status": "success",
        **stats
    }, 200