import sqlite3

connection = sqlite3.connect('cyberwatch.db')

cursor = connection.cursor()

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'analyst',
        created_at TEXT NOT NULL
    )
    '''
)

connection.commit()

connection.close()

print("Users table created successfully.")