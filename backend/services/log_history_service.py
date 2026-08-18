from database.db import get_db_connection


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
            "history": history,
            "total": len(history)
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