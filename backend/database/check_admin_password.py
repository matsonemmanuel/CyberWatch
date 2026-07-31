import sqlite3
from werkzeug.security import check_password_hash

connection = sqlite3.connect("cyberwatch.db")
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute(
    """
    SELECT username, password
    FROM users
    WHERE username = ?
    """,
    ("admin",)
)

user = cursor.fetchone()

if user:
    print("Username:", user["username"])
    print("Hash:", user["password"])
    print(
        "Matches Admin@123:",
        check_password_hash(
            user["password"],
            "Admin@123"
        )
    )
else:
    print("Admin user not found.")

connection.close()