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
    "PRAGMA table_info(audit_logs)"
)

columns = cursor.fetchall()

print("AUDIT LOGS TABLE")

for column in columns:
    print(column)

connection.close()