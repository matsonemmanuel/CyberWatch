import sqlite3

connection = sqlite3.connect('cyberwatch.db')

cursor = connection.cursor()

cursor.execute("SELECT * FROM logs")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()