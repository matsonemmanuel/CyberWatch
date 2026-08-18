from database.db import get_db_connection


def create_log_history_table():

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            log_id INTEGER NOT NULL,

            user_id INTEGER,

            username TEXT,

            field_name TEXT NOT NULL,

            old_value TEXT,

            new_value TEXT,

            reason TEXT NOT NULL,

            created_at TEXT NOT NULL,

            FOREIGN KEY (log_id)
                REFERENCES logs(id)

        )
    """)

    connection.commit()

    connection.close()

    print("log_history table created successfully.")


if __name__ == "__main__":

    create_log_history_table()