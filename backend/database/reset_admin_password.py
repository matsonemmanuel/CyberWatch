import sqlite3
from werkzeug.security import generate_password_hash

connection = sqlite3.connect("cyberwatch.db")

cursor = connection.cursor()

new_password = generate_password_hash("Admin@123")

cursor.execute(
    """
    UPDATE users
    SET password = ?
    WHERE username = ?
    """,
    (
        new_password,
        "admin"
    )
)

connection.commit()

print("Rows updated:", cursor.rowcount)

connection.close()