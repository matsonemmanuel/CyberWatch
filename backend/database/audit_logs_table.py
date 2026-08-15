import sqlite3
import os

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "cyberwatch.db"
)

connection = sqlite3.connect(
    DATABASE_PATH
)

cursor = connection.cursor()

# Recreate the audit_logs table

cursor.execute("""
DROP TABLE IF EXISTS audit_logs
""")

cursor.execute("""
CREATE TABLE audit_logs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    username TEXT NOT NULL,

    action TEXT NOT NULL,

    timestamp TEXT NOT NULL,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
)
""")

connection.commit()

connection.close()

print(
    "Audit logs table recreated successfully."
)
