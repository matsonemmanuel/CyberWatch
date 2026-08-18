from database.db import get_db_connection


def create_alerts_table():

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alerts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            log_id INTEGER NOT NULL,

            device_id INTEGER,

            title TEXT NOT NULL,

            message TEXT NOT NULL,

            severity TEXT NOT NULL,

            status TEXT NOT NULL DEFAULT 'active',

            created_at TEXT NOT NULL,

            FOREIGN KEY (log_id)
                REFERENCES logs(id)

        )
        """
    )

    connection.commit()

    connection.close()

    print("alerts table created successfully.")


if __name__ == "__main__":

    create_alerts_table()