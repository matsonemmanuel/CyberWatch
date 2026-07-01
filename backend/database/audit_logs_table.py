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

cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_logs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    username TEXT NOT NULL,

    action TEXT NOT NULL,

    timestamp TEXT NOT NULL
)
""")

connection.commit()

connection.close()

print(
    "audit_logs table created successfully"
)