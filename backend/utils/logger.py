

from datetime import datetime, timezone

from database.db import get_db_connection


# Function to Log User Activities for Auditing Purposes
def log_activity(
    user_id,
    username,
    action
):

    connection = get_db_connection()

    cursor = connection.cursor()

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    cursor.execute(
        """
        INSERT INTO audit_logs (
            user_id,
            username,
            action,
            timestamp
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            username,
            action,
            timestamp
        )
    )

    connection.commit()

    connection.close()