import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "..",
    "database",
    "cyberwatch.db"
)

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

# Add deleted column
try:

    cursor.execute("""
        ALTER TABLE devices
        ADD COLUMN deleted INTEGER NOT NULL DEFAULT 0
    """)

    print("deleted column added.")

except sqlite3.OperationalError:

    print("deleted column already exists.")

# Add deleted_at column
try:

    cursor.execute("""
        ALTER TABLE devices
        ADD COLUMN deleted_at TEXT
    """)

    print("deleted_at column added.")

except sqlite3.OperationalError:

    print("deleted_at column already exists.")

connection.commit()

connection.close()

print("Soft delete migration completed successfully.")