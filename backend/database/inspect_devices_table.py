import sqlite3

connection = sqlite3.connect('cyberwatch.db')

cursor = connection.cursor()

cursor.execute("PRAGMA table_info(devices)")

for column in cursor.fetchall():
    print(column)

connection.close()