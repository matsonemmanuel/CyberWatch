from database.db import get_db_connection


connection = get_db_connection()

cursor = connection.cursor()

columns = cursor.execute(
    "PRAGMA table_info(alerts)"
).fetchall()

print("\nALERTS TABLE STRUCTURE:\n")

for column in columns:

    print(
        f"Column: {column['name']} | "
        f"Type: {column['type']} | "
        f"Not Null: {column['notnull']} | "
        f"Primary Key: {column['pk']}"
    )

connection.close()