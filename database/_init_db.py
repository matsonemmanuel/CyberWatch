import sqlite3

# Connect To Database
connection = sqlite3.connect('database/cyberwatch.db')

# Create Cursor
cursor = connection.cursor()

# Create Logs Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device TEXT NOT NULL,
    event TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    archived INTEGER DEFAULT 0
)
''')

# Save Changes
connection.commit()

# Close Connection
connection.close()

print("CyberWatch database initialized successfully.")