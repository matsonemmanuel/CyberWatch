import sqlite3

connection = sqlite3.connect('cyberwatch.db')

cursor = connection.cursor()

cursor.execute(
    "PRAGMA table_info(users)"
)

for row in cursor.fetchall():
    print(row)

connection.close()