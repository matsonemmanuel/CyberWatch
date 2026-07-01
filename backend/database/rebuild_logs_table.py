import sqlite3

connection = sqlite3.connect('cyberwatch.db')

cursor = connection.cursor()

# Remove old logs table
cursor.execute("DROP TABLE IF EXISTS logs")

# Create new logs table
cursor.execute("""
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id INTEGER NOT NULL,
    event TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    archived INTEGER DEFAULT 0,

    FOREIGN KEY (device_id)
    REFERENCES devices(id)
)
""")

connection.commit()

print("Logs table recreated successfully.")

connection.close()