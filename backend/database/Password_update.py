from werkzeug.security import generate_password_hash
import sqlite3

connection = sqlite3.connect("cyberwatch.db")
cursor = connection.cursor()

# Update admin password
cursor.execute(
    """
    UPDATE users
    SET password = ?
    WHERE username = ?
    """,
    (
        generate_password_hash("admin123"),
        "admin"
    )
)

# Update john password
cursor.execute(
    """
    UPDATE users
    SET password = ?
    WHERE username = ?
    """,
    (
        generate_password_hash("john123"),
        "john"
    )
)

connection.commit()

print("Passwords updated successfully")

connection.close()