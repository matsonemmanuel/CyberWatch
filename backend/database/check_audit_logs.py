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

cursor.execute(
    "SELECT * FROM audit_logs"
)

logs = cursor.fetchall()

print(
    f"Total Audit Logs: {len(logs)}"
)

for log in logs:
    print(log)

connection.close()